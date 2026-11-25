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

Checks JavaScript syntax, local file references, anchor targets, SVG validity, image descriptions, generated SEO consistency, canonical/social metadata, JSON-LD, sitemap XML, and crawler rules.

## GitHub Pages

In [repository Settings → Pages](https://github.com/lakviat/coffee_factory/settings/pages), choose **Deploy from a branch**, **main**, **/ (root)**, then Save.

The site will be at **https://lakviat.github.io/coffee_factory/** after GitHub finishes publishing. All asset paths are relative, so the repository subpath works without configuration. `.nojekyll` keeps the static files intact. A GitHub Actions workflow is deliberately unnecessary for this buildless site.

## What is included

- Responsive desktop and mobile layout, mobile navigation, keyboard focus styles, native accessible product dialogs, and a skip link.
- Animated photographic hero, subtle section reveals, a scrolling brand ribbon, a pause control, and automatic reduced-motion support.
- Crema, Classico, and Intenso capsule details taken from the supplied package photos, and filters for capsules, coffee bags, or all formats.
- All five capsule and bag formats are visible by default; the existing bag illustrations remain unchanged pending approval of any new black-bag artwork.
- Small and large bag concept previews. Product names for the bags are working names, not a confirmed product catalog.
- A café section with the supplied street address and an address-search link. This does not imply an existing Google business listing.
- Instagram and Facebook links supplied by the owner, plus a TikTok coming-soon placeholder. Instagram currently opens the supplied homepage URL until the brand profile URL is available.
- A matching delivery section linking to Uber Eats, DoorDash, and Grubhub, reached through the header and mobile navigation. Links currently open the official platform homepages in new tabs; the page clearly states that Coffee Factory listings are coming soon.
- A matching online marketplace section linking to Amazon and Etsy homepages until the actual stores are ready. No eBay links are included.
- A separate wholesale and bulk-orders section with planned formats and a coming-soon status; no pricing, minimum quantities, or active order collection is implied.
- Clickable café addresses and neighborhood badge that open a compact Google Maps / Apple Maps chooser. Address links fall back to Google Maps without JavaScript; no embedded map is added.
- Search and social metadata and a scalable favicon.
- Static search metadata, a one-page XML sitemap, crawler rules, and connected WebSite, WebPage, and CafeOrCoffeeShop structured data. Miami-area and South Florida copy accurately places the planned café in Hallandale Beach and describes delivery and online shopping as coming soon.

## Brand direction and references

`assets/brand/owner-logo.webp` is a pixel-identical, lossless web export of the higher-resolution logo supplied by the owner. The header, footer, hero badge, and favicon use this artwork. Existing packaging concepts retain their original illustrations.

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

When delivery listings are ready, replace the three `href` values in `#delivery .delivery-platform` in `index.html` with the exact Coffee Factory storefront URLs. Update the link text, status, and explanatory note to reflect actual availability. No JavaScript or API integration is needed for these outbound ordering links.

For Amazon and Etsy, update the two `href` values in `#marketplaces .marketplace-platform` and the section's status when the stores are available. Add approved wholesale contact and ordering details to `#wholesale` when ready. Map destinations live in the `.map-dialog`; every address trigger keeps a direct Google Maps fallback.

Update the Instagram and Facebook URLs in `#connect .social-links` when their final Coffee Factory profiles are ready. Replace the TikTok placeholder button with a matching link once its profile URL is supplied.

## Search setup and the future domain

`site.config.json` is the source for the public site URL, title, description, social preview, and business identity. Run `npm run seo` after changing it, then `npm run check`. Generated metadata is included in the served HTML; crawlers do not need JavaScript. GitHub Pages needs no build step.

- The current canonical is `https://lakviat.github.io/coffee_factory/`. `sitemap.xml` lists this one page; section fragments and product dialogs are not separate pages. There is no invented modification date or ranking priority.
- `robots.txt` allows crawling and advertises the absolute sitemap URL. **On the current project URL, `/coffee_factory/robots.txt` is not the host-root robots file and does not control crawlers.** Google reads `https://lakviat.github.io/robots.txt`; it returned 404 during this setup, so no host-root restriction was present. This repository does not modify that separate host-root site. Recheck it if another project adds rules. The prepared file will apply when the custom domain serves this repository at `/`.
- Titles, descriptions, readable copy, and business data cover Hallandale Beach, the Miami area, South Florida, coffee capsules/boxes, small and large bags, planned coffee delivery, and wholesale. No hidden keyword lists or meta-keyword tag are used; Google ignores meta keywords.
- Business markup uses the supplied name and actual planned address. Opening hours, launch dates, phone, coordinates, pricing, ratings, order actions, and active delivery coverage are omitted until confirmed. Generic platform URLs and the Facebook page still using another identity are not asserted as official `sameAs` identities. Product/merchant rich-result markup waits for confirmed sale details.
- The page is indexable over HTTPS. Publishing these files does **not** verify ownership, submit a sitemap, create a Maps listing, guarantee indexing/rankings, or certify compliance with every platform policy.

### Search engine account steps

These require the owner's account and a real verification token; none is fabricated or committed:

1. In [Google Search Console](https://search.google.com/search-console/), add the URL-prefix property `https://lakviat.github.io/coffee_factory/`. Use the provided HTML verification file in the repository root, or place the exact verification meta tag outside the generated SEO block. Verify ownership, submit `https://lakviat.github.io/coffee_factory/sitemap.xml`, then inspect the homepage and request indexing.
2. In [Bing Webmaster Tools](https://www.bing.com/webmasters/), verify/import the same site and submit the sitemap. Track processing and crawl/indexing errors in both tools.
3. For Google Maps and Apple Maps, claim and verify separate business listings using confirmed opening and business details. Website structured data is not a substitute for those listings.

### When the domain is purchased

1. Configure the custom domain in GitHub Pages, its DNS records, domain ownership verification, and HTTPS. Add the actual `CNAME` only then; no unpurchased domain is claimed now.
2. Generate all domain-dependent SEO from one command (replace this example):

   ```sh
   npm run seo -- --site-url https://your-domain.example/
   npm run check
   ```

   This updates `site.config.json`, canonical/Open Graph URLs, structured-data IDs and asset URLs, `sitemap.xml`, and the sitemap directive in `robots.txt`. Commit and deploy them together. Existing relative image, font, stylesheet, and navigation paths also work at the domain root.
3. Check that the old GitHub Pages URL redirects to the custom domain, and the new homepage, `/robots.txt`, `/sitemap.xml`, images, and styles return successfully over HTTPS. Use one preferred hostname and ensure other variants redirect there.
4. Verify the new domain property in Search Console and Bing; submit its sitemap, inspect the page, and monitor the move. Update social profiles and any external links to the final URL.

References: [Google sitemap guidance](https://developers.google.com/search/docs/crawling-indexing/sitemaps/build-sitemap), [host-root robots rules](https://developers.google.com/crawling/docs/robots-txt/create-robots-txt), [supported meta tags](https://developers.google.com/search/docs/crawling-indexing/special-tags), and [local business structured data](https://developers.google.com/search/docs/appearance/structured-data/local-business).
