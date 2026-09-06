#!/usr/bin/env python3
"""Phase 4 pages: About, Contact, Order & Pay."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build import (SITE, PRODUCTS, I, rupee, stars, head, render, write, page_hero,
                   cta_band, wa, org_schema, breadcrumb, faq_schema, product_card)


# ============================================================== ABOUT
def build_about():
    body = page_hero(
        "Our Story",
        'Built on Science,<br>Guided by <em>Responsibility</em>',
        "A healthcare-focused pharmaceutical and cosmetic company delivering products we would trust for our own families.",
        [("Home", "index.html"), ("About Us", None)],
    )

    body += f"""
  <section class="section grain" aria-labelledby="ov-h">
    <div class="container">
      <div class="overview__grid">
        <div class="overview__visual" data-reveal="mask-x">
          <div class="overview__frame" aria-hidden="true"></div>
          <div class="overview__img">
            <img src="assets/img/posters/poster-2.jpg" alt="Macro photograph of a golden serum droplet representing KIARIT's scientific formulations" width="800" height="960" loading="lazy">
          </div>
          <div class="overview__badge" data-reveal="up" data-delay="420">
            {I['award']}
            <div><strong>ISO &amp; GMP</strong><span>Quality Standards</span></div>
          </div>
        </div>
        <div class="overview__body">
          <span class="eyebrow" data-reveal="fade">Company Overview</span>
          <h2 id="ov-h" data-reveal="up" data-delay="90">Who We <em class="gold-text serif">Are</em></h2>
          <p class="lead" data-reveal="up" data-delay="170">{SITE['overview'][:150]}</p>
          <p data-reveal="up" data-delay="230">{SITE['overview'][150:]}</p>
          <div class="pillars" data-stagger="100">
            <div class="pillar" data-reveal="up">{I['flask']}<div><strong>Dermatology</strong><span>Clinically guided skin therapy</span></div></div>
            <div class="pillar" data-reveal="up">{I['drop']}<div><strong>Skincare</strong><span>Everyday luxury rituals</span></div></div>
            <div class="pillar" data-reveal="up">{I['leaf']}<div><strong>Nutraceuticals</strong><span>Wellness from within</span></div></div>
            <div class="pillar" data-reveal="up">{I['box']}<div><strong>Formulations</strong><span>Research-led development</span></div></div>
          </div>
        </div>
      </div>
    </div>
  </section>

  <section class="section section--alt grain" aria-labelledby="mv-h">
    <div class="container">
      <div class="sec-head sec-head--center">
        <span class="eyebrow eyebrow--center" data-reveal="fade">Purpose</span>
        <h2 id="mv-h" data-reveal="up" data-delay="90">Mission &amp; <em class="gold-text serif">Vision</em></h2>
      </div>
      <div class="mv__grid" data-stagger="120">
        <article class="mv__card" data-reveal="up">
          <div class="why__icon">{I['target']}</div>
          <h3>Our Mission</h3>
          <p>To provide safe, effective and scientifically developed products while maintaining the highest standards of quality, integrity and customer satisfaction — making genuine healthcare accessible and affordable.</p>
        </article>
        <article class="mv__card" data-reveal="up">
          <div class="why__icon">{I['eyeglass']}</div>
          <h3>Our Vision</h3>
          <p>Through continuous innovation and a patient-centric approach, to become a trusted name in healthcare and personal care solutions across India and beyond.</p>
        </article>
      </div>
    </div>
  </section>

  <section class="section grain" aria-labelledby="val-h">
    <div class="container">
      <div class="sec-head sec-head--center">
        <span class="eyebrow eyebrow--center" data-reveal="fade">What Guides Us</span>
        <h2 id="val-h" data-reveal="up" data-delay="90">Our Core <em class="gold-text serif">Values</em></h2>
      </div>
      <div class="why__grid" data-stagger="100">
        <article class="why__card" data-reveal="up"><span class="why__num" aria-hidden="true">01</span>
          <div class="why__icon">{I['shield']}</div><h3>Quality First</h3>
          <p>Every batch is manufactured in a GMP-certified facility and tested against strict internal specifications before release.</p></article>
        <article class="why__card" data-reveal="up"><span class="why__num" aria-hidden="true">02</span>
          <div class="why__icon">{I['bulb']}</div><h3>Innovation</h3>
          <p>Our R&amp;D team continuously evaluates emerging actives and delivery systems to keep the range genuinely effective.</p></article>
        <article class="why__card" data-reveal="up"><span class="why__num" aria-hidden="true">03</span>
          <div class="why__icon">{I['lock']}</div><h3>Integrity</h3>
          <p>Honest labelling, honest claims and honest pricing. We would rather under-promise than mislead.</p></article>
        <article class="why__card" data-reveal="up"><span class="why__num" aria-hidden="true">04</span>
          <div class="why__icon">{I['heart']}</div><h3>Patient-Centric</h3>
          <p>Clear guidance and responsive support, because our responsibility does not end at the point of purchase.</p></article>
      </div>
    </div>
  </section>

  <section class="poster" data-reveal="fade" aria-labelledby="qual-h">
    <div class="poster__bg" data-parallax="0.16">
      <img src="assets/img/posters/poster-1.jpg" alt="" width="1920" height="1080" loading="lazy">
    </div>
    <div class="poster__shimmer" aria-hidden="true"></div>
    <div class="poster__frame" aria-hidden="true"></div>
    <span class="poster__tag" aria-hidden="true">Quality &amp; Compliance</span>
    <div class="container poster__inner">
      <div class="poster__content">
        <span class="eyebrow eyebrow--light" data-reveal="fade">Our Standards</span>
        <h2 id="qual-h" class="poster__title" data-reveal="up" data-delay="120">Quality Is Not a<br>Step — It Is the <em>Process</em></h2>
        <p data-reveal="up" data-delay="230">From raw-material sourcing to the final seal, every stage is documented, tested and signed off. We manufacture under GMP conditions and retain samples from every batch we release.</p>
        <div class="poster__stats" data-stagger="120">
          <div class="poster__stat" data-reveal="up"><strong><span data-count="100">100</span>%</strong><span>Batch Tested</span></div>
          <div class="poster__stat" data-reveal="up"><strong><span data-count="12">12</span></strong><span>QC Checkpoints</span></div>
          <div class="poster__stat" data-reveal="up"><strong>GMP</strong><span>Certified Facility</span></div>
        </div>
      </div>
    </div>
  </section>

  <section class="section grain" aria-labelledby="jour-h">
    <div class="container container--narrow">
      <div class="sec-head sec-head--center">
        <span class="eyebrow eyebrow--center" data-reveal="fade">Our Journey</span>
        <h2 id="jour-h" data-reveal="up" data-delay="90">Milestones That <em class="gold-text serif">Shaped Us</em></h2>
      </div>
      <ol class="timeline" data-stagger="110">
        <li class="timeline__item" data-reveal="up"><span class="timeline__year">2019</span>
          <div><strong>The Beginning</strong><p>KIARIT PHARMACEUTICALS is founded with a focus on dermatology and honest, accessible healthcare products.</p></div></li>
        <li class="timeline__item" data-reveal="up"><span class="timeline__year">2021</span>
          <div><strong>GMP Certification</strong><p>Our manufacturing partner facility achieves GMP certification, formalising our quality systems end to end.</p></div></li>
        <li class="timeline__item" data-reveal="up"><span class="timeline__year">2023</span>
          <div><strong>Skincare Expansion</strong><p>The daily skincare range launches, extending our dermatology expertise into everyday routines.</p></div></li>
        <li class="timeline__item" data-reveal="up"><span class="timeline__year">2025</span>
          <div><strong>Nutraceuticals</strong><p>Kiarit Nutra Boost introduces inner wellness to the portfolio, completing our care philosophy.</p></div></li>
        <li class="timeline__item" data-reveal="up"><span class="timeline__year">2026</span>
          <div><strong>Nationwide Reach</strong><p>Serving customers across India with a focused six-product signature collection.</p></div></li>
      </ol>
    </div>
  </section>

  <section class="section ceo grain" aria-labelledby="ceo-h">
    <div class="ceo__deco" aria-hidden="true"></div>
    <div class="container">
      <div class="ceo__grid">
        <div class="ceo__portrait" data-reveal="zoom">
          <div class="ceo__arch" aria-hidden="true"></div>
          <div class="ceo__portrait-inner">
            <img src="assets/img/ceo.jpg" alt="{SITE['ceo']}, Founder and Chief Executive Officer of {SITE['name']}" width="800" height="940" loading="lazy">
          </div>
          <div class="ceo__sig-card"><strong>{SITE['ceo']}</strong><span>Founder &amp; CEO</span></div>
        </div>
        <div class="ceo__body">
          <span class="ceo__quote-mark" aria-hidden="true">&ldquo;</span>
          <span class="eyebrow" data-reveal="fade">Message from the CEO</span>
          <h2 id="ceo-h" data-reveal="up" data-delay="90">A Commitment to <em class="gold-text serif">Every Person We Serve</em></h2>
          <blockquote data-reveal="up" data-delay="170">At KIARIT PHARMACEUTICALS, we believe good health and genuine confidence should never be a luxury — they should be accessible to everyone.</blockquote>
          <p data-reveal="up" data-delay="240">When we founded this company, our intention was simple: to build products we would trust for our own families. That single principle continues to guide every formulation we develop, every ingredient we approve and every batch we release.</p>
          <p data-reveal="up" data-delay="300">Our team of researchers, dermatologists and quality specialists work with a shared sense of responsibility. We do not chase trends — we invest in science, transparency and consistency. Whether it is a dermatology solution, a daily skincare essential or a nutraceutical supplement, our promise remains unchanged: safe, effective and honestly priced.</p>
          <p data-reveal="up" data-delay="360">Thank you for placing your trust in us. Your confidence inspires us to keep raising our standards, every single day.</p>
          <div class="ceo__signature" data-reveal="up" data-delay="430">
            <span class="sig-name">{SITE['ceo']}</span>
            <span class="sig-role">Founder &amp; Chief Executive Officer</span>
          </div>
        </div>
      </div>
    </div>
  </section>
