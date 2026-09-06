#!/usr/bin/env python3
"""Phase 5 pages: products listing + 6 product detail pages."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build import (SITE, PRODUCTS, PMAP, I, rupee, stars, render, write, page_hero,
                   cta_band, wa, org_schema, breadcrumb, faq_schema, product_card)

REVIEWS = {
    "product-1": [("Priya Kulkarni", "Pune, Maharashtra", 5, "The only thing that has faded my post-acne marks. Breakouts settled in about two weeks and the dark spots have genuinely lightened since."),
                  ("Ritu Agarwal", "Jaipur, Rajasthan", 5, "Gentle enough for my sensitive skin, which azelaic acid usually is not. No stinging, and it layers fine under sunscreen.")],
    "product-2": [("Rohit Menon", "Bengaluru, Karnataka", 5, "No white cast at all on my skin tone, and it does not turn greasy by afternoon. Finally a sunscreen I actually reapply."),
                  ("Neha Bhatt", "Ahmedabad, Gujarat", 5, "Matte finish that lasts, sits beautifully under makeup, and survives a humid commute. Repurchasing.")],
    "product-3": [("Kavya Nair", "Kochi, Kerala", 5, "Cleans off sunscreen properly without that tight squeaky feeling. My skin feels comfortable straight after washing."),
                  ("Arjun Malhotra", "Mumbai, Maharashtra", 4, "Great for oily skin in Mumbai weather. I use it twice a day and it has not dried me out once.")],
    "product-4": [("Shalini Gupta", "Lucknow, Uttar Pradesh", 5, "I wash my hair every day and this is the first shampoo that has not left it dry and frizzy. Scalp itchiness is gone too."),
                  ("Deepak Iyer", "Chennai, Tamil Nadu", 5, "Lathers really well for a sulphate-free formula, and rinses clean without weighing my hair down.")],
    "product-5": [("Meera Venkatesh", "Bengaluru, Karnataka", 5, "My eczema-prone skin does not flare with this. I have stopped using body lotion entirely since switching."),
                  ("Pooja Saxena", "Indore, Madhya Pradesh", 5, "Turns into a lovely milk in the shower. Skin feels soft rather than stripped, even with our hard water.")],
}
RATINGS = {"product-1": (4.8, 214), "product-2": (4.9, 246), "product-3": (4.7, 168),
           "product-4": (4.7, 132), "product-5": (4.8, 118)}


def review_card(name, place, rating, text):
    initials = "".join(w[0] for w in name.split()[:2]).upper()
    return f"""        <figure class="rcard" data-reveal="up">
          {stars(rating)}
          <blockquote>{text}</blockquote>
          <figcaption>
            <span class="rcard__avatar" aria-hidden="true">{initials}</span>
            <span><strong>{name}</strong><span>{place}</span></span>
            <span class="rcard__verified">{I['check']} Verified Buyer</span>
          </figcaption>
        </figure>
"""


# ============================================================== LISTING
def build_products():
    body = page_hero(
        "Our Collection",
        'Five Formulations,<br>One <em>Standard</em>',
        "A focused range covering dermatology, daily skincare, hair care and inner wellness — each developed under strict quality controls.",
        [("Home", "index.html"), ("Products", None)],
    )

    cats = []
    for p in PRODUCTS:
        if p["cat"] not in cats:
            cats.append(p["cat"])
    chips = '<button class="chip is-active" type="button" data-filter="all">All Products</button>\n'
    chips += "\n".join(f'        <button class="chip" type="button" data-filter="{c}">{c}</button>' for c in cats)

    body += f"""
  <section class="section grain" aria-labelledby="all-h">
    <div class="container">
      <div class="sec-head">
        <span class="eyebrow" data-reveal="fade">Browse</span>
        <h2 id="all-h" data-reveal="up" data-delay="90">The Complete <em class="gold-text serif">KIARIT Range</em></h2>
        <p data-reveal="up" data-delay="170">Every product below is manufactured in a GMP-certified facility and dispatched within 24 working hours.</p>
      </div>

      <div class="chips" role="group" aria-label="Filter products by category" data-reveal="up">
        {chips}
      </div>

      <div class="products__grid" id="grid" data-stagger="60">
