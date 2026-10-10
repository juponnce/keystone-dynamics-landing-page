from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

project = Path(__file__).resolve().parent.parent
out_dir = Path(__file__).resolve().parent
W, H = 3300, 1800
PANEL = W // 3
NAVY = (19, 37, 83)
PAPER = (246, 247, 251)
INK = (27, 35, 58)
MUTED = (101, 111, 134)
WHITE = (255, 255, 255)
RED = (201, 54, 67)
font_path = "/System/Library/Fonts/Supplemental/Arial.ttf"
bold_path = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
def font(size, bold=False): return ImageFont.truetype(bold_path if bold else font_path, size)
def crop(image, size):
    w, h = size; scale = max(w / image.width, h / image.height)
    image = image.resize((round(image.width * scale), round(image.height * scale)), Image.Resampling.LANCZOS)
    left, top = (image.width-w)//2, (image.height-h)//2
    return image.crop((left, top, left+w, top+h))
def contain(image, size):
    w, h = size
    scale = min(w / image.width, h / image.height)
    return image.resize((round(image.width * scale), round(image.height * scale)), Image.Resampling.LANCZOS)
def wrap(draw, x, y, text, max_width, f, fill, gap=12):
    words, line = text.split(), ""
    for word in words:
        candidate = f"{line} {word}".strip()
        if draw.textlength(candidate, font=f) <= max_width: line = candidate
        else:
            draw.text((x,y), line, font=f, fill=fill); y += f.size + gap; line = word
    if line: draw.text((x,y), line, font=f, fill=fill); y += f.size + gap
    return y

canvas = Image.new("RGB", (W, H), PAPER); draw = ImageDraw.Draw(canvas)

# Panel 1: who we are
draw.text((85,120), "QUIÉNES SOMOS", font=font(67, True), fill=INK)
draw.rectangle((85,220,330,235), fill=RED)
y = wrap(draw, 85, 350, "Keystone Dynamics suministra equipamiento, sistemas y soluciones profesionales para los sectores de seguridad, defensa y operación especializada.", PANEL-170, font(43, True), INK, 17)
wrap(draw, 85, y+85, "Trabajamos con productos confiables, atención profesional y configuraciones alineadas con las necesidades de cada proyecto.", PANEL-170, font(34), INK, 18)
draw.line((85,1390,PANEL-85,1390), fill=(184,190,205), width=3)
draw.text((85,1460), "SEGURIDAD · MOVILIDAD · DESEMPEÑO", font=font(28, True), fill=INK)
draw.text((85,1520), "Soluciones para operaciones exigentes.", font=font(33), fill=INK)

# Panel 2: actual solutions and photographs
x = PANEL
draw.rectangle((x,0,x+PANEL,H), fill=WHITE)
draw.text((x+85,120), "SOLUCIONES", font=font(74, True), fill=INK)
draw.rectangle((x+85,220,x+330,235), fill=RED)
def place_photo(image_name, frame, title, description, description_size=25):
    fx, fy, fw, fh = frame
    draw.rectangle((fx, fy, fx+fw, fy+fh), fill=(237, 240, 245))
    photo = contain(Image.open(project / image_name).convert("RGB"), (fw, fh))
    canvas.paste(photo, (fx + (fw-photo.width)//2, fy + (fh-photo.height)//2))
    draw.text((fx, fy+fh+22), title, font=font(30, True), fill=INK)
    wrap(draw, fx, fy+fh+66, description, fw, font(description_size), INK, 6)

# Restore the original vertical, step-by-step sequence: three full photographs, never cropped.
frame_w = PANEL - 170
place_photo("hero-slide-4.jpg", (x+85, 330, frame_w, 270), "PROTECCIÓN Y EQUIPO", "Protección antimotín, equipo táctico, óptica y visión, sistemas médicos, iluminación, sistemas aéreos, infraestructura, almacenamiento y materiales para operación especializada.", 25)
place_photo("hero-slide-1.jpg", (x+85, 835, frame_w, 270), "MOVILIDAD TÁCTICA", "Vehículo blindado táctico · UH-60 Black Hawk.", 25)
place_photo("chaleco-pelon-min.jpg", (x+85, 1240, frame_w, 270), "EQUIPO TÁCTICO BALÍSTICO", "Chaleco III-A · Placa III · Placa IV · Casco FAST nivel III-A · Casco MICH nivel III-A · Casco PASGT nivel III-A · Escudo balístico nivel III-A · Escudo balístico nivel III · Escudo balístico nivel IV.", 25)

# Panel 3: reasons
x = PANEL * 2
draw.rectangle((x,0,x+PANEL,H), fill=NAVY)
draw.text((x+85,120), "POR QUÉ", font=font(66, True), fill=WHITE)
draw.text((x+85,205), "ELEGIRNOS", font=font(66, True), fill=WHITE)
draw.rectangle((x+85,310,x+330,325), fill=RED)
items = [
    ("CALIDAD", "Equipamiento seleccionado para operaciones exigentes."),
    ("CONFIABILIDAD", "Soluciones orientadas al desempeño y la continuidad."),
    ("ATENCIÓN PROFESIONAL", "Acompañamiento para cada necesidad y proyecto."),
    ("SOLUCIONES A MEDIDA", "Configuraciones según la misión y el entorno."),
]
y = 440
for title, text in items:
    draw.ellipse((x+85,y+8,x+120,y+43), fill=RED)
    draw.text((x+150,y), title, font=font(34, True), fill=WHITE)
    y = wrap(draw, x+150, y+55, text, PANEL-235, font(28), (210,216,232), 12) + 48
draw.line((x+85,1450,W-85,1450), fill=(151,164,197), width=3)
wrap(draw, x+85, 1515, "Hablemos de la capacidad que necesita su organización.", PANEL-170, font(40, True), WHITE, 12)

draw.line((PANEL,0,PANEL,H), fill=(184,190,205), width=3)
draw.line((PANEL*2,0,PANEL*2,H), fill=(184,190,205), width=3)
canvas.save(out_dir / "triptico_interior_keystone_boceto_real.png", quality=95)
