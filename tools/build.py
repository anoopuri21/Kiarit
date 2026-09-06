#!/usr/bin/env python3
"""
KIARIT PHARMACEUTICALS — static site builder.

Renders plain HTML files from shared partials + per-page content so the
header, footer, meta and schema stay identical across all 16 pages.

    python3 tools/build.py

Output is 100% static HTML/CSS/JS — no runtime dependency on this script.
"""
import os, re, json, datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ---------------------------------------------------------------- site config
SITE = {
    "name": "KIARIT PHARMACEUTICALS",
    "short": "KIARIT",
    "url": "https://www.kiaritpharmaceuticals.com",
    "phone_display": "+91 98765 43210",
    "phone_link": "+919876543210",
    "wa": "919876543210",
    "email": "info@kiaritpharmaceuticals.com",
    "addr_line1": "Plot No. 24, Industrial Area Phase II",
    "addr_line2": "New Delhi 110020, India",
    "street": "Plot No. 24, Industrial Area Phase II",
    "city": "New Delhi",
    "region": "Delhi",
    "zip": "110020",
    "upi_id": "kiaritpharma@upi",
    "bank_name": "HDFC Bank",
    "bank_ac": "5010 0123 4567 89",
    "bank_ifsc": "HDFC0001234",
    "bank_holder": "KIARIT PHARMACEUTICALS",
    "hours_week": "Monday – Saturday · 9:30 AM – 6:30 PM",
    "hours_sun": "Sunday · Closed",
    "social": {
        "facebook": "https://www.facebook.com/kiaritpharmaceuticals",
        "instagram": "https://www.instagram.com/kiaritpharmaceuticals",
        "linkedin": "https://www.linkedin.com/company/kiaritpharmaceuticals",
        "youtube": "https://www.youtube.com/@kiaritpharmaceuticals",
    },
    "ceo": "Yogesh Kumar Bharta",
    "overview": ("KIARIT PHARMACEUTICALS is a healthcare-focused pharmaceutical and cosmetic "
                 "company committed to delivering high-quality, innovative, and affordable "
                 "products. We specialize in dermatology, skincare, nutraceuticals, and "
                 "pharmaceutical formulations designed to improve health, wellness, and "
                 "confidence. Our mission is to provide safe, effective, and scientifically "
                 "developed products while maintaining the highest standards of quality, "
                 "integrity, and customer satisfaction. Through continuous innovation and a "
                 "patient-centric approach, KIARIT PHARMACEUTICALS strives to become a trusted "
                 "name in healthcare and personal care solutions."),
}

