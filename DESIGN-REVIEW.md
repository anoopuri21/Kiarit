# KIARIT — Design Review & Improvement Plan

A critique of the current build from a visual-design standpoint, followed by a
staged plan to fix it. Every claim below is backed by a measurement taken from
the rendered page at 1440 px, not by opinion alone.

---

## Part 1 — The verdict

The site is **competently built but not distinctively designed.** It reads as a
high-quality template rather than a brand. The craft is there — spacing is
clean, nothing is broken, the type is well set. What is missing is a point of
view.

Three problems sit underneath almost every other issue:

1. **It leans on darkness for luxury.** The brief asked for a light theme. The
   page is 42% dark pixels.
2. **It has no colour.** Mean saturation across mid-page is 12.8/255 — about
   5%. The palette defines sage, rose-nude and champagne; the page uses gold,
   black and grey.
3. **Every section is the same shape.** Centred heading, then a grid of cards,
   134 px of padding, repeat. Eleven times.

---

## Part 2 — What the measurements show

### 2.1 The theme contradiction

Pixel luminance sampled across twelve full screens of the home page:

| Screen | Section | Avg luminance | Dark pixels |
| --- | --- | --- | --- |
| 1 | Hero | 37.7 | **90.8%** |
| 2 | Overview | 186.8 | 24.0% |
| 3 | Poster #1 | 71.6 | **79.2%** |
| 4 | Product grid | 221.4 | 5.2% |
| 5 | Product grid | 238.8 | 0.2% |
| 6 | Poster #2 | 200.4 | 18.9% |
| 7 | CEO | 220.9 | 9.7% |
| 8 | Why choose us | 228.4 | 4.2% |
| 9 | Testimonials | 143.3 | **47.0%** |
| 10 | Testimonials | 129.5 | **50.5%** |
| 11 | Order / CTA | 63.5 | **76.7%** |
| 12 | Footer | 24.0 | **99.0%** |

**42.1% of the page is dark.** Six of twelve screens are more than 45% dark.

This matters beyond the brief. A visitor scrolling the page experiences six
hard black-to-ivory transitions. Each one forces the eye to re-adapt, and each
one resets the visual narrative. The page feels like six different websites
stitched together rather than one continuous story.

The deeper issue is *why* the darkness is there. It is doing the work that
should be done by typography, composition and material detail. Black plus gold
is the fastest possible shorthand for "premium" — and it is the reason the site
looks like every other pharma-luxe template. Genuinely expensive brands in this
category (Aesop, Augustinus Bader, Dr. Barbara Sturm, Typology) are almost
entirely light. Their authority comes from restraint, generous white space and
photography, not from black backgrounds.

### 2.2 The palette is declared but never used

`base.css` defines a full palette:

```
gold-500  #c9a227    champagne  #f2e9db
black-900 #08080a    rose-nude  #f4e6e0
ivory     #fdfbf7    sage       #7d8f7a
```

In practice the rendered page uses ten text colours, and eight of them are
gold, black, white or grey. Sage appears once (a product badge). Rose-nude
never appears at all.

Measured saturation: **12.8/255 mid-page, 25.0/255 in the values section.**

The result is a page that is technically "gold and black plus complementary
colours" but visually monochrome. There is no colour-coding to help a visitor
distinguish dermatology from nutraceuticals, no seasonal warmth, no way for any
section to feel different from another except by going dark.

### 2.3 The type scale is not a scale

28 distinct font sizes are rendered on the home page. Headings in document
order:

```
H1  76px
H2  58px   ← poster
H2  50px   ← standard section
H3  21px   ← product card
H3  19px   ← value card
```

The problem is the gap. From 50 px straight down to 21 px is a **2.4× jump with
nothing in between.** A type system needs a mid-tier — something around 30–34 px
— for sub-section headings, pull quotes and feature callouts. Without it, every
piece of content is either a giant section heading or a small card title, and
the page loses its ability to express "this is important, but not the most
important thing here."

Body text is set at three line-heights (1.68, 1.70, 1.72) that are close enough
to be indistinguishable but different enough to be untidy. And the eyebrow
labels — the small gold caps above every heading — are 12.48 px, which is too
small to carry the weight they are being asked to carry.