"""
    body += cta_band("Explore the <em>KIARIT</em> Collection",
                     "Six focused formulations across dermatology, skincare and inner wellness.",
                     ("View Products", "products.html"), ("Contact Us", "contact.html"))

    page = {
        "file": "about.html",
        "title": "About Us | KIARIT PHARMACEUTICALS — Our Story, Mission & Quality",
        "desc": "Learn about KIARIT PHARMACEUTICALS — a healthcare-focused pharmaceutical and cosmetic company delivering high-quality, innovative and affordable dermatology, skincare and nutraceutical products.",
        "og_title": "About KIARIT PHARMACEUTICALS — Science, Quality, Responsibility",
        "schema": [org_schema(),
                   breadcrumb([("Home", ""), ("About Us", "about.html")]),
                   {"@context": "https://schema.org", "@type": "AboutPage",
                    "name": "About KIARIT PHARMACEUTICALS",
                    "url": SITE["url"] + "/about.html",
                    "description": SITE["overview"],
                    "mainEntity": {"@id": SITE["url"] + "/#organization"}},
                   {"@context": "https://schema.org", "@type": "Person",
                    "name": SITE["ceo"], "jobTitle": "Founder & Chief Executive Officer",
                    "worksFor": {"@id": SITE["url"] + "/#organization"},
                    "image": SITE["url"] + "/assets/img/ceo.jpg"}],
    }
    write("about.html", render(page, body))


# ============================================================== CONTACT
def build_contact():
    body = page_hero(
        "Get in Touch",
        'We Would Love to<br><em>Hear From You</em>',
        "Questions about a product, an order or bulk enquiries — reach us directly by phone, email or WhatsApp.",
        [("Home", "index.html"), ("Contact", None)],
    )

    body += f"""
  <section class="section grain" aria-labelledby="ways-h">
    <div class="container">
      <div class="sec-head sec-head--center">
        <span class="eyebrow eyebrow--center" data-reveal="fade">Contact Channels</span>
        <h2 id="ways-h" data-reveal="up" data-delay="90">Reach Us <em class="gold-text serif">Directly</em></h2>
        <p data-reveal="up" data-delay="170">No forms, no waiting queues. Every channel below reaches our team directly during business hours.</p>
      </div>

      <div class="contact__grid" data-stagger="100">
        <a class="contact__card" href="tel:{SITE['phone_link']}" data-reveal="up">
          <div class="why__icon">{I['phone']}</div>
          <h3>Call Us</h3>
          <p>Speak to our customer care team for product guidance or order support.</p>
          <span class="contact__value">{SITE['phone_display']}</span>
          <span class="link-gold">Call Now {I['arrow']}</span>
        </a>

        <a class="contact__card contact__card--wa" href="{wa('Hello KIARIT, I have a question.')}" target="_blank" rel="noopener noreferrer" data-reveal="up">
          <div class="why__icon">{I['wa']}</div>
          <h3>WhatsApp</h3>
          <p>The fastest way to place an order, share a payment screenshot or track a shipment.</p>
          <span class="contact__value">{SITE['phone_display']}</span>
          <span class="link-gold">Start Chat {I['arrow']}</span>
        </a>

        <a class="contact__card" href="mailto:{SITE['email']}" data-reveal="up">
          <div class="why__icon">{I['mail']}</div>
          <h3>Email Us</h3>
          <p>For detailed enquiries, distribution partnerships or documentation requests.</p>
          <span class="contact__value">{SITE['email']}</span>
          <span class="link-gold">Send Email {I['arrow']}</span>
        </a>
      </div>
    </div>
  </section>

  <section class="section section--alt grain" aria-labelledby="visit-h">
    <div class="container">
      <div class="contact__split">
        <div>
          <span class="eyebrow" data-reveal="fade">Our Office</span>
          <h2 id="visit-h" data-reveal="up" data-delay="90">Visit Our <em class="gold-text serif">Corporate Office</em></h2>
          <p data-reveal="up" data-delay="170">Our corporate office handles customer support, distribution and partnership enquiries. Visits are by prior appointment.</p>

          <div class="infolist" data-stagger="100">
            <div class="infolist__row" data-reveal="up">
              {I['pin']}
              <div><strong>Registered Address</strong>
                <span>{SITE['addr_line1']}<br>{SITE['addr_line2']}</span></div>
            </div>
            <div class="infolist__row" data-reveal="up">
              {I['clock']}
              <div><strong>Business Hours</strong>
                <span>{SITE['hours_week']}<br>{SITE['hours_sun']}</span></div>
            </div>
            <div class="infolist__row" data-reveal="up">
              {I['truck']}
              <div><strong>Dispatch &amp; Delivery</strong>
                <span>Orders dispatched within 24 working hours<br>Typical delivery: 3–7 business days across India</span></div>
            </div>
            <div class="infolist__row" data-reveal="up">
              {I['users']}
              <div><strong>Bulk &amp; Distribution</strong>
                <span>Retail, clinic and distribution enquiries welcome<br>Write to {SITE['email']}</span></div>
            </div>
          </div>

          <div class="contact__actions" data-reveal="up" data-delay="440">
            <a class="btn btn--wa" href="{wa('Hello KIARIT, I would like to place an order.')}" target="_blank" rel="noopener noreferrer">{I['wa']} Order on WhatsApp</a>
            <a class="btn btn--outline" href="order.html">How to Order &amp; Pay</a>
          </div>
        </div>

        <div class="contact__mapwrap" data-reveal="mask">
          <div class="contact__mapfallback" aria-hidden="true">
            <span class="contact__mapfallback-pin">{I['pin']}</span>
            <strong>{SITE['city']}, {SITE['region']}</strong>
            <span>{SITE['addr_line1']}<br>{SITE['addr_line2']}</span>
            <a class="btn btn--sm btn--outline" href="https://www.google.com/maps/search/?api=1&amp;query={SITE['street'].replace(' ', '+')}+{SITE['city']}" target="_blank" rel="noopener noreferrer">Open in Google Maps</a>
          </div>
          <iframe
            title="Map showing the location of KIARIT PHARMACEUTICALS corporate office in New Delhi"
            src="https://www.openstreetmap.org/export/embed.html?bbox=77.2450%2C28.5200%2C77.3150%2C28.5700&amp;layer=mapnik&amp;marker=28.5450%2C77.2800"
            width="600" height="520" loading="lazy" referrerpolicy="no-referrer-when-downgrade"
            style="border:0"></iframe>
          <div class="contact__mapcard">
            {I['pin']}
            <div><strong>{SITE['name']}</strong><span>{SITE['addr_line1']}, {SITE['addr_line2']}</span></div>
          </div>
        </div>
      </div>
    </div>
  </section>

  <section class="section section--tight orderband grain" aria-labelledby="qr-h">
    <div class="container">
      <div class="orderband__grid">
        <div class="qr-card" data-reveal="zoom">
          <img src="assets/img/qr/payment-qr.png" alt="Scan this UPI QR code to pay {SITE['name']}" width="652" height="726" loading="lazy">
          <div class="qr-card__note">Scan &amp; Pay via UPI</div>
        </div>
        <div>
          <span class="eyebrow" data-reveal="fade">Ready to Order</span>
          <h2 id="qr-h" data-reveal="up" data-delay="90">Ordering Is <em class="gold-text serif">Simple</em></h2>
          <p data-reveal="up" data-delay="160">Message us on WhatsApp with your product and address, scan the QR to pay, and share the screenshot. That is the whole process.</p>
          <div class="steps" data-stagger="110">
            <div class="step" data-reveal="up"><span class="step__num">1</span><div><strong>Message Us</strong><span>Share the product name, quantity and delivery address.</span></div></div>
            <div class="step" data-reveal="up"><span class="step__num">2</span><div><strong>Scan &amp; Pay</strong><span>We confirm the total including shipping, then you pay via any UPI app.</span></div></div>
            <div class="step" data-reveal="up"><span class="step__num">3</span><div><strong>Send Screenshot</strong><span>We dispatch within 24 working hours and share tracking.</span></div></div>
          </div>
          <div class="contact__actions" data-reveal="up" data-delay="440">
            <a class="btn btn--gold" href="order.html" data-magnetic>Full Payment Details {I['arrow']}</a>
          </div>
        </div>
      </div>
    </div>
  </section>
