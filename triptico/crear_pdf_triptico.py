from pathlib import Path
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader

base = Path(__file__).resolve().parent
output = base / "triptico_keystone_dynamics.pdf"
pages = [
    base / "triptico_exterior_keystone_boceto_real.png",
    base / "triptico_interior_keystone_boceto_real.png",
]

# Match the 3300 x 1800 source ratio on a 11 x 6 inch landscape page.
page_size = (792, 432)
pdf = canvas.Canvas(str(output), pagesize=page_size)
for image_path in pages:
    pdf.drawImage(ImageReader(str(image_path)), 0, 0, width=page_size[0], height=page_size[1])
    pdf.showPage()
pdf.save()
print(output)