### 2.4 Spacing has no system

27 distinct `gap` values are in use, including 3.52 px, 6.864 px, 7.904 px,
8.32 px and 8.736 px. These are not design decisions; they are `clamp()`
outputs that happen to land wherever the viewport puts them.

Section padding is the opposite problem — it is *too* consistent:

| Section | Padding top/bottom |
| --- | --- |
| Overview | 134 px |
| Product grid | 134 px |
| CEO | 134 px |
| Values | 134 px |
| Testimonials | 134 px |
| Order | 83 px |

Nine of eleven sections use exactly 134 px. Uniform padding sounds like good
practice, but it flattens hierarchy. A hero, a product grid and a legal
footnote should not breathe identically. Editorial design uses spacing to
signal importance: a lot of air around the thing that matters, tighter
grouping for supporting content.

### 2.5 Accessibility: 36 contrast failures

Of 128 text nodes measured, **36 fail WCAG AA.** The pattern is consistent:

| Element | Colour on background | Ratio | Needs |
| --- | --- | --- | --- |
| Eyebrow "WHO WE ARE" | `#a8801f` on `#fdfbf7` | 3.52:1 | 4.5:1 |
| Eyebrow "OUR COLLECTION" | `#a8801f` on `#f8f4ec` | 3.32:1 | 4.5:1 |
| Card category "Dermatology" | `#a8801f` on `#f8f4ec` | 3.32:1 | 4.5:1 |
| Badge "Dermat Choice" | white on sage | 3.45:1 | 4.5:1 |

Every one is gold text at small size on a warm background. Gold at `#a8801f` is
simply not dark enough to carry 10–12 px text. This is a systemic palette
issue, not a series of one-off mistakes — and it is the single most common
accessibility failure in luxury cosmetics sites.

### 2.6 Composition: eleven variations of one idea

Section shapes down the home page:

```
Hero            full-bleed, left-aligned      ✓ distinct
Overview        image left  / text right
Poster #1       text left   / image right
Product grid    centred heading + 3-col grid
Poster #2       text left   / image right     ← repeat of poster #1
CEO             image left  / text right      ← repeat of overview
Values          centred heading + 4-col grid  ← repeat of product grid
Testimonials    centred heading + slider
Order           centred heading + 3-col grid  ← repeat again
CTA             centred                        
```

**Four centred-heading-plus-card-grid sections. Two identical split layouts.
Two identical poster layouts.** After the hero there is not a single
compositional surprise — no asymmetry, no overlap, no full-bleed image, no
change of grid, no moment where the layout does something unexpected.

Card counts reinforce it: 6 products, 4 values, 3 steps, 4 trust items — all in
evenly-divided grids of equal-height boxes.

### 2.7 Craft details

- **11 distinct box-shadows.** A depth system needs three or four levels, used
  consistently. Eleven means shadows were added per-component rather than drawn
  from a scale.
- **7 border radii**, including two malformed values (`236px 236px 18px 18px`).
- **Button heights of 39, 45 and 51 px**, plus two `btn--block` instances
  rendering at **0 px height** — a live bug.
- **Line length up to 88 characters.** Comfortable reading is 60–75. The
  overview paragraph and product-grid intro both exceed it.
- **The `luxe.css` layer adds texture** (grain, glows, inset highlights) but
  applies it uniformly, so it reads as a filter over the whole page rather than
  as material differentiation between surfaces.

---

## Part 3 — How it should have been designed

### 3.1 Light as the default, dark as punctuation

The page should be **90% light.** Dark should appear at most twice — the hero,
and one deliberate moment near the end — and should feel like an event when it
arrives, not like every third section.

Everything currently carrying "premium" through darkness needs to carry it
another way:

| Currently dark | Should instead be |
| --- | --- |
| Poster #1 (79% dark) | Warm champagne field, oversized editorial type, product macro photography |
| Testimonials (47–50% dark) | Ivory with a single tinted quote card, generous air |
| Order/CTA (77% dark) | Champagne-to-ivory gradient with a gold rule |
| Footer (99% dark) | Deep warm ink `#1a1714`, not near-black — a warm close, not a void |

