# KIARIT PHARMACEUTICALS — Website Master Plan
**Luxury Cosmetic / Pharma Brand Website — Static (HTML + CSS + Vanilla JS)**

Version: 1.0 · Date: 2026-09-05 · Status: Awaiting client approval

---

## 1. Project Snapshot

| Item | Decision |
|---|---|
| Company | KIARIT PHARMACEUTICALS |
| Type | Static, multi-page website (no backend, no build tools) |
| Tech Stack | HTML5, CSS3 (custom, no framework), Vanilla JS (ES6, no libraries) |
| Theme | **Light theme** — ivory / warm white base |
| Base Colors | **Gold + Black** |
| Support Colors | Champagne beige, warm ivory, soft rose-nude, deep charcoal, muted sage (pharma trust accent) |
| Typography | Headings: elegant serif (Cormorant Garamond / Playfair Display) · Body: formal humanist sans (Inter / Source Sans 3) |
| Payment | **No payment gateway** — UPI/Bank **QR code** based manual payment |
| Forms | **Zero forms** — all contact via `tel:`, `mailto:`, WhatsApp deep links |
| Products | 6 products |
| Blog | Not included |
| Hosting target | Any static host (GitHub Pages / Netlify / cPanel) |

---

## 2. Page List (Final Proposal)

### A. Core Pages — 11 HTML files

| # | Page | File | Purpose | Key Sections |
|---|---|---|---|---|
| 1 | **Home** | `index.html` | Brand impact + full funnel | Hero video, About teaser, Poster #1, Products grid (6), Poster #2, CEO message, Why Choose Us, Testimonials slider, CTA band, Footer |
| 2 | **About Us** | `about.html` | Company story & trust | Overview, Mission/Vision, Values, Quality & Compliance, Milestones timeline, CEO full message, CTA |
| 3 | **Products (Listing)** | `products.html` | All 6 products in one place | Filter/category chips, 6 product cards, Ordering info strip, CTA |
| 4–9 | **Product Detail ×6** | `product-1.html` … `product-6.html` | SEO landing page per product | Gallery, name, price, description, key benefits, how to use, ingredients, "Order on WhatsApp" + QR, related products |
| 10 | **Contact** | `contact.html` | Reach-out hub (no form) | Phone / Email / Address cards, WhatsApp CTA, Google Map embed, business hours, social links |
| 11 | **How to Order & Pay** | `order.html` | QR payment flow explained | 3-step order process, large QR code, UPI ID, bank details, order-confirm-on-WhatsApp CTA, FAQ accordion |

> Product detail pages are **separate HTML files (not modals)** — this is the single biggest SEO win: 6 extra indexable pages with their own title, meta description, Product schema, and price.

### B. Legal / Utility Pages — 5 files

| # | Page | File | Purpose |
|---|---|---|---|
| 12 | Privacy Policy | `privacy-policy.html` | Trust + Google requirement |
| 13 | Terms & Conditions | `terms.html` | Trust + legal |
| 14 | Shipping & Returns | `shipping-returns.html` | E-commerce trust signal |
| 15 | Disclaimer | `disclaimer.html` | Mandatory for pharma/cosmetic claims |
| 16 | 404 Page | `404.html` | Branded not-found page |

### C. SEO / Config Files — 5 files

| File | Purpose |
|---|---|
| `sitemap.xml` | All 16 URLs listed for search engines |
| `robots.txt` | Crawl rules + sitemap pointer |
| `site.webmanifest` | PWA-lite, favicon set, theme color |
| `.htaccess` (optional) | Clean URLs, gzip, cache headers |
| `README.md` | Handover / deployment doc |

**TOTAL = 16 pages + 5 config files**

---

## 3. Folder Structure

```
/
├── index.html
├── about.html
├── products.html
├── product-1.html  ...  product-6.html
├── contact.html
├── order.html
├── privacy-policy.html
├── terms.html
├── shipping-returns.html
├── disclaimer.html
├── 404.html
├── robots.txt
├── sitemap.xml
├── site.webmanifest
└── assets/
    ├── css/
    │   ├── base.css        (reset, tokens/variables, typography)
    │   ├── components.css  (buttons, cards, navbar, footer, slider)
    │   └── pages.css       (page-specific blocks)
    ├── js/
    │   ├── main.js         (nav, dropdown, mobile menu, floating buttons)
    │   ├── reveal.js       (cinematic scroll engine — IntersectionObserver)
    │   └── slider.js       (testimonial slider, product gallery)
    ├── img/
    │   ├── logo.svg / logo.png
    │   ├── ceo.jpg
    │   ├── products/  (6 product images — client to provide)
    │   ├── posters/   (2 custom poster artworks)
    │   ├── qr/        (payment QR)
    │   └── og/        (social share images)
    ├── video/
    │   ├── hero.mp4
    │   ├── hero.webm
    │   └── hero-poster.jpg  (first-frame fallback)
    └── fonts/  (self-hosted woff2 for speed)
```