# ---------------------------------------------------------------- product data
PRODUCTS = [
    {
        "slug": "product-1", "name": "Kiarit Glow Serum", "cat": "Dermatology",
        "tag": "Bestseller", "tag_class": "",
        "size": "30 ml", "price": 849, "mrp": 1099, "sku": "KRT-GS-030",
        "short": "A lightweight Vitamin C & niacinamide serum that visibly brightens dull skin, evens tone and defends against daily environmental stress.",
        "meta": "Kiarit Glow Serum with Vitamin C and niacinamide brightens dull skin, evens tone and protects against daily environmental stress. 30 ml. Order on WhatsApp.",
        "long": [
            "Kiarit Glow Serum is a fast-absorbing daily brightening treatment built around a stabilised form of Vitamin C, supported by niacinamide and a light hyaluronic base. It is formulated for Indian skin and climate — potent enough to deliver visible results, gentle enough for everyday use.",
            "Used consistently each morning, it helps soften the appearance of dullness, uneven tone and early pigmentation, while the antioxidant complex helps defend skin against pollution and daily oxidative stress.",
        ],
        "benefits": [
            ("Visible Brightening", "Helps reduce the look of dullness and uneven tone over 4–6 weeks."),
            ("Antioxidant Defence", "Supports the skin's barrier against pollution and free-radical stress."),
            ("Lightweight Finish", "Absorbs in seconds with no sticky or greasy residue."),
            ("Gentle Formulation", "Free from parabens, sulphates and added synthetic fragrance."),
        ],
        "how": ["Cleanse and pat the skin dry.",
                "Apply 3–4 drops to the face and neck, avoiding the eye area.",
                "Follow with Kiarit Aqua Cream to lock in hydration.",
                "Always finish with Kiarit Sun Shield SPF 50+ during the day."],
        "ingredients": "Aqua, Ethyl Ascorbic Acid (Vitamin C), Niacinamide, Sodium Hyaluronate, Glycerin, Propanediol, Ferulic Acid, Panthenol, Tocopherol, Xanthan Gum, Phenoxyethanol.",
        "faq": [("How soon will I see results?", "Most users notice improved radiance within 3–4 weeks of consistent daily use, with tone improvements around 6–8 weeks."),
                ("Can I use it with other actives?", "Yes. Use the serum in the morning and keep exfoliating acids or retinoids for your night routine.")],
    },
    {
        "slug": "product-2", "name": "Kiarit Aqua Cream", "cat": "Skincare",
        "tag": "", "tag_class": "",
        "size": "50 g", "price": 699, "mrp": 899, "sku": "KRT-AC-050",
        "short": "A weightless hyaluronic acid moisturiser that locks in hydration for 24 hours, restoring softness and a healthy, dewy finish.",
        "meta": "Kiarit Aqua Cream is a weightless hyaluronic acid moisturiser delivering 24-hour hydration with a non-greasy, dewy finish. 50 g. Order on WhatsApp.",
        "long": [
            "Kiarit Aqua Cream is a gel-cream moisturiser built on multi-weight hyaluronic acid, ceramides and glycerin. The low-weight molecules draw moisture deep into the skin while the ceramide complex helps seal the barrier so hydration lasts through the day.",
            "The texture is deliberately weightless — it disappears into the skin without tack or shine, which makes it comfortable in humid weather and easy to layer under sunscreen or makeup.",
        ],
        "benefits": [
            ("24-Hour Hydration", "Multi-weight hyaluronic acid holds moisture at every layer of the skin."),
            ("Barrier Support", "Ceramides help strengthen and repair a compromised moisture barrier."),
            ("Non-Comedogenic", "Formulated so it will not clog pores or trigger congestion."),
            ("Layers Cleanly", "Sits comfortably under sunscreen, serum or makeup."),
        ],
        "how": ["Apply to clean, slightly damp skin morning and night.",
                "Warm a pea-sized amount between fingertips.",
                "Press gently into the face and neck using upward strokes.",
                "Follow with sunscreen during the daytime."],
        "ingredients": "Aqua, Glycerin, Sodium Hyaluronate, Ceramide NP, Squalane, Caprylic/Capric Triglyceride, Cetearyl Alcohol, Panthenol, Allantoin, Tocopherol, Phenoxyethanol.",
        "faq": [("Is it suitable for oily skin?", "Yes. The gel-cream base is oil-free and non-comedogenic, making it well suited to oily and combination skin."),
                ("Can it be used under makeup?", "Absolutely. Allow one minute to absorb fully, then apply sunscreen and makeup as usual.")],
    },
    {
        "slug": "product-3", "name": "Kiarit Clarify Gel", "cat": "Dermatology",
        "tag": "Dermat Choice", "tag_class": " pcard__tag--sage",
        "size": "30 g", "price": 579, "mrp": 749, "sku": "KRT-CG-030",
        "short": "A non-drying salicylic acid gel that calms active breakouts, refines pores and helps prevent post-acne marks over time.",
        "meta": "Kiarit Clarify Gel with 2% salicylic acid calms active breakouts, unclogs pores and helps prevent post-acne marks without over-drying. 30 g.",
        "long": [
            "Kiarit Clarify Gel pairs 2% salicylic acid with soothing zinc PCA and centella asiatica. The salicylic acid works inside the pore to clear congestion, while the calming actives keep irritation and post-treatment dryness in check.",
            "It is designed as a targeted daily treatment for oily and acne-prone skin — effective on active breakouts, but balanced enough that the skin does not end up tight, flaky or over-stripped.",
        ],
        "benefits": [
            ("Clears Congestion", "2% salicylic acid dissolves oil and debris trapped inside pores."),
            ("Calms Redness", "Centella and zinc PCA soothe inflammation around active breakouts."),
            ("Refines Texture", "Regular use helps visibly minimise the appearance of enlarged pores."),
            ("No Over-Drying", "Balanced formulation avoids the tightness typical of acne treatments."),
        ],
        "how": ["Cleanse thoroughly and pat dry.",
                "Apply a thin layer over affected areas once daily to begin.",
                "Increase to twice daily only once your skin has adjusted.",
                "Always use sunscreen — exfoliating acids increase sun sensitivity."],
        "ingredients": "Aqua, Salicylic Acid (2%), Zinc PCA, Centella Asiatica Extract, Niacinamide, Glycerin, Propanediol, Allantoin, Panthenol, Xanthan Gum, Phenoxyethanol.",
        "faq": [("Can I use it on my whole face?", "Yes, a thin layer across oily areas is fine. Start once daily and build up slowly."),
                ("Is it safe during pregnancy?", "Please consult your physician before using salicylic acid products during pregnancy.")],
    },
    {
        "slug": "product-4", "name": "Kiarit Sun Shield SPF 50+", "cat": "Daily Protection",
        "tag": "", "tag_class": "",
        "size": "50 ml", "price": 749, "mrp": 949, "sku": "KRT-SS-050",
        "short": "Broad-spectrum SPF 50+ PA++++ protection in a matte, no-white-cast finish that layers beautifully under makeup.",
        "meta": "Kiarit Sun Shield SPF 50+ PA++++ offers broad-spectrum UVA and UVB protection with a matte, no-white-cast finish. 50 ml. Order on WhatsApp.",
        "long": [
            "Kiarit Sun Shield delivers SPF 50+ PA++++ broad-spectrum protection using a modern hybrid filter system. It shields against UVA, UVB and visible-light stress without the heaviness or chalky cast associated with traditional sunscreens.",
            "The finish is genuinely matte, which makes it practical for daily Indian weather — comfortable through humidity, and clean enough to wear under makeup without pilling.",
        ],
        "benefits": [
            ("SPF 50+ PA++++", "Highest tier of broad-spectrum UVA and UVB defence."),
            ("No White Cast", "Blends invisibly across a wide range of Indian skin tones."),
            ("Matte Finish", "Controls shine through the day without drying the skin."),
            ("Makeup Friendly", "Sits smoothly under foundation without pilling or patchiness."),
        ],
        "how": ["Apply as the final step of your morning routine.",
                "Use approximately two finger-lengths for face and neck.",
                "Apply 15 minutes before sun exposure.",
                "Reapply every 3–4 hours when outdoors."],
        "ingredients": "Aqua, Ethylhexyl Methoxycinnamate, Zinc Oxide, Titanium Dioxide, Bis-Ethylhexyloxyphenol Methoxyphenyl Triazine, Glycerin, Niacinamide, Silica, Tocopherol, Phenoxyethanol.",
        "faq": [("Does it leave a white cast?", "No. The hybrid filter system is formulated specifically to blend invisibly on deeper skin tones."),
                ("How often should I reapply?", "Every 3–4 hours when outdoors, or immediately after heavy sweating or swimming.")],
    },
    {
        "slug": "product-5", "name": "Kiarit Repair Hair Oil", "cat": "Hair Care",
        "tag": "", "tag_class": "",
        "size": "100 ml", "price": 649, "mrp": 829, "sku": "KRT-RH-100",
        "short": "A fast-absorbing blend of botanical oils and peptides that strengthens roots, reduces breakage and restores natural shine.",
        "meta": "Kiarit Repair Hair Oil blends botanical oils, biotin and peptides to strengthen roots, reduce breakage and restore shine. 100 ml. Order on WhatsApp.",
        "long": [
            "Kiarit Repair Hair Oil combines cold-pressed botanical oils with biotin and a lightweight peptide complex. Rather than sitting on the surface, the blend is formulated to absorb into the scalp and hair shaft, supporting stronger roots and reducing mechanical breakage.",
            "Regular use helps improve the look of density and shine, while the non-sticky texture means it can be used as a pre-wash treatment or a light overnight nourishing oil.",
        ],
        "benefits": [
            ("Strengthens Roots", "Biotin and peptides support the scalp and follicle health."),
            ("Reduces Breakage", "Improves elasticity so hair resists everyday mechanical damage."),
            ("Restores Shine", "Botanical oils smooth the cuticle for natural, healthy lustre."),
            ("Non-Sticky", "Absorbs cleanly without the heaviness of traditional hair oils."),
        ],
        "how": ["Section dry hair and apply directly to the scalp.",
                "Massage gently with fingertips for 3–5 minutes.",
                "Work the remaining oil through the mid-lengths and ends.",
                "Leave for at least one hour, or overnight, then shampoo."],
        "ingredients": "Cocos Nucifera Oil, Sesamum Indicum Oil, Argania Spinosa Kernel Oil, Ricinus Communis Oil, Biotin, Copper Tripeptide-1, Rosmarinus Officinalis Extract, Tocopherol, Parfum (Natural).",
        "faq": [("How often should I use it?", "Two to three times a week as a pre-wash treatment gives the best results."),
                ("Will it make my hair greasy?", "No. The blend is formulated to absorb, and it washes out cleanly with a single shampoo.")],
    },
    {
        "slug": "product-6", "name": "Kiarit Nutra Boost Collagen", "cat": "Nutraceutical",
        "tag": "New Launch", "tag_class": "",
        "size": "200 g", "price": 1199, "mrp": 1499, "sku": "KRT-NB-200",
        "short": "Marine collagen peptides with biotin and Vitamin C to support skin elasticity, hair strength and joint comfort from within.",
        "meta": "Kiarit Nutra Boost delivers marine collagen peptides with biotin and Vitamin C to support skin elasticity, hair strength and joint comfort. 200 g.",
        "long": [
            "Kiarit Nutra Boost provides hydrolysed marine collagen peptides in a readily absorbable form, combined with Vitamin C — an essential cofactor in the body's own collagen synthesis — plus biotin and zinc.",
            "It is an unflavoured powder that dissolves cleanly in water, juice or a morning beverage, with none of the fishy aftertaste common to marine collagen supplements.",
        ],
        "benefits": [
            ("Skin Elasticity", "Supports the skin's natural collagen structure and firmness."),
            ("Hair & Nail Strength", "Biotin and zinc support keratin production from within."),
            ("Joint Comfort", "Type I and III peptides support connective tissue health."),
            ("Dissolves Cleanly", "Unflavoured and fully soluble with no aftertaste."),
        ],
        "how": ["Add one scoop (10 g) to 200 ml of water or juice.",
                "Stir well until completely dissolved.",
                "Take once daily, preferably on an empty stomach.",
                "Use consistently for at least 8–12 weeks for best results."],
        "ingredients": "Hydrolysed Marine Collagen Peptides (Type I & III), Ascorbic Acid (Vitamin C), Biotin, Zinc Gluconate, Hyaluronic Acid, Natural Flavour.",
        "faq": [("Does it taste fishy?", "No. The peptides are processed and deodorised so the powder is genuinely neutral in taste."),
                ("When is the best time to take it?", "Most people take it in the morning on an empty stomach, but any consistent daily time works.")],
    },
]
PMAP = {p["slug"]: p for p in PRODUCTS}


