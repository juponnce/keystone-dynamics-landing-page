from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

root = Path(__file__).resolve().parent.parent
out_dir = Path(__file__).resolve().parent

W, H = 1200, 1800
NAVY = (19, 37, 83)
WHITE = (255, 255, 255)
ACCENT = (201, 54, 67)

canvas = Image.new("RGB", (W, H), NAVY)

# Header: project logo, using the existing brand artwork without regenerating it.
logo = Image.open(root / "keystone-logo.png").convert("RGB")
logo.thumbnail((1020, 370), Image.Resampling.LANCZOS)
logo_x = (W - logo.width) // 2
canvas.paste(logo, (logo_x, 78))

# Narrow brand rule separates the header from the hero photo.
draw = ImageDraw.Draw(canvas)
draw.rectangle((90, 490, W - 90, 501), fill=ACCENT)

# Hero: real user-provided helicopter photograph, cropped to a cover-safe portrait frame.
photo = Image.open(out_dir / "helicoptero_real_portada.png").convert("RGB")
target = (W, 1040)
scale = max(target[0] / photo.width, target[1] / photo.height)
resized = photo.resize((round(photo.width * scale), round(photo.height * scale)), Image.Resampling.LANCZOS)
left = (resized.width - target[0]) // 2
top = max(0, (resized.height - target[1]) // 2 - 60)
photo = resized.crop((left, top, left + target[0], top + target[1]))
canvas.paste(photo, (0, 550))

# Subtle bottom veil reserves a quiet area for the cover title.
veil = Image.new("RGBA", (W, 420), (5, 8, 18, 0))
odraw = ImageDraw.Draw(veil)
for y in range(420):
    alpha = int(190 * (y / 419))
    odraw.line((0, y, W, y), fill=(5, 8, 18, alpha))
overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
overlay.alpha_composite(veil, (0, H - 420))
canvas = Image.alpha_composite(canvas.convert("RGBA"), overlay)

draw = ImageDraw.Draw(canvas)
font_large = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 28)
font_small = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 24)
draw.text((90, 1602), "PREPARADOS PARA LAS", fill=WHITE, font=font_small)
draw.text((90, 1642), "MISIONES MÁS EXIGENTES.", fill=WHITE, font=font_large)
draw.rectangle((90, 1690, 360, 1701), fill=ACCENT)
draw.text((90, 1725), "PRECISION. PERFORMANCE. PROGRESS.", fill=WHITE, font=font_small)

canvas.convert("RGB").save(out_dir / "portada_keystone_boceto_real.png", quality=95)