---

## 4. Global Components (present on every page)

### 4.1 Top Bar (thin, black background, gold text)
`📞 +91-XXXXXXXXXX` · `✉ info@kiaritpharma.com` · right side → Facebook, Instagram, LinkedIn, YouTube, WhatsApp icons.
Hides on scroll-down, reappears on scroll-up (premium behaviour).

### 4.2 Navbar (sticky, glass-blur white, gold underline animation)
```
[LOGO]   Home   About   Products ▾   Contact   Order & Pay        [ Shop on WhatsApp ]
                          └─ dropdown: Product 1 … Product 6 · View All Products
```
- Only **Products** has a dropdown (as requested).
- Mobile: full-screen slide-in menu with staggered link animation.

### 4.3 Floating Buttons (bottom-right stack)
- 🟢 **WhatsApp** — always visible, gentle pulse ring.
- ⬆ **Scroll to Top** — fades in after 400px, gold circle with progress ring showing scroll %.

### 4.4 Footer (deep black, gold hairline dividers, 4 columns)
Brand + short overview · Quick Links · Our Products (6 links) · Contact & QR thumbnail
Bottom bar: © 2026 KIARIT PHARMACEUTICALS · Privacy · Terms · Disclaimer

---

## 5. HOME PAGE — Detailed Design Blueprint

> Scroll story: **Cinema → Trust → Desire → Proof → Action**

| # | Section | Design Detail | Animation |
|---|---|---|---|
| 1 | **Hero (100vh)** | Full-bleed muted autoplay loop video (mp4 + webm), dark-to-transparent gold gradient scrim, centered: eyebrow "SCIENCE MEETS BEAUTY", H1 *KIARIT PHARMACEUTICALS*, one-line tagline, 2 CTAs (**Explore Products** / **About Us**), scroll-cue arrow | Text lines rise + blur-in in sequence; video slow zoom (Ken Burns); parallax on scroll |
| 2 | **Trust Strip** | Thin gold-bordered band: GMP Certified · Dermatologist Tested · Cruelty Free · Made in India | Count-up / fade-in |
| 3 | **Overview / About Teaser** | Split 55/45 — left: gold-framed image collage; right: the official company overview paragraph + "Read Our Story" ghost button | Image clip-path reveal from left, text slide-up |
| 4 | **POSTER SECTION #1 — "The Gold Standard of Skincare"** | Full-width custom-designed editorial poster (custom artwork, not stock): black canvas, gold foil typography, product silhouette, hairline gold frame, offset headline block | Layered parallax (3 depths) + gold shimmer sweep on scroll-in |
| 5 | **Our Products (6)** | 3×2 grid of luxury cards: soft ivory card, product image on champagne circle backdrop, name (serif), 2-line description, price in gold, "View Details" + "Order on WhatsApp" | Staggered card rise (80ms delay each), hover: lift + gold border draw + image zoom |
| 6 | **POSTER SECTION #2 — "Formulated by Science, Perfected by Nature"** | Split diagonal poster: left ivory with big serif claim + 3 icon pillars (Research · Purity · Results); right black panel with gold macro texture | Diagonal wipe reveal, counter numbers animate |
| 7 | **CEO's Message** | Ivory bg, large gold quote mark, portrait in gold arch frame with subtle grain, generic message paragraph, signature line: **Yogesh Kumar Bharta — Founder & CEO** | Portrait scale-in, quote text word-by-word fade |
| 8 | **Why Choose Us** | 4 icon cards (Quality Assurance, Innovation, Affordability, Patient-Centric) | Icon draw-in + card stagger |
| 9 | **Testimonials Slider** | Dark charcoal band, custom-built vanilla JS slider: 1 card desktop-centered / peek of next, 5-star gold, avatar initials in gold circle, autoplay + dots + arrows + swipe, pause on hover | Card cross-fade + slide, dots morph |
| 10 | **Order & Pay Teaser** | Compact band: QR code card + 3-step how-to-order + "Full Payment Details" link | Fade-up |
| 11 | **CTA Band (2 buttons)** | Black band with gold radial glow: headline "Ready to experience KIARIT?" → **[About Us]** (gold solid) + **[Contact Us]** (gold outline) | Glow pulse, buttons magnetic hover |
| 12 | **Footer** | As per §4.4 | Fade-in |

