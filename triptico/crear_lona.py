from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

project = Path(__file__).resolve().parent.parent
out_dir = Path(__file__).resolve().parent
W, H = 2400, 2400
NAVY = (19, 37, 83)
WHITE = (255, 255, 255)
RED = (201, 54, 67)
PANEL = (10, 17, 35)
font_regular = "/System/Library/Fonts/Supplemental/Arial.ttf"
font_bold = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
def font(size, bold=False): return ImageFont.truetype(font_bold if bold else font_regular, size)
def contain(image, size):
    max_w, max_h = size
    ratio = min(max_w / image.width, max_h / image.height)
    return image.resize((round(image.width*ratio), round(image.height*ratio)), Image.Resampling.LANCZOS)

canvas = Image.new("RGB", (W, H), NAVY)
draw = ImageDraw.Draw(canvas)

# Brand header
logo = Image.open(project / "keystone-logo.png").convert("RGB")
logo.thumbnail((860, 290), Image.Resampling.LANCZOS)
canvas.paste(logo, (160, 105))
draw.text((1130, 135), "SOLUCIONES PARA", font=font(70, True), fill=WHITE)
draw.text((1130, 225), "OPERACIONES EXIGENTES", font=font(70, True), fill=WHITE)
draw.rectangle((1130, 350, 2110, 367), fill=RED)
draw.text((1130, 412), "SEGURIDAD  ·  MOVILIDAD  ·  TECNOLOGÍA", font=font(31), fill=WHITE)
draw.line((120, 535, W-120, 535), fill=(132, 149, 190), width=3)

# Four equal panels featuring complete, real source photos.
cards = [
    ("helicoptero_real_portada.png", "HELICÓPTEROS", "Movilidad y soporte para misión"),
    ("hero-slide-1.jpg", "VEHÍCULOS TÁCTICOS", "Plataformas para despliegue"),
    ("hero-slide-4.jpg", "EQUIPO ANTIMOTINES", "Protección para operación"),
    ("hero-slide-3.jpg", "SISTEMAS AÉREOS", "Vigilancia y tecnología"),
]
margin, gap, card_w, card_h = 150, 60, 1020, 750
positions = [(margin, 650), (margin + card_w + gap, 650), (margin, 1470), (margin + card_w + gap, 1470)]
for i, (filename, title, subtitle) in enumerate(cards):
    x, card_y = positions[i]
    draw.rectangle((x, card_y, x+card_w, card_y+card_h), fill=PANEL)
    local_assets = {"helicoptero_real_portada.png"}
    source = Image.open((out_dir if filename in local_assets else project) / filename).convert("RGB")
    shown = contain(source, (card_w-44, 550))
    canvas.paste(shown, (x+(card_w-shown.width)//2, card_y+28+(550-shown.height)//2))
    draw.rectangle((x, card_y+600, x+card_w, card_y+card_h), fill=(8, 15, 34))
    draw.text((x+38, card_y+630), title, font=font(39, True), fill=WHITE)
    draw.text((x+38, card_y+685), subtitle, font=font(29), fill=(205, 214, 235))

draw.text((150, 2290), "PRECISION. PERFORMANCE. PROGRESS.", font=font(30, True), fill=WHITE)
draw.text((W-590, 2290), "Keystone Dynamics", font=font(30), fill=WHITE)
canvas.save(out_dir / "lona_keystone_boceto_real.png", quality=95)
