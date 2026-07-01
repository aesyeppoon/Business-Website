from pathlib import Path
from textwrap import wrap

from PIL import Image
from reportlab.lib.colors import HexColor, white
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfgen import canvas


ROOT = Path(r"C:\Users\Nick_\Documents\Adaptive Electrical Solutions PTY LTD\Company Logo")
OUT = Path(r"C:\Users\Nick_\Documents\Business Website\brand-guide")
PDF_PATH = OUT / "Adaptive_Electrical_Solutions_Brand_Guide.pdf"

LOGO_BRAND = ROOT / "Logo" / "Brand" / "AES_brand.png"
LOGO_BRAND_REV = ROOT / "Logo" / "Brand" / "AES_brand_REV.png"
LOGO_CENTRED = ROOT / "Logo" / "Centred" / "AES_centred.png"
LOGO_CENTRED_REV = ROOT / "Logo" / "Centred" / "AES_cent_REV.png"
LOGO_LEFT = ROOT / "Logo" / "Left aligned" / "AES_left.png"
LOGO_LEFT_REV = ROOT / "Logo" / "Left aligned" / "AES_left_REV.png"
SOCIAL_ICON = ROOT / "Social" / "Facebook_icon copy.jpg"
SOCIAL_HEADER = ROOT / "Social" / "Header_Desktop copy.jpg"
LETTERHEAD = ROOT / "Letterhead" / "Letterhead.jpg"

YELLOW = HexColor("#FFF200")
TEAL = HexColor("#2893A2")
CYAN = HexColor("#35C2D5")
CHARCOAL = HexColor("#58585A")
INK = HexColor("#202225")
MID = HexColor("#6C7075")
LIGHT = HexColor("#F3F4F4")
LINE = HexColor("#D9DDDF")
PALE_CYAN = HexColor("#EAF8FA")

W, H = A4
M = 42


def fit_image(path, max_w, max_h):
    with Image.open(path) as image:
        w, h = image.size
    ratio = min(max_w / w, max_h / h)
    return w * ratio, h * ratio


def draw_image_contain(c, path, x, y, w, h, anchor="center"):
    iw, ih = fit_image(path, w, h)
    if anchor == "left":
        ix = x
    elif anchor == "right":
        ix = x + w - iw
    else:
        ix = x + (w - iw) / 2
    iy = y + (h - ih) / 2
    c.drawImage(str(path), ix, iy, iw, ih, preserveAspectRatio=True, mask="auto")


def set_fill(c, color):
    c.setFillColor(color)


def text(c, value, x, y, size=10, color=INK, font="Helvetica", align="left"):
    c.setFont(font, size)
    c.setFillColor(color)
    if align == "center":
        c.drawCentredString(x, y, value)
    elif align == "right":
        c.drawRightString(x, y, value)
    else:
        c.drawString(x, y, value)


def paragraph(c, value, x, y, width, size=10, leading=14, color=INK,
              font="Helvetica", max_lines=None):
    approx = max(12, int(width / (size * 0.52)))
    lines = []
    for raw in value.split("\n"):
        lines.extend(wrap(raw, approx) or [""])
    if max_lines:
        lines = lines[:max_lines]
    c.setFillColor(color)
    c.setFont(font, size)
    cy = y
    for line in lines:
        c.drawString(x, cy, line)
        cy -= leading
    return cy


def section_title(c, kicker, title, intro=None, dark=False):
    base = white if dark else INK
    muted = HexColor("#D6D9DB") if dark else MID
    text(c, kicker.upper(), M, H - 58, 8.5, YELLOW if dark else TEAL,
         "Helvetica-Bold")
    text(c, title, M, H - 88, 24, base, "Helvetica-Bold")
    if intro:
        paragraph(c, intro, M, H - 111, W - 2 * M, 10, 14, muted)


