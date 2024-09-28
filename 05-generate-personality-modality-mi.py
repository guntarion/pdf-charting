import os
from PyPDF2 import PdfReader, PdfWriter
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
from io import BytesIO
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import plotly.graph_objects as go
from PIL import Image
from reportlab.lib.utils import ImageReader
from reportlab.platypus import Paragraph
from reportlab.lib.styles import getSampleStyleSheet

# Register fonts
pdfmetrics.registerFont(TTFont('Arial', 'Arial.ttf'))
pdfmetrics.registerFont(TTFont('Arial-Bold', 'Arial-Bold.ttf'))

# Global variables for chart dimensions
CHART_WIDTH = 500
CHART_HEIGHT = 700
CHART_PDF_WIDTH = 6 * cm
CHART_PDF_HEIGHT = 8.4 * cm

# Extroversion
narasiExtroversionTinggi = "Individu dengan skor tinggi pada dimensi ini umumnya ramah, mudah bergaul, dan komunikatif. Mereka menikmati keramaian dan aktif mencari interaksi sosial. Sering kali, mereka dipersepsikan sebagai orang yang energik, antusias, dan percaya diri. Mereka cenderung terlibat dalam aktivitas yang menantang atau menyenangkan, seperti menghadiri pesta atau mencari pengalaman baru yang menarik."
narasiExtroversionSedang = "Individu dengan skor sedang pada dimensi ini menunjukkan keseimbangan antara sifat ekstrovert dan introvert. Mereka dapat menikmati interaksi sosial, namun juga menghargai waktu sendiri. Dalam situasi sosial, mereka mampu berkomunikasi dengan baik, tetapi tidak selalu menjadi pusat perhatian. Mereka fleksibel dalam beradaptasi dengan berbagai lingkungan sosial, nyaman baik dalam kelompok kecil maupun besar."
narasiExtroversionRendah = "Individu dengan skor rendah pada dimensi ini cenderung lebih introvert dan pendiam. Mereka lebih nyaman menghabiskan waktu sendiri atau dalam kelompok kecil yang akrab. Dalam situasi sosial yang lebih besar, mereka mungkin merasa kurang nyaman atau kewalahan. Mereka umumnya lebih reflektif, hati-hati dalam berinteraksi, dan cenderung mempertimbangkan sesuatu dengan matang sebelum berbicara atau bertindak."
# Emotional Stability
narasiEmotionalStabilityTinggi = "Individu dengan skor tinggi pada stabilitas emosional umumnya tangguh secara emosional dan tenang. Mereka jarang mengalami emosi negatif dan mampu mengatasi stres dengan baik. Mereka cenderung merasakan lebih banyak emosi positif seperti kebahagiaan dan kepuasan. Kemampuan mereka dalam mengelola emosi membantu mereka menghadapi tantangan hidup dengan lebih efektif."
narasiEmotionalStabilitySedang = "Individu dengan skor sedang pada stabilitas emosional menunjukkan keseimbangan dalam respon emosional mereka. Mereka dapat mengalami berbagai emosi, baik positif maupun negatif, namun umumnya mampu mengelolanya dengan cukup baik. Dalam menghadapi stres, mereka mungkin kadang merasa tertekan, tetapi biasanya dapat pulih dan beradaptasi seiring waktu."
narasiEmotionalStabilityRendah = "Individu dengan skor rendah pada stabilitas emosional mungkin lebih sensitif terhadap perubahan emosi. Mereka cenderung mengalami berbagai perasaan dengan intensitas yang lebih tinggi. Dalam situasi yang menantang, mereka mungkin memerlukan waktu lebih lama untuk menyesuaikan diri. Kemampuan mereka untuk merasakan berbagai emosi dapat membuat mereka lebih empatik."
# Agreeableness
narasiAgreeablenessTinggi = "Individu dengan skor tinggi pada Agreeableness umumnya hangat, ramah, dan perhatian. Mereka cenderung bekerja sama dengan baik dan termotivasi untuk menjaga hubungan sosial yang harmonis. Mereka sering menunjukkan empati yang kuat dan kepedulian terhadap kesejahteraan orang lain. Kemampuan mereka dalam berinteraksi sosial dapat membantu dalam berbagai situasi interpersonal."
narasiAgreeablenessSedang = "Individu dengan skor sedang pada Agreeableness menunjukkan keseimbangan antara kerja sama dan ketegasan. Mereka dapat berempati dan bekerja sama dengan orang lain, namun juga mampu mempertahankan pendapat mereka sendiri. Dalam interaksi sosial, mereka fleksibel, dapat menyesuaikan pendekatan mereka tergantung pada situasi dan orang yang mereka hadapi."
narasiAgreeablenessRendah = "Individu dengan skor rendah pada Agreeableness cenderung lebih mandiri dalam pemikiran dan tindakan. Mereka mungkin lebih fokus pada tujuan pribadi dan tidak ragu untuk menyatakan pendapat mereka. Dalam situasi kerja sama, mereka mungkin lebih suka mengambil pendekatan yang langsung dan berorientasi pada tugas daripada fokus pada harmoni interpersonal."
# Conscientiousness
narasiConscientiousnessTinggi = "Individu dengan skor tinggi pada Conscientiousness umumnya dapat diandalkan, pekerja keras, dan efisien. Mereka cenderung terorganisir dengan baik, bertanggung jawab, dan termotivasi untuk mencapai tujuan. Mereka sering menunjukkan disiplin diri yang kuat dan ketekunan dalam menghadapi tantangan. Kemampuan mereka dalam perencanaan dan pelaksanaan tugas dapat sangat bermanfaat dalam berbagai aspek kehidupan."
narasiConscientiousnessSedang = "Individu dengan skor sedang pada Conscientiousness menunjukkan keseimbangan antara fleksibilitas dan struktur. Mereka mampu mengorganisir dan menyelesaikan tugas dengan baik, namun juga dapat beradaptasi dengan perubahan. Mereka biasanya memiliki tujuan yang jelas, tetapi tidak kaku dalam pencapaiannya. Pendekatan mereka terhadap pekerjaan dan tanggung jawab cenderung seimbang."
narasiConscientiousnessRendah = "Individu dengan skor rendah pada Conscientiousness cenderung lebih fleksibel dan spontan dalam pendekatan mereka terhadap kehidupan. Mereka mungkin lebih nyaman dengan lingkungan yang tidak terstruktur dan dapat beradaptasi cepat dengan perubahan. Pendekatan mereka yang lebih santai dapat membuat mereka kreatif dalam menyelesaikan masalah dan menanggapi situasi yang tidak terduga."
# OpennessToExperience
narasiOpennessToExperienceTinggi = "Individu dengan skor tinggi pada keterbukaan terhadap pengalaman umumnya imajinatif, penuh rasa ingin tahu, dan terbuka terhadap ide-ide baru. Mereka cenderung tertarik secara intelektual dan menikmati eksplorasi konsep serta pengalaman baru. Mereka sering menunjukkan preferensi terhadap kreativitas dan estetika. Pendekatan mereka yang inovatif dapat sangat bermanfaat dalam situasi yang membutuhkan pemikiran out-of-the-box."
narasiOpennessToExperienceSedang = "Individu dengan skor sedang pada keterbukaan terhadap pengalaman menunjukkan keseimbangan antara tradisi dan inovasi. Mereka dapat menghargai metode yang telah terbukti, namun juga terbuka untuk mencoba pendekatan baru. Dalam menghadapi ide-ide baru, mereka cenderung berhati-hati namun tidak menolak. Mereka mampu beradaptasi dengan perubahan sambil mempertahankan stabilitas."
narasiOpennessToExperienceRendah = "Individu dengan skor rendah pada keterbukaan terhadap pengalaman cenderung lebih praktis dan berorientasi pada realitas. Mereka mungkin lebih nyaman dengan hal-hal yang familiar dan dapat diandalkan. Pendekatan mereka yang konsisten dan fokus pada hal-hal konkret dapat sangat bermanfaat dalam situasi yang membutuhkan stabilitas dan efisiensi dalam pelaksanaan tugas-tugas rutin."