"""
    for p in PRODUCTS:
        card = product_card(p)
        card = card.replace('<article class="pcard"', f'<article class="pcard" data-cat="{p["cat"]}"')
        body += card

    body += f"""      </div>
      <p class="chips__empty" hidden>No products found in this category.</p>
    </div>
  </section>

  <section class="section section--alt grain" aria-labelledby="help-h">
    <div class="container">
      <div class="sec-head">
        <span class="eyebrow" data-reveal="fade">Not Sure Where to Start</span>
        <h2 id="help-h" data-reveal="up" data-delay="90">Build Your <em class="gold-text serif">Routine</em></h2>
      </div>
      <div class="bigsteps" data-stagger="60">
        <article class="bigstep" data-reveal="up">
          <span class="bigstep__num">AM</span>
          <div class="why__icon">{I['drop']}</div>
          <h3>Morning Routine</h3>
          <p>Cleanse with Ritglow Face Wash, apply Ritclear AZ Serum, and always finish with Ritshade Sunscreen.</p>
          <a class="link-gold" href="product-2.html">Start with Ritshade {I['arrow']}</a>
        </article>
        <article class="bigstep" data-reveal="up">
          <span class="bigstep__num">PM</span>
          <div class="why__icon">{I['leaf']}</div>
          <h3>Evening Routine</h3>
          <p>Cleanse away the day with Ritglow, then let Ritclear AZ Serum work on breakouts and marks overnight.</p>
          <a class="link-gold" href="product-1.html">Explore Ritclear AZ {I['arrow']}</a>
        </article>
        <article class="bigstep" data-reveal="up">
          <span class="bigstep__num">+</span>
          <div class="why__icon">{I['heart']}</div>
          <h3>Hair &amp; Body</h3>
          <p>Kiamild Shampoo as often as you wash, and Kiarestora Shower Oil in place of soap for comfortable skin.</p>
          <a class="link-gold" href="product-5.html">Discover Kiarestora {I['arrow']}</a>
        </article>
      </div>
    </div>
  </section>
"""
    body += cta_band("Need Help Choosing the Right <em>Product</em>?",
                     "Message our team — we will recommend a routine based on your skin type and concern.",
                     ("Contact Us", "contact.html"), ("How to Order", "order.html"))

    item_list = {
        "@context": "https://schema.org", "@type": "ItemList",
        "name": "KIARIT PHARMACEUTICALS Product Collection",
        "numberOfItems": len(PRODUCTS),
        "itemListElement": [{
            "@type": "ListItem", "position": i + 1,
            "url": f"{SITE['url']}/{p['slug']}.html",
            "name": p["name"],
        } for i, p in enumerate(PRODUCTS)],
    }
    page = {
        "file": "products.html",
        "title": "All Products | KIARIT PHARMACEUTICALS — Skincare & Nutraceuticals",
        "desc": "Browse the KIARIT range — Ritclear AZ Serum, Ritshade Sunscreen, Ritglow Face Wash, Kiamild Shampoo and Kiarestora Shower Oil. GMP certified, 24-hour dispatch.",
        "og_title": "All Products — KIARIT PHARMACEUTICALS",
        "schema": [org_schema(), breadcrumb([("Home", ""), ("Products", "products.html")]), item_list],
        "head_extra": "",
    }
    html = render(page, body)
    html = html.replace("</body>", '<script src="assets/js/filter.js" defer></script>\n</body>')
    write("products.html", html)


# ============================================================== DETAIL
def build_product(p, idx):
    rating, rcount = RATINGS[p["slug"]]
    prev_p = PRODUCTS[(idx - 1) % len(PRODUCTS)]
    next_p = PRODUCTS[(idx + 1) % len(PRODUCTS)]
    save = p["mrp"] - p["price"]
    savepct = round(save / p["mrp"] * 100)

    body = f"""
  <section class="pdp">
    <div class="container">
      <nav class="crumbs crumbs--light" aria-label="Breadcrumb">
        <a href="index.html">Home</a><span aria-hidden="true">/</span>
        <a href="products.html">Products</a><span aria-hidden="true">/</span>
        <span aria-current="page">{p['name']}</span>
      </nav>

      <div class="pdp__grid">
        <div class="pdp__media" data-reveal="mask-x">
          <div class="pdp__imgwrap">
            <img src="assets/img/products/{p['slug']}.jpg" alt="{p['name']} — {p['cat'].lower()} product by KIARIT Pharmaceuticals, {p['size']}" width="900" height="900" fetchpriority="high">
          </div>
          <ul class="pdp__badges">
            <li>{I['shield']} GMP Certified</li>
            <li>{I['leaf']} Cruelty Free</li>
            <li>{I['truck']} 24h Dispatch</li>
          </ul>
        </div>

        <div class="pdp__info">
          <div class="pdp__cat">{p['cat']}</div>
          <h1 class="pdp__title" data-reveal="up">{p['name']}</h1>

          <div class="pdp__rating" data-reveal="up" data-delay="80">
            {stars(5)}
            <span><strong>{rating}</strong> · {rcount} verified reviews</span>
          </div>

          <p class="pdp__short lead" data-reveal="up" data-delay="140">{p['short']}</p>

          <div class="pdp__pricebox" data-reveal="up" data-delay="200">
            <div class="pdp__price">
              <strong>{rupee(p['price'])}</strong>
              <del>{rupee(p['mrp'])}</del>
              <span class="pdp__save">Save {savepct}%</span>
            </div>
            <div class="pdp__meta">
              <span>{p['size']}</span><span aria-hidden="true">·</span>
              <span>SKU {p['sku']}</span><span aria-hidden="true">·</span>
              <span class="pdp__stock">{I['check']} In Stock</span>
            </div>
            <p class="pdp__tax">Inclusive of all taxes. Free shipping on orders above ₹999.</p>
          </div>

          <div class="pdp__actions" data-reveal="up" data-delay="260">
            <a class="btn btn--wa btn--lg" href="{wa('Hello KIARIT, I want to order the ' + p['name'] + ' (' + p['size'] + ') at ' + rupee(p['price']) + '. Please confirm availability.')}" target="_blank" rel="noopener noreferrer">
              {I['wa']} Order on WhatsApp
            </a>
            <a class="btn btn--outline btn--lg" href="order.html">{I['qr']} Pay via QR</a>
          </div>

          <div class="pdp__assure" data-reveal="up" data-delay="320">
            <div>{I['phone']}<span>Call {SITE['phone_display']}<br>for order support</span></div>
            <div>{I['box']}<span>Secure, tamper-evident<br>packaging</span></div>
          </div>
        </div>
      </div>
    </div>
  </section>

  <section class="section grain" aria-labelledby="about-h">
    <div class="container">
      <div class="pdp__cols">
        <div>
          <span class="eyebrow" data-reveal="fade">About This Product</span>
          <h2 id="about-h" data-reveal="up" data-delay="90">Why It <em class="gold-text serif">Works</em></h2>
