#!/usr/bin/env python3
"""Phase 6: legal pages, 404 and generated SEO config files."""
import sys, os, datetime
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build import (SITE, PRODUCTS, I, render, write, page_hero, cta_band, wa,
                   org_schema, breadcrumb, ROOT)

UPDATED = "6 September 2026"


def legal(file, nav_title, eyebrow, h1, sub, title, desc, blocks, schema_type="WebPage"):
    body = page_hero(eyebrow, h1, sub, [("Home", "index.html"), (nav_title, None)])
    body += f"""
  <section class="section grain">
    <div class="container container--narrow">
      <p class="prose__updated">Last updated: {UPDATED}</p>
      <div class="prose">
"""
    for block in blocks:
        body += block + "\n"
    body += f"""      </div>

      <div class="notice notice--gold" style="margin-top:var(--sp-7)">
        {I['mail']}
        <p><strong>Questions about this policy?</strong> Write to us at
          <a href="mailto:{SITE['email']}">{SITE['email']}</a> or call
          <a href="tel:{SITE['phone_link']}">{SITE['phone_display']}</a>. We respond within one working day.</p>
      </div>
    </div>
  </section>
"""
    body += cta_band("Have a Question We Have Not <em>Answered</em>?",
                     "Our team is happy to walk you through any of our policies in plain language.",
                     ("About Us", "about.html"), ("Contact Us", "contact.html"))

    page = {
        "file": file,
        "title": title,
        "desc": desc,
        "og_title": h1.replace("<em>", "").replace("</em>", "").replace("<br>", " "),
        "schema": [org_schema(), breadcrumb([("Home", ""), (nav_title, file)]),
                   {"@context": "https://schema.org", "@type": schema_type,
                    "name": nav_title, "url": f"{SITE['url']}/{file}",
                    "description": desc, "dateModified": "2026-09-06",
                    "isPartOf": {"@id": SITE["url"] + "/#website"},
                    "publisher": {"@id": SITE["url"] + "/#organization"}}],
    }
    write(file, render(page, body))


def h(t):
    return f'        <h2 data-reveal="up">{t}</h2>'


def p(t):
    return f'        <p data-reveal="up">{t}</p>'


def ul(items):
    li = "\n".join(f"          <li>{i}</li>" for i in items)
    return f'        <ul data-reveal="up">\n{li}\n        </ul>'