narasi_mi_pengantar = "Kecerdasan majemuk tidaklah dimaksudkan untuk berdiri sendiri, melainkan bekerja dalam sinergi dengan kecerdasan lainnya. Dalam kehidupan nyata, seseorang dapat mencapai prestasi yang optimal ketika berbagai tipe kecerdasan saling mendukung dan melengkapi. Setiap individu memiliki kekuatan unik dalam kecerdasan tertentu, namun untuk mencapai potensi diri yang maksimal, penting untuk mengoptimalkan dan mendayagunakan setidaknya tiga tipe kecerdasan terkuat yang dimiliki."
narasi_mi_musikal = "Kecerdasan Musikal adalah kemampuan seseorang dalam memahami, menciptakan, dan mengekspresikan ide atau perasaan melalui musik. Orang dengan kecerdasan ini memiliki kepekaan terhadap nada, ritme, melodi, dan harmoni. Mereka cenderung menikmati mendengarkan musik, bernyanyi, bermain alat musik, atau bahkan menciptakan komposisi musik. Kecerdasan musikal penting dalam profesi seperti musisi, komposer, penyanyi, dan pengajar musik."
narasi_mi_linguistik = "Kecerdasan Linguistik adalah kemampuan seseorang dalam menggunakan bahasa, baik lisan maupun tulisan, untuk mengekspresikan pikiran, ide, dan perasaan dengan jelas dan efektif. Individu dengan kecerdasan ini cenderung memiliki bakat dalam menulis, berbicara, dan memahami makna serta struktur kata-kata. Mereka sering kali menikmati membaca, menulis, bercerita, dan bermain dengan kata-kata. Kecerdasan linguistik sangat penting dalam komunikasi, sastra, jurnalistik, dan pendidikan."
narasi_mi_spasial = "Kecerdasan Spasial adalah kemampuan seseorang untuk berpikir dalam bentuk visual dan gambar, serta untuk memahami dan memanipulasi ruang secara mental. Individu sdengan kecerdasan spasial yang tinggi biasanya memiliki kemampuan untuk melihat dan memvisualisasikan objek dari berbagai sudut, memahami hubungan antara objek-objek tersebut dalam ruang, serta mengenali pola dan detail visual. Kecerdasan ini sering ditemukan pada arsitek, seniman, desainer, dan individu yang bekerja dengan elemen visual dan ruang."
narasi_mi_naturalis = "Kecerdasan Naturalis adalah kemampuan seseorang untuk mengenali, memahami, dan berinteraksi dengan alam dan lingkungan sekitar. Individu dengan kecerdasan ini memiliki ketertarikan yang mendalam terhadap flora, fauna, dan ekosistem, serta kemampuan untuk mengamati dan menganalisis pola-pola di alam. Mereka sering kali menunjukkan kepekaan terhadap isu-isu lingkungan dan memiliki kemampuan untuk bekerja dengan baik dalam lingkungan alam terbuka."
narasi_mi_interpersonal = "Kecerdasan Interpersonal adalah kemampuan seseorang untuk memahami, berempati, dan berinteraksi dengan orang lain secara efektif. Individu dengan kecerdasan ini memiliki kepekaan terhadap perasaan, motivasi, dan kebutuhan orang lain. Mereka biasanya pandai dalam membangun hubungan, bekerja sama dalam kelompok, dan memahami dinamika sosial. Kecerdasan interpersonal sangat penting dalam membina hubungan yang harmonis dan dalam situasi yang memerlukan komunikasi dan kolaborasi."
narasi_mi_intrapersonal = "Kecerdasan Intrapersonal adalah kemampuan seseorang untuk memahami diri sendiri secara mendalam, termasuk emosi, motivasi, nilai-nilai, dan kelemahan pribadi. Individu dengan kecerdasan ini cenderung memiliki kesadaran diri yang tinggi dan mampu merefleksikan pengalaman hidup mereka. Mereka pandai mengatur emosi, mengenali kebutuhan pribadi, dan membuat keputusan berdasarkan pemahaman yang baik tentang diri mereka sendiri. Kecerdasan intrapersonal sangat penting untuk pengembangan diri, kesejahteraan emosional, dan pengambilan keputusan yang bijaksana."
narasi_mi_kinestetik = "Kecerdasan Kinestetik adalah kemampuan seseorang untuk menggunakan tubuhnya dengan terampil dan efektif dalam berbagai aktivitas fisik, seperti olahraga, tarian, kerajinan tangan, dan keterampilan manual lainnya. Individu dengan kecerdasan kinestetik cenderung memiliki koordinasi tubuh yang baik, kontrol gerakan yang presisi, dan kesadaran yang tinggi terhadap postur serta gerak tubuh mereka. Mereka belajar dengan baik melalui pengalaman langsung dan sering mengekspresikan diri melalui gerakan fisik. Kecerdasan ini sangat penting dalam berbagai bidang, termasuk seni, olahraga, dan pekerjaan yang melibatkan keterampilan tangan."
narasi_mi_logika = "Kecerdasan Logika, juga dikenal sebagai kecerdasan logis-matematis, adalah kemampuan seseorang untuk berpikir secara logis, analitis, dan sistematis. Individu dengan kecerdasan ini cenderung unggul dalam memahami pola, menghitung angka, memecahkan masalah, dan menganalisis situasi secara rasional. Mereka menikmati tantangan intelektual seperti teka-teki, permainan strategi, dan pemecahan masalah yang membutuhkan pemikiran kritis. Kecerdasan logika sangat penting dalam bidang-bidang seperti matematika, sains, teknologi, dan pemrograman."