"""
    for i, para in enumerate(p["long"]):
        body += f'          <p data-reveal="up" data-delay="{160 + i*60}">{para}</p>\n'

    body += f"""
          <h3 class="pdp__subh" data-reveal="up">How to Use</h3>
          <ol class="pdp__steps" data-stagger="60">
"""
    for step in p["how"]:
        body += f'            <li data-reveal="up">{step}</li>\n'

    body += f"""          </ol>
        </div>

        <aside class="pdp__benefits">
          <h3 data-reveal="up">Key Benefits</h3>
          <div class="benefits" data-stagger="60">
"""
    for title, txt in p["benefits"]:
        body += f"""            <div class="benefit" data-reveal="up">
              <span class="benefit__tick">{I['check']}</span>
              <div><strong>{title}</strong><span>{txt}</span></div>
            </div>
"""
    body += f"""          </div>

          <div class="notice notice--gold" data-reveal="up">
            {I['shield']}
            <p><strong>Patch test advised.</strong> Discontinue use if irritation occurs. For external use only. Keep out of reach of children.</p>
          </div>
        </aside>
      </div>

      <!-- Reference data in a full-width strip below the two-column block,
           so neither column is padded out to match the other. -->
      <div class="pdpref">
        <div class="inci" data-reveal="up">
          <h3 class="inci__label">Full Ingredient List<span>INCI</span></h3>
          <p class="inci__list">{p['ingredients']}</p>
        </div>
        <div class="pdp__spec" data-reveal="up">
          <dl>
            <div><dt>Net Quantity</dt><dd>{p['size']}</dd></div>
            <div><dt>Category</dt><dd>{p['cat']}</dd></div>
            <div><dt>SKU</dt><dd>{p['sku']}</dd></div>
            <div><dt>Shelf Life</dt><dd>24 months from manufacture</dd></div>
            <div><dt>Manufactured In</dt><dd>India (GMP facility)</dd></div>
          </dl>
        </div>
      </div>
    </div>
  </section>

  <section class="section section--alt grain" aria-labelledby="rev-h">
    <div class="container">
      <div class="revhead">
        <div>
          <span class="eyebrow" data-reveal="fade">Customer Reviews</span>
          <h2 id="rev-h" data-reveal="up" data-delay="90">What Buyers <em class="gold-text serif">Say</em></h2>
        </div>
        <div class="revhead__score" data-reveal="up" data-delay="170">
          <strong>{rating}</strong>
          <div>{stars(round(rating))}<span>{rcount} verified purchases</span></div>
        </div>
      </div>
      <div class="rgrid" data-stagger="60">
"""
    for name, place, r, txt in REVIEWS[p["slug"]]:
        body += review_card(name, place, r, txt)

    body += f"""      </div>
    </div>
  </section>

  <section class="section grain" aria-labelledby="faq-h">
    <div class="container">
      <div class="faqsplit">
        <div class="faqsplit__aside">
          <span class="eyebrow" data-reveal="fade">Questions</span>
          <h2 id="faq-h" data-reveal="up" data-delay="90">Common <em class="gold-text serif">Questions</em></h2>
          <p data-reveal="up" data-delay="160">Still unsure? Message us on WhatsApp and a real person will answer before you order.</p>
          <a class="btn btn--outline" href="{wa('Hello KIARIT, I have a question about ' + p['name'] + '.')}" target="_blank" rel="noopener noreferrer" data-reveal="up" data-delay="220">Ask about this product</a>
        </div>
        <div class="faq" data-stagger="60">
