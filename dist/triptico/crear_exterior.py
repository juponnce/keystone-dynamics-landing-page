from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

project = Path(__file__).resolve().parent.parent
out_dir = Path(__file__).resolve().parent

W, H = 3300, 1800
PANEL = W // 3
NAVY = (19, 37, 83)
NAVY_DARK = (10, 20, 50)
PAPER = (246, 247, 251)
INK = (27, 35, 58)
MUTED = (101, 111, 134)
WHITE = (255, 255, 255)
RED = (201, 54, 67)

font_path = "/System/Library/Fonts/Supplemental/Arial.ttf"
bold_path = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
def font(size, bold=False):
    return ImageFont.truetype(bold_path if bold else font_path, size)

def fit_crop(image, size, focus_y=0.5):
    target_w, target_h = size
    scale = max(target_w / image.width, target_h / image.height)
    new = image.resize((round(image.width * scale), round(image.height * scale)), Image.Resampling.LANCZOS)
    left = (new.width - target_w) // 2
    top = round((new.height - target_h) * focus_y)
    top = max(0, min(top, new.height - target_h))
    return new.crop((left, top, left + target_w, top + target_h))

def draw_wrapped(draw, xy, text, width, font_obj, fill, spacing=10):
    words = text.split()
    lines, current = [], ""
    for word in words:
        candidate = f"{current} {word}".strip()
        if draw.textlength(candidate, font=font_obj) <= width:
            current = candidate
        else:
            lines.append(current)
            current = word
    if current:
        lines.append(current)
    x, y = xy
    for line in lines:
        draw.text((x, y), line, font=font_obj, fill=fill)
        y += font_obj.size + spacing
    return y

canvas = Image.new("RGB", (W, H), PAPER)
draw = ImageDraw.Draw(canvas)

# Panel 1 — inside flap
draw.rectangle((0, 0, PANEL, H), fill=NAVY)
draw.text((85, 120), "PERFIL", font=font(74, True), fill=WHITE)
draw.rectangle((85, 220, 330, 235), fill=RED)
body = "Una empresa especializada en el suministro de equipo y soluciones profesionales para los sectores militar, policial y de seguridad."
y = draw_wrapped(draw, (85, 335), body, PANEL - 170, font(43, True), WHITE, 18)
draw_wrapped(draw, (85, y + 105), "Compromiso con la excelencia, el desempeño y la seguridad para cumplir las necesidades de nuestros clientes.", PANEL - 170, font(34), (210, 216, 232), 18)
draw.line((85, 1510, PANEL - 85, 1510), fill=(151, 164, 197), width=3)
draw.text((85, 1570), "SOLUCIONES CONFIABLES", font=font(31, True), fill=WHITE)
draw.text((85, 1618), "PARA CADA MISIÓN.", font=font(31, True), fill=WHITE)

# Panel 2 — back cover / contact
draw.rectangle((PANEL, 0, PANEL * 2, H), fill=PAPER)
draw.text((PANEL + 85, 120), "CONTACTO", font=font(74, True), fill=INK)
draw.rectangle((PANEL + 85, 220, PANEL + 330, 235), fill=RED)
draw.text((PANEL + 85, 335), "Juan Jose Ponce", font=font(45, True), fill=INK)
draw.text((PANEL + 85, 405), "+52 5613 956385", font=font(40), fill=INK)
draw_wrapped(draw, (PANEL + 85, 535), "Para cotizaciones, disponibilidad, configuraciones especiales y fichas técnicas, solicita la información correspondiente al producto o proyecto.", PANEL - 170, font(34), INK, 16)
qr = Image.open(project / "qr-catalogo-2026-nuevo.png").convert("RGB")
qr.thumbnail((650, 650), Image.Resampling.LANCZOS)
qr_x = PANEL + (PANEL - qr.width) // 2
# Keep both text blocks fixed; center only the QR in the space between them.
canvas.paste(qr, (qr_x, 800))
draw.text((PANEL + 85, 1540), "ESCANEA PARA VER EL CATÁLOGO", font=font(27, True), fill=INK)
draw.text((PANEL + 85, 1590), "Keystone Dynamics", font=font(31), fill=INK)

# Panel 3 — front cover
cover_x = PANEL * 2
draw.rectangle((cover_x, 0, W, H), fill=NAVY)
logo = Image.open(project / "keystone-logo.png").convert("RGB")
logo.thumbnail((PANEL - 170, 360), Image.Resampling.LANCZOS)
canvas.paste(logo, (cover_x + (PANEL - logo.width) // 2, 90))
draw.rectangle((cover_x + 85, 475, W - 85, 490), fill=RED)
helicopter = Image.open(out_dir / "helicoptero_real_portada.png").convert("RGB")
# Keep the complete real photograph visible instead of aggressively cropping it.
hero = helicopter.copy()
hero.thumbnail((PANEL - 80, 690), Image.Resampling.LANCZOS)
hero_x = cover_x + (PANEL - hero.width) // 2
canvas.paste(hero, (hero_x, 610))
veil = Image.new("RGBA", (PANEL, 390), (0, 0, 0, 0))
vdraw = ImageDraw.Draw(veil)
for yy in range(390):
    vdraw.line((0, yy, PANEL, yy), fill=(7, 12, 29, int(210 * yy / 389)))
overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
overlay.alpha_composite(veil, (cover_x, H - 390))
canvas = Image.alpha_composite(canvas.convert("RGBA"), overlay).convert("RGB")
draw = ImageDraw.Draw(canvas)
draw.text((cover_x + 85, 1510), "PREPARADOS PARA LAS", font=font(37), fill=WHITE)
draw.text((cover_x + 85, 1570), "MISIONES MÁS EXIGENTES.", font=font(49, True), fill=WHITE)
draw.rectangle((cover_x + 85, 1650, cover_x + 420, 1664), fill=RED)
draw.text((cover_x + 85, 1700), "PRECISION. PERFORMANCE. PROGRESS.", font=font(27), fill=WHITE)

# Fine fold guides are intentionally visible in the concept sheet only.
draw.line((PANEL, 0, PANEL, H), fill=(184, 190, 205), width=3)
draw.line((PANEL * 2, 0, PANEL * 2, H), fill=(184, 190, 205), width=3)
canvas.save(out_dir / "triptico_exterior_keystone_boceto_real.png", quality=95)
