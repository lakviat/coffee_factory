"""Check local references, unique IDs, and metadata before publishing."""
from html.parser import HTMLParser
from pathlib import Path
import re
import sys
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parent.parent

class SiteParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids, self.refs, self.errors = set(), [], []
        self.h1s, self.descriptions = 0, 0
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if 'id' in attrs:
            if attrs['id'] in self.ids:
                self.errors.append('Duplicate ID: '+attrs['id'])
            self.ids.add(attrs['id'])
        if tag == 'h1': self.h1s += 1
        if tag == 'meta' and attrs.get('name') == 'description': self.descriptions += 1
        if tag == 'img' and 'alt' not in attrs: self.errors.append('Image missing alt text')
        for key in ['src','href']:
            value = attrs.get(key, '')
            if value.startswith(('./','#')): self.refs.append(value)

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
if page.errors:
    print('\n'.join(page.errors))
    sys.exit(1)
print(f'Passed: {len(page.refs)} local references, {len(page.ids)} unique IDs, image descriptions, SVGs, dialog images and page metadata.')
