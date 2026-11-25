"""Check local references, unique IDs, and metadata before publishing."""
from html.parser import HTMLParser
from pathlib import Path
import json
import re
import sys
from urllib.parse import urljoin, urlsplit
from urllib.robotparser import RobotFileParser
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parent.parent

class SiteParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids, self.refs, self.errors = set(), [], []
        self.h1s, self.descriptions = 0, 0
        self.titles, self.canonicals, self.schemas = [], [], []
        self.metadata, self.body_text = {}, []
        self.in_title = self.in_json = self.in_body = False
        self.json_text = ''
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if 'id' in attrs:
            if attrs['id'] in self.ids:
                self.errors.append('Duplicate ID: '+attrs['id'])
            self.ids.add(attrs['id'])
        if tag == 'h1': self.h1s += 1
        if tag == 'body': self.in_body = True
        if tag == 'title':
            self.in_title = True
            self.titles.append('')
        if tag == 'meta':
            key = attrs.get('name', attrs.get('property'))
            if key:
                if key in self.metadata: self.errors.append('Duplicate metadata: '+key)
                self.metadata[key] = attrs.get('content', '')
        if tag == 'link' and attrs.get('rel') == 'canonical':
            self.canonicals.append(attrs.get('href', ''))
        if tag == 'script' and attrs.get('type') == 'application/ld+json':
            self.in_json = True
            self.json_text = ''
        if tag == 'meta' and attrs.get('name') == 'description': self.descriptions += 1
        if tag == 'img' and 'alt' not in attrs: self.errors.append('Image missing alt text')
        for key in ['src','href']:
            value = attrs.get(key, '')
            if value.startswith(('./','#')): self.refs.append(value)

    def handle_data(self, data):
        if self.in_title: self.titles[-1] += data
        if self.in_json: self.json_text += data
        elif self.in_body: self.body_text.append(data)

    def handle_endtag(self, tag):
        if tag == 'title': self.in_title = False
        if tag == 'body': self.in_body = False
        if tag == 'script' and self.in_json:
            self.in_json = False
            try: self.schemas.append(json.loads(self.json_text))
            except json.JSONDecodeError as e: self.errors.append('Invalid JSON-LD: '+str(e))

page = SiteParser()
page.feed((ROOT/'index.html').read_text())
for ref in page.refs:
    if ref.startswith('#'):
        if ref[1:] not in page.ids: page.errors.append('Missing anchor: '+ref)
    elif not (ROOT/ref.split('#')[0].split('?')[0]).is_file(): page.errors.append('Missing local asset: '+ref)
if page.h1s != 1: page.errors.append('Expected exactly one H1')
if page.descriptions != 1: page.errors.append('Expected exactly one meta description')
for svg in (ROOT/'assets').rglob('*.svg'):
    try: ET.parse(svg)
    except ET.ParseError as e: page.errors.append(f'Invalid SVG {svg.name}: {e}')
for image in re.findall(r"image: '([^']+)'", (ROOT/'script.js').read_text()):
    if not (ROOT/'assets/images'/image).is_file(): page.errors.append('Missing dialog image: '+image)
for css in [ROOT/'styles.css', ROOT/'assets/fonts.css']:
    for ref in re.findall(r"url\(['\"]?([^'\")]+)", css.read_text()):
        if not ref.startswith(('http:', 'https:', 'data:')) and not (css.parent/ref).is_file():
            page.errors.append('Missing CSS asset: '+ref)

# Search configuration must agree across HTML, sitemap, crawler rules and JSON-LD.
config = json.loads((ROOT/'site.config.json').read_text())
base = config['site_url']
if page.titles != [config['title']]: page.errors.append('Expected one configured page title')
if page.canonicals != [base]: page.errors.append('Canonical does not match site URL')
for key in ['description', 'og:title', 'og:description', 'og:site_name', 'og:image',
            'og:image:alt', 'twitter:card', 'twitter:title', 'twitter:description',
            'twitter:image', 'twitter:image:alt']:
    if not page.metadata.get(key): page.errors.append('Missing search/social metadata: '+key)
if page.metadata.get('og:url') != base: page.errors.append('Open Graph URL differs from canonical')
directives = {x.strip() for x in page.metadata.get('robots', '').lower().split(',')}
if not {'index','follow'}.issubset(directives) or {'noindex','nofollow','none'} & directives:
    page.errors.append('Homepage must allow indexing and following links')
try:
    ns = {'s': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
    sitemap = ET.parse(ROOT/'sitemap.xml').getroot()
    locations = [x.text for x in sitemap.findall('s:url/s:loc', ns)]
    if sitemap.tag != '{'+ns['s']+'}urlset' or locations != [base]:
        page.errors.append('Sitemap must contain the single canonical page, without fragments')
except ET.ParseError as e: page.errors.append('Invalid sitemap XML: '+str(e))
robots_text = (ROOT/'robots.txt').read_text()
robots = RobotFileParser()
robots.parse(robots_text.splitlines())
if robots.site_maps() != [urljoin(base,'sitemap.xml')]:
    page.errors.append('robots.txt sitemap differs from canonical URL')
for bot in ['Googlebot','Bingbot','*']:
    for resource in ['', 'styles.css', 'script.js', config['logo'], 'sitemap.xml']:
        if not robots.can_fetch(bot, urljoin(base,resource)):
            page.errors.append(f'Crawler rules block {bot}: {resource}')
if len(page.schemas) != 1 or page.schemas[0].get('@context') != 'https://schema.org':
    page.errors.append('Expected one schema.org JSON-LD graph')
else:
    graph = page.schemas[0].get('@graph', [])
    entities = {entry.get('@type'): entry for entry in graph}
    for kind in ['WebSite','WebPage','CafeOrCoffeeShop']:
        if entities.get(kind,{}).get('url') != base:
            page.errors.append('Missing or inconsistent structured data: '+kind)
    ids = [entry.get('@id') for entry in graph]
    if len(ids) != len(set(ids)) or any(not item or not item.startswith(base+'#') for item in ids):
        page.errors.append('Structured data IDs must be unique and use the canonical base')
    business = entities.get('CafeOrCoffeeShop', {})
    if business.get('name') != config['name']:
        page.errors.append('Business name differs from configured name')
    if business.get('address') != {'@type':'PostalAddress', **config['business']['address']}:
        page.errors.append('Business address differs from configured location')
    visible = ' '.join(page.body_text)
    for field in ['streetAddress','addressLocality']:
        if config['business']['address'][field] not in visible:
            page.errors.append('Structured address is missing from page text: '+field)
    for image in [business.get('logo'), business.get('image'), page.metadata.get('og:image')]:
        if not image or not image.startswith(base):
            page.errors.append('Structured/social image must use the site URL')
        else:
            local_path = urlsplit(image).path.removeprefix(urlsplit(base).path)
            if not (ROOT/local_path).is_file(): page.errors.append('Missing SEO image: '+local_path)
if page.errors:
    print('\n'.join(page.errors))
    sys.exit(1)
print(f'Passed: {len(page.refs)} local references, {len(page.ids)} unique IDs, images, SVGs, canonical/social metadata, JSON-LD, sitemap and crawler rules.')