"""
    for i, (q, a) in enumerate(p["faq"]):
        body += f"""        <details class="faq__item" data-reveal="up"{' open' if i == 0 else ''}>
          <summary class="faq__q"><span>{q}</span><i class="faq__icon" aria-hidden="true"></i></summary>
          <div class="faq__a"><p>{a}</p></div>
        </details>
"""
    body += f"""        </div>
      </div>
    </div>
  </section>

  <section class="section section--alt grain" aria-labelledby="rel-h">
    <div class="container">
      <div class="sec-head">
        <span class="eyebrow" data-reveal="fade">You May Also Like</span>
        <h2 id="rel-h" data-reveal="up" data-delay="90">Related <em class="gold-text serif">Products</em></h2>
      </div>
      <div class="products__grid" data-stagger="60">
"""
    related = [q for q in PRODUCTS if q["slug"] != p["slug"]][:3]
    for q in related:
        body += product_card(q)

    body += f"""      </div>

      <nav class="pdp__nav" aria-label="Product navigation">
        <a class="pdp__nav-link pdp__nav-link--prev" href="{prev_p['slug']}.html">
          <span>Previous</span><strong>{prev_p['name']}</strong>
        </a>
        <a class="btn btn--outline" href="products.html">All Products</a>
        <a class="pdp__nav-link pdp__nav-link--next" href="{next_p['slug']}.html">
          <span>Next</span><strong>{next_p['name']}</strong>
        </a>
      </nav>
    </div>
  </section>
"""
    body += cta_band(f"Ready to Try <em>{p['name'].replace('Kiarit ', '')}</em>?",
                     "Message us on WhatsApp and our team will confirm your order within minutes.",
                     ("How to Order", "order.html"), ("Contact Us", "contact.html"))

    product_schema = {
        "@context": "https://schema.org", "@type": "Product",
        "@id": f"{SITE['url']}/{p['slug']}.html#product",
        "name": p["name"], "sku": p["sku"], "category": p["cat"],
        "description": p["short"],
        "image": [f"{SITE['url']}/assets/img/products/{p['slug']}.jpg"],
        "brand": {"@type": "Brand", "name": SITE["short"]},
        "manufacturer": {"@id": SITE["url"] + "/#organization"},
        "size": p["size"],
        "offers": {
            "@type": "Offer",
            "url": f"{SITE['url']}/{p['slug']}.html",
            "priceCurrency": "INR", "price": str(p["price"]),
            "priceValidUntil": "2027-12-31",
            "availability": "https://schema.org/InStock",
            "itemCondition": "https://schema.org/NewCondition",
            "seller": {"@id": SITE["url"] + "/#organization"},
            "shippingDetails": {
                "@type": "OfferShippingDetails",
                "shippingRate": {"@type": "MonetaryAmount", "value": "0", "currency": "INR"},
                "shippingDestination": {"@type": "DefinedRegion", "addressCountry": "IN"},
                "deliveryTime": {"@type": "ShippingDeliveryTime",
                                 "handlingTime": {"@type": "QuantitativeValue", "minValue": 0, "maxValue": 1, "unitCode": "DAY"},
                                 "transitTime": {"@type": "QuantitativeValue", "minValue": 3, "maxValue": 7, "unitCode": "DAY"}}},
        },
        "aggregateRating": {"@type": "AggregateRating", "ratingValue": str(rating),
                            "reviewCount": str(rcount), "bestRating": "5", "worstRating": "1"},
        "review": [{
            "@type": "Review",
            "author": {"@type": "Person", "name": n},
            "reviewRating": {"@type": "Rating", "ratingValue": str(r), "bestRating": "5"},
            "reviewBody": t,
        } for n, pl, r, t in REVIEWS[p["slug"]]],
    }

    page = {
        "file": f"{p['slug']}.html",
        "title": f"{p['name']} — {p['size']} | {rupee(p['price'])} | KIARIT",
        "desc": p["meta"],
        "og_title": f"{p['name']} — {rupee(p['price'])} | KIARIT PHARMACEUTICALS",
        "og_type": "product",
        "og": f"assets/img/products/{p['slug']}.jpg",
        "schema": [org_schema(),
                   breadcrumb([("Home", ""), ("Products", "products.html"), (p["name"], f"{p['slug']}.html")]),
                   product_schema,
                   faq_schema(p["faq"])],
    }
    write(f"{p['slug']}.html", render(page, body))


if __name__ == "__main__":
    print("Building Phase 5 pages...")
    build_products()
    for i, p in enumerate(PRODUCTS):
        build_product(p, i)
    print("Done.")