"""
    body += cta_band("Have a Question About <em>KIARIT</em>?",
                     "Learn more about our science and standards, or browse the full product range.",
                     ("About Us", "about.html"), ("View Products", "products.html"))

    page = {
        "file": "contact.html",
        "title": "Contact Us | KIARIT PHARMACEUTICALS — Phone, WhatsApp & Email",
        "desc": f"Contact KIARIT PHARMACEUTICALS by phone {SITE['phone_display']}, WhatsApp or email {SITE['email']}. Corporate office in New Delhi. Order support, bulk and distribution enquiries welcome.",
        "og_title": "Contact KIARIT PHARMACEUTICALS",
        "schema": [org_schema(),
                   breadcrumb([("Home", ""), ("Contact", "contact.html")]),
                   {"@context": "https://schema.org", "@type": "LocalBusiness",
                    "@id": SITE["url"] + "/#localbusiness",
                    "name": SITE["name"], "url": SITE["url"] + "/contact.html",
                    "image": SITE["url"] + "/assets/img/og/og-default.jpg",
                    "telephone": "+" + SITE["wa"], "email": SITE["email"],
                    "priceRange": "₹₹",
                    "address": {"@type": "PostalAddress", "streetAddress": SITE["street"],
                                "addressLocality": SITE["city"], "addressRegion": SITE["region"],
                                "postalCode": SITE["zip"], "addressCountry": "IN"},
                    "geo": {"@type": "GeoCoordinates", "latitude": 28.5450, "longitude": 77.2800},
                    "openingHoursSpecification": [{
                        "@type": "OpeningHoursSpecification",
                        "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"],
                        "opens": "09:30", "closes": "18:30"}],
                    "sameAs": list(SITE["social"].values())},
                   {"@context": "https://schema.org", "@type": "ContactPage",
                    "name": "Contact KIARIT PHARMACEUTICALS",
                    "url": SITE["url"] + "/contact.html"}],
    }
    write("contact.html", render(page, body))


# ============================================================== ORDER & PAY
ORDER_FAQ = [
    ("How do I place an order with KIARIT?",
     "Send us a WhatsApp message with the product name, quantity and your full delivery address including PIN code. Our team confirms availability and the final total including shipping, then shares payment details."),
    ("What payment methods do you accept?",
     "We accept UPI payments through any UPI app by scanning our QR code, and direct bank transfer via NEFT, IMPS or RTGS. We do not process card payments on the website."),
    ("Is there a minimum order value?",
     "There is no minimum order value. Shipping is complimentary on orders above ₹999; below that a flat shipping charge of ₹79 applies."),
    ("How long does delivery take?",
     "Orders are dispatched within 24 working hours of payment confirmation. Typical delivery is 3–5 business days for metro cities and 5–7 business days for other locations across India."),
    ("How do I know my payment was received?",
     "Share your payment screenshot on WhatsApp. Our team verifies it and sends you a written order confirmation along with tracking details once dispatched."),
    ("Do you offer cash on delivery?",
     "Cash on delivery is available on selected PIN codes. Please confirm availability with our team on WhatsApp before placing your order."),
    ("Can I order in bulk or for my clinic?",
     f"Yes. For bulk, retail or clinic orders, please write to {SITE['email']} or message us on WhatsApp and our team will share institutional pricing."),
]


def build_order():
    body = page_hero(
        "Order &amp; Payment",
        'Simple Ordering,<br><em>Secure Payment</em>',
        "No checkout forms and no card details. Message us, scan the QR code and your order is on its way.",
        [("Home", "index.html"), ("How to Order & Pay", None)],
    )

    body += f"""
  <section class="section grain" aria-labelledby="steps-h">
    <div class="container">
      <div class="sec-head sec-head--center">
        <span class="eyebrow eyebrow--center" data-reveal="fade">The Process</span>
        <h2 id="steps-h" data-reveal="up" data-delay="90">Order in Three <em class="gold-text serif">Easy Steps</em></h2>
        <p data-reveal="up" data-delay="170">Our ordering process is intentionally personal — a real person confirms every order before it ships.</p>
      </div>

      <div class="bigsteps" data-stagger="140">
        <article class="bigstep" data-reveal="up">
          <span class="bigstep__num">01</span>
          <div class="why__icon">{I['chat']}</div>
          <h3>Message Us on WhatsApp</h3>
          <p>Send the product name, quantity and your full delivery address with PIN code. Our team replies with availability and the final total including shipping.</p>
          <a class="link-gold" href="{wa('Hello KIARIT, I would like to place an order.')}" target="_blank" rel="noopener noreferrer">Start Your Order {I['arrow']}</a>
        </article>

        <article class="bigstep" data-reveal="up">
          <span class="bigstep__num">02</span>
          <div class="why__icon">{I['qr']}</div>
          <h3>Scan the QR &amp; Pay</h3>
          <p>Open any UPI app, scan the QR code below and pay the confirmed amount. You may also transfer directly to our bank account using the details provided.</p>
          <a class="link-gold" href="#payment">View Payment Details {I['arrow']}</a>
        </article>

        <article class="bigstep" data-reveal="up">
          <span class="bigstep__num">03</span>
          <div class="why__icon">{I['truck']}</div>
          <h3>Share Screenshot &amp; Relax</h3>
          <p>Send us your payment screenshot on WhatsApp. We confirm your order in writing and dispatch within 24 working hours with tracking details.</p>
          <a class="link-gold" href="shipping-returns.html">Shipping Policy {I['arrow']}</a>
        </article>
      </div>
    </div>
  </section>

  <section class="section section--alt grain" id="payment" aria-labelledby="pay-h">
    <div class="container">
      <div class="pay__grid">
        <div class="pay__qrcol" data-reveal="zoom">
          <div class="qr-card qr-card--lg">
            <img src="assets/img/qr/payment-qr.png" alt="Scan this UPI QR code to pay {SITE['name']}" width="652" height="726">
            <div class="qr-card__note">Scan with any UPI app</div>
          </div>
          <div class="pay__apps" aria-label="Supported UPI applications">
            <span>Google&nbsp;Pay</span><span>PhonePe</span><span>Paytm</span><span>BHIM</span><span>Any UPI App</span>
          </div>
        </div>

        <div>
          <span class="eyebrow" data-reveal="fade">Payment Details</span>
          <h2 id="pay-h" data-reveal="up" data-delay="90">Pay by <em class="gold-text serif">UPI or Bank Transfer</em></h2>
          <p data-reveal="up" data-delay="160">Always confirm the final amount with our team on WhatsApp before making a payment.</p>

          <div class="paybox" data-reveal="up" data-delay="220">
            <div class="paybox__head">{I['qr']}<h3>UPI Payment</h3></div>
            <dl class="paybox__list">
              <div><dt>UPI ID</dt><dd class="mono">{SITE['upi_id']}</dd></div>
              <div><dt>Payee Name</dt><dd>{SITE['bank_holder']}</dd></div>
            </dl>
          </div>

          <div class="paybox" data-reveal="up" data-delay="290">
            <div class="paybox__head">{I['rupee']}<h3>Bank Transfer (NEFT / IMPS / RTGS)</h3></div>
            <dl class="paybox__list">
              <div><dt>Account Name</dt><dd>{SITE['bank_holder']}</dd></div>
              <div><dt>Bank</dt><dd>{SITE['bank_name']}</dd></div>
              <div><dt>Account Number</dt><dd class="mono">{SITE['bank_ac']}</dd></div>
              <div><dt>IFSC Code</dt><dd class="mono">{SITE['bank_ifsc']}</dd></div>
            </dl>
          </div>

          <div class="notice notice--gold" data-reveal="up" data-delay="350">
            {I['shield']}
            <p><strong>Payment safety.</strong> KIARIT will never ask for your UPI PIN, OTP or card CVV. Verify the payee name reads <strong>{SITE['bank_holder']}</strong> before you confirm any transaction.</p>
          </div>

          <div class="contact__actions" data-reveal="up" data-delay="420">
            <a class="btn btn--wa" href="{wa('Hello KIARIT, I have completed the payment. Please find the screenshot attached.')}" target="_blank" rel="noopener noreferrer">{I['wa']} Send Payment Screenshot</a>
            <a class="btn btn--outline" href="tel:{SITE['phone_link']}">Call {SITE['phone_display']}</a>
          </div>
        </div>
      </div>
    </div>
  </section>

  <section class="section grain" aria-labelledby="ship-h">
    <div class="container">
      <div class="sec-head sec-head--center">
        <span class="eyebrow eyebrow--center" data-reveal="fade">Good to Know</span>
        <h2 id="ship-h" data-reveal="up" data-delay="90">Shipping at a <em class="gold-text serif">Glance</em></h2>
      </div>
      <div class="why__grid" data-stagger="100">
        <article class="why__card" data-reveal="up"><div class="why__icon">{I['truck']}</div>
          <h3>Free Above ₹999</h3><p>Complimentary shipping across India on orders above ₹999. A flat ₹79 applies below that.</p></article>
        <article class="why__card" data-reveal="up"><div class="why__icon">{I['clock']}</div>
          <h3>24-Hour Dispatch</h3><p>Orders confirmed before 4 PM are dispatched the same working day wherever possible.</p></article>
        <article class="why__card" data-reveal="up"><div class="why__icon">{I['box']}</div>
          <h3>Secure Packaging</h3><p>Tamper-evident, cushioned packaging protects every product in transit.</p></article>
        <article class="why__card" data-reveal="up"><div class="why__icon">{I['shield']}</div>
          <h3>Damage Protection</h3><p>Report transit damage within 48 hours with an unboxing photo for a free replacement.</p></article>
      </div>
    </div>
  </section>

  <section class="section section--alt grain" aria-labelledby="faq-h">
    <div class="container container--narrow">
      <div class="sec-head sec-head--center">
        <span class="eyebrow eyebrow--center" data-reveal="fade">Questions</span>
        <h2 id="faq-h" data-reveal="up" data-delay="90">Frequently Asked <em class="gold-text serif">Questions</em></h2>
      </div>
      <div class="faq" data-stagger="70">
