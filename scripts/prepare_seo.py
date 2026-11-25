"""Generate static search metadata; keep domain changes consistent across files."""
import argparse
from html import escape
import json
from pathlib import Path
import re
from urllib.parse import urljoin, urlsplit

ROOT = Path(__file__).resolve().parent.parent
START = '  <!-- Generated SEO: edit site.config.json, then run npm run seo. -->'
END = '  <!-- End generated SEO. -->'


def normalize_url(value):
    url = urlsplit(value)
    if (url.scheme != 'https' or not url.hostname or url.username or url.password
            or url.port not in (None, 443) or url.query or url.fragment
            or any(part in ('.', '..') for part in url.path.split('/'))
            or any(char.isspace() for char in value)):
        raise ValueError('Use a public HTTPS site URL without credentials, query, or fragment.')
    return value.rstrip('/') + '/'


def generate(config):
    base = normalize_url(config['site_url'])
    absolute = lambda path: urljoin(base, path)
    image = config['image']
    business_id, website_id = base + '#business', base + '#website'
    graph = {
        '@context': 'https://schema.org',
        '@graph': [
            {
                '@type': 'CafeOrCoffeeShop', '@id': business_id,
                'name': config['name'], 'url': base,
                'description': config['business']['description'],
                'logo': absolute(config['logo']),
                'image': absolute(config['logo']),
                'address': {'@type': 'PostalAddress', **config['business']['address']},
                'servesCuisine': 'Coffee'
            },
            {
                '@type': 'WebSite', '@id': website_id, 'url': base,
                'name': config['name'], 'inLanguage': config['language'],
                'publisher': {'@id': business_id}
            },
            {
                '@type': 'WebPage', '@id': base + '#webpage', 'url': base,
                'name': config['title'], 'description': config['description'],
                'inLanguage': config['language'], 'isPartOf': {'@id': website_id},
                'about': {'@id': business_id},
                'primaryImageOfPage': {
                    '@type': 'ImageObject', 'url': absolute(image['path']),
                    'width': image['width'], 'height': image['height'],
                    'caption': image['alt']
                }
            }
        ]
    }
    lines = [START, f"  <title>{escape(config['title'])}</title>"]

    def meta(key, value, attribute='name'):
        lines.append(f'  <meta {attribute}="{key}" content="{escape(str(value), quote=True)}">')

    meta('description', config['description'])
    meta('robots', 'index, follow, max-image-preview:large')
    for key, value in {
        'og:type': 'website', 'og:site_name': config['name'],
        'og:locale': config['locale'], 'og:title': config['title'],
        'og:description': config['description'], 'og:url': base,
        'og:image': absolute(image['path']), 'og:image:type': image['type'],
        'og:image:width': image['width'], 'og:image:height': image['height'],
        'og:image:alt': image['alt']
    }.items():
        meta(key, value, 'property')
    for key, value in {
        'twitter:card': 'summary_large_image', 'twitter:title': config['title'],
        'twitter:description': config['description'],
        'twitter:image': absolute(image['path']), 'twitter:image:alt': image['alt']
    }.items():
        meta(key, value)
    lines.extend([
        f'  <link rel="canonical" href="{escape(base, quote=True)}">',
        '  <link rel="sitemap" type="application/xml" title="Sitemap" href="./sitemap.xml">',
        '  <script type="application/ld+json">',
        json.dumps(graph, ensure_ascii=False, indent=2).replace('<', '\\u003c'),
        '  </script>', END
    ])
    page = (ROOT / 'index.html').read_text()
    pattern = re.escape(START) + r'.*?' + re.escape(END)
    if len(re.findall(pattern, page, flags=re.S)) != 1:
        raise ValueError('Expected exactly one generated SEO block in index.html.')
    page = re.sub(pattern, lambda _: '\n'.join(lines), page, flags=re.S)
    # One canonical document: section fragments and product dialogs are not pages.
    sitemap = ('<?xml version="1.0" encoding="UTF-8"?>\n'
               '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
               f'  <url><loc>{escape(base)}</loc></url>\n</urlset>\n')
    robots = ('# Crawlers read this file only at the host root (/robots.txt).\n'
              '# On GitHub project Pages, submit sitemap.xml directly in webmaster tools.\n'
              'User-agent: *\nAllow: /\n\n'
              f'Sitemap: {absolute("sitemap.xml")}\n')
    return {'index.html': page, 'sitemap.xml': sitemap, 'robots.txt': robots}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--site-url', help='Set the canonical HTTPS URL after a domain move.')
    parser.add_argument('--check', action='store_true', help='Check generated files without writing.')
    args = parser.parse_args()
    if args.check and args.site_url:
        parser.error('--check cannot be combined with --site-url')
    config_path = ROOT / 'site.config.json'
    config = json.loads(config_path.read_text())
    if args.site_url:
        config['site_url'] = normalize_url(args.site_url)
    outputs = generate(config)
    if args.check:
        stale = [name for name, content in outputs.items()
                 if not (ROOT / name).is_file() or (ROOT / name).read_text() != content]
        if stale:
            parser.exit(1, 'SEO files are out of date: ' + ', '.join(stale) + '. Run npm run seo.\n')
        print('Passed: generated metadata, structured data, sitemap and robots match site.config.json.')
    else:
        if args.site_url:
            config_path.write_text(json.dumps(config, ensure_ascii=False, indent=2) + '\n')
        for name, content in outputs.items():
            (ROOT / name).write_text(content)
        print('Updated static SEO files for ' + config['site_url'])


if __name__ == '__main__':
    main()
