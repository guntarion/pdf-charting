import os
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Paragraph, Image, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet
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

    margin = 1*cm
    doc = SimpleDocTemplate(
        content_pdf_path,
        pagesize=A4,
        rightMargin=margin,
        leftMargin=margin,
        topMargin=margin,
        bottomMargin=margin
    )

    available_width = A4[0] - 2*margin

    styles = getSampleStyleSheet()
    h2_style = styles['Heading2']
    normal_style = styles['Normal']

    content = []

    # Page 1 content
    content.append(Paragraph("Page 1 Content", h2_style))

    # Add the bigfive-opening image
    img_path = os.path.join('img', 'bigfive-opening.jpg')
    if os.path.exists(img_path):
        img = Image(img_path, width=available_width,
                    height=available_width/2)  # Assuming 2:1 aspect ratio
        img.hAlign = 'CENTER'
        content.append(img)

    content.append(Spacer(1, 12))
    content.append(Paragraph("Visual", h2_style))
    content.append(Paragraph(
        "Orang dengan preferensi modalitas visual cenderung memahami dan mengingat informasi "
        "lebih baik ketika disajikan dalam bentuk gambar, diagram, grafik, atau bentuk visual "
        "lainnya. Mereka mungkin merasa lebih mudah untuk belajar dari materi yang mencakup "
        "ilustrasi, peta konsep, atau presentasi yang kaya akan elemen visual. Mengingat dan "
        "memahami informasi melalui penglihatan membantu mereka mengasosiasikan ide-ide dan "
        "konsep dengan representasi visual yang kuat.",
        normal_style
    ))

    # Add a page break before page 2 content
    content.append(PageBreak())

    # Page 2 content
    content.append(Paragraph("Page 2 Content", h2_style))
    content.append(Paragraph("Second Page", h2_style))
    content.append(
        Paragraph("This is the content of the second page.", normal_style))

    # Build the content PDF
    doc.build(content)

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