"""
    for i, (q, a) in enumerate(ORDER_FAQ):
        body += f"""        <details class="faq__item" data-reveal="up"{' open' if i == 0 else ''}>
          <summary class="faq__q"><span>{q}</span><i class="faq__icon" aria-hidden="true"></i></summary>
          <div class="faq__a"><p>{a}</p></div>
        </details>
"""
    body += """      </div>
    </div>
  </section>
"""
    body += cta_band("Ready to Place Your <em>Order</em>?",
                     "Our team is available Monday to Saturday, 9:30 AM to 6:30 PM.",
                     ("View Products", "products.html"), ("Contact Us", "contact.html"))

    page = {
        "file": "order.html",
        "title": "How to Order & Pay | KIARIT PHARMACEUTICALS — UPI QR Payment",
        "desc": "Order KIARIT products in three simple steps — message us on WhatsApp, scan our UPI QR code to pay, and share the screenshot. Free shipping above ₹999, dispatch within 24 hours.",
        "og_title": "How to Order & Pay — KIARIT PHARMACEUTICALS",
        "schema": [org_schema(),
                   breadcrumb([("Home", ""), ("How to Order & Pay", "order.html")]),
                   faq_schema(ORDER_FAQ),
                   {"@context": "https://schema.org", "@type": "HowTo",
                    "name": "How to order from KIARIT PHARMACEUTICALS",
                    "description": "Order KIARIT products in three steps using WhatsApp and UPI QR payment.",
                    "totalTime": "PT5M",
                    "step": [
                        {"@type": "HowToStep", "position": 1, "name": "Message us on WhatsApp",
                         "text": "Send the product name, quantity and your full delivery address with PIN code.",
                         "url": SITE["url"] + "/order.html#payment"},
                        {"@type": "HowToStep", "position": 2, "name": "Scan the QR code and pay",
                         "text": "Open any UPI app, scan our QR code and pay the confirmed amount.",
                         "url": SITE["url"] + "/order.html#payment"},
                        {"@type": "HowToStep", "position": 3, "name": "Share the payment screenshot",
                         "text": "Send your payment screenshot on WhatsApp. We dispatch within 24 working hours.",
                         "url": SITE["url"] + "/order.html#payment"}]}],
    }
    write("order.html", render(page, body))


if __name__ == "__main__":
    print("Building Phase 4 pages...")
    build_about()
    build_contact()
    build_order()
    print("Done.")