# ======================================================= PRIVACY
def build_privacy():
    legal(
        "privacy-policy.html", "Privacy Policy", "Legal",
        'Privacy <em>Policy</em>',
        "How KIARIT PHARMACEUTICALS collects, uses and protects the limited personal information you share with us.",
        "Privacy Policy | KIARIT PHARMACEUTICALS",
        "Read how KIARIT PHARMACEUTICALS collects, uses, stores and protects your personal data. We do not sell your information and we collect only what an order requires.",
        [
            h("Our Commitment"),
            p(f"{SITE['name']} respects your privacy. This policy explains what information we collect when you contact us or place an order, why we collect it, how long we keep it and the choices available to you. We follow the Information Technology Act, 2000 and the Digital Personal Data Protection Act, 2023 as applicable in India."),
            p("This website does not host any order form, account system or payment gateway. Orders are placed by WhatsApp, phone or email, which means the information we hold about you is deliberately minimal."),

            h("Information We Collect"),
            p("We only collect information that you choose to send us. This typically includes:"),
            ul([
                "<strong>Contact details</strong> — your name, phone number and email address, shared when you message or call us.",
                "<strong>Delivery details</strong> — the shipping address and PIN code required to dispatch your order.",
                "<strong>Order details</strong> — the products, quantities and any preferences you specify.",
                "<strong>Payment confirmation</strong> — the UPI reference number or payment screenshot you send us. We never see or store your full card number, UPI PIN, OTP or CVV.",
                "<strong>Correspondence</strong> — the content of your WhatsApp, email or phone conversations with our team, kept for order support and dispute resolution.",
            ]),
            p("We do not run advertising trackers, behavioural profiling or third-party analytics scripts on this website. No cookies are set by us for marketing purposes."),

            h("How We Use Your Information"),
            ul([
                "To confirm, pack, dispatch and track your order.",
                "To answer product questions and provide usage guidance.",
                "To process replacements or resolve delivery issues.",
                "To maintain sales and tax records as required by Indian law.",
                "To send order-related updates only. We do not send promotional messages unless you explicitly ask us to.",
            ]),

            h("Sharing Your Information"),
            p("We do not sell, rent or trade your personal data. We share the minimum necessary information with:"),
            ul([
                "<strong>Courier partners</strong> — your name, address and phone number, so your parcel can be delivered.",
                "<strong>Our banking partner</strong> — only the transaction reference needed to reconcile a payment.",
                "<strong>Government authorities</strong> — where disclosure is required by law, a court order or a valid regulatory request.",
            ]),

            h("Data Retention"),
            p("Order and invoice records are retained for eight financial years to satisfy Indian tax and accounting requirements. General enquiry conversations that do not result in an order are deleted within twelve months. Payment screenshots are deleted once the transaction is reconciled."),

            h("How We Protect Your Data"),
            p("Access to customer information is restricted to the staff who process orders. Devices used by our team are password protected, our email and messaging accounts use two-factor authentication, and physical records are stored in a locked office. While no method of transmission over the internet is completely secure, we take reasonable steps to guard against unauthorised access, alteration and disclosure."),

            h("Your Rights"),
            p("You may at any time ask us to:"),
            ul([
                "Confirm what personal data we hold about you.",
                "Correct information that is inaccurate or out of date.",
                "Delete your data, where we are not legally required to retain it.",
                "Stop contacting you, other than for an order already in progress.",
            ]),
            p(f"Send any such request to <a href='mailto:{SITE['email']}'>{SITE['email']}</a> from the email address or phone number associated with your order. We respond within thirty days."),

            h("Children"),
            p("Our products and this website are intended for adults. We do not knowingly collect personal information from anyone under eighteen. If you believe a minor has shared data with us, contact us and we will delete it."),

            h("External Links"),
            p("This website links to WhatsApp, Google Maps, OpenStreetMap and our social media profiles. Once you follow those links, the privacy policy of that service applies. We are not responsible for the content or practices of external sites."),

            h("Changes to This Policy"),
            p("We may update this policy to reflect changes in our practices or the law. The revised version, with an updated date, will be published on this page. Material changes affecting existing orders will be communicated directly."),
        ],
        "PrivacyPolicy" if False else "WebPage",
    )


# ======================================================= TERMS
def build_terms():
    legal(
        "terms.html", "Terms & Conditions", "Legal",
        'Terms &amp; <em>Conditions</em>',
        "The terms that govern your use of this website and any order placed with KIARIT PHARMACEUTICALS.",
        "Terms & Conditions | KIARIT PHARMACEUTICALS",
        "The terms governing use of the KIARIT PHARMACEUTICALS website, order acceptance, pricing, payment, delivery, product use and limitation of liability.",
        [
            h("Agreement"),
            p(f"By browsing this website or placing an order with {SITE['name']} (\"KIARIT\", \"we\", \"us\"), you agree to these terms. Please read them before ordering. If you do not accept them, please do not use this website or our ordering channels."),

            h("About This Website"),
            p("This website is an informational catalogue. It contains no shopping cart, no user accounts and no online payment gateway. All orders are placed through WhatsApp, telephone or email and are confirmed manually by our team."),

            h("Orders and Acceptance"),
            ul([
                "A message or call from you is a request to purchase, not a completed sale.",
                "A contract is formed only when we confirm your order in writing and the payment is received.",
                "We may decline or cancel an order if stock is unavailable, if a pricing error has occurred, if the delivery address is outside our service area, or where we suspect misuse or fraud.",
                "Where we cancel a confirmed and paid order, the full amount is refunded to the original payment method.",
            ]),

            h("Pricing and Payment"),
            ul([
                "All prices are in Indian Rupees and inclusive of applicable taxes unless stated otherwise.",
                "Prices, offers and product availability may change without prior notice. The price confirmed to you at the time of order is the price that applies.",
                "Payment is accepted by UPI QR code or bank transfer only. We do not operate a card gateway and we never ask for your UPI PIN, OTP or card CVV.",
                "Orders are dispatched only after payment is credited and verified.",
                "Always verify that the payee name reads <strong>KIARIT PHARMACEUTICALS</strong> before confirming a transfer. We are not liable for funds sent to an account that is not ours.",
            ]),

            h("Delivery"),
            p("Estimated delivery timelines are indicative and depend on the courier network, your location and factors beyond our control such as weather, strikes or public holidays. Delivery details, charges and timelines are set out on our <a href='shipping-returns.html'>Shipping &amp; Returns</a> page, which forms part of these terms."),

            h("Product Use and Suitability"),
            ul([
                "Our cosmetic and personal-care products are for external use only, unless the label states otherwise.",
                "Nutraceutical products are dietary supplements and are not intended to diagnose, treat, cure or prevent any disease.",
                "Always read the label and directions before use, and perform a patch test before first applying a new topical product.",
                "Individual results vary. Descriptions on this website reflect typical outcomes and are not a guarantee of a specific result.",
                "If you are pregnant, breastfeeding, under medical treatment or have a known allergy, consult a qualified healthcare professional before use.",
            ]),

            h("Intellectual Property"),
            p("All content on this website — including the KIARIT name, logo, product names, text, layout, graphics and photography — is owned by or licensed to us and is protected by Indian and international intellectual property law. You may view and print pages for personal, non-commercial use. Reproduction, republication, resale or use of our branding without prior written permission is prohibited."),

            h("Acceptable Use"),
            p("You agree not to use this website to transmit malicious code, to attempt unauthorised access to our systems, to scrape content in bulk for commercial purposes, or in any way that interferes with the operation of the site or the enjoyment of other users."),

            h("Limitation of Liability"),
            p("To the maximum extent permitted by law, our total liability for any claim arising from an order is limited to the amount you paid for the product concerned. We are not liable for indirect or consequential losses. Nothing in these terms excludes liability that cannot be excluded under Indian consumer law, including liability for death or personal injury caused by our negligence."),

            h("Indemnity"),
            p("You agree to indemnify us against any claim arising from your breach of these terms or your misuse of our products contrary to the label instructions."),

            h("Governing Law"),
            p(f"These terms are governed by the laws of India. The courts at {SITE['city']} have exclusive jurisdiction over any dispute, subject to your rights under the Consumer Protection Act, 2019 to approach a consumer forum in your own district."),

            h("Changes to These Terms"),
            p("We may revise these terms from time to time. The version published on this page at the time you place an order is the version that applies to that order."),
        ],
    )