def rupee(n):
    return "₹" + format(n, ",d")


# ---------------------------------------------------------------- icons
I = {
    "phone": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.13.96.36 1.9.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.9.34 1.85.57 2.81.7A2 2 0 0 1 22 16.92z"/></svg>',
    "mail": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="2" y="4" width="20" height="16" rx="2"/><path d="m22 7-10 6L2 7"/></svg>',
    "pin": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0z"/><circle cx="12" cy="10" r="3"/></svg>',
    "clock": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/></svg>',
    "wa": '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M17.47 14.38c-.3-.15-1.76-.87-2.03-.97s-.47-.15-.67.15-.77.96-.94 1.16-.35.22-.65.07a8.13 8.13 0 0 1-2.39-1.47 9 9 0 0 1-1.65-2.06c-.17-.3 0-.46.13-.61s.3-.35.45-.52a2 2 0 0 0 .3-.5.55.55 0 0 0 0-.53c0-.15-.67-1.62-.92-2.21s-.49-.51-.67-.52h-.57a1.1 1.1 0 0 0-.8.37 3.35 3.35 0 0 0-1.04 2.49 5.82 5.82 0 0 0 1.21 3.08 13.3 13.3 0 0 0 5.09 4.49c.71.3 1.26.49 1.69.63a4.07 4.07 0 0 0 1.87.12 3.06 3.06 0 0 0 2-1.41 2.48 2.48 0 0 0 .17-1.41c-.07-.13-.27-.2-.57-.35zM12.05 21.8h-.01a9.78 9.78 0 0 1-4.98-1.37l-.36-.21-3.7.97.99-3.61-.23-.37a9.8 9.8 0 1 1 8.29 4.59zM20.4 3.6A11.75 11.75 0 0 0 2.06 17.79L.4 23.85l6.2-1.63a11.76 11.76 0 0 0 5.45 1.39h.01a11.75 11.75 0 0 0 8.34-20.01z"/></svg>',
    "home": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M3 10.5 12 3l9 7.5"/><path d="M5 9.5V20a1 1 0 0 0 1 1h4v-6h4v6h4a1 1 0 0 0 1-1V9.5"/></svg>',
    "grid": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="3" y="3" width="7.5" height="7.5" rx="1.5"/><rect x="13.5" y="3" width="7.5" height="7.5" rx="1.5"/><rect x="3" y="13.5" width="7.5" height="7.5" rx="1.5"/><rect x="13.5" y="13.5" width="7.5" height="7.5" rx="1.5"/></svg>',
    "arrow": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg>',
    "eye": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M2 12s3.6-7 10-7 10 7 10 7-3.6 7-10 7-10-7-10-7z"/><circle cx="12" cy="12" r="3"/></svg>',
    "check": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="m20 6-11 11-5-5"/></svg>',
    "shield": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 2 4 5v6c0 5 3.4 9.7 8 11 4.6-1.3 8-6 8-11V5z"/><path d="m9 12 2 2 4-4"/></svg>',
    "flask": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M10 2v7.31"/><path d="M14 9.3V1.99"/><path d="M8.5 2h7"/><path d="M14 9.3a6.5 6.5 0 1 1-4 0"/><path d="M5.58 16.5h12.85"/></svg>',
    "drop": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 22a7 7 0 0 0 7-7c0-2-1-3.9-3-5.5s-3.5-4-4-6.5c-.5 2.5-2 4.9-4 6.5C6 11.1 5 13 5 15a7 7 0 0 0 7 7z"/></svg>',
    "heart": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M19 14c1.49-1.46 3-3.21 3-5.5A5.5 5.5 0 0 0 16.5 3c-1.76 0-3 .5-4.5 2-1.5-1.5-2.74-2-4.5-2A5.5 5.5 0 0 0 2 8.5c0 2.3 1.5 4.05 3 5.5l7 7Z"/></svg>',
    "bulb": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M15 14c.2-1 .7-1.7 1.5-2.5 1-.9 1.5-2.2 1.5-3.5A6 6 0 0 0 6 8c0 1 .2 2.2 1.5 3.5.7.7 1.3 1.5 1.5 2.5"/><path d="M9 18h6M10 22h4"/></svg>',
    "rupee": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M6 3h12M6 8h12M6 13h6a5 5 0 0 0 0-10"/><path d="m6 13 8 8"/></svg>',
    "chart": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M3 3v16a2 2 0 0 0 2 2h16"/><path d="m19 9-5 5-4-4-3 3"/></svg>',
    "truck": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M14 18V6a2 2 0 0 0-2-2H4a2 2 0 0 0-2 2v11a1 1 0 0 0 1 1h2"/><path d="M14 9h4l4 4v4a1 1 0 0 1-1 1h-1"/><circle cx="7.5" cy="18.5" r="2.5"/><circle cx="17.5" cy="18.5" r="2.5"/></svg>',
    "qr": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="3" y="3" width="7" height="7" rx="1"/><rect x="14" y="3" width="7" height="7" rx="1"/><rect x="3" y="14" width="7" height="7" rx="1"/><path d="M14 14h3v3h-3zM18 18h3v3h-3z"/></svg>',
    "leaf": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M11 20A7 7 0 0 1 9.8 6.1C15.5 5 17 4.48 19 2c1 2 2 4.18 2 8 0 5.5-4.78 10-10 10"/><path d="M2 21c0-3 1.85-5.36 5.08-6C9.5 14.52 12 13 13 12"/></svg>',
    "globe": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="10"/><path d="M2 12h20M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/></svg>',
    "star": '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="m12 2 3.1 6.3 6.9 1-5 4.9 1.2 6.9L12 17.8 5.8 21.1 7 14.2l-5-4.9 6.9-1z"/></svg>',
    "award": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="8" r="6"/><path d="M15.5 13.5 17 22l-5-3-5 3 1.5-8.5"/></svg>',
    "box": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="m7.5 4.27 9 5.15"/><path d="M21 8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16Z"/><path d="m3.3 7 8.7 5 8.7-5M12 22V12"/></svg>',
    "chat": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg>',
    "users": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87M16 3.13a4 4 0 0 1 0 7.75"/></svg>',
    "lock": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="3" y="11" width="18" height="11" rx="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/></svg>',
    "target": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="6"/><circle cx="12" cy="12" r="2"/></svg>',
    "eyeglass": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3"/></svg>',
}