### Cinematic Scroll System (vanilla JS, no library)
- `IntersectionObserver` adds `.is-visible` → CSS transitions handle motion (GPU-friendly: `transform` + `opacity` only).
- Data attributes: `data-reveal="up|left|right|zoom|blur|mask"`, `data-delay="120"`.
- Parallax on hero/posters via `requestAnimationFrame` + `transform: translate3d()`.
- Section-level `scroll-driven` gold progress line in navbar.
- Full `prefers-reduced-motion` fallback (accessibility + SEO/UX score).

---

## 6. SEO Plan (complete, on-page)

- Unique `<title>` (≤60 chars) + `meta description` (≤160) per page.
- Canonical URLs, `lang="en-IN"`, `theme-color`.
- **Open Graph + Twitter Cards** with custom OG images.
- **JSON-LD structured data**: `Organization` + `LocalBusiness` (all pages), `Product` + `Offer` + `AggregateRating` (6 product pages), `BreadcrumbList`, `FAQPage` (order page), `Person` (CEO).
- Semantic HTML5 landmarks, single `<h1>` per page, logical H2/H3 order.
- All images: descriptive `alt`, `width`/`height` set (CLS = 0), `loading="lazy"` below fold, WebP with fallback.
- Video: `preload="metadata"`, poster image, no layout shift.
- `sitemap.xml`, `robots.txt`, clean descriptive URLs, internal linking mesh.
- Performance targets: Lighthouse **90+** on Performance / SEO / Best Practices / Accessibility. Critical CSS inlined, fonts `font-display:swap`, self-hosted.
- Skip-to-content link, ARIA labels on nav/slider/floating buttons, keyboard-navigable dropdown & slider.

---

## 7. Phase-wise Execution Roadmap

| Phase | Deliverable | Notes |
|---|---|---|
| **Phase 0** ✅ | This plan + page list approval | You are here |
| **Phase 1** | Design foundation: `base.css` design tokens (colors, type scale, spacing, shadows), global Top bar + Navbar + Footer + floating buttons, scroll engine (`reveal.js`) | The "look" gets locked here |
| **Phase 2** | **HOME PAGE** full build — all 12 sections incl. 2 custom posters, testimonial slider, CEO block (placeholder images where assets pending) | Main visual deliverable |
| **Phase 3** | Hero video sourced/generated (product-free, abstract luxury: gold silk / ink-in-water / light rays), optimized mp4 + webm + poster frame | Can run parallel to Phase 2 |
| **Phase 4** | About page + Contact page + Order & Pay page (QR) | |
| **Phase 5** | Products listing + 6 product detail pages (wired to your images/names/prices) | Needs your product data |
| **Phase 6** | Legal pages + 404 + sitemap/robots/manifest/favicons | |
| **Phase 7** | SEO audit, schema validation, responsive QA (360 / 768 / 1024 / 1440 / 1920), performance pass, cross-browser check, handover README | Final polish |

---

## 8. Assets Needed From Client

| Asset | Status |
|---|---|
| 6 product images | ⏳ You'll share in next chat |
| Logo (PNG/SVG, transparent) | ⏳ Pending |
| CEO photo — Yogesh Kumar Bharta | ⏳ Pending |
| Payment QR code image (UPI) | ⏳ Pending — placeholder till then |
| Product names, descriptions, prices (6) | ⏳ Pending |
| Phone, WhatsApp number, email, office address | ⏳ Pending |
| Social media profile links | ⏳ Pending |
| Hero video | 🔧 I will research/generate (product-free, abstract luxury) |
| 2 poster artworks | 🔧 I will design custom for KIARIT |
| Testimonial content | 🔧 I will write generic (you can replace) |
| CEO message text | 🔧 I will write generic as requested |

---

## 9. What "10k$ Luxury" Means Here (execution standards)

1. **Restraint** — lots of white space, max 2 fonts, gold used as accent (≤10% of surface), never as fill everywhere.
2. **Editorial layout** — asymmetric grids, oversized serif headlines, hairline rules, generous letter-spacing on eyebrows.
3. **Motion with intent** — slow easing curves (`cubic-bezier(.16,1,.3,1)`), 600–900ms, nothing bouncy.
4. **Micro-details** — gold border-draw on hover, image grain overlay, custom cursor-ish magnetic buttons, gold scroll progress, custom-styled scrollbar.
5. **Consistency** — one 8pt spacing system, one radius scale, one shadow scale, all from CSS variables.