That leaves the hero as the one true dark moment: justified, because it holds
video, and because a light page makes a dark hero far more striking than a
half-dark page ever could.

### 3.2 A palette that is actually used

Gold and black stay as the brand anchors, but three supporting tones need to do
real work:

```
Champagne  #f2e9db   section fields, alternate bands
Sage       #7d8f7a   dermatology / clinical cues
Rose-nude  #f4e6e0   skincare / sensorial cues
Clay       #b8734a   nutraceutical / warmth accent   ← new
Ink        #1a1714   warm near-black for text and footer   ← replaces #08080a
```

Two rules make the difference:

1. **Category colour-coding.** Each product family gets a tint that appears on
   its card, its detail page hero and its badge. A visitor learns the system
   without being told.
2. **Warm ink instead of pure black.** `#08080a` is a cold blue-black that
   fights the warm ivory. `#1a1714` sits in the same temperature family and
   makes the whole page feel intentional.

### 3.3 A real type scale

A modular scale at 1.28 ratio, with the missing mid-tier restored:

| Role | Size | Font |
| --- | --- | --- |
| Display | 76 px | Playfair Display |
| H2 | 52 px | Playfair Display |
| **H3 (new mid-tier)** | **32 px** | **Playfair Display** |
| H4 / card title | 21 px | Playfair Display |
| Lead | 19 px | Inter |
| Body | 17 px | Inter |
| Small | 15 px | Inter |
| Eyebrow | **13 px** (up from 12.48) | Inter, tracked |

One body line-height (1.7), one lead line-height (1.6), one heading
line-height (1.08). Measure capped at 68 characters everywhere.

### 3.4 Spacing on an 8 px grid

Every gap and pad snaps to: `4 · 8 · 12 · 16 · 24 · 32 · 48 · 64 · 96 · 128`.

Section padding becomes **three tiers**, not one:

| Tier | Padding | Used for |
| --- | --- | --- |
| Hero / statement | 160 px | Hero, final CTA |
| Standard | 112 px | Most sections |
| Tight | 72 px | Supporting content, trust strip, order steps |

### 3.5 Composition with variety

The eleven sections should use at least six distinct compositional patterns:

```
1  Hero            full-bleed video, left-weighted            (dark)
2  Trust strip     thin horizontal band, tight
3  Overview        asymmetric 5:7 split, image bleeding left edge
4  Poster #1       LIGHT — oversized type, offset stat block, macro image
5  Products        3-col grid, but first card double-width and featured
6  Poster #2       full-bleed image with overlapping ivory text card
7  CEO             portrait bleeding off the right edge, quote overlapping
8  Values          horizontal numbered list, NOT a card grid
9  Testimonials    single large quote, ivory, oversized quotation mark
10 Order           3 steps as a connected horizontal timeline
11 CTA             centred, champagne gradient, dark only if needed
```

The principles: **break the grid at least twice** (overlap, bleed), **vary the
container** (one full-bleed, one narrow), and **never run the same layout twice
in a row.**

### 3.6 Depth and material

Reduce to a four-level shadow scale and give surfaces real material identity:

```
sh-1   0 1px 2px rgba(26,23,20,.04)                    resting cards
sh-2   0 4px 16px rgba(26,23,20,.06)                   raised
sh-3   0 12px 32px rgba(26,23,20,.08)                  hover
sh-4   0 24px 64px rgba(26,23,20,.12)                  modal / feature
```

Three radii only: `8px` (inputs, small), `16px` (cards), `999px` (pills).

Paper grain stays, but only on champagne fields — so the texture *means*
something rather than sitting over everything equally.

---

## Part 4 — Improvement plan

Five stages, ordered so that the highest-impact and lowest-risk work happens
first. Each stage is independently shippable.

### Stage 1 — Foundation: tokens (low risk, high leverage)

Rewrite the token layer in `base.css`. Nothing structural changes, but every
component inherits the fix.