# ======================================================= SHIPPING
def build_shipping():
    legal(
        "shipping-returns.html", "Shipping & Returns", "Customer Care",
        'Shipping &amp; <em>Returns</em>',
        "Clear timelines, honest charges and a straightforward replacement process — everything you need to know before you order.",
        "Shipping & Returns Policy | KIARIT PHARMACEUTICALS",
        "KIARIT shipping charges, dispatch and delivery timelines across India, damaged-parcel replacement, the returns policy for sealed goods, and refund processing times.",
        [
            h("Shipping Charges"),
            ul([
                "<strong>Free shipping</strong> on all prepaid orders above ₹999.",
                "<strong>Flat ₹79</strong> shipping on orders below ₹999.",
                "Cash on delivery is available on selected PIN codes and carries an additional handling fee, confirmed at the time of order.",
            ]),

            h("Dispatch Timeline"),
            p("Orders confirmed and paid before 4:00 PM on a working day are usually dispatched the same day. All other orders are dispatched within 24 working hours. We do not dispatch on Sundays or public holidays."),
            p("You will receive the courier name and tracking number on WhatsApp as soon as your parcel leaves our facility."),

            h("Delivery Timeline"),
            ul([
                "<strong>Metro cities</strong> — typically 3 to 5 business days from dispatch.",
                "<strong>Other cities and towns</strong> — typically 5 to 7 business days from dispatch.",
                "<strong>Remote and hill regions</strong> — may take 7 to 10 business days.",
            ]),
            p("These are courier estimates, not guarantees. Festive periods, weather disruptions and regional restrictions can extend delivery times."),

            h("Order Tracking"),
            p(f"Send your order number on WhatsApp at <a href='{wa('Hello KIARIT, I would like to track my order.')}' target='_blank' rel='noopener noreferrer'>{SITE['phone_display']}</a> and we will share the live status. If tracking has not updated for more than 72 hours, tell us and we will raise a query with the courier on your behalf."),

            h("Damaged or Incorrect Parcels"),
            p("We pack every order in tamper-evident packaging, but transit accidents happen. If your parcel arrives damaged, leaking or containing the wrong item:"),
            ul([
                "Report it within <strong>48 hours</strong> of delivery.",
                "Send us a photograph of the outer packaging, the shipping label and the affected product. An unboxing video is ideal but not mandatory.",
                "Once verified, we ship a <strong>free replacement</strong> at our cost. You do not pay return shipping.",
                "Where a replacement is unavailable, we issue a full refund instead.",
            ]),

            h("Returns of Sealed Goods"),
            p("For hygiene and safety reasons, cosmetic, dermatological and nutraceutical products cannot be returned once the seal is broken. This is standard practice for personal-care goods in India and protects every customer."),
            p("Unopened products with an intact seal may be returned within <strong>7 days</strong> of delivery if you have changed your mind. The product must be in its original packaging and in resaleable condition. Return shipping in this case is borne by the customer, and the refund covers the product value less the original shipping cost."),

            h("Non-Returnable Items"),
            ul([
                "Any product whose seal, shrink wrap or safety cap has been opened.",
                "Products returned without their original packaging, outer carton or batch label.",
                "Items reported more than 7 days after delivery, except in the case of transit damage reported within 48 hours.",
                "Products damaged by misuse, incorrect storage or use beyond the printed expiry date.",
            ]),

            h("Refunds"),
            p("Approved refunds are processed to the original payment method within <strong>5 to 7 business days</strong> of the returned item reaching us, or of a damage claim being approved. Your bank may take a further 2 to 3 days to reflect the credit. We share the refund reference number with you as soon as it is issued."),

            h("Order Cancellation"),
            p("You may cancel a confirmed order free of charge at any time before it is dispatched — simply message us. Once the parcel has left our facility it cannot be cancelled, but you may refuse delivery, after which the standard refund process applies less the shipping cost actually incurred."),

            h("Undelivered Parcels"),
            p("If a courier is unable to deliver after three attempts, or if the address is incorrect or incomplete, the parcel returns to us. We will contact you to arrange redelivery, for which the shipping charge applies again, or to process a refund of the product value."),
        ],
    )