def stars(n=5):
    return '<div class="testi__stars" aria-label="Rated %d out of 5">%s</div>' % (n, I["star"] * n)


# ---------------------------------------------------------------- partials
def read(p):
    with open(os.path.join(ROOT, p), encoding="utf-8") as f:
        return f.read()


HEADER = read("tools/partials/header.html")
FOOTER = read("tools/partials/footer.html")
FLOATERS = read("tools/partials/floaters.html")


def head(page):
    """Build the <head> block."""
    canonical = SITE["url"] + "/" + ("" if page["file"] == "index.html" else page["file"])
    og_img = page.get("og", "assets/img/og/og-default.jpg")
    robots = page.get("robots", "index, follow, max-image-preview:large, max-snippet:-1")
    schema = "\n".join(
        '<script type="application/ld+json">\n%s\n</script>' % json.dumps(s, indent=2, ensure_ascii=False)
        for s in page.get("schema", [])
    )
    return f"""<!DOCTYPE html>
<html lang="en-IN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{page['title']}</title>
<meta name="description" content="{page['desc']}">
<meta name="author" content="{SITE['name']}">
<meta name="robots" content="{robots}">
<meta name="theme-color" content="#08080a">
<link rel="canonical" href="{canonical}">

<meta property="og:type" content="{page.get('og_type', 'website')}">
<meta property="og:site_name" content="{SITE['name']}">
<meta property="og:locale" content="en_IN">
<meta property="og:title" content="{page.get('og_title', page['title'])}">
<meta property="og:description" content="{page['desc']}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{SITE['url']}/{og_img}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{SITE['name']}">

<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{page.get('og_title', page['title'])}">
<meta name="twitter:description" content="{page['desc']}">
<meta name="twitter:image" content="{SITE['url']}/{og_img}">

<link rel="icon" href="assets/img/logo.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="assets/img/logo.svg">
<link rel="manifest" href="site.webmanifest">

<link rel="preload" as="font" type="font/woff2" href="assets/fonts/playfair-normal.woff2" crossorigin>
<link rel="preload" as="font" type="font/woff2" href="assets/fonts/inter-normal.woff2" crossorigin>
<link rel="stylesheet" href="assets/css/fonts.css">
{page.get('head_extra', '')}
<link rel="stylesheet" href="assets/css/base.css">
<link rel="stylesheet" href="assets/css/components.css">
<link rel="stylesheet" href="assets/css/pages.css">
<link rel="stylesheet" href="assets/css/inner.css">
<link rel="stylesheet" href="assets/css/luxe.css">

{schema}
</head>
<body>
<a class="skip-link" href="#main">Skip to main content</a>
"""