image_mi_interpersonal = os.path.join(".", "img", "mi", "mi_interpersonal.jpg")
image_mi_intrapersonal = os.path.join(".", "img", "mi", "mi_intrapersonal.jpg")
image_mi_kinestetik = os.path.join(".", "img", "mi", "mi_kinesthetic.jpg")
image_mi_logika = os.path.join(".", "img", "mi", "mi_logical.jpg")
image_mi_musikal = os.path.join(".", "img", "mi", "mi_musical.jpg")
image_mi_naturalis = os.path.join(".", "img", "mi", "mi_naturalist.jpg")
image_mi_spasial = os.path.join(".", "img", "mi", "mi_spatial.jpg")
image_mi_linguistik = os.path.join(".", "img", "mi", "mi_linguistic.jpg")

modalitas_pengantar = "Modalitas belajar—visual, auditori, dan kinestetik—masing-masing memiliki keunggulan unik dalam membantu seseorang memahami dan mengingat informasi. Namun, untuk mencapai hasil belajar yang optimal, penting untuk mendayagunakan ketiga modalitas ini secara bersamaan. Menggabungkan berbagai pendekatan dapat memperkuat pemahaman dan memori, serta membuat proses belajar menjadi lebih kaya dan menyeluruh"

visual_pertama = "Untuk mengoptimalkan belajar, fokuslah pada materi yang disajikan secara visual, seperti diagram, peta konsep, atau video. Cobalah untuk membuat catatan dengan gambar atau sketsa. "
visual_kedua = "Gunakan visual sebagai pendukung tambahan untuk memperkuat pemahaman. Misalnya, setelah mendengarkan penjelasan atau terlibat dalam diskusi (auditory), buat catatan dengan poin-poin visual seperti diagram atau peta konsep. "
visual_ketiga = "Visual bisa digunakan sebagai alat bantu tambahan untuk memperjelas konsep yang sulit. Misalnya, setelah mendengarkan dan melakukan aktivitas, lihatlah diagram atau peta konsep untuk memperkuat ingatan dan pemahaman Anda."

