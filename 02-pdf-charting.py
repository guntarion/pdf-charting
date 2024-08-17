# pip install plotly kaleido reportlab

import plotly.graph_objects as go
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas
import os

# Global variables for chart dimensions
CHART_WIDTH = 700  # in pixels, for high-resolution chart creation
CHART_PDF_WIDTH = 10 * cm  # width when placing in PDF


def create_big_five_chart(data):
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=list(data.values()),
        theta=list(data.keys()),
        fill='toself'
    ))
    fig.update_layout(
        polar=dict(radialaxis=dict(
            visible=True, range=[0, max(data.values())])),
        showlegend=False,
        title="Big Five Personality",
        width=CHART_WIDTH,
        height=CHART_WIDTH  # Make it square
    )
    return fig


def create_learning_modality_chart(data):
    fig = go.Figure(go.Bar(
        x=list(data.keys()),
        y=list(data.values()),
        text=list(data.values()),
        textposition='auto'
    ))
    fig.update_traces(marker_color='rgb(158,202,225)', marker_line_color='rgb(8,48,107)',
                      marker_line_width=1.5, opacity=0.6)
    fig.update_layout(
        title="Learning Modality Preference",
        xaxis_title="Modality Type",
        yaxis_title="Score",
        width=CHART_WIDTH,
        height=int(CHART_WIDTH * 0.6)  # Adjust height as needed
    )
    return fig


def create_multiple_intelligence_chart(data):
    fig = go.Figure(go.Bar(
        x=list(data.keys()),
        y=list(data.values()),
        text=list(data.values()),
        textposition='auto'
    ))
    fig.update_traces(marker_color='rgb(158,202,225)', marker_line_color='rgb(8,48,107)',
                      marker_line_width=1.5, opacity=0.6)
    fig.update_layout(
        title="Multiple Intelligences Scores",
        xaxis_title="Intelligence Type",
        yaxis_title="Score",
        width=CHART_WIDTH,
        height=int(CHART_WIDTH * 0.8)  # Adjust height as needed
    )
    return fig


def save_chart(fig, filename):
    if not os.path.exists('img'):
        os.makedirs('img')
    fig.write_image(f"img/{filename}.png")


def create_pdf(filename):
    c = canvas.Canvas(filename, pagesize=A4)

    # First page
    c.drawImage("img/big_five_personality.png", 2*cm,
                A4[1] - 5*cm - CHART_PDF_WIDTH, width=CHART_PDF_WIDTH, height=CHART_PDF_WIDTH, preserveAspectRatio=True)
    c.drawImage("img/learning_modality.png", 2*cm, A4[1] - 15*cm - CHART_PDF_WIDTH *
                0.6, width=CHART_PDF_WIDTH, height=CHART_PDF_WIDTH*0.6, preserveAspectRatio=True)

    c.showPage()  # Move to the next page

    # Second page
    c.drawImage("img/multiple_intelligence.png", 2*cm, A4[1] - 3*cm - CHART_PDF_WIDTH *
                0.8, width=CHART_PDF_WIDTH, height=CHART_PDF_WIDTH*0.8, preserveAspectRatio=True)

    c.save()


# Example data (replace with your MongoDB data retrieval logic)
big_five_personality = {
    "Extroversion": 63, "Agreeableness": 40, "Openness To Experience": 23,
    "Conscientiousness": 13, "Emotional Stability": 27
}

learning_modality = {
    "Visual": 49, "Auditory": 47, "Kinesthetic": 35
}

multiple_intelligences = {
    "Logika": 16, "Linguistik": 57, "Spasial": 30, "Musikal": 45,
    "Naturalis": 36, "Interpersonal": 21, "Intrapersonal": 32, "Kinestetik": 18
}

# Generate and save charts
save_chart(create_big_five_chart(big_five_personality), "big_five_personality")
save_chart(create_learning_modality_chart(
    learning_modality), "learning_modality")
save_chart(create_multiple_intelligence_chart(
    multiple_intelligences), "multiple_intelligence")

# Generate PDF
if not os.path.exists('pdf'):
    os.makedirs('pdf')
create_pdf("pdf/02-pdf-charting.pdf")

print("PDF generated: pdf/02-pdf-charting.pdf")
