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
    "phone_display": "+91 85878 75749",
    "phone_link": "+918587875749",
    "wa": "918587875749",
    "email": "kiaritpharma@gmail.com",
    "addr_line1": "1st Floor, 1st Main, Ganga Nagar, Gramatana,",
    "addr_line2": "HMT Layout, CBI Main Rd, Bengaluru, Karnataka 560032",
    "street": "1st Floor, 1st Main, Ganga Nagar, Gramatana, HMT Layout, CBI Main Rd",
    "city": "Bengaluru",
    "region": "Karnataka",
    "zip": "560032",
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
    "ceo": "Yogesh Kumar Bhatra",
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

# Set True to restore the Order & Pay nav item, footer link, and related CTAs.
SHOW_ORDER_PAY = False

# ---------------------------------------------------------------- product data
PRODUCTS = [
    {
        "slug": "ritclear-az-serum", "img": "product-1.jpg", "legacy": "product-1",
        "name": "Ritclear AZ Serum", "cat": "Dermatology",
        "tag": "Bestseller", "tag_class": "",
        "size": "30 ml", "price": 1499, "mrp": 1499, "sku": "KRT-RCAZ-030",
        "spec_img": "ritclear-AZ-serum.jpg",
        "short": "A liposomal advance repair serum with azelaic acid 10%, tranexamic acid 3% and niacinamide 5% that brightens, fades dark spots and calms oil and pores.",
        "meta": "Ritclear AZ Serum is a liposomal advance repair serum with azelaic acid 10%, tranexamic acid 3%, niacinamide 5%, liquorice, salicylic acid and alpha arbutin. For all skin types.",
        "long": [
            "Ritclear AZ Serum is a liposomal advance repair serum for all skin types. Azelaic acid at 10% helps settle acne and blemishes while evening tone. Tranexamic acid at 3% and alpha arbutin at 1% work on dark spots and excess pigment. Niacinamide at 5% refines pores, reins in oil and supports the barrier.",
            "Liquorice extract at 2% calms redness, and salicylic acid at 1% keeps pores from clogging. The liposomal base lets these strengths sit on skin that still has to wear sunscreen the next morning. Use it when breakouts and leftover marks show up together.",
        ],
        "benefits": [
            ("Brightens Skin", "Niacinamide and liquorice lift dullness without a harsh peel."),
            ("Reduces Dark Spots", "Tranexamic acid and alpha arbutin interrupt leftover pigment."),
            ("Oil Control and Pore Care", "Niacinamide and salicylic acid keep pores clearer and less shiny."),
            ("Soothes and Hydrates", "Liquorice and the liposomal base calm skin while the acids work."),
        ],
        "how": ["Cleanse with Ritglow Face Wash and pat the skin dry.",
                "Apply a few drops to the face, avoiding the eye area.",
                "Use once daily at night to start, then morning and night if skin stays calm.",
                "Finish daytime use with Ritshade Sunscreen."],
        "ingredients": "Aqua, Azelaic Acid (10%), Tranexamic Acid (3%), Niacinamide (5%), Glycyrrhiza Glabra (Liquorice) Extract (2%), Salicylic Acid (1%), Alpha Arbutin (1%), Phospholipids (Liposomal Complex), Glycerin, Propanediol, Phenoxyethanol.",
        "faq": [("How soon will I see results?", "Active spots often look calmer in 2\u20133 weeks. Dark marks take longer \u2014 usually 8\u201312 weeks of steady use."),
                ("Can I use it with other actives?", "Yes, but add them one at a time. Keep strong retinoids or extra acids on alternate nights until you know how your skin responds.")],
    },
    {
        "slug": "ritshade-sunscreen", "img": "product-2.jpg", "legacy": "product-2",
        "name": "Ritshade Sunscreen", "cat": "Daily Protection",
        "tag": "", "tag_class": "",
        "size": "50 ml", "price": 599, "mrp": 599, "sku": "KRT-RSH-050",
        "spec_img": "ritshade-sunscreen.jpg",
        "short": "A daily SPF 50+ PA+++ sunscreen with Tinosorb M, micronized titanium dioxide and vitamin C \u2014 light, non-comedogenic and no white cast.",
        "meta": "Ritshade Daily Sunscreen is SPF 50+ PA+++ with Tinosorb M 2%, micronized titanium dioxide 10%, vitamin C 5% and niacinamide. No white cast. 50 ml.",
        "long": [
            "Ritshade is a daily sunscreen built to protect, brighten and support repair. Tinosorb M at 2% covers UVA and UVB. Micronized titanium dioxide at 10% adds a physical block. Together they deliver SPF 50+ PA+++ without a chalky film on Indian skin tones.",
            "Vitamin C at 5% and niacinamide at 2% work on dullness and uneven tone under the filter. Hyaluronic acid, rosehip oil, tea tree oil and a little olive oil keep the texture light and non-comedogenic, so it can sit on oily or acne-prone skin through a humid day.",
        ],
        "benefits": [
            ("SPF 50+ PA+++", "Broad-spectrum UVA and UVB protection for everyday sun."),
            ("No White Cast", "Micronized filters blend in instead of sitting white."),
            ("Brightens Under SPF", "Vitamin C and niacinamide help tone while you stay protected."),
            ("Daily, All Skin Types", "Ultra-light, non-comedogenic and made for everyday wear."),
        ],
        "how": ["Apply as the last step of your morning routine.",
                "Use two finger-lengths for the face and neck.",
                "Wait about 15 minutes before strong sun.",
                "Reapply every 3\u20134 hours when you are outdoors."],
        "ingredients": "Aqua, Titanium Dioxide (micronized, 10%), Bis-Ethylhexyloxyphenol Methoxyphenyl Triazine (Tinosorb M, 2%), Ascorbic Acid (Vitamin C, 5%), Niacinamide (2%), Sodium Hyaluronate (2%), Rosa Canina Fruit Oil (Rosehip, 2%), Melaleuca Alternifolia Leaf Oil (Tea Tree, 1%), Olea Europaea Fruit Oil (Olive, 0.5%), Glycerin, Phenoxyethanol.",
        "faq": [("Will it clog pores?", "It is non-comedogenic and light enough for oily and acne-prone skin."),
                ("Does it leave a white cast?", "No. The micronized titanium dioxide is chosen so it disappears on medium and deep skin tones.")],
    },
    {
        "slug": "ritglow-face-wash", "img": "product-3.jpg", "legacy": "product-3",
        "name": "Ritglow Face Wash", "cat": "Skincare",
        "tag": "Oil-Free", "tag_class": " pcard__tag--sage",
        "size": "100 ml", "price": 399, "mrp": 399, "sku": "KRT-RGF-100",
        "spec_img": "ritglow-face-wash.jpg",
        "short": "An oil-free daily face wash with vitamin C, kojic acid dipalmitate, niacinamide and glycolic acid that brightens while it cleans.",
        "meta": "Ritglow Oil-Free Daily Face Wash uses vitamin C 3%, kojic acid dipalmitate 2%, niacinamide, glycolic acid and salicylic acid. Use morning and night. 100 ml.",
        "long": [
            "Ritglow is an oil-free daily face wash for skin that looks dull by evening and still needs a proper clean. Sodium ascorbyl phosphate (vitamin C) at 3% and kojic acid dipalmitate at 2% target dark spots. Niacinamide at 1% helps pores and oil. Glycolic acid at 2% and salicylic acid at 1% lift dead cells and clear blackheads.",
            "Hyaluronic acid, aloe at 2.5%, D-panthenol, liquorice and tocopheryl acetate keep the wash from leaving skin tight. Glutathione is in the blend for extra brightness. Use it morning and night on a wet face.",
        ],
        "benefits": [
            ("Brightens as It Washes", "Vitamin C and kojic acid dipalmitate fade dullness and dark spots."),
            ("Clears Pores", "Salicylic acid and glycolic acid help with blackheads and rough texture."),
            ("Oil-Free Daily Clean", "Lifts sebum and sunscreen without putting oil back on the skin."),
            ("Comfort After Rinsing", "Aloe, panthenol and hyaluronic acid limit that tight, dry feeling."),
        ],
        "how": ["Use morning and night on clean, wet skin.",
                "Massage a small amount over the face for about 30 seconds.",
                "Rinse thoroughly and pat dry.",
                "Follow with Ritclear AZ Serum at night and Ritshade in the morning."],
        "ingredients": "Aqua, Glutathione, Sodium Ascorbyl Phosphate (Vitamin C, 3%), Kojic Acid Dipalmitate (2%), Sodium Hyaluronate, Niacinamide (1%), Glycolic Acid (2%), Salicylic Acid (1%), Panthenol (0.5%), Tocopheryl Acetate (0.4%), Aloe Barbadensis Leaf Extract (2.5%), Glycyrrhiza Glabra (Licorice) Extract (1%), Phenoxyethanol.",
        "faq": [("Will it dry my skin?", "It is oil-free, but aloe, panthenol and hyaluronic acid are there so skin should not feel stripped after you rinse."),
                ("Can I use it twice a day?", "Yes. The sheet is written for morning and night use on wet skin.")],
    },
    {
        "slug": "kiatral-ad-anti-dandruff-shampoo", "img": "product-4.jpg", "legacy": "product-4",
        "name": "Kiatral-AD Anti Dandruff Shampoo", "cat": "Hair Care",
        "tag": "", "tag_class": "",
        "size": "250 ml", "price": 799, "mrp": 799, "sku": "KRT-KAD-250",
        "spec_img": "kiarit-AD-anti-dandruff-shapoo.jpg",
        "short": "An anti-dandruff shampoo with piroctone olamine and climbazole that clears flakes while ceramides, avocado and hyaluronic acid keep the scalp comfortable.",
        "meta": "Kiatral-AD Anti Dandruff Shampoo uses piroctone olamine, climbazole, ceramide, avocado and hyaluronic acid to control dandruff without stripping the scalp. 250 ml.",
        "long": [
            "Kiatral-AD is built for scalp that sheds white flakes and itches after every wash. Piroctone olamine and climbazole target the yeast that drives dandruff, so flakes settle instead of bouncing back in a day or two.",
            "Ceramide, avocado oil and hyaluronic acid support the scalp barrier while you cleanse, so hair does not feel squeaky-dry afterwards. Suited to dry and normal scalp. Use two to three times a week at first, then ease into a routine that keeps flakes away.",
        ],
        "benefits": [
            ("Fights Dandruff", "Piroctone olamine and climbazole reduce flakes, itch and the fungus behind them."),
            ("Soothes an Itchy Scalp", "Climbazole and ceramides calm irritation instead of leaving the scalp raw."),
            ("Moisturises While It Cleans", "Ceramide, avocado and hyaluronic acid lock moisture into the scalp."),
            ("Safe for Daily Use", "Strong enough for flakes, mild enough to wash with regularly."),
        ],
        "how": ["Wet hair thoroughly with lukewarm water.",
                "Work a coin-sized amount into the scalp and massage for 60\u201390 seconds.",
                "Leave on for 2\u20133 minutes so the actives can work, then rinse well.",
                "Use 2\u20133 times a week, or as advised for stubborn dandruff."],
        "ingredients": "Aqua, Piroctone Olamine, Climbazole, Ceramide NP, Persea Gratissima (Avocado) Oil, Sodium Hyaluronate, Sodium Cocoyl Isethionate, Cocamidopropyl Betaine, Glycerin, Panthenol, Citric Acid, Sodium Benzoate, Phenoxyethanol.",
        "faq": [("How soon will flakes reduce?", "Most people notice less itch and fewer flakes within 1\u20132 weeks of regular use. Stick with it for a full month before judging the result."),
                ("Can I use it every day?", "Start with 2\u20133 washes a week. If your scalp stays comfortable, you can wash more often, but daily use is not required for most people.")],
    },
    {
        "slug": "kiarestora-shower-oil", "img": "product-5.jpg", "legacy": "product-5",
        "name": "KiaRestora Shower Oil", "cat": "Body Care",
        "tag": "", "tag_class": "",
        "size": "250 ml", "price": 999, "mrp": 999, "sku": "KRT-KRS-250",
        "spec_img": "kiaRestora-Shower-oil.jpg",
        "short": "An oil-to-milk shower oil with avocado oil, lecithin and lactic acid that cleans dry to normal skin without stripping the barrier.",
        "meta": "KiaRestora Shower Oil is a soap-free, fragrance-free, paraben-free oil-to-milk cleanser with avocado oil, lecithin and lactic acid. For dry to normal skin. 250 ml.",
        "long": [
            "KiaRestora is a nourishing oil-to-milk cleanser for dry to normal skin. On wet skin it turns milky, lifts the day\u2019s grime, and still leaves lipids behind so the barrier does not collapse. Avocado oil nourishes. Lecithin supports the barrier. Lactic acid gives a light smooth without a scrub.",
            "It is soap-free, fragrance-free, paraben-free and dermatologically tested, for external use. Useful when dryness, weather or everyday irritants leave skin tight after a normal body wash. Skin should feel soft and velvety once you rinse.",
        ],
        "benefits": [
            ("Oil-to-Milk Cleanse", "Melts impurities without stripping the moisture the skin already has."),
            ("Barrier Support", "Lecithin and avocado oil help the skin hold together after washing."),
            ("Gentle Smooth", "Lactic acid lightly refines texture without a harsh scrub."),
            ("Daily, Sensitive-Friendly", "Soap-free, fragrance-free and paraben-free for dry to normal skin."),
        ],
        "how": ["Apply on wet skin in the shower.",
                "Massage gently until the oil turns milky.",
                "Rinse thoroughly with lukewarm water.",
                "Pat dry. Follow with KiaMoist if skin still feels dry."],
        "ingredients": "Glycine Soja Oil, Lecithin, Laureth-4, Cocamide DEA, Poloxamer 101, Persea Gratissima (Avocado) Oil, Lactic Acid, Aqua, Caprylic/Capric Triglyceride, Ascorbyl Palmitate, Citric Acid.",
        "faq": [("Do I still need body lotion?", "Often the oil is enough. On very dry days, follow with KiaMoist Body Lotion."),
                ("Is it soap-free?", "Yes. It is also fragrance-free and paraben-free, and marked for external use only.")],
    },
    {
        "slug": "kiamoist-body-lotion", "img": "product-6.jpg", "legacy": "product-6",
        "name": "KiaMoist Body Lotion", "cat": "Body Care",
        "tag": "New Launch", "tag_class": "",
        "size": "250 ml", "price": 799, "mrp": 799, "sku": "KRT-KMB-250",
        "spec_img": "kiamoist-body-lotion.jpg",
        "short": "A daily body lotion with shea, mango and cocoa butters that deeply moisturises dry to normal skin and helps limit water loss.",
        "meta": "KiaMoist Body Lotion deeply moisturises, supports the skin barrier and helps prevent TEWL. Shea, mango, cocoa butter and aloe. Dry to normal skin. 250 ml.",
        "long": [
            "KiaMoist is a daily full-body lotion for dry to normal skin that wants moisture without a greasy coat. Glycerin and propylene glycol pull water in. Shea butter, mango seed butter and cocoa butter soften rough patches on hands, feet, elbows and knees. Coconut oil conditions dry skin.",
            "Caprylic/capric triglyceride and isoamyl laurate keep the feel light. Dimethicone forms a thin layer that slows moisture loss (TEWL). Aloe soothes skin that feels stressed after a hot shower. Use it once the skin is still slightly damp.",
        ],
        "benefits": [
            ("Intensive Moisture", "Glycerin, propylene glycol and butters hold water on dry skin."),
            ("Barrier Care", "Shea butter and dimethicone support the barrier and slow water loss."),
            ("Softens Rough Spots", "Mango, cocoa and coconut oils help elbows, knees, hands and feet."),
            ("Smooth, Non-Greasy Feel", "Lightweight emollients sink in instead of sitting on the skin."),
        ],
        "how": ["After a bath or shower, pat skin until it is slightly damp.",
                "Warm a small amount between your palms.",
                "Smooth over the body, including hands, feet, elbows and knees.",
                "Use daily. A second pass is fine on very dry areas."],
        "ingredients": "Aqua, Glycerin, Propylene Glycol, Butyrospermum Parkii (Shea) Butter, Mangifera Indica (Mango) Seed Butter, Theobroma Cacao (Cocoa) Butter, Cocos Nucifera (Coconut) Oil, Caprylic/Capric Triglyceride, Isoamyl Laurate, Dimethicone, Aloe Barbadensis Leaf Extract, Phenoxyethanol.",
        "faq": [("Will it feel greasy?", "The lightweight oils and dimethicone are there for a smooth, non-greasy finish. Use less if you dress immediately."),
                ("Who is it for?", "Dry to normal skin, for daily full-body moisturising \u2014 not as a face cream.")],
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


def _expand_partial(tpl):
    """Fill the shared placeholders so the product lists in the nav and the
    footer are generated from PRODUCTS rather than hand-maintained."""
    menu = "\n".join(
        f'            <a href="{url(p["slug"])}" role="menuitem">'
        f'<span class="dd-dot"></span>{p["name"]}</a>'
        for p in PRODUCTS)
    links = "\n".join(
        f'          <a href="{url(p["slug"])}">{p["name"]}</a>'
        for p in PRODUCTS)
    order_nav = ""
    order_footer = ""
    if SHOW_ORDER_PAY:
        order_nav = '        <div class="nav__item"><a class="nav__link" href="/order">Order &amp; Pay</a></div>\n'
        order_footer = '          <a href="/order">How to Order &amp; Pay</a>\n'
    return (tpl.replace("{{PRODUCT_MENU}}", menu)
               .replace("{{PRODUCT_LINKS}}", links)
               .replace("{{ORDER_NAV}}", order_nav)
               .replace("{{ORDER_FOOTER}}", order_footer)
               .replace("{{WA_ORDER}}", wa("Hello KIARIT, I would like to place an order."))
               .replace("{{WA_ASK}}", wa("Hello KIARIT, I have a question."))
               .replace("{{WA_PLAIN}}", "https://wa.me/" + SITE["wa"])
               .replace("{{PHONE_LINK}}", SITE["phone_link"])
               .replace("{{PHONE_DISPLAY}}", SITE["phone_display"])
               .replace("{{EMAIL}}", SITE["email"])
               .replace("{{ADDR1}}", SITE["addr_line1"])
               .replace("{{ADDR2}}", SITE["addr_line2"]))


_HEADER_RAW = read("tools/partials/header.html")
_FOOTER_RAW = read("tools/partials/footer.html")
_FLOATERS_RAW = read("tools/partials/floaters.html")


def url(target):
    """Map a page filename to its public URL.

    The site is served from Cloudflare with clean URLs, so "about.html" is
    published at "/about" and the home page at "/". Every link, canonical tag
    and sitemap entry goes through here so the whole site agrees on one form
    per page — a mismatch would put a redirect in front of an indexed URL.
    """
    name = target[:-5] if target.endswith(".html") else target
    return "/" if name == "index" else "/" + name


def head(page):
    """Build the <head> block."""
    canonical = SITE["url"] + url(page["file"])
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
{'' if page.get('file') == 'index.html' else '<link rel="stylesheet" href="assets/css/inner.css">'}
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


def cta_band(title, text, b1=("About Us", "about"), b2=("Contact Us", "contact")):
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


# Partials depend on wa(), so expand them once it is defined.
HEADER = _expand_partial(_HEADER_RAW)
FOOTER = _expand_partial(_FOOTER_RAW)
FLOATERS = _expand_partial(_FLOATERS_RAW)


CAT_TINT = {
    "Dermatology":      "derma",
    "Skincare":         "skin",
    "Daily Protection": "sun",
    "Hair Care":        "hair",
    "Nutraceutical":    "nutra",
    "Body Care":        "body",
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
            <a href="{url(p['slug'])}" aria-label="View {p['name']} details">
              <picture>
                <source srcset="assets/img/products/{p['img'].rsplit('.', 1)[0]}.webp" type="image/webp">
                <img src="assets/img/products/{p['img']}" alt="{p['name']} — {p['cat'].lower()} product by KIARIT Pharmaceuticals" width="900" height="900" loading="lazy">
              </picture>
            </a>
          </div>
          <div class="pcard__body">
            <div class="pcard__cat">{p['cat']}</div>
            <h3 class="pcard__title"><a href="{url(p['slug'])}">{p['name']}</a></h3>
            <p class="pcard__desc">{p['short']}</p>
            <div class="pcard__foot">
              <div class="pcard__price">{rupee(p['price'])}{(' <del>' + rupee(p['mrp']) + '</del>') if p['mrp'] > p['price'] else ''}<small>{p['size']} · Inclusive of taxes</small></div>
              <div class="pcard__actions">
                <a class="pcard__icon-btn" href="{url(p['slug'])}" aria-label="View {p['name']} details" title="View details">{I['eye']}</a>
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
    # slider.js only initialises [data-slider] roots, so pages without a
    # carousel should not pay to download and parse it. Same idea for
    # filter.js, which the products listing adds for itself.
    scripts = ('\n<script src="assets/js/main.js" defer></script>\n'
               '<script src="assets/js/reveal.js" defer></script>\n')
    if 'data-slider' in body:
        scripts += '<script src="assets/js/slider.js" defer></script>\n'
    return (head(page) + header_for(page) + '<main id="main">\n' + body +
            "\n</main>\n" + FOOTER + FLOATERS + scripts +
            "</body>\n</html>\n")


def write(name, html):
    with open(os.path.join(ROOT, name), "w", encoding="utf-8") as f:
        f.write(html)
    print("  wrote", name, f"({len(html)//1024} KB)")