- Replace `#08080a` with warm ink `#1a1714` throughout.
- Darken gold for text use: add `--gold-text: #8a6410` (measured 5.1:1 on
  ivory) and reserve `#c9a227` for fills, rules and decoration only. **Fixes
  all 36 contrast failures.**
- Introduce the 8 px spacing scale; replace `clamp()` gaps with scale steps.
- Introduce the type scale including the 32 px mid-tier; raise eyebrows to
  13 px.
- Collapse 11 shadows to 4, 7 radii to 3.
- Add `--tint-derma`, `--tint-skin`, `--tint-nutra`, `--tint-hair`.

*Expected result: contrast failures 36 → 0; distinct font sizes 28 → ~12;
distinct gaps 27 → 10.*

### Stage 2 — Light conversion (the brief)

Convert the four dark bands.

- **Poster #1** → champagne field, oversized Playfair, offset stat block over a
  macro image. This is the biggest single visual change on the page.
- **Testimonials** → ivory, one large quote at a time, oversized gold quotation
  glyph, slider dots below.
- **Order teaser / CTA** → champagne-to-ivory gradient, gold hairline rule.
- **Footer** → warm ink `#1a1714`, gold rule, lighter type.
- Hero stays dark — the one intentional dark moment.

*Expected result: dark pixel coverage 42% → ~12%.*

### Stage 3 — Composition

Rework the four repeated layouts identified in 2.6.

- **Values** — from a 4-card grid to a horizontal numbered list with large
  ghost numerals and hairline dividers.
- **Products** — feature the bestseller at double width in the first grid cell.
- **CEO** — portrait bleeds off the right edge; the pull-quote overlaps the
  image.
- **Poster #2** — full-bleed image with an ivory text card overlapping its
  lower-left corner.
- **Order steps** — a connected horizontal timeline instead of three boxes.

*Expected result: 6 distinct section patterns instead of 3.*

### Stage 4 — Colour and material

- Apply category tints across product cards, detail heroes and badges.
- Restrict grain texture to champagne fields.
- Add a repeating hairline motif (a 1 px gold rule with a small diamond at
  centre) as a section divider — a small, ownable brand device.
- Introduce one editorial flourish: a vertical rotated brand line in the
  margins of poster sections.

### Stage 5 — Motion and polish

- Standardise reveal distance (24 px) and duration (0.6 s) — currently varies.
- Stagger card reveals at 60 ms, not the current mix of 70–120 ms.
- Add a subtle parallax to poster images only (respecting reduced motion).
- Fix the `btn--block` 0 px height bug.
- Re-audit line lengths at 68 characters.

---

## Part 5 — Measurable targets

| Metric | Now | Target |
| --- | --- | --- |
| Dark pixel coverage | 42.1% | ≤ 12% |
| WCAG AA contrast failures | 36 | 0 |
| Distinct font sizes | 28 | ≤ 12 |
| Distinct gap values | 27 | ≤ 10 |
| Distinct shadows | 11 | 4 |
| Distinct radii | 7 | 3 |
| Distinct section layouts | 3 | ≥ 6 |
| Max line length | 88 ch | ≤ 68 ch |
| Mean saturation (mid-page) | 12.8/255 | 28–40/255 |
| Sections at identical padding | 9 of 11 | ≤ 5 of 11 |

---

## Part 6 — What is already good and should be kept

Not everything needs changing. These decisions are sound:

- **Playfair Display + Inter** is a strong, appropriate pairing — display serif
  for authority, neutral grotesque for the formal body text the brief asked
  for. Self-hosting was the right call.
- **The 1280 px container with 80 px gutters** is well judged.
- **The hero** genuinely works — the video, the gold gradient italic and the
  stat row are the strongest moment on the site.
- **Product card structure** — image panel, category, title, description, price
  row — is correct and needs only tinting, not rebuilding.
- **The gold gradient text treatment** on headings is distinctive and should
  stay as the brand's signature device.
- **The information architecture** across all 16 pages is complete and logical.
- **Technical quality** — zero broken links, valid structured data, no layout
  shift, no horizontal overflow, 124–228 ms FCP.

The foundation is solid. What follows is a design pass, not a rebuild.