# ======================================================= DISCLAIMER
def build_disclaimer():
    legal(
        "disclaimer.html", "Disclaimer", "Legal",
        'Medical &amp; Product <em>Disclaimer</em>',
        "Important information about how the content on this website should — and should not — be used.",
        "Disclaimer | KIARIT PHARMACEUTICALS",
        "Important medical and product disclaimer for KIARIT PHARMACEUTICALS: our content is informational, not medical advice, and results vary between individuals.",
        [
            h("Not Medical Advice"),
            p(f"The content on this website is provided by {SITE['name']} for general information only. It is not medical advice, a diagnosis or a treatment plan, and it is not a substitute for consultation with a qualified physician, dermatologist, pharmacist or nutritionist."),
            p("Never disregard professional medical advice, or delay seeking it, because of something you have read here. If you have a persistent skin condition, an adverse reaction or any medical concern, consult a registered healthcare practitioner promptly."),

            h("Individual Results Vary"),
            p("Skin, hair and general wellness outcomes depend on genetics, age, climate, diet, medication, hormonal factors and consistency of use. Any timeframe, percentage or outcome mentioned on this website reflects typical experience or study observations for the ingredient concerned. It is an indication, not a promise, and your own results may differ."),

            h("Cosmetic Products"),
            ul([
                "Our topical products are cosmetics for external use only.",
                "Avoid contact with the eyes and mucous membranes. Rinse thoroughly with water if contact occurs.",
                "Perform a patch test on the inner forearm 24 hours before first use.",
                "Discontinue immediately if redness, burning, swelling or persistent irritation develops, and seek medical advice.",
                "Store as directed on the label, away from direct sunlight and excessive heat.",
                "Keep out of reach of children.",
            ]),

            h("Nutraceutical Products"),
            p("Our nutraceutical products are dietary supplements. They are not intended to diagnose, treat, cure or prevent any disease. Supplements are not a substitute for a varied, balanced diet and a healthy lifestyle. Do not exceed the recommended daily dose."),
            p("Consult your doctor before use if you are pregnant or breastfeeding, are under eighteen, have a diagnosed medical condition, are scheduled for surgery, or are taking prescription medication — particularly blood thinners, thyroid medication or immunosuppressants."),

            h("Allergens"),
            p("Full ingredient lists are printed on every pack and published on each product page. If you have a known allergy or sensitivity, read the complete list before use. If you are unsure whether a formulation is suitable for you, contact us before ordering and we will help you check."),

            h("Product Images"),
            p("Product photographs on this website are for illustration. Packaging, shade and texture may vary slightly between production batches, and screen colour rendering differs between devices. Where a formulation is updated, the pack you receive always carries the current, accurate ingredient list — which takes precedence over any information on this website."),

            h("Accuracy of Information"),
            p("We take care to keep this website accurate and current, but we do not warrant that every detail is complete or error free at all times. Prices, availability, specifications and policies may change without notice. Typographical errors are corrected as soon as they are identified."),

            h("External Links"),
            p("Links to third-party websites and services are provided for convenience. We do not control and are not responsible for their content, accuracy or privacy practices. A link does not constitute an endorsement."),

            h("Testimonials"),
            p("Customer reviews published on this website are genuine, unedited except for length and obvious typing errors, and shared with the customer's consent. They describe one individual's experience and should not be read as a typical or guaranteed outcome."),

            h("Regulatory Position"),
            p("Our products are manufactured in facilities holding the licences required for their category under Indian law. Statements on this website have not been evaluated by any drug regulatory authority except where explicitly stated on the product label."),
        ],
    )


