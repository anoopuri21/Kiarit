# KIARIT PHARMACEUTICALS — Website

A luxury, light-theme marketing website for KIARIT PHARMACEUTICALS, built with
plain HTML, CSS and vanilla JavaScript. No frameworks, no build step, no
dependencies at runtime — the files in this repository are the files you deploy.

---

## Quick start

Any static host or web server will do. To preview locally:

```bash
python3 -m http.server 8080
# then open http://localhost:8080
```

Deploying is a straight file copy: upload everything except `tools/` and
`PLAN.md` to your web root.

---

## Pages

| File | Purpose |
| --- | --- |
| `index.html` | Home — hero video, trust strip, overview, two poster sections, product grid, CEO message, why-choose-us, testimonial slider, QR teaser, CTA |
| `about.html` | Company overview, mission and vision, core values, quality band, milestone timeline, CEO message |
| `products.html` | All five products with a category filter |
| `product-1.html` … `product-5.html` | Individual product pages with pricing, benefits, how-to-use, ingredients, reviews and FAQ |
| `contact.html` | Phone, WhatsApp and email cards, office location with map |
| `order.html` | Three-step ordering guide, UPI QR and bank details, shipping summary, FAQ |
| `privacy-policy.html` | Privacy policy |
| `terms.html` | Terms and conditions |
| `shipping-returns.html` | Shipping, returns and refunds |
| `disclaimer.html` | Medical and product disclaimer |
| `404.html` | Error page |

Supporting files: `sitemap.xml`, `robots.txt`, `site.webmanifest`, `.htaccess`.

---

## Project structure

```
.
├── index.html, about.html, products.html, product-1..6.html,
│   contact.html, order.html, privacy-policy.html, terms.html,
│   shipping-returns.html, disclaimer.html, 404.html
├── sitemap.xml, robots.txt, site.webmanifest, .htaccess
├── assets/
│   ├── css/
│   │   ├── fonts.css        self-hosted @font-face declarations
│   │   ├── base.css         design tokens, reset, typography
│   │   ├── components.css   buttons, header, nav, footer, cards, slider
│   │   ├── pages.css        home page sections
│   │   ├── inner.css        inner pages, product detail, legal prose
│   │   └── luxe.css         depth, texture and finishing layer (loads last)
│   ├── js/
│   │   ├── main.js          nav, dropdown, scroll progress, floaters, video
│   │   ├── reveal.js        scroll reveal animations
│   │   ├── slider.js        testimonial slider
│   │   └── filter.js        product category filter
│   ├── fonts/               Playfair Display + Inter (woff2)
│   ├── img/                 logo, CEO, posters, products, QR, OG image
│   └── video/               hero.mp4, hero.webm, hero-poster.jpg
└── tools/                   page generator — development only, do not deploy
```

### Stylesheet order

The five stylesheets are cascade-dependent and must stay in this order:

```
fonts.css → base.css → components.css → pages.css → inner.css → luxe.css
```

---

## Editing content

### The quick way — edit the HTML

Every page is readable, hand-formatted static HTML. Open the file, change the
text, save. Nothing to compile.

### The consistent way — use the generator

Because the header, footer, meta tags and structured data repeat across
fifteen pages, they are generated from shared partials. If you change anything
that appears on every page, edit the source and regenerate:

```bash
python3 tools/pages_phase4.py   # about, contact, order
python3 tools/pages_phase5.py   # products listing + 5 product pages
python3 tools/pages_phase6.py   # legal pages, 404, sitemap.xml, robots.txt
```

| To change | Edit |
| --- | --- |
| Phone, email, address, UPI, bank details, social links | `SITE` dict in `tools/build.py` |
| Product names, prices, copy, benefits, ingredients, FAQs | `PRODUCTS` list in `tools/build.py` |
| Header, footer or floating buttons | `tools/partials/*.html` — product lists and contact details are placeholders filled from `SITE` and `PRODUCTS` at build time |
| Reviews and ratings | `REVIEWS` / `RATINGS` in `tools/pages_phase5.py` |
| Legal text | `tools/pages_phase6.py` |