auditory_pertama = "Untuk mengoptimalkan belajar, fokuslah pada mendengarkan penjelasan, diskusi, atau podcast. Cobalah merekam dan mendengarkan kembali materi pelajaran atau mengikuti diskusi kelompok untuk memperkuat pemahaman. "
auditory_kedua = "Gunakan pendengaran sebagai pendukung untuk memperkuat informasi yang Anda terima secara visual. Misalnya, setelah melihat diagram atau presentasi (visual), dengarkan penjelasan atau diskusi terkait untuk memperjelas konsep. "
auditory_ketiga = "Pendengaran bisa digunakan sebagai alat bantu tambahan untuk memperjelas konsep yang sulit. Misalnya, setelah melihat diagram atau melakukan aktivitas fisik, dengarkan penjelasan tambahan atau diskusi."

kinesthetic_pertama = "Untuk mengoptimalkan belajar, fokuslah pada kegiatan yang melibatkan gerakan fisik atau manipulasi objek. Lakukan eksperimen, simulasi, atau aktivitas praktik langsung untuk memperdalam pemahaman. "
kinesthetic_kedua = "Gunakan gerakan fisik sebagai pendukung untuk memperkuat informasi yang Anda terima secara visual atau auditory. Misalnya, setelah melihat video atau diagram (visual), cobalah untuk mempraktikkan atau membuat model dari konsep tersebut."
kinesthetic_ketiga = "Gunakan aktivitas kinestetik sebagai alat bantu tambahan untuk memperjelas konsep yang sulit. Misalnya, setelah melihat diagram (visual) atau mendengarkan penjelasan (auditory), lakukan praktik langsung atau simulasi. "