# ======================================================= 404
def build_404():
    body = f"""
  <section class="e404 on-dark">
    <div class="e404__bg" aria-hidden="true"></div>
    <div class="container">
      <div class="e404__inner">
        <span class="e404__code" aria-hidden="true">404</span>
        <span class="eyebrow eyebrow--center">Page Not Found</span>
        <h1 class="e404__title">This Page Has <em>Moved On</em></h1>
        <p class="e404__sub">The link you followed may be broken, or the page may have been renamed. Let us get you back to something useful.</p>
        <div class="e404__actions">
          <a class="btn btn--gold btn--lg" href="index.html">{I['home']} Back to Home</a>
          <a class="btn btn--ghost btn--lg" href="products.html">{I['grid']} Browse Products</a>
        </div>

        <div class="e404__links">
          <span>Popular pages</span>
          <nav aria-label="Popular pages">
            <a href="about.html">About Us</a>
            <a href="products.html">All Products</a>
            <a href="order.html">Order &amp; Pay</a>
            <a href="contact.html">Contact</a>
            <a href="shipping-returns.html">Shipping &amp; Returns</a>
          </nav>
        </div>
      </div>
    </div>
  </section>

  <section class="section grain" aria-labelledby="pop-h">
    <div class="container">
      <div class="sec-head sec-head--center">
        <span class="eyebrow eyebrow--center" data-reveal="fade">While You Are Here</span>
        <h2 id="pop-h" data-reveal="up" data-delay="90">Our <em class="gold-text serif">Bestsellers</em></h2>
      </div>
      <div class="products__grid" data-stagger="90">
"""
    from build import product_card
    for prod in [PRODUCTS[0], PRODUCTS[3], PRODUCTS[1]]:
        body += product_card(prod)
    body += """      </div>
    </div>
  </section>
"""
    page = {
        "file": "404.html",
        "title": "Page Not Found (404) | KIARIT PHARMACEUTICALS",
        "desc": "The page you are looking for could not be found. Browse the KIARIT product range or return to the home page.",
        "og_title": "Page Not Found — KIARIT PHARMACEUTICALS",
        "robots": "noindex, follow",
        "schema": [org_schema()],
    }
    write("404.html", render(page, body))


# ======================================================= SITEMAP / ROBOTS
def build_sitemap():
    today = "2026-09-06"
    entries = [("", "1.0", "weekly"), ("products.html", "0.9", "weekly"),
               ("about.html", "0.8", "monthly"), ("order.html", "0.8", "monthly"),
               ("contact.html", "0.8", "monthly")]
    entries += [(f"{p['slug']}.html", "0.9", "weekly") for p in PRODUCTS]
    entries += [("shipping-returns.html", "0.5", "yearly"), ("privacy-policy.html", "0.3", "yearly"),
                ("terms.html", "0.3", "yearly"), ("disclaimer.html", "0.3", "yearly")]

    x = ['<?xml version="1.0" encoding="UTF-8"?>',
         '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"',
         '        xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">']
    for loc, prio, freq in entries:
        url = f"{SITE['url']}/{loc}" if loc else f"{SITE['url']}/"
        x.append("  <url>")
        x.append(f"    <loc>{url}</loc>")
        x.append(f"    <lastmod>{today}</lastmod>")
        x.append(f"    <changefreq>{freq}</changefreq>")
        x.append(f"    <priority>{prio}</priority>")
        prod = next((p for p in PRODUCTS if f"{p['slug']}.html" == loc), None)
        if prod:
            x.append("    <image:image>")
            x.append(f"      <image:loc>{SITE['url']}/assets/img/products/{prod['slug']}.jpg</image:loc>")
            x.append(f"      <image:title>{prod['name']}</image:title>")
            x.append("    </image:image>")
        x.append("  </url>")
    x.append("</urlset>")
    open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8").write("\n".join(x) + "\n")
    print("  wrote sitemap.xml (%d urls)" % len(entries))

    robots = f"""# robots.txt — {SITE['name']}
User-agent: *
Allow: /
Disallow: /tools/
Disallow: /404.html

# Courtesy crawl delay for aggressive bots
User-agent: AhrefsBot
Crawl-delay: 10

User-agent: SemrushBot
Crawl-delay: 10

Sitemap: {SITE['url']}/sitemap.xml
"""
    open(os.path.join(ROOT, "robots.txt"), "w", encoding="utf-8").write(robots)
    print("  wrote robots.txt")


