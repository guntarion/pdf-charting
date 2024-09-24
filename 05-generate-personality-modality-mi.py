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
narasi_mi_Musikal = "Kecerdasan Musikal adalah kemampuan seseorang dalam memahami, menciptakan, dan mengekspresikan ide atau perasaan melalui musik. Orang dengan kecerdasan ini memiliki kepekaan terhadap nada, ritme, melodi, dan harmoni. Mereka cenderung menikmati mendengarkan musik, bernyanyi, bermain alat musik, atau bahkan menciptakan komposisi musik. Kecerdasan musikal penting dalam profesi seperti musisi, komposer, penyanyi, dan pengajar musik."
narasi_mi_Linguistik = "Kecerdasan Linguistik adalah kemampuan seseorang dalam menggunakan bahasa, baik lisan maupun tulisan, untuk mengekspresikan pikiran, ide, dan perasaan dengan jelas dan efektif. Individu dengan kecerdasan ini cenderung memiliki bakat dalam menulis, berbicara, dan memahami makna serta struktur kata-kata. Mereka sering kali menikmati membaca, menulis, bercerita, dan bermain dengan kata-kata. Kecerdasan linguistik sangat penting dalam komunikasi, sastra, jurnalistik, dan pendidikan."
narasi_mi_Spasial = "Kecerdasan Spasial adalah kemampuan seseorang untuk berpikir dalam bentuk visual dan gambar, serta untuk memahami dan memanipulasi ruang secara mental. Individu sdengan kecerdasan spasial yang tinggi biasanya memiliki kemampuan untuk melihat dan memvisualisasikan objek dari berbagai sudut, memahami hubungan antara objek-objek tersebut dalam ruang, serta mengenali pola dan detail visual. Kecerdasan ini sering ditemukan pada arsitek, seniman, desainer, dan individu yang bekerja dengan elemen visual dan ruang."
narasi_mi_Naturalis = "Kecerdasan Naturalis adalah kemampuan seseorang untuk mengenali, memahami, dan berinteraksi dengan alam dan lingkungan sekitar. Individu dengan kecerdasan ini memiliki ketertarikan yang mendalam terhadap flora, fauna, dan ekosistem, serta kemampuan untuk mengamati dan menganalisis pola-pola di alam. Mereka sering kali menunjukkan kepekaan terhadap isu-isu lingkungan dan memiliki kemampuan untuk bekerja dengan baik dalam lingkungan alam terbuka."
narasi_mi_Interpersonal = "Kecerdasan Interpersonal adalah kemampuan seseorang untuk memahami, berempati, dan berinteraksi dengan orang lain secara efektif. Individu dengan kecerdasan ini memiliki kepekaan terhadap perasaan, motivasi, dan kebutuhan orang lain. Mereka biasanya pandai dalam membangun hubungan, bekerja sama dalam kelompok, dan memahami dinamika sosial. Kecerdasan interpersonal sangat penting dalam membina hubungan yang harmonis dan dalam situasi yang memerlukan komunikasi dan kolaborasi."
narasi_mi_Intrapersonal = "Kecerdasan Intrapersonal adalah kemampuan seseorang untuk memahami diri sendiri secara mendalam, termasuk emosi, motivasi, nilai-nilai, dan kelemahan pribadi. Individu dengan kecerdasan ini cenderung memiliki kesadaran diri yang tinggi dan mampu merefleksikan pengalaman hidup mereka. Mereka pandai mengatur emosi, mengenali kebutuhan pribadi, dan membuat keputusan berdasarkan pemahaman yang baik tentang diri mereka sendiri. Kecerdasan intrapersonal sangat penting untuk pengembangan diri, kesejahteraan emosional, dan pengambilan keputusan yang bijaksana."
narasi_mi_Kinestetik = "Kecerdasan Kinestetik adalah kemampuan seseorang untuk menggunakan tubuhnya dengan terampil dan efektif dalam berbagai aktivitas fisik, seperti olahraga, tarian, kerajinan tangan, dan keterampilan manual lainnya. Individu dengan kecerdasan kinestetik cenderung memiliki koordinasi tubuh yang baik, kontrol gerakan yang presisi, dan kesadaran yang tinggi terhadap postur serta gerak tubuh mereka. Mereka belajar dengan baik melalui pengalaman langsung dan sering mengekspresikan diri melalui gerakan fisik. Kecerdasan ini sangat penting dalam berbagai bidang, termasuk seni, olahraga, dan pekerjaan yang melibatkan keterampilan tangan."
narasi_mi_Logika = "Kecerdasan Logika, juga dikenal sebagai kecerdasan logis-matematis, adalah kemampuan seseorang untuk berpikir secara logis, analitis, dan sistematis. Individu dengan kecerdasan ini cenderung unggul dalam memahami pola, menghitung angka, memecahkan masalah, dan menganalisis situasi secara rasional. Mereka menikmati tantangan intelektual seperti teka-teki, permainan strategi, dan pemecahan masalah yang membutuhkan pemikiran kritis. Kecerdasan logika sangat penting dalam bidang-bidang seperti matematika, sains, teknologi, dan pemrograman."

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
        height=CHART_HEIGHT
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
        height=CHART_HEIGHT
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
        height=CHART_HEIGHT
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
    text = "<br/><br/>"

    for i, (modality, score) in enumerate(sorted_modalities):
        if i == 0:
            text += globals()[f"{modality.lower()}_pertama"] + "<br/>"
        elif i == 1:
            text += globals()[f"{modality.lower()}_kedua"] + "<br/>"
        else:
            text += globals()[f"{modality.lower()}_ketiga"] + "<br/>"

    return text


