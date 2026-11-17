# Coffee Factory

A responsive, static first website for Coffee Factory: a coffee collection and a planned neighborhood café at **1801 South Ocean Drive, Hallandale Beach, Florida**, on the first floor at the corner of Imperial Towers.

## Preview

```sh
npm run dev
```

Open `http://127.0.0.1:4173`. No installation or build step is needed; the development command uses Python 3's static server.

```sh
npm run check
```

Checks JavaScript syntax, local file references, anchor targets, SVG validity, image descriptions, and essential metadata.

## GitHub Pages

In [repository Settings → Pages](https://github.com/lakviat/coffee_factory/settings/pages), choose **Deploy from a branch**, **main**, **/ (root)**, then Save.

The site will be at **https://lakviat.github.io/coffee_factory/** after GitHub finishes publishing. All asset paths are relative, so the repository subpath works without configuration. `.nojekyll` keeps the static files intact. A GitHub Actions workflow is deliberately unnecessary for this buildless site.

## What is included

- Responsive desktop and mobile layout, mobile navigation, keyboard focus styles, native accessible product dialogs, and a skip link.
- Animated photographic hero, subtle section reveals, a scrolling brand ribbon, a pause control, and automatic reduced-motion support.
- Crema, Classico, and Intenso capsule details taken from the supplied package photos, and filters for capsules, coffee bags, or all formats.
- Small and large bag concept previews. Product names for the bags are working names, not a confirmed product catalog.
- A café section with the supplied street address and an address-search link. This does not imply an existing Google business listing.
- Instagram, Facebook, LinkedIn, and online store placeholders that explain their coming-soon status when selected.
- Search and social metadata and a scalable favicon.

## Brand direction and references

The supplied packaging is the source of truth: charcoal, ivory, copper, and burgundy; a circular cup-and-steam seal; and straightforward sans-serif package typography. `assets/brand/logo-source.webp` contains a transparent, photo-based reconstruction of the supplied seal, with its solid cup, broad steam, bold ring lettering and four beans. It is a close reconstruction, not the original production artwork. The SVG wrappers apply consistent ink colors and embed this source so they work on standalone packaging previews as well. `scripts/prepare_vectors.py` recreates those wrappers and packaging illustrations. Replace the source with approved production artwork when available.

Barlow Condensed supplies the bold editorial headings, while DM Sans keeps supporting information readable. Both fonts are self-hosted with their licenses in `assets/fonts/`.

The reference sites informed the balance of café and retail content, warm neutrals, large visual opening, and approachable product browsing:

- https://coffeebar.com/
- https://www.gingerandwhite.com/
- https://thinkingcup.info/
- https://www.tobysestate.com.au/
- https://gritcoffee.com/

The design and copy are original; no competitor branding or photographs have been reused.

## Images and concept status

- `espresso-hero.webp` and `coffee-still-life.webp`: generated concept photography. The package still life was reconstructed from the supplied Coffee Factory photographs. Replace with final brand photography when available.
- `crema.svg`, `classico.svg`, and `intenso.svg`: vector packaging reconstructions based on the supplied boxes. Bag illustrations are early concepts; weights, grind, blends, and pricing remain unconfirmed.
- `imperial-towers.jpg`: building photo reused with the user's permission from `lakviat/imperial_towers/public/images/imperial-towers-original.jpg`; original credit: Imperial Towers Condominium Inc.
- Source photographs and full-resolution image generations remain outside the published asset set. They are intentionally excluded from Git.

## Before launch

Confirm the final logo, street address and entrance, opening status, hours, café menu, contact details, final product list, prices, package sizes, and social URLs. The current page deliberately announces no opening date, hours, prices, reviews, sourcing claims, or unconfirmed certifications.

Ordering and social integrations are future work. There is no checkout, payment processing, mailing-list collection, or backend in this design phase. Product data lives in `script.js`; text and sections live in `index.html`; visual tokens are at the top of `styles.css`.