`index.html` is maintained by hand and is not generated. If you change a
partial, apply the same edit to `index.html`.

Requires Python 3 only — no packages. `tools/` is development tooling; it is
excluded from crawling by `robots.txt` and blocked by `.htaccess`.

---

## Before going live

Replace these placeholders with real values:

Real: contact details, product names, packaging specs and ingredient lists.

Still placeholder:

- [ ] **Payment details** — UPI ID, bank account, IFSC, and the QR image at
      `assets/img/qr/payment-qr.png`
- [ ] **Social links** — Facebook, Instagram, LinkedIn, YouTube
- [ ] **Logo** — `assets/img/logo.svg`
- [ ] **Product photography** — `assets/img/products/product-1..5.jpg` are
      AI-rendered from the supplied packaging artwork, not studio shots.
      Replace with real photography when available (square, ideally 1200×1200).
- [ ] **CEO photograph** — `assets/img/ceo.jpg`
- [ ] **Prices** — currently indicative
- [ ] **Domain** — set `url` in `SITE`, then regenerate so canonical tags,
      Open Graph URLs and `sitemap.xml` all point at the live domain
- [ ] **Reviews** — replace the sample reviews with genuine ones, or remove
      the review sections and the `aggregateRating` from the Product schema
- [ ] **Milestone years** on the About timeline
- [ ] **Map coordinates** in `tools/pages_phase4.py` for the real office

After changing `SITE`, run all three generator scripts and redeploy.

---

## SEO

- Unique title and meta description on every page, within recommended lengths
- Canonical URL, Open Graph and Twitter Card tags throughout
- JSON-LD structured data: `Organization`, `WebSite`, `BreadcrumbList`,
  `AboutPage`, `ContactPage`, `LocalBusiness`, `FAQPage`, `HowTo`, `ItemList`,
  `Product` with `offers` and `aggregateRating`, and `Person` for the CEO
- `sitemap.xml` with image entries for product pages, referenced from
  `robots.txt`
- Semantic landmarks, one `h1` per page and a correct heading hierarchy
- Descriptive `alt` text on every image

## Accessibility

- Skip-to-content link, visible focus rings, full keyboard navigation
- Touch targets of at least 24×24 px on coarse pointers
- `prefers-reduced-motion` disables scroll reveals, smooth scrolling and
  magnetic buttons, and skips the hero video download entirely, leaving its
  poster as a still hero
- ARIA labelling on the navigation, slider, accordions and filter controls
- Text contrast meets WCAG AA

## Performance

- Self-hosted variable fonts with `font-display: swap` and preloading
- Hero video is lazy-loaded: its sources sit in `data-src` behind
  `preload="none"` and are only attached once an IntersectionObserver reports
  the hero is near the viewport. Playback pauses off-screen and on hidden
  tabs. `prefers-reduced-motion` and Save-Data skip the download entirely.
- Lazy loading and explicit dimensions on below-the-fold images to avoid
  layout shift
- No third-party scripts, trackers or web fonts — the site makes no external
  requests
- First Contentful Paint measured at ~208 ms locally, with CSS, poster and JS
  all delivered before the video begins downloading

### Hero video

`assets/video/hero.*` is an 18-second seamless loop of the product range,
rendered by `tools/make_hero_video.py`. The committed output is all the site
needs; the source plates are gitignored, and the script header explains how to
re-create them if the video ever has to be rebuilt.

## Browser support

Current versions of Chrome, Edge, Firefox and Safari, desktop and mobile.
Tested at 390, 768, 1024, 1440 and 1920 px with no horizontal overflow.

---

## Notes

- There are no forms anywhere on the site by design. Orders are placed through
  WhatsApp, phone or email.
- There is no payment gateway. Payment is by UPI QR code or bank transfer, with
  confirmation handled manually.
- There is no blog and no CMS.