def org_schema():
    return {
        "@context": "https://schema.org", "@type": "Organization",
        "@id": SITE["url"] + "/#organization",
        "name": SITE["name"], "alternateName": SITE["short"], "url": SITE["url"] + "/",
        "logo": SITE["url"] + "/assets/img/logo.svg",
        "image": SITE["url"] + "/assets/img/og/og-default.jpg",
        "description": SITE["overview"], "foundingDate": "2019",
        "founder": {"@type": "Person", "name": SITE["ceo"], "jobTitle": "Founder & Chief Executive Officer"},
        "address": {"@type": "PostalAddress", "streetAddress": SITE["street"],
                    "addressLocality": SITE["city"], "addressRegion": SITE["region"],
                    "postalCode": SITE["zip"], "addressCountry": "IN"},
        "contactPoint": [{"@type": "ContactPoint", "telephone": "+" + SITE["wa"],
                          "contactType": "customer service", "email": SITE["email"],
                          "areaServed": "IN", "availableLanguage": ["en", "hi"]}],
        "sameAs": list(SITE["social"].values()),
    }


def breadcrumb(items):
    return {"@context": "https://schema.org", "@type": "BreadcrumbList",
            "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n,
                                 "item": SITE["url"] + "/" + u} for i, (n, u) in enumerate(items)]}


