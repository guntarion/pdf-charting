# pip install plotly kaleido reportlab

import plotly.graph_objects as go
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas
import os

# Global variables for chart dimensions
CHART_WIDTH = 500  # in pixels, for high-resolution chart creation
CHART_HEIGHT = 700  # in pixels, for high-resolution chart creation
CHART_PDF_WIDTH = 10 * cm  # width when placing in PDF
CHART_PDF_HEIGHT = 14 * cm  # height when placing in PDF


def create_riasec_chart(data):
    labels = ['    R   ', 'I   ', 'A   ', 'S   ', 'E   ', 'C   ']
    values = [data['Realistic'], data['Investigative'], data['Artistic'],
              data['Social'], data['Enterprising'], data['Conventional']]

    fig = go.Figure(go.Bar(
        y=labels[::-1],  # Reverse the order to have R at the top
        x=values[::-1],  # Reverse the order to match the labels
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
        margin=dict(l=80, r=20, t=20, b=20),  # Increase left margin for labels
        yaxis=dict(
            showticklabels=False,
            showgrid=False,
            zeroline=False,
        ),
        xaxis=dict(
            showticklabels=False,
            showgrid=False,
            zeroline=False,
        ),
    )

    # Add text annotations for R, I, A, S, E, C
    for i, label in enumerate(labels[::-1]):
        fig.add_annotation(
            x=-0.2,  # Adjust this value to position the text
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


def create_pdf(filename):
    c = canvas.Canvas(filename, pagesize=A4)

    # First page
    c.drawImage("img/riasec_career.png", 2*cm,
                A4[1] - 3*cm - CHART_PDF_HEIGHT, width=CHART_PDF_WIDTH, height=CHART_PDF_HEIGHT, preserveAspectRatio=True)

    c.save()


# Example data (replace with your MongoDB data retrieval logic)
riasec_career_data = {
    "Realistic": 73, "Investigative": 30, "Artistic": 23,
    "Social": 13, "Enterprising": 47, "Conventional": 57
}

# Generate and save charts
save_chart(create_riasec_chart(riasec_career_data), "riasec_career")

# Generate PDF
if not os.path.exists('pdf'):
    os.makedirs('pdf')
create_pdf("pdf/03-pdf-charting-riasec.pdf")

print("PDF generated: pdf/03-pdf-charting-riasec.pdf")