def add_content_to_pdf(input_pdf, output_pdf, content_list):
    packet = BytesIO()
    can = canvas.Canvas(packet, pagesize=A4)

    for content in content_list:
        content_type = content['type']
        x, y = content['position']
        page = content['page']

        if content_type == 'chart':
            chart = content['data']
            img_data = chart.to_image(format="png")
            img_buffer = BytesIO(img_data)
            img = Image.open(img_buffer)
            can.drawImage(ImageReader(img), x, y,
                          width=CHART_PDF_WIDTH, height=CHART_PDF_HEIGHT)

        elif content_type == 'text':
            text_content = content['data']
            styles = getSampleStyleSheet()
            style = styles['BodyText']
            style.fontSize = 9
            p = Paragraph(text_content, style)
            p.wrapOn(can, 11*cm, 20*cm)  # Adjust width and height as needed
            p.drawOn(can, x, y)

        if page > can.getPageNumber():
            can.showPage()

    can.save()
    packet.seek(0)
    new_pdf = PdfReader(packet)

    existing_pdf = PdfReader(open(input_pdf, "rb"))
    output = PdfWriter()

    for i in range(len(existing_pdf.pages)):
        page = existing_pdf.pages[i]
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
        "Visual": 49, "Auditory": 47, "Kinesthetic": 35
    }

    multiple_intelligences = {
        "Logika": 16, "Linguistik": 57, "Spasial": 30, "Musikal": 45,
        "Naturalis": 36, "Interpersonal": 21, "Intrapersonal": 32, "Kinestetik": 18
    }

    # Create charts
    big_five_chart = create_big_five_chart(big_five_personality)
    learning_modality_chart = create_learning_modality_chart(learning_modality)
    multiple_intelligence_chart = create_multiple_intelligence_chart(
        multiple_intelligences)

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

    # Prepare content list
    content_list = [
        {'type': 'chart', 'data': big_five_chart, 'position': (
            13*cm, A4[1] - 7*cm - CHART_PDF_HEIGHT), 'page': 1},
        {'type': 'text', 'data': big_five_text,
            'position': (8*cm, A4[1] - 29*cm), 'page': 1},
        {'type': 'chart', 'data': learning_modality_chart, 'position': (
            1*cm, A4[1] - 3*cm - CHART_PDF_HEIGHT), 'page': 2},
        {'type': 'text', 'data': learning_modality_text,
            'position': (1*cm, A4[1] - 13*cm), 'page': 2},
        {'type': 'chart', 'data': multiple_intelligence_chart, 'position': (
            1*cm, A4[1] - 23*cm - CHART_PDF_HEIGHT), 'page': 2}
    ]

    # Add content to the PDF
    add_content_to_pdf(output_pdf, output_pdf, content_list)

    print(f"PDF generated: {output_pdf}")


if __name__ == "__main__":
    main()