def build_htaccess():
    txt = f"""# ==========================================================================
# {SITE['name']} — Apache configuration
# ==========================================================================

# ---- Custom error page ----
ErrorDocument 404 /404.html

# ---- Compression ----
<IfModule mod_deflate.c>
  AddOutputFilterByType DEFLATE text/html text/plain text/xml text/css
  AddOutputFilterByType DEFLATE application/javascript application/json
  AddOutputFilterByType DEFLATE image/svg+xml application/manifest+json
</IfModule>

# ---- Browser caching ----
<IfModule mod_expires.c>
  ExpiresActive On
  ExpiresByType text/html                 "access plus 1 hour"
  ExpiresByType text/css                  "access plus 1 year"
  ExpiresByType application/javascript    "access plus 1 year"
  ExpiresByType image/jpeg                "access plus 1 year"
  ExpiresByType image/png                 "access plus 1 year"
  ExpiresByType image/svg+xml             "access plus 1 year"
  ExpiresByType image/webp                "access plus 1 year"
  ExpiresByType font/woff2                "access plus 1 year"
  ExpiresByType video/mp4                 "access plus 1 year"
  ExpiresByType video/webm                "access plus 1 year"
</IfModule>

# ---- Security headers ----
<IfModule mod_headers.c>
  Header always set X-Content-Type-Options "nosniff"
  Header always set X-Frame-Options "SAMEORIGIN"
  Header always set Referrer-Policy "strict-origin-when-cross-origin"
  Header always set Permissions-Policy "geolocation=(), microphone=(), camera=(), payment=()"
  Header unset X-Powered-By
  <FilesMatch "\\.(woff2|css|js|jpg|png|svg|webp|mp4|webm)$">
    Header set Cache-Control "public, max-age=31536000, immutable"
  </FilesMatch>
</IfModule>

# ---- Correct MIME types ----
<IfModule mod_mime.c>
  AddType font/woff2 .woff2
  AddType application/manifest+json .webmanifest
  AddType image/webp .webp
  AddType video/webm .webm
</IfModule>

# ---- Canonical host and HTTPS ----
<IfModule mod_rewrite.c>
  RewriteEngine On

  # Force HTTPS
  RewriteCond %{{HTTPS}} !=on
  RewriteRule ^(.*)$ https://%{{HTTP_HOST}}/$1 [R=301,L]

  # Force www
  RewriteCond %{{HTTP_HOST}} !^www\\. [NC]
  RewriteRule ^(.*)$ https://www.%{{HTTP_HOST}}/$1 [R=301,L]

  # Allow extensionless URLs (/about -> /about.html)
  RewriteCond %{{REQUEST_FILENAME}} !-d
  RewriteCond %{{REQUEST_FILENAME}}\\.html -f
  RewriteRule ^(.*)$ $1.html [L]
</IfModule>

# ---- Block access to the build tooling ----
RedirectMatch 404 ^/tools/
Options -Indexes
"""
    open(os.path.join(ROOT, ".htaccess"), "w", encoding="utf-8").write(txt)
    print("  wrote .htaccess")


if __name__ == "__main__":
    print("Building Phase 6 pages...")
    build_privacy()
    build_terms()
    build_shipping()
    build_disclaimer()
    build_404()
    build_sitemap()
    build_htaccess()
    print("Done.")