nama_user = "Anastasya Rachellia"
nama_sekolah = "SMAN 15 Surabaya"
foto_user = os.path.join(".", "img", "gambarku.jpg")
logo_institusi = os.path.join(".", "img", "logo-institusi.jpeg")


def create_big_five_chart(data, width=CHART_WIDTH, height=CHART_HEIGHT):
    trait_abbreviations = {
        "Extroversion": "EXT",
        "Agreeableness": "AGR",
        "Openness To Experience": "OPN",
        "Conscientiousness": "CSN",
        "Emotional Stability": "EST"
    }

    fig = go.Figure()

    fig.add_trace(go.Scatterpolar(
        r=list(data.values()),
        theta=[trait_abbreviations[key] for key in data.keys()],
        fill='toself',
        line=dict(color='rgb(158,202,225)'),
        fillcolor='rgba(158,202,225,0.5)'
    ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, max(data.values())],
                showticklabels=False
            ),
            angularaxis=dict(
                tickfont=dict(size=10)
            )
        ),
        showlegend=False,
        width=width,
        height=height,
        margin=dict(l=20, r=20, t=20, b=20),
        paper_bgcolor='white'
    )

    return fig


def create_learning_modality_chart(data, width=300, height=200):
    label_map = {"Visual": "V" + "&nbsp;&nbsp;",
                 "Auditory": "A" + "&nbsp;&nbsp;", "Kinesthetic": "K" + "&nbsp;&nbsp;"}
    sorted_data = sorted(data.items(), key=lambda x: x[1], reverse=True)

    fig = go.Figure(go.Bar(
        x=[item[1] for item in sorted_data],
        y=[label_map[item[0]] for item in sorted_data],
        text=[str(item[1]) for item in sorted_data],
        textposition='inside',
        textfont=dict(size=14, color='black'),
        marker_color='rgb(158,202,225)',
        marker_line_color='rgb(8,48,107)',
        marker_line_width=1.5,
        orientation='h'
    ))

    fig.update_layout(
        width=width,
        height=height,
        margin=dict(l=30, r=10, t=10, b=10),
        paper_bgcolor='white',
        plot_bgcolor='white',
        xaxis=dict(showticklabels=False, showline=False, zeroline=False),
        yaxis=dict(showticklabels=True, showline=False, zeroline=False,
                   tickmode='array', tickvals=[0, 1, 2], ticktext=['V', 'A', 'K']),
        bargap=0.2,
        showlegend=False
    )
    return fig


def create_multiple_intelligence_chart(data, width=CHART_WIDTH, height=CHART_HEIGHT):
    sorted_data = sorted(data.items(), key=lambda x: x[1], reverse=True)

    fig = go.Figure(go.Bar(
        x=[item[0] for item in sorted_data],
        y=[item[1] for item in sorted_data],
        text=[str(item[1]) for item in sorted_data],
        textposition='inside',
        textfont=dict(size=10, color='black'),
        marker_color='rgb(158,202,225)',
        marker_line_color='rgb(8,48,107)',
        marker_line_width=1.5
    ))

    fig.update_layout(
        width=width,
        height=height,
        margin=dict(l=10, r=10, t=30, b=50),
        paper_bgcolor='white',
        plot_bgcolor='white',
        xaxis=dict(
            tickangle=45,
            tickfont=dict(size=8),
            title=None
        ),
        yaxis=dict(
            showticklabels=False,
            showgrid=False,
            zeroline=False,
            title=None
        ),
        bargap=0.2,
        showlegend=False
    )

    return fig


def categorize_score(score):
    if 0 <= score <= 40:
        return "Rendah"
    elif 41 <= score <= 60:
        return "Sedang"
    else:
        return "Tinggi"


