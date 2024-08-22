import os
from PyPDF2 import PdfReader, PdfWriter
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
from io import BytesIO
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import plotly.graph_objects as go

# Register fonts
pdfmetrics.registerFont(TTFont('Arial', 'Arial.ttf'))
pdfmetrics.registerFont(TTFont('Arial-Bold', 'Arial-Bold.ttf'))

# Global variables for chart dimensions
CHART_WIDTH = 500
CHART_HEIGHT = 700
CHART_PDF_WIDTH = 6 * cm
CHART_PDF_HEIGHT = 8.4 * cm


def create_riasec_chart(data):
    labels = ['    R   ', 'I   ', 'A   ', 'S   ', 'E   ', 'C   ']
    values = [data['Realistic'], data['Investigative'], data['Artistic'],
              data['Social'], data['Enterprising'], data['Conventional']]

    fig = go.Figure(go.Bar(
        y=labels[::-1],
        x=values[::-1],
        orientation='h',
        text=values[::-1],
        textposition='inside',
        insidetextfont=dict(size=16),
        textangle=0,
        marker=dict(color='rgb(158,202,225)', line=dict(
            color='rgb(8,48,107)', width=1.5)),
        opacity=0.6
    ))

    fig.update_layout(
        width=CHART_WIDTH,
        height=CHART_HEIGHT,
        margin=dict(l=80, r=20, t=20, b=20),
        yaxis=dict(showticklabels=False, showgrid=False, zeroline=False),
        xaxis=dict(showticklabels=False, showgrid=False, zeroline=False),
    )

    for i, label in enumerate(labels[::-1]):
        fig.add_annotation(
            x=-0.2,
            y=i,
            text=label,
            showarrow=False,
            font=dict(size=24),
            xanchor='right',
            yanchor='middle'
        )

    return fig


def save_chart(fig, filename):
    if not os.path.exists('img'):
        os.makedirs('img')
    fig.write_image(f"img/{filename}.png")


def extract_page(input_path, page_number):
    reader = PdfReader(input_path)
    writer = PdfWriter()
    if page_number <= len(reader.pages):
        writer.add_page(reader.pages[page_number - 1])
    output = BytesIO()
    writer.write(output)
    output.seek(0)
    return output


def append_pdf(input_pdf, output_pdf):
    reader = PdfReader(input_pdf)
    writer = PdfWriter()

    if os.path.exists(output_pdf):
        existing_pdf = PdfReader(output_pdf)
        for page in existing_pdf.pages:
            writer.add_page(page)

    for page in reader.pages:
        writer.add_page(page)

    with open(output_pdf, 'wb') as output_file:
        writer.write(output_file)


def add_content_to_pdf(input_pdf, output_pdf, nama_user, nama_sekolah, riasec_data, upper_image, lower_image):
    packet = BytesIO()
    can = canvas.Canvas(packet, pagesize=A4)
    width, height = A4

    # First page
    can.setFont("Arial-Bold", 24)
    can.drawString(width/2 - 2*cm, height - 5.5*cm, nama_user.upper())
    can.setFont("Arial", 14)
    can.drawString(width/2 - 2*cm, height - 6.5*cm, nama_sekolah)

    # Add RIASEC chart
    chart = create_riasec_chart(riasec_data)
    save_chart(chart, "riasec_chart")
    can.drawImage("img/riasec_chart.png", 1.3*cm, height - 18*cm,
                  width=CHART_PDF_WIDTH, height=CHART_PDF_HEIGHT)

    can.showPage()

    # Second page
    image_width = width * 0.85
    image_height = height * 0.45

    can.drawImage(upper_image, width*0.15 - 2 * cm, height*0.5,
                  width=image_width, height=image_height)
    can.drawImage(lower_image, width*0.15 - 2 * cm, height*0.05 - 0.5 * cm,
                  width=image_width, height=image_height)
    can.drawImage("img/riasec/header-prioritas-pertama.jpg",
                  11 * cm, 27.2 * cm, width=300, height=30)
    can.drawImage("img/riasec/header-prioritas-kedua.jpg",
                  11 * cm, 13.5 * cm, width=300, height=30)

    can.setFont("Arial", 12)
    can.drawString(width - 4*cm, height - 1*cm, nama_user)

    can.save()
    packet.seek(0)

    new_pdf = PdfReader(packet)
    existing_pdf = PdfReader(input_pdf)
    output = PdfWriter()

    for i in range(len(existing_pdf.pages)):
        page = existing_pdf.pages[i]
        page.merge_page(new_pdf.pages[i])
        output.add_page(page)

    with open(output_pdf, "wb") as outputStream:
        output.write(outputStream)


def main():
    if not os.path.exists('output'):
        os.makedirs('output')

    output_pdf = 'output/report-titian-bakat.pdf'

    # Step 1: Extract 10th page from the first PDF
    first_pdf = 'pdf/TitianBakat-Report-RIASEC-Page1.pdf'
    page_10 = extract_page(first_pdf, 10)
    with open(output_pdf, 'wb') as f:
        f.write(page_10.getvalue())

    # Step 2: Append the second PDF
    second_pdf = 'pdf/TitianBakat-Report-RIASEC-Page2.pdf'
    append_pdf(second_pdf, output_pdf)

    # Step 3, 4 & 5: Add content to the PDF
    nama_user = "Mirriam Eka"
    nama_sekolah = "SMAN 15 Surabaya"
    riasec_career_data = {
        "Realistic": 73, "Investigative": 30, "Artistic": 23,
        "Social": 13, "Enterprising": 47, "Conventional": 57
    }
    upper_image = 'img/riasec/artistik-RIASEC.jpg'
    lower_image = 'img/riasec/enterprising-RIASEC.jpg'

    add_content_to_pdf(output_pdf, output_pdf, nama_user,
                       nama_sekolah, riasec_career_data, upper_image, lower_image)

    print(f"PDF generated: {output_pdf}")


if __name__ == "__main__":
    main()