def faq_schema(pairs):
    return {"@context": "https://schema.org", "@type": "FAQPage",
            "mainEntity": [{"@type": "Question", "name": q,
                            "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in pairs]}


def page_hero(eyebrow, title, sub, crumbs):
    crumb_html = " ".join(
        f'<a href="{u}">{n}</a><span aria-hidden="true">/</span>' if u else f'<span aria-current="page">{n}</span>'
        for n, u in crumbs)
    return f"""
  <section class="phero on-dark" aria-labelledby="phero-h">
    <div class="phero__bg" aria-hidden="true"></div>
    <div class="container phero__inner">
      <nav class="crumbs" aria-label="Breadcrumb">{crumb_html}</nav>
      <span class="eyebrow eyebrow--light" data-reveal="fade">{eyebrow}</span>
      <h1 id="phero-h" class="phero__title" data-reveal="blur" data-delay="120">{title}</h1>
      <p class="phero__sub" data-reveal="up" data-delay="240">{sub}</p>
    </div>
  </section>
"""


def cta_band(title, text, b1=("About Us", "about.html"), b2=("Contact Us", "contact.html")):
    return f"""
  <section class="ctaband" aria-labelledby="cta-h">
    <div class="ctaband__glow" aria-hidden="true"></div>
    <div class="container ctaband__inner">
      <span class="eyebrow eyebrow--light eyebrow--center" data-reveal="fade">Let's Begin</span>
      <h2 id="cta-h" data-reveal="up" data-delay="90">{title}</h2>
      <p data-reveal="up" data-delay="170">{text}</p>
      <div class="ctaband__actions" data-reveal="up" data-delay="250">
        <a class="btn btn--gold btn--lg" href="{b1[1]}" data-magnetic>{b1[0]} {I['arrow']}</a>
        <a class="btn btn--outline-gold btn--lg" href="{b2[1]}" data-magnetic>{b2[0]} {I['arrow']}</a>
      </div>
      <div class="ctaband__contact" data-reveal="up" data-delay="330">
        <a href="tel:{SITE['phone_link']}">{I['phone']} {SITE['phone_display']}</a>
        <a href="mailto:{SITE['email']}">{I['mail']} {SITE['email']}</a>
        <a href="https://wa.me/{SITE['wa']}" target="_blank" rel="noopener noreferrer">{I['wa']} Chat on WhatsApp</a>
      </div>
    </div>
  </section>
"""


def wa(msg):
    from urllib.parse import quote
    return f"https://wa.me/{SITE['wa']}?text={quote(msg)}"


CAT_TINT = {
    "Dermatology":      "derma",
    "Skincare":         "skin",
    "Daily Protection": "sun",
    "Hair Care":        "hair",
    "Nutraceutical":    "nutra",
}


def tint_of(p):
    """Category tint slug, used to colour-code cards, badges and PDP heroes."""
    return CAT_TINT.get(p["cat"], "derma")


def product_card(p, reveal=True):
    r = ' data-reveal="up"' if reveal else ""
    tag = f'<span class="pcard__tag{p["tag_class"]}">{p["tag"]}</span>' if p["tag"] else ""
    return f"""        <article class="pcard" data-tint="{tint_of(p)}"{r}>
          <div class="pcard__media">
            {tag}
            <a href="{p['slug']}.html" aria-label="View {p['name']} details">
              <img src="assets/img/products/{p['slug']}.jpg" alt="{p['name']} — {p['cat'].lower()} product by KIARIT Pharmaceuticals" width="900" height="900" loading="lazy">
            </a>
          </div>
          <div class="pcard__body">
            <div class="pcard__cat">{p['cat']}</div>
            <h3 class="pcard__title"><a href="{p['slug']}.html">{p['name']}</a></h3>
            <p class="pcard__desc">{p['short']}</p>
            <div class="pcard__foot">
              <div class="pcard__price">{rupee(p['price'])} <del>{rupee(p['mrp'])}</del><small>{p['size']} · Inclusive of taxes</small></div>
              <div class="pcard__actions">
                <a class="pcard__icon-btn" href="{p['slug']}.html" aria-label="View {p['name']} details" title="View details">{I['eye']}</a>
                <a class="pcard__icon-btn pcard__icon-btn--wa" href="{wa('Hello KIARIT, I want to order the ' + p['name'] + '.')}" target="_blank" rel="noopener noreferrer" aria-label="Order {p['name']} on WhatsApp" title="Order on WhatsApp">{I['wa']}</a>
              </div>
            </div>
          </div>
        </article>
"""


"""Map each generated file to the top-level nav item it belongs under, so the
current page is marked with aria-current and the matching active style."""
NAV_OWNER = {
    "index.html": "index.html",
    "about.html": "about.html",
    "products.html": "products.html",
    "contact.html": "contact.html",
    "order.html": "order.html",
}
for _p in PRODUCTS:
    NAV_OWNER[f"{_p['slug']}.html"] = "products.html"


def header_for(page):
    """Return the shared header with the active nav item marked up."""
    owner = NAV_OWNER.get(page.get("file", ""))
    if not owner:
        return HEADER
    target = f'<a class="nav__link" href="{owner}"'
    if target not in HEADER:
        return HEADER
    replacement = f'<a class="nav__link is-active" href="{owner}" aria-current="page"'
    return HEADER.replace(target, replacement, 1)


def render(page, body):
    return (head(page) + header_for(page) + '<main id="main">\n' + body +
            "\n</main>\n" + FOOTER + FLOATERS +
            '\n<script src="assets/js/main.js" defer></script>\n'
            '<script src="assets/js/reveal.js" defer></script>\n'
            '<script src="assets/js/slider.js" defer></script>\n'
            "</body>\n</html>\n")


def write(name, html):
    with open(os.path.join(ROOT, name), "w", encoding="utf-8") as f:
        f.write(html)
    print("  wrote", name, f"({len(html)//1024} KB)")