def footer(c, page, dark=False):
    color = HexColor("#B8BDC0") if dark else MID
    c.setStrokeColor(HexColor("#74787B") if dark else LINE)
    c.setLineWidth(0.6)
    c.line(M, 29, W - M, 29)
    text(c, "ADAPTIVE ELECTRICAL SOLUTIONS | BRAND GUIDE", M, 17, 6.8,
         color, "Helvetica-Bold")
    text(c, f"{page:02d}", W - M, 17, 7.5, color, "Helvetica-Bold", "right")


def card(c, x, y, w, h, fill=white, stroke=LINE, radius=8):
    c.setFillColor(fill)
    c.setStrokeColor(stroke)
    c.setLineWidth(0.7)
    c.roundRect(x, y, w, h, radius, fill=1, stroke=1)


def label(c, value, x, y, color=TEAL):
    text(c, value.upper(), x, y, 7.5, color, "Helvetica-Bold")


def bullet_list(c, items, x, y, width, size=9.3, leading=13.2, color=INK,
                bullet_color=TEAL, gap=7):
    cy = y
    for item in items:
        c.setFillColor(bullet_color)
        c.circle(x + 3, cy + 3, 2.2, fill=1, stroke=0)
        cy = paragraph(c, item, x + 13, cy, width - 13, size, leading, color)
        cy -= gap
    return cy


def page_cover(c):
    c.setFillColor(INK)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    c.setFillColor(YELLOW)
    c.rect(0, H - 17, W, 17, fill=1, stroke=0)
    c.setFillColor(TEAL)
    c.rect(0, 0, 14, H, fill=1, stroke=0)
    c.setFillColor(CYAN)
    c.rect(14, 0, 5, H, fill=1, stroke=0)

    draw_image_contain(c, LOGO_BRAND_REV, W - 250, H - 350, 185, 220)
    text(c, "BRAND STANDARDS", M + 12, 356, 9, CYAN, "Helvetica-Bold")
    text(c, "Adaptive Electrical", M + 12, 314, 31, white, "Helvetica-Bold")
    text(c, "Solutions", M + 12, 277, 31, white, "Helvetica-Bold")
    paragraph(
        c,
        "A practical visual and verbal guide for a trusted Central Queensland "
        "electrical business.",
        M + 12,
        239,
        320,
        12,
        17,
        HexColor("#D8DCDE"),
    )
    c.setFillColor(YELLOW)
    c.rect(M + 12, 189, 48, 4, fill=1, stroke=0)
    text(c, "VERSION 1.0 | JUNE 2026", M + 12, 160, 8, HexColor("#AEB4B7"),
         "Helvetica-Bold")
    text(c, "YEPPOON | ROCKHAMPTON | CENTRAL QUEENSLAND", M + 12, 143, 7.5,
         HexColor("#AEB4B7"), "Helvetica-Bold")