def get_narration(trait, score):
    category = categorize_score(score)
    narration_key = f"narasi{trait}{category}"
    return globals()[narration_key]


def get_learning_modality_text(learning_modality):
    sorted_modalities = sorted(
        learning_modality.items(), key=lambda x: x[1], reverse=True)
    text = "<br/>"

    # Define indentation (6 non-breaking spaces)
    indent = "&nbsp;" * 6

    for i, (modality, score) in enumerate(sorted_modalities):
        if i == 0:
            text += f"{indent}{globals()[f'{modality.lower()}_pertama']}<br/>"
        elif i == 1:
            text += f"{indent}{globals()[f'{modality.lower()}_kedua']}<br/>"
        else:
            text += f"{indent}{globals()[f'{modality.lower()}_ketiga']}<br/>"

    return text


def get_multiple_intelligences_content(multiple_intelligences):
    sorted_intelligences = sorted(
        multiple_intelligences.items(), key=lambda x: x[1], reverse=True)
    content = []

    for i, (intelligence, score) in enumerate(sorted_intelligences[:3]):
        intel_lower = intelligence.lower()
        narration = globals()[f"narasi_mi_{intel_lower}"]
        image_path = globals()[f"image_mi_{intel_lower}"]

        content.append({
            'type': 'image',
            'data': image_path,
            'width': 2.2*cm,
            'height': 2.2*cm
        })
        content.append({
            'type': 'text',
            'data': f"<b>{intelligence.capitalize()}:</b> {narration}"
        })

    return content


def add_content_to_pdf(input_pdf, output_pdf, content_list):
    packet = BytesIO()
    can = canvas.Canvas(packet, pagesize=A4)

    # Register fonts
    pdfmetrics.registerFont(TTFont('Arial', 'Arial.ttf'))
    pdfmetrics.registerFont(TTFont('Arial-Bold', 'Arial-Bold.ttf'))

    # Add user name, school name, and photo
    can.setFont("Arial-Bold", 24)
    can.drawString(8.3*cm, A4[1] - 2.6*cm, nama_user)
    can.setFont("Arial", 14)
    can.drawString(8.3*cm, A4[1] - 3.8*cm, nama_sekolah)

    # Add user photo with aspect ratio preservation
    user_img = Image.open(foto_user)
    user_img_width, user_img_height = user_img.size
    user_img_aspect = user_img_height / user_img_width
    user_img_pdf_width = 5*cm
    user_img_pdf_height = user_img_pdf_width * user_img_aspect
    can.drawImage(ImageReader(user_img), 1.5*cm,
                  A4[1] - 6*cm, width=user_img_pdf_width, height=user_img_pdf_height)

    # Add a line under the name
    can.setStrokeColorRGB(0, 0, 0)
    can.line(8.3*cm, A4[1] - 3*cm, 19*cm, A4[1] - 3*cm)

    # Add institution logo with aspect ratio preservation
    logo_institusi = os.path.join(".", "img", "logo-institusi.jpeg")
    logo_img = Image.open(logo_institusi)
    logo_img_width, logo_img_height = logo_img.size
    logo_img_aspect = logo_img_height / logo_img_width
    logo_img_pdf_width = 4*cm
    logo_img_pdf_height = logo_img_pdf_width * logo_img_aspect
    can.drawImage(ImageReader(logo_img), 1.3*cm,
                  A4[1] - 25*cm, width=logo_img_pdf_width, height=logo_img_pdf_height)

    for content in content_list:
        content_type = content['type']
        x, y = content['position']
        page = content['page']

        if page > can.getPageNumber():
            can.showPage()

        if content_type == 'chart':
            chart = content['data']
            img_data = chart.to_image(format="png")
            img_buffer = BytesIO(img_data)
            img = Image.open(img_buffer)
            width = content.get('width', CHART_PDF_WIDTH)
            height = content.get('height', CHART_PDF_HEIGHT)
            can.drawImage(ImageReader(img), x, y, width=width, height=height)

        elif content_type == 'text':
            text_content = content['data']
            styles = getSampleStyleSheet()
            style = styles['BodyText']
            style.fontSize = 9
            p = Paragraph(text_content, style)
            width = content.get('width', 11*cm)
            p.wrapOn(can, width, 20*cm)
            p.drawOn(can, x, y)

        elif content_type == 'image':
            image_path = content['data']
            img = Image.open(image_path)
            img_width, img_height = img.size
            img_aspect = img_height / img_width
            pdf_width = content.get('width', 2*cm)
            pdf_height = pdf_width * img_aspect
            can.drawImage(ImageReader(img), x, y,
                          width=pdf_width, height=pdf_height)

    can.save()
    packet.seek(0)
    new_pdf = PdfReader(packet)

    existing_pdf = PdfReader(open(input_pdf, "rb"))
    output = PdfWriter()

    for i in range(len(existing_pdf.pages)):
        page = existing_pdf.pages[i]
        if i < len(new_pdf.pages):
            page.merge_page(new_pdf.pages[i])
        output.add_page(page)

    with open(output_pdf, "wb") as outputStream:
        output.write(outputStream)


