import os
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import Paragraph
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
from PyPDF2 import PdfWriter, PdfReader


def create_background_pdf(filename):
    c = canvas.Canvas(filename, pagesize=A4)

    # Page 1 background
    bg_path_1 = os.path.join('img', 'bg-page-1.jpg')
    if os.path.exists(bg_path_1):
        c.drawImage(bg_path_1, 0, 0, width=A4[0], height=A4[1])
    c.showPage()

    # Page 2 background
    bg_path_2 = os.path.join('img', 'bg-page-2.jpg')
    if os.path.exists(bg_path_2):
        c.drawImage(bg_path_2, 0, 0, width=A4[0], height=A4[1])
    c.showPage()

    c.save()


def add_content_to_pdf(input_pdf, output_pdf):
    # Create a temporary PDF for content
    content_pdf_path = "temp_content.pdf"

    # Create the canvas
    c = canvas.Canvas(content_pdf_path, pagesize=A4)
    width, height = A4

    def add_text_at_position(text, left_margin, top_margin, style='Normal', align=TA_LEFT):
        styles = getSampleStyleSheet()
        base_style = styles[style]

        # Calculate available width
        available_width = width - left_margin - 1*cm  # 1 cm right margin

        # Create a custom style based on the base style
        custom_style = ParagraphStyle(
            'CustomStyle',
            parent=base_style,
            alignment=align
        )

        # Create the paragraph
        p = Paragraph(text, custom_style)

        # Calculate the height of the paragraph
        w, h = p.wrap(available_width, height)

        # Draw the paragraph
        p.drawOn(c, left_margin, height - top_margin - h)

    # Page 1 content
    add_text_at_position("Page 1 Content", 4*cm, 10*cm, style='Heading2')
    add_text_at_position(
        "Orang dengan preferensi modalitas visual cenderung memahami dan mengingat informasi "
        "lebih baik ketika disajikan dalam bentuk gambar, diagram, grafik, atau bentuk visual "
        "lainnya. Mereka mungkin merasa lebih mudah untuk belajar dari materi yang mencakup "
        "ilustrasi, peta konsep, atau presentasi yang kaya akan elemen visual. Mengingat dan "
        "memahami informasi melalui penglihatan membantu mereka mengasosiasikan ide-ide dan "
        "konsep dengan representasi visual yang kuat.",
        4*cm, 12*cm
    )

    # Add the bigfive-opening image
    img_path = os.path.join('img', 'bigfive-opening.jpg')
    if os.path.exists(img_path):
        img_width = width - 5*cm  # 4 cm left margin + 1 cm right margin
        img_height = img_width / 2  # Assuming 2:1 aspect ratio
        c.drawImage(img_path, 4*cm, height - 5*cm - img_height,
                    width=img_width, height=img_height)

    c.showPage()  # End of page 1

    # Page 2 content
    add_text_at_position("Page 2 Content", 4*cm, 10*cm, style='Heading2')
    add_text_at_position(
        "This is the content of the second page.", 4*cm, 12*cm)

    c.save()

    # Merge background and content PDFs
    background_pdf = PdfReader(open(input_pdf, "rb"))
    content_pdf = PdfReader(open(content_pdf_path, "rb"))
    output = PdfWriter()

    for i in range(min(len(background_pdf.pages), len(content_pdf.pages))):
        page = background_pdf.pages[i]
        page.merge_page(content_pdf.pages[i])
        output.add_page(page)

    with open(output_pdf, "wb") as output_stream:
        output.write(output_stream)

    # Close the PDF readers
    background_pdf.stream.close()
    content_pdf.stream.close()

    # Remove temporary content PDF
    os.remove(content_pdf_path)


def generate_pdf(filename):
    if not os.path.exists('pdf'):
        os.makedirs('pdf')

    background_pdf = os.path.join('pdf', 'background.pdf')
    output_pdf = os.path.join('pdf', filename)

    create_background_pdf(background_pdf)
    add_content_to_pdf(background_pdf, output_pdf)

    print(f"PDF generated: {filename}")


# Generate the PDF
generate_pdf('01-generatedfile.pdf')