def page_foundation(c):
    section_title(
        c,
        "01 | Brand foundation",
        "Practical. Safe. Local.",
        "The brand should feel capable and modern without losing the direct, "
        "down-to-earth character customers expect from a local trade business.",
    )
    cards = [
        ("SAFE", "Compliance-led work, careful testing and dependable outcomes."),
        ("PRACTICAL", "Clear recommendations that suit the property and the job."),
        ("RESPONSIVE", "Straightforward communication and reliable follow-through."),
        ("NEAT", "Respectful work practices and tidy, considered finishes."),
    ]
    y = 505
    for i, (head, body) in enumerate(cards):
        x = M + (i % 2) * 257
        yy = y - (i // 2) * 127
        card(c, x, yy, 238, 102, LIGHT)
        c.setFillColor(YELLOW if i in (0, 3) else CYAN)
        c.rect(x, yy, 7, 102, fill=1, stroke=0)
        text(c, head, x + 23, yy + 66, 13, INK, "Helvetica-Bold")
        paragraph(c, body, x + 23, yy + 46, 194, 9.1, 13, MID)

    label(c, "Positioning statement", M, 285)
    paragraph(
        c,
        "Adaptive Electrical Solutions provides safe, compliant and practical "
        "electrical work for homeowners, rental properties, real estate agencies "
        "and small renovation projects across Yeppoon, Rockhampton and Central "
        "Queensland.",
        M,
        260,
        W - 2 * M,
        12,
        17,
        INK,
        "Helvetica-Bold",
    )
    c.setFillColor(INK)
    c.roundRect(M, 95, W - 2 * M, 105, 8, fill=1, stroke=0)
    label(c, "Brand promise", M + 22, 170, CYAN)
    paragraph(
        c,
        "Clear communication. Neat workmanship. Electrical solutions that are "
        "designed to work properly and stand up over time.",
        M + 22,
        145,
        W - 2 * M - 44,
        14,
        20,
        white,
        "Helvetica-Bold",
    )
    footer(c, 2)


def page_logo_suite(c):
    section_title(
        c,
        "02 | Logo system",
        "One mark, three useful formats",
        "Select the version that best fits the available space. Never rebuild, "
        "retype or rearrange the supplied artwork.",
    )
    specs = [
        ("Primary brand mark", LOGO_BRAND, "Best for avatars, badges, vehicle details and compact brand moments."),
        ("Centred lock-up", LOGO_CENTRED, "Best for centred headers, proposals, signage and balanced square layouts."),
        ("Left-aligned lock-up", LOGO_LEFT, "Best for website headers, email signatures and horizontal applications."),
    ]
    y_positions = [530, 325, 120]
    for idx, ((name, path, desc), y) in enumerate(zip(specs, y_positions)):
        card(c, M, y, W - 2 * M, 172, white)
        preview_fill = INK if idx == 0 else LIGHT
        c.setFillColor(preview_fill)
        c.roundRect(M + 12, y + 12, 205, 148, 6, fill=1, stroke=0)
        draw_image_contain(c, path, M + 27, y + 27, 175, 118)
        label(c, f"0{idx + 1}", M + 240, y + 130)
        text(c, name, M + 240, y + 101, 15, INK, "Helvetica-Bold")
        paragraph(c, desc, M + 240, y + 77, 265, 9.5, 14, MID)
        text(c, "Use original EPS/PDF for print; PNG for digital.", M + 240,
             y + 30, 8, TEAL, "Helvetica-Bold")
    footer(c, 3)


def page_logo_rules(c):
    section_title(
        c,
        "03 | Logo control",
        "Protect recognition",
        "Consistency matters more than novelty. Give the mark space, contrast and "
        "enough size to remain clear.",
    )
    card(c, M, 420, 305, 270, LIGHT)
    label(c, "Clear space", M + 18, 663)
    draw_image_contain(c, LOGO_BRAND, M + 78, 465, 175, 175)
    c.setStrokeColor(TEAL)
    c.setDash(4, 3)
    c.setLineWidth(1)
    c.rect(M + 57, 444, 217, 217, fill=0, stroke=1)
    c.setDash()
    text(c, "X", M + 45, 548, 10, TEAL, "Helvetica-Bold")
    paragraph(
        c,
        "Keep clear space around the logo equal to at least the width of the "
        "lower teal stroke. More space is preferred.",
        M + 18,
        438,
        268,
        8.8,
        12,
        MID,
    )

    card(c, M + 323, 420, W - 2 * M - 323, 270, white)
    label(c, "Minimum size", M + 341, 663)
    text(c, "Digital", M + 341, 623, 11, INK, "Helvetica-Bold")
    text(c, "Brand mark: 48 px wide", M + 341, 603, 9.2, MID)
    text(c, "Lock-ups: 160 px wide", M + 341, 586, 9.2, MID)
    text(c, "Print", M + 341, 543, 11, INK, "Helvetica-Bold")
    text(c, "Brand mark: 18 mm wide", M + 341, 523, 9.2, MID)
    text(c, "Lock-ups: 45 mm wide", M + 341, 506, 9.2, MID)
    c.setFillColor(YELLOW)
    c.roundRect(M + 341, 448, 167, 39, 5, fill=1, stroke=0)
    text(c, "WHEN IN DOUBT, GO LARGER", M + 424, 462, 7.7, INK,
         "Helvetica-Bold", "center")

    label(c, "Do not", M, 378)
    bad = [
        "Stretch, squash or rotate the logo.",
        "Change individual logo colours.",
        "Add shadows, outlines, glows or gradients.",
        "Place it over a busy image without a clear field.",
        "Crop the mark or separate its interlocking elements.",
        "Retype the business name as part of the lock-up.",
    ]
    bullet_list(c, bad, M, 352, W - 2 * M, 9.5, 13, INK, TEAL, 6)
    footer(c, 4)


def page_colour(c):
    section_title(
        c,
        "04 | Colour",
        "High visibility, used with restraint",
        "Charcoal and white form the foundation. Yellow creates urgency and "
        "recognition; teal and cyan provide a capable, contemporary counterpoint.",
    )
    swatches = [
        ("SAFETY YELLOW", "#FFF200", "RGB 255 / 242 / 0", YELLOW, INK),
        ("DEEP TEAL", "#2893A2", "RGB 40 / 147 / 162", TEAL, white),
        ("ELECTRIC CYAN", "#35C2D5", "RGB 53 / 194 / 213", CYAN, INK),
        ("CHARCOAL", "#58585A", "RGB 88 / 88 / 90", CHARCOAL, white),
    ]
    y = 556
    for i, (name, hex_code, rgb, fill, fg) in enumerate(swatches):
        x = M + (i % 2) * 257
        yy = y - (i // 2) * 158
        c.setFillColor(fill)
        c.roundRect(x, yy, 238, 132, 8, fill=1, stroke=0)
        text(c, name, x + 16, yy + 86, 11, fg, "Helvetica-Bold")
        text(c, hex_code, x + 16, yy + 57, 17, fg, "Helvetica-Bold")
        text(c, rgb, x + 16, yy + 30, 8, fg, "Helvetica")

    label(c, "Recommended balance", M, 343)
    bar_x, bar_y, bar_w, bar_h = M, 300, W - 2 * M, 28
    widths = [0.50, 0.25, 0.15, 0.10]
    colors = [white, CHARCOAL, TEAL, YELLOW]
    labels = ["50% WHITE", "25% CHARCOAL", "15% TEAL/CYAN", "10% YELLOW"]
    cx = bar_x
    for ratio, fill in zip(widths, colors):
        cw = bar_w * ratio
        c.setFillColor(fill)
        c.setStrokeColor(LINE)
        c.rect(cx, bar_y, cw, bar_h, fill=1, stroke=1)
        cx += cw
    ly = 270
    lx = M
    for label_text, fill in zip(labels, colors):
        c.setFillColor(fill)
        c.circle(lx + 5, ly + 3, 4, fill=1, stroke=0)
        text(c, label_text, lx + 15, ly, 7.1, MID, "Helvetica-Bold")
        lx += 126

    c.setFillColor(PALE_CYAN)
    c.roundRect(M, 95, W - 2 * M, 127, 8, fill=1, stroke=0)
    label(c, "Accessibility note", M + 20, 192)
    paragraph(
        c,
        "Do not use yellow or cyan for body copy on white. Use charcoal for "
        "reading text. White text is suitable on charcoal and deep teal; charcoal "
        "text is suitable on yellow. Check contrast for every website component.",
        M + 20,
        166,
        W - 2 * M - 40,
        10.3,
        15,
        INK,
    )
    footer(c, 5)


def page_typography(c):
    section_title(
        c,
        "05 | Typography",
        "Bold headings, effortless reading",
        "The logo lettering is artwork and should never be recreated with a font. "
        "For the website and documents, use this accessible digital type system.",
    )
    card(c, M, 469, W - 2 * M, 218, INK, INK)
    label(c, "Primary | Montserrat", M + 22, 653, CYAN)
    text(c, "CAPABLE & DIRECT", M + 22, 596, 31, white, "Helvetica-Bold")
    paragraph(
        c,
        "Use Montserrat Bold or SemiBold for page titles, navigation, service "
        "headings, buttons and short statements.",
        M + 22,
        552,
        455,
        10,
        15,
        HexColor("#D8DCDE"),
    )
    text(c, "Aa  Bb  Cc  0123456789", M + 22, 500, 15, YELLOW,
         "Helvetica-Bold")

    card(c, M, 232, W - 2 * M, 205, white)
    label(c, "Secondary | Source Sans 3", M + 22, 403)
    text(c, "Clear communication builds trust.", M + 22, 357, 21, INK,
         "Helvetica")
    paragraph(
        c,
        "Use Source Sans 3 Regular for paragraphs, captions, forms and practical "
        "service information. Use SemiBold for labels and supporting emphasis.",
        M + 22,
        325,
        455,
        10.2,
        15,
        MID,
    )
    text(c, "Aa  Bb  Cc  0123456789", M + 22, 266, 15, TEAL, "Helvetica")

    label(c, "Website scale", M, 194)
    scale = [
        ("H1", "42-56 px / 700"),
        ("H2", "30-38 px / 700"),
        ("H3", "22-26 px / 600"),
        ("BODY", "17-19 px / 400"),
        ("LABEL", "13-14 px / 600"),
    ]
    x = M
    for role, spec in scale:
        text(c, role, x, 156, 8, TEAL, "Helvetica-Bold")
        text(c, spec, x, 136, 8.4, INK, "Helvetica-Bold")
        x += 103
    text(c, "Fallback stack: Arial, Helvetica, sans-serif", M, 99, 8.6, MID,
         "Helvetica")
    footer(c, 6)


def page_imagery(c):
    section_title(
        c,
        "06 | Imagery",
        "Real work, clearly shown",
        "Photography should make competence visible. Prefer authentic local work "
        "over generic stock imagery or over-styled trade clichés.",
    )
    draw_image_contain(c, SOCIAL_HEADER, M, 414, W - 2 * M, 250)
    c.setFillColor(INK)
    c.rect(M, 414, W - 2 * M, 38, fill=1, stroke=0)
    text(c, "EXISTING SOCIAL HEADER | GOOD MATERIAL DETAIL + BRAND COLOUR",
         M + 14, 428, 7.2, white, "Helvetica-Bold")

    label(c, "Photography direction", M, 376)
    positives = [
        "Show clean switchboards, fittings, testing, fault finding and finished installations.",
        "Use natural light, neutral surfaces and uncluttered compositions.",
        "Include hands, tools and process details where they demonstrate care.",
        "Show recognisable Central Queensland homes and properties when appropriate.",
    ]
    bullet_list(c, positives, M, 352, 250, 8.7, 12.2, INK, TEAL, 5)

    label(c, "Avoid", M + 275, 376, CHARCOAL)
    avoids = [
        "Staged sparks, lightning effects or glowing cables.",
        "Over-saturated filters and heavy HDR processing.",
        "Messy worksites, unsafe practices or obscured PPE.",
        "Generic corporate handshake imagery.",
    ]
    bullet_list(c, avoids, M + 275, 352, 238, 8.7, 12.2, INK, YELLOW, 5)

    c.setFillColor(LIGHT)
    c.roundRect(M, 90, W - 2 * M, 78, 7, fill=1, stroke=0)
    label(c, "Graphic language", M + 18, 141)
    paragraph(
        c,
        "Use clean blocks, strong alignment, generous white space and occasional "
        "45-degree yellow corner cuts inspired by the existing letterhead. Avoid "
        "patterns, bevels, metallic textures and decorative electrical icons.",
        M + 18,
        120,
        W - 2 * M - 36,
        9.3,
        13,
        MID,
    )
    footer(c, 7)


def page_website(c):
    section_title(
        c,
        "07 | Website application",
        "Make trust easy to scan",
        "The website should quickly answer three questions: what you do, where you "
        "work, and why a customer should feel comfortable contacting you.",
    )
    card(c, M, 416, W - 2 * M, 278, white)
    c.setFillColor(INK)
    c.roundRect(M + 12, 428, W - 2 * M - 24, 244, 6, fill=1, stroke=0)
    draw_image_contain(c, LOGO_LEFT_REV, M + 28, 620, 190, 38, "left")
    text(c, "SERVICES", W - 225, 638, 7.5, white, "Helvetica-Bold")
    text(c, "SERVICE AREA", W - 160, 638, 7.5, white, "Helvetica-Bold")
    c.setFillColor(YELLOW)
    c.roundRect(W - 107, 623, 54, 27, 4, fill=1, stroke=0)
    text(c, "CALL", W - 80, 633, 7.5, INK, "Helvetica-Bold", "center")
    text(c, "Safe, practical electrical work", M + 28, 565, 22, white,
         "Helvetica-Bold")
    text(c, "for homes and rental properties.", M + 28, 537, 22, white,
         "Helvetica-Bold")
    paragraph(
        c,
        "Electrical maintenance, repairs, upgrades, air conditioning and "
        "renovation work across Yeppoon, Rockhampton and Central Queensland.",
        M + 28,
        506,
        330,
        9.2,
        13,
        HexColor("#D8DCDE"),
    )
    c.setFillColor(YELLOW)
    c.roundRect(M + 28, 452, 118, 32, 4, fill=1, stroke=0)
    text(c, "REQUEST A QUOTE", M + 87, 463, 7.2, INK, "Helvetica-Bold",
         "center")
    c.setStrokeColor(CYAN)
    c.roundRect(M + 155, 452, 102, 32, 4, fill=0, stroke=1)
    text(c, "VIEW SERVICES", M + 206, 463, 7.2, white, "Helvetica-Bold",
         "center")

    label(c, "Recommended page structure", M, 376)
    structure = [
        "Hero: clear service promise, location and one primary contact action.",
        "Service categories: maintenance, installations, safety, air conditioning and renovations.",
        "Trust: licence details, local service area, neat workmanship and clear communication.",
        "Proof: authentic project photos, concise testimonials and real estate capability.",
        "Contact: tap-to-call phone number, simple quote form and expected response guidance.",
    ]
    bullet_list(c, structure, M, 351, W - 2 * M, 9, 12.8, INK, TEAL, 6)
    footer(c, 8)


def page_voice(c):
    section_title(
        c,
        "08 | Voice and messaging",
        "Confident, clear and useful",
        "Write like an experienced electrician speaking plainly to a customer. "
        "Explain the work without jargon, hype or fear-based selling.",
    )
    columns = [
        ("SOUND LIKE", [
            "Direct and informed",
            "Calm and safety-conscious",
            "Helpful and specific",
            "Local and approachable",
        ], PALE_CYAN, TEAL),
        ("DO NOT SOUND LIKE", [
            "Overly technical",
            "Sales-heavy or urgent",
            "Casual to the point of vague",
            "Grandiose or corporate",
        ], LIGHT, CHARCOAL),
    ]
    for i, (head, items, fill, accent) in enumerate(columns):
        x = M + i * 257
        card(c, x, 463, 238, 226, fill)
        label(c, head, x + 18, 657, accent)
        bullet_list(c, items, x + 18, 620, 198, 10, 15, INK, accent, 9)

    label(c, "Core message", M, 421)
    c.setFillColor(INK)
    c.roundRect(M, 316, W - 2 * M, 84, 8, fill=1, stroke=0)
    paragraph(
        c,
        "Safe, compliant electrical solutions with clear communication and neat workmanship.",
        M + 22,
        366,
        W - 2 * M - 44,
        15,
        21,
        white,
        "Helvetica-Bold",
    )

    label(c, "Example website copy", M, 280)
    text(c, "Heading", M, 249, 8, TEAL, "Helvetica-Bold")
    text(c, "Electrical work done properly.", M + 92, 247, 15, INK,
         "Helvetica-Bold")
    text(c, "Support", M, 207, 8, TEAL, "Helvetica-Bold")
    paragraph(
        c,
        "From fault finding and everyday repairs to switchboard upgrades, split "
        "systems and renovation wiring, we provide practical electrical work for "
        "homes and rental properties across Yeppoon and Rockhampton.",
        M + 92,
        207,
        412,
        9.5,
        14,
        MID,
    )
    text(c, "Button", M, 137, 8, TEAL, "Helvetica-Bold")
    c.setFillColor(YELLOW)
    c.roundRect(M + 92, 116, 122, 34, 4, fill=1, stroke=0)
    text(c, "REQUEST A QUOTE", M + 153, 128, 7.5, INK, "Helvetica-Bold",
         "center")
    footer(c, 9)


def page_checklist(c):
    section_title(
        c,
        "09 | Quick reference",
        "A simple approval check",
        "Use this page before publishing website pages, social graphics, signs, "
        "documents or advertising.",
    )
    checks = [
        ("LOGO", "Correct supplied variant, enough clear space, no effects or distortion."),
        ("COLOUR", "Charcoal and white lead; yellow is an accent; teal supports hierarchy."),
        ("TYPE", "Bold, concise headings; readable body copy; no novelty or script fonts."),
        ("IMAGERY", "Authentic, tidy and safety-conscious; no staged electrical effects."),
        ("MESSAGE", "Service, location and next action are obvious within a few seconds."),
        ("TONE", "Clear and helpful, with practical detail and no exaggerated claims."),
    ]
    y = 635
    for i, (head, body) in enumerate(checks):
        yy = y - i * 83
        c.setFillColor(YELLOW if i % 2 == 0 else CYAN)
        c.circle(M + 14, yy + 5, 11, fill=1, stroke=0)
        text(c, "OK", M + 14, yy + 2, 6.2, INK, "Helvetica-Bold", "center")
        text(c, head, M + 40, yy + 12, 9, INK, "Helvetica-Bold")
        paragraph(c, body, M + 40, yy - 6, W - 2 * M - 40, 9.2, 13, MID)

    c.setFillColor(INK)
    c.roundRect(M, 75, W - 2 * M, 100, 8, fill=1, stroke=0)
    text(c, "ASSET RULE", M + 20, 145, 7.5, CYAN, "Helvetica-Bold")
    paragraph(
        c,
        "Use EPS or PDF artwork for professional print production. Use transparent "
        "PNG files for the website and digital documents. Keep a single approved "
        "master asset folder so old variants do not drift back into use.",
        M + 20,
        121,
        W - 2 * M - 40,
        8.8,
        12,
        white,
    )
    footer(c, 10)


def build():
    OUT.mkdir(parents=True, exist_ok=True)
    c = canvas.Canvas(str(PDF_PATH), pagesize=A4)
    c.setTitle("Adaptive Electrical Solutions Brand Guide")
    c.setAuthor("Adaptive Electrical Solutions")
    pages = [
        page_cover,
        page_foundation,
        page_logo_suite,
        page_logo_rules,
        page_colour,
        page_typography,
        page_imagery,
        page_website,
        page_voice,
        page_checklist,
    ]
    for index, page in enumerate(pages):
        page(c)
        if index != len(pages) - 1:
            c.showPage()
    c.save()
    print(PDF_PATH)


if __name__ == "__main__":
    build()