def main():
    # Example data (replace with your MongoDB data retrieval logic)
    big_five_personality = {
        "Extroversion": 63, "Agreeableness": 40, "Openness To Experience": 23,
        "Conscientiousness": 13, "Emotional Stability": 27
    }

    learning_modality = {
        "Visual": 49, "Auditory": 87, "Kinesthetic": 15
    }

    multiple_intelligences = {
        "Logika": 16, "Linguistik": 57, "Spasial": 30, "Musikal": 45,
        "Naturalis": 36, "Interpersonal": 21, "Intrapersonal": 32, "Kinestetik": 18
    }

    # Create charts
    big_five_chart = create_big_five_chart(
        big_five_personality, width=300, height=300)
    learning_modality_chart = create_learning_modality_chart(
        learning_modality, width=300, height=200)
    multiple_intelligence_chart = create_multiple_intelligence_chart(
        multiple_intelligences, width=400, height=300)

    # Create a copy of the template PDF
    input_pdf = "pdf/PPPReportTemplate.pdf"
    output_pdf = "pdf/05-ppp-report.pdf"
    os.system(f"cp {input_pdf} {output_pdf}")

    # Prepare Big Five Personality text
    traits_order = ["Extroversion", "Emotional Stability",
                    "Agreeableness", "Conscientiousness", "Openness To Experience"]
    big_five_text = ""
    for trait in traits_order:
        score = big_five_personality[trait]
        narration = get_narration(trait.replace(" ", ""), score)
        big_five_text += f"<b>{trait}:</b> {narration}<br/><br/>"

    # Prepare Learning Modality text
    learning_modality_text = get_learning_modality_text(learning_modality)

    # Get Multiple Intelligences content
    mi_content = get_multiple_intelligences_content(multiple_intelligences)

    # Prepare content list
    content_list = [
        {'type': 'chart', 'data': big_five_chart, 'position': (
            13*cm, A4[1] - 5*cm - CHART_PDF_HEIGHT), 'page': 1, 'width': 6*cm, 'height': 6*cm},

        {'type': 'text', 'data': big_five_text,
            'position': (8*cm, A4[1] - 29*cm), 'page': 1},

        {'type': 'chart', 'data': learning_modality_chart, 'position': (
            11*cm, A4[1] - 7*cm), 'page': 2, 'width': 6*cm, 'height': 4.2*cm},

        {'type': 'chart', 'data': multiple_intelligence_chart, 'position': (
            10*cm, A4[1] - 11*cm - CHART_PDF_HEIGHT), 'page': 2, 'width': 9*cm, 'height': 8*cm},

        {'type': 'text', 'data': learning_modality_text,
            'position': (2.7*cm, A4[1] - 11.7*cm), 'page': 2, 'width': 16*cm},  # Custom width for learning modality text

    ]

    # Add Multiple Intelligences content
    y_position = A4[1] - 22*cm
    for i in range(0, len(mi_content), 2):
        image_item = mi_content[i]
        text_item = mi_content[i+1]

        content_list.append(
            {**image_item, 'position': (2*cm, y_position), 'page': 2})
        content_list.append(
            {**text_item, 'position': (5*cm, y_position), 'page': 2, 'width': 14*cm})

        y_position -= 3*cm  # Reduced space between sets

    # Add content to the PDF
    add_content_to_pdf(output_pdf, output_pdf, content_list)

    print(f"PDF generated: {output_pdf}")


if __name__ == "__main__":
    main()
