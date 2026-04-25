import streamlit as st
import requests
import csv
import os
from datetime import datetime
from io import BytesIO

# ── PDF libs ──────────────────────────────────────────────────────────────────
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, HRFlowable, Table, TableStyle
)
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT

# ── PAGE CONFIG ───────────────────────────────────────────────────────────────
st.set_page_config(page_title="فرصتك المهنية", page_icon="💼", layout="centered")

# ── CUSTOM CSS — Classic Professional Light Theme ─────────────────────────────
st.markdown("""
<style>
  /* Import elegant font */
  @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;600;700&family=Inter:wght@300;400;500;600&display=swap');

  /* Background */
  .stApp {
    background-color: #F7F5F2;
    font-family: 'Inter', sans-serif;
  }

  /* Hide default streamlit elements */
  #MainMenu, footer, header { visibility: hidden; }

  /* Main container */
  .main .block-container {
    max-width: 680px;
    padding: 3rem 2rem;
  }

  /* Hero card */
  .hero-card {
    background: #FFFFFF;
    border: 1px solid #E8E4DF;
    border-radius: 4px;
    padding: 48px 40px;
    text-align: center;
    margin-bottom: 2rem;
    box-shadow: 0 2px 20px rgba(0,0,0,0.06);
  }

  .hero-logo {
    font-size: 13px;
    letter-spacing: 4px;
    text-transform: uppercase;
    color: #9B8B7A;
    font-family: 'Inter', sans-serif;
    font-weight: 500;
    margin-bottom: 24px;
  }

  .hero-title {
    font-family: 'Playfair Display', serif;
    font-size: 36px;
    font-weight: 700;
    color: #1A1A1A;
    line-height: 1.3;
    margin-bottom: 12px;
  }

  .hero-subtitle {
    font-size: 15px;
    color: #6B6460;
    font-weight: 300;
    line-height: 1.6;
    margin-bottom: 32px;
  }

  /* Stats row */
  .stats-row {
    display: flex;
    justify-content: center;
    gap: 40px;
    padding: 24px 0;
    border-top: 1px solid #F0ECE8;
    border-bottom: 1px solid #F0ECE8;
    margin-bottom: 32px;
  }

  .stat-item {
    text-align: center;
  }

  .stat-value {
    font-family: 'Playfair Display', serif;
    font-size: 22px;
    font-weight: 600;
    color: #1A1A1A;
  }

  .stat-label {
    font-size: 11px;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: #9B8B7A;
    margin-top: 4px;
  }

  /* Section header */
  .section-header {
    font-size: 11px;
    letter-spacing: 3px;
    text-transform: uppercase;
    color: #9B8B7A;
    font-weight: 500;
    margin-bottom: 20px;
    padding-bottom: 10px;
    border-bottom: 1px solid #E8E4DF;
  }

  /* Step indicator */
  .step-indicator {
    display: flex;
    justify-content: center;
    gap: 8px;
    margin-bottom: 32px;
  }

  .step-dot {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: #E8E4DF;
    display: inline-block;
  }

  .step-dot.active {
    background: #2C2C2C;
    width: 24px;
    border-radius: 4px;
  }

  /* Success card */
  .success-banner {
    background: #F0F7F4;
    border: 1px solid #B8D4C8;
    border-left: 4px solid #2D6A4F;
    padding: 16px 20px;
    border-radius: 4px;
    color: #2D6A4F;
    font-size: 14px;
    font-weight: 500;
    margin-bottom: 24px;
  }

  /* Form styling */
  .stTextInput > div > div > input,
  .stTextArea > div > div > textarea,
  .stSelectbox > div > div > div {
    border-radius: 3px !important;
    border-color: #E0DBD6 !important;
    background: #FAFAF9 !important;
    font-family: 'Inter', sans-serif !important;
  }

  .stTextInput > div > div > input:focus,
  .stTextArea > div > div > textarea:focus {
    border-color: #8B7B6B !important;
    box-shadow: 0 0 0 2px rgba(139, 123, 107, 0.12) !important;
  }

  /* Labels */
  .stTextInput label, .stTextArea label, .stSelectbox label, .stRadio label {
    font-size: 13px !important;
    font-weight: 500 !important;
    color: #4A4540 !important;
    letter-spacing: 0.3px !important;
  }

  /* Primary button */
  .stButton > button {
    background: #1A1A1A !important;
    color: #FFFFFF !important;
    border: none !important;
    border-radius: 3px !important;
    font-size: 13px !important;
    font-weight: 500 !important;
    letter-spacing: 1.5px !important;
    text-transform: uppercase !important;
    padding: 14px 32px !important;
    transition: all 0.2s ease !important;
    font-family: 'Inter', sans-serif !important;
  }

  .stButton > button:hover {
    background: #333333 !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 12px rgba(0,0,0,0.15) !important;
  }

  /* Download button */
  .stDownloadButton > button {
    background: #2D6A4F !important;
    color: #FFFFFF !important;
    border: none !important;
    border-radius: 3px !important;
    font-size: 13px !important;
    font-weight: 500 !important;
    letter-spacing: 1.5px !important;
    text-transform: uppercase !important;
    padding: 14px 32px !important;
  }

  .stDownloadButton > button:hover {
    background: #245A42 !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 12px rgba(45,106,79,0.25) !important;
  }

  /* Progress bar */
  .stProgress > div > div > div > div {
    background: #1A1A1A !important;
  }

  /* Radio buttons */
  .stRadio > div {
    gap: 8px !important;
  }

  .stRadio > div > label {
    background: #FAFAF9 !important;
    border: 1px solid #E8E4DF !important;
    border-radius: 3px !important;
    padding: 10px 16px !important;
    cursor: pointer !important;
    transition: all 0.15s !important;
  }

  .stRadio > div > label:hover {
    border-color: #8B7B6B !important;
    background: #F5F2EF !important;
  }

  /* Result CV box */
  .cv-result-box {
    background: #FFFFFF;
    border: 1px solid #E8E4DF;
    border-radius: 4px;
    padding: 32px;
    font-family: 'Inter', sans-serif;
    font-size: 14px;
    line-height: 1.7;
    color: #2C2C2C;
    white-space: pre-wrap;
  }
</style>
""", unsafe_allow_html=True)

# ── GROQ ──────────────────────────────────────────────────────────────────────
GROQ_API_KEY = st.secrets["GROQ_API_KEY"]

def ask_ai(prompt):
    try:
        response = requests.post(
            url="https://api.groq.com/openai/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {GROQ_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "llama-3.3-70b-versatile",
                "messages": [{"role": "user", "content": prompt}]
            },
            timeout=30
        )
        result = response.json()
        if "choices" in result:
            return result["choices"][0]["message"]["content"]
        else:
            st.error(f"❌ خطأ: {result}")
            return None
    except Exception as e:
        st.error(f"❌ خطأ: {str(e)}")
        return None

# ── CSV ───────────────────────────────────────────────────────────────────────
def save_to_csv(data):
    filename = "applicants.csv"
    fieldnames = ["timestamp","name","email","phone","city","education","major","q1","q2","q3","q4","q5","open_q"]
    file_exists = os.path.isfile(filename)
    with open(filename, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()
        row = {k: data.get(k, "") for k in fieldnames}
        row["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        writer.writerow(row)

# ── PDF GENERATOR ─────────────────────────────────────────────────────────────
def parse_cv_sections(cv_text):
    """Parse the AI output into structured sections."""
    lines = cv_text.strip().split("\n")
    sections = {
        "assessment": [],
        "summary": [],
        "competencies": [],
        "education": [],
        "attributes": [],
        "languages": [],
        "name_line": "",
        "contact_line": "",
        "score": "",
    }
    current = None

    for line in lines:
        line = line.strip()
        if not line or line == "---":
            continue

        # Detect name (first ALL CAPS line after CV header)
        upper = line.replace(" ", "").replace(",","").replace("|","")
        if upper.isupper() and len(line) > 3 and sections["name_line"] == "" and "CURRICULUM" not in line and "ASSESSMENT" not in line:
            sections["name_line"] = line
            continue

        # Contact line (contains | and email)
        if "|" in line and "@" in line and sections["contact_line"] == "":
            sections["contact_line"] = line
            continue

        # Score line
        if "Score:" in line or "score:" in line.lower():
            sections["score"] = line
            continue

        # Section headers
        low = line.lower()
        if "assessment" in low:
            current = "assessment"
            continue
        elif "curriculum vitae" in low:
            current = None
            continue
        elif "professional summary" in low:
            current = "summary"
            continue
        elif "core competencies" in low:
            current = "competencies"
            continue
        elif "education" in low:
            current = "education"
            continue
        elif "key attributes" in low:
            current = "attributes"
            continue
        elif "languages" in low:
            current = "languages"
            continue

        if current and line:
            sections[current].append(line.lstrip("-•– ").strip())

    return sections


def generate_pdf(cv_text, data):
    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=18*mm,
        leftMargin=18*mm,
        topMargin=14*mm,
        bottomMargin=14*mm,
    )

    # ── Color palette ──────────────────────────────────────────────────────────
    BLACK       = colors.HexColor("#1A1A1A")
    DARK_GRAY   = colors.HexColor("#2C2C2C")
    MID_GRAY    = colors.HexColor("#6B6460")
    LIGHT_GRAY  = colors.HexColor("#9B8B7A")
    RULE_COLOR  = colors.HexColor("#D8D4CF")
    HEADER_BG   = colors.HexColor("#1A1A1A")
    ACCENT      = colors.HexColor("#2D6A4F")
    PAGE_BG     = colors.HexColor("#F7F5F2")
    WHITE       = colors.white

    # ── Styles ─────────────────────────────────────────────────────────────────
    name_style = ParagraphStyle(
        "Name",
        fontName="Helvetica-Bold",
        fontSize=22,
        textColor=WHITE,
        alignment=TA_CENTER,
        spaceAfter=4,
    )
    contact_style = ParagraphStyle(
        "Contact",
        fontName="Helvetica",
        fontSize=9,
        textColor=colors.HexColor("#CCCCCC"),
        alignment=TA_CENTER,
        spaceAfter=0,
    )
    section_title_style = ParagraphStyle(
        "SectionTitle",
        fontName="Helvetica-Bold",
        fontSize=8,
        textColor=LIGHT_GRAY,
        spaceAfter=6,
        spaceBefore=14,
        leading=12,
        letterSpacing=2,
    )
    body_style = ParagraphStyle(
        "Body",
        fontName="Helvetica",
        fontSize=9.5,
        textColor=DARK_GRAY,
        spaceAfter=4,
        leading=15,
    )
    bullet_style = ParagraphStyle(
        "Bullet",
        fontName="Helvetica",
        fontSize=9.5,
        textColor=DARK_GRAY,
        spaceAfter=3,
        leading=14,
        leftIndent=12,
        bulletIndent=0,
    )
    assess_style = ParagraphStyle(
        "Assess",
        fontName="Helvetica",
        fontSize=9,
        textColor=MID_GRAY,
        spaceAfter=3,
        leading=14,
        leftIndent=8,
    )
    score_style = ParagraphStyle(
        "Score",
        fontName="Helvetica-Bold",
        fontSize=10,
        textColor=ACCENT,
        spaceAfter=6,
        leading=14,
    )

    story = []
    sections = parse_cv_sections(cv_text)

    # ── HEADER BLOCK ───────────────────────────────────────────────────────────
    name_text   = sections["name_line"] or data.get("name","").upper()
    contact_text = sections["contact_line"] or f"{data.get('city','')} | {data.get('phone','')} | {data.get('email','')}"

    header_data = [[
        Paragraph(name_text, name_style),
    ], [
        Paragraph(contact_text, contact_style),
    ]]

    header_table = Table(header_data, colWidths=[174*mm])
    header_table.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), HEADER_BG),
        ("TOPPADDING",    (0,0), (-1,0), 18),
        ("BOTTOMPADDING", (0,0), (-1,0), 4),
        ("TOPPADDING",    (0,1), (-1,1), 0),
        ("BOTTOMPADDING", (0,1), (-1,1), 18),
        ("LEFTPADDING",  (0,0), (-1,-1), 16),
        ("RIGHTPADDING", (0,0), (-1,-1), 16),
    ]))
    story.append(header_table)
    story.append(Spacer(1, 6*mm))

    # ── ASSESSMENT SECTION ─────────────────────────────────────────────────────
    if sections["assessment"] or sections["score"]:
        story.append(Paragraph("ASSESSMENT REPORT", section_title_style))
        story.append(HRFlowable(width="100%", thickness=0.5, color=RULE_COLOR, spaceAfter=6))

        if sections["score"]:
            story.append(Paragraph(sections["score"], score_style))

        for line in sections["assessment"]:
            if line:
                story.append(Paragraph(f"• {line}", assess_style))
        story.append(Spacer(1, 4*mm))

    # ── PROFESSIONAL SUMMARY ───────────────────────────────────────────────────
    if sections["summary"]:
        story.append(Paragraph("PROFESSIONAL SUMMARY", section_title_style))
        story.append(HRFlowable(width="100%", thickness=0.5, color=RULE_COLOR, spaceAfter=6))
        summary_text = " ".join(sections["summary"])
        story.append(Paragraph(summary_text, body_style))
        story.append(Spacer(1, 4*mm))

    # ── CORE COMPETENCIES — 2 columns ─────────────────────────────────────────
    if sections["competencies"]:
        story.append(Paragraph("CORE COMPETENCIES", section_title_style))
        story.append(HRFlowable(width="100%", thickness=0.5, color=RULE_COLOR, spaceAfter=6))

        items = sections["competencies"]
        # Pad to even number
        if len(items) % 2 != 0:
            items.append("")
        mid = len(items) // 2
        left_col  = items[:mid]
        right_col = items[mid:]

        table_data = []
        for l, r in zip(left_col, right_col):
            lp = Paragraph(f"▪  {l}", bullet_style) if l else Paragraph("", bullet_style)
            rp = Paragraph(f"▪  {r}", bullet_style) if r else Paragraph("", bullet_style)
            table_data.append([lp, rp])

        comp_table = Table(table_data, colWidths=[87*mm, 87*mm])
        comp_table.setStyle(TableStyle([
            ("VALIGN", (0,0), (-1,-1), "TOP"),
            ("TOPPADDING",    (0,0), (-1,-1), 2),
            ("BOTTOMPADDING", (0,0), (-1,-1), 2),
            ("LEFTPADDING",   (0,0), (-1,-1), 0),
            ("RIGHTPADDING",  (0,0), (-1,-1), 0),
        ]))
        story.append(comp_table)
        story.append(Spacer(1, 4*mm))

    # ── EDUCATION ─────────────────────────────────────────────────────────────
    if sections["education"]:
        story.append(Paragraph("EDUCATION", section_title_style))
        story.append(HRFlowable(width="100%", thickness=0.5, color=RULE_COLOR, spaceAfter=6))
        for line in sections["education"]:
            if line:
                story.append(Paragraph(line, body_style))
        story.append(Spacer(1, 4*mm))

    # ── KEY ATTRIBUTES ────────────────────────────────────────────────────────
    if sections["attributes"]:
        story.append(Paragraph("KEY ATTRIBUTES", section_title_style))
        story.append(HRFlowable(width="100%", thickness=0.5, color=RULE_COLOR, spaceAfter=6))
        for line in sections["attributes"]:
            if line:
                story.append(Paragraph(f"• {line}", bullet_style))
        story.append(Spacer(1, 4*mm))

    # ── LANGUAGES ─────────────────────────────────────────────────────────────
    if sections["languages"]:
        story.append(Paragraph("LANGUAGES", section_title_style))
        story.append(HRFlowable(width="100%", thickness=0.5, color=RULE_COLOR, spaceAfter=6))
        for line in sections["languages"]:
            if line:
                story.append(Paragraph(f"• {line}", bullet_style))

    # ── FOOTER LINE ───────────────────────────────────────────────────────────
    story.append(Spacer(1, 8*mm))
    story.append(HRFlowable(width="100%", thickness=0.5, color=RULE_COLOR))
    story.append(Spacer(1, 2*mm))
    footer_style = ParagraphStyle(
        "Footer",
        fontName="Helvetica",
        fontSize=7.5,
        textColor=LIGHT_GRAY,
        alignment=TA_CENTER,
    )
    story.append(Paragraph(
        f"Prepared on {datetime.now().strftime('%B %d, %Y')}  ·  ATS-Optimized CV",
        footer_style
    ))

    doc.build(story)
    buffer.seek(0)
    return buffer

# ── SESSION STATE ─────────────────────────────────────────────────────────────
for key, val in [("step", 0), ("data", {}), ("cv_text", None)]:
    if key not in st.session_state:
        st.session_state[key] = val

# ══════════════════════════════════════════════════════════════════════════════
# STEP 0 — LANDING
# ══════════════════════════════════════════════════════════════════════════════
if st.session_state.step == 0:
    st.markdown("""
    <div class="hero-card">
      <div class="hero-logo">Career Intelligence Platform</div>
      <div class="hero-title">ابدأ مسيرتك المهنية</div>
      <div class="hero-subtitle">
        أداة متخصصة تحلل ملفك الشخصي وتنشئ<br>
        سيرة ذاتية احترافية جاهزة للتقديم
      </div>
      <div class="stats-row">
        <div class="stat-item">
          <div class="stat-value">4</div>
          <div class="stat-label">دقائق</div>
        </div>
        <div class="stat-item">
          <div class="stat-value">ATS</div>
          <div class="stat-label">محسّن</div>
        </div>
        <div class="stat-item">
          <div class="stat-value">PDF</div>
          <div class="stat-label">احترافي</div>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    if st.button("ابدأ الآن  →", use_container_width=True):
        st.session_state.step = 1
        st.rerun()

# ══════════════════════════════════════════════════════════════════════════════
# STEP 1 — BASIC INFO
# ══════════════════════════════════════════════════════════════════════════════
elif st.session_state.step == 1:
    st.progress(33)
    st.markdown('<div class="section-header">الخطوة 1 من 3 — البيانات الأساسية</div>', unsafe_allow_html=True)

    with st.form("basic_info"):
        name  = st.text_input("الاسم الكامل", value=st.session_state.data.get("name",""))
        email = st.text_input("البريد الإلكتروني", value=st.session_state.data.get("email",""))
        phone = st.text_input("رقم الموبايل", value=st.session_state.data.get("phone",""))
        city  = st.selectbox("المدينة", ["اختر","القاهرة","الإسكندرية","الجيزة","المنصورة","أخرى"])
        education = st.selectbox("المؤهل الدراسي", ["اختر","طالب جامعي","بكالوريوس","دبلوم","ماجستير","ثانوية"])
        major = st.text_input("التخصص", value=st.session_state.data.get("major",""))
        submitted = st.form_submit_button("التالي  →", use_container_width=True)

        if submitted:
            if not name or not email or not phone:
                st.error("⚠️ من فضلك أكمل الاسم والإيميل ورقم الموبايل")
            elif city == "اختر":
                st.error("⚠️ من فضلك اختر المدينة")
            elif education == "اختر":
                st.error("⚠️ من فضلك اختر المؤهل")
            else:
                st.session_state.data.update({
                    "name": name, "email": email, "phone": phone,
                    "city": city, "education": education, "major": major
                })
                st.session_state.step = 2
                st.rerun()

# ══════════════════════════════════════════════════════════════════════════════
# STEP 2 — PERSONALITY
# ══════════════════════════════════════════════════════════════════════════════
elif st.session_state.step == 2:
    st.progress(66)
    st.markdown('<div class="section-header">الخطوة 2 من 3 — ملفك المهني</div>', unsafe_allow_html=True)

    q1_opts = ["أحاول أفهم سبب الرفض وأعيد الشرح","أقبل الرفض وأنتقل لعميل آخر","أطلب مساعدة من زميلي","أحتاج وقت أفكر"]
    q2_opts = ["سريع التعلم ومحب للتطور","منظم ودقيق في التفاصيل","اجتماعي وبحب التعامل مع الناس","مبدع وعندي أفكار جديدة"]
    q3_opts = ["من البيت (Remote)","في المكتب مع الفريق","مش مهم طالما في تطور","هجين (Hybrid)"]
    q4_opts = ["أصبر وأستمر","أطلب تدريب إضافي","أدور على طريقة أسهل","أقيّم وأقرر"]
    q5_opts = ["الراتب والعمولات","التطور والتعلم","الاستقرار والبيئة المريحة","التأثير وإني أحس إن شغلي مهم"]

    with st.form("personality"):
        q1 = st.radio("لو عندك عميل رافض يشتري، هتعمل إيه؟", q1_opts)
        q2 = st.radio("إزاي بتوصف نفسك في الشغل؟", q2_opts)
        q3 = st.radio("بيئة الشغل المفضلة عندك؟", q3_opts)
        q4 = st.radio("لو الشغل صعب في البداية، هتعمل إيه؟", q4_opts)
        q5 = st.radio("إيه اللي يحفزك في الشغل؟", q5_opts)
        open_q = st.text_area("عرّف عن نفسك في 3 جمل", value=st.session_state.data.get("open_q",""), height=100)

        col_back, col_next = st.columns(2)
        with col_back:
            back = st.form_submit_button("← رجوع", use_container_width=True)
        with col_next:
            submitted2 = st.form_submit_button("إنشاء السيرة الذاتية  →", use_container_width=True)

        if back:
            st.session_state.step = 1
            st.rerun()
        if submitted2:
            if not open_q.strip():
                st.error("⚠️ من فضلك اكتب عن نفسك")
            else:
                st.session_state.data.update({
                    "q1": q1, "q2": q2, "q3": q3, "q4": q4, "q5": q5, "open_q": open_q
                })
                st.session_state.step = 3
                st.rerun()

# ══════════════════════════════════════════════════════════════════════════════
# STEP 3 — RESULT
# ══════════════════════════════════════════════════════════════════════════════
elif st.session_state.step == 3:
    st.progress(100)
    data = st.session_state.data

    if st.session_state.cv_text is None:
        st.markdown('<div class="section-header">جاري إعداد سيرتك الذاتية...</div>', unsafe_allow_html=True)

        prompt = f"""
You are a professional HR expert and ATS-certified resume writer specializing in Sales and Marketing roles in Egypt.

Your task: Write a professional ATS-optimized CV in English only. Use ONLY English. Do NOT use any Arabic or other languages.

Candidate Information:
- Full Name: {data['name']}
- Phone: {data['phone']}
- Email: {data['email']}
- City: {data['city']}, Egypt
- Education: {data['education']} - {data['major']}
- Handles client rejection by: {data['q1']}
- Self description: {data['q2']}
- Preferred work environment: {data['q3']}
- Handles work challenges by: {data['q4']}
- Motivated by: {data['q5']}
- About himself: {data['open_q']}

Write the CV in this EXACT format:

## ASSESSMENT REPORT
- Score: X/10
- Strengths: (3 bullet points)
- Recommendation: Suitable for Sales / Not Suitable

---

## CURRICULUM VITAE

{data['name'].upper()}
{data['city']}, Egypt | {data['phone']} | {data['email']}

PROFESSIONAL SUMMARY
(Write 3 strong sentences describing the candidate for a Sales role. Use action verbs. ATS-friendly.)

CORE COMPETENCIES
- (skill 1)
- (skill 2)
- (skill 3)
- (skill 4)
- (skill 5)
- (skill 6)

EDUCATION
{data['education']} in {data['major']}
Egypt

KEY ATTRIBUTES
- (attribute based on answers)
- (attribute based on answers)
- (attribute based on answers)

LANGUAGES
- Arabic: Native
- English: Intermediate

IMPORTANT RULES:
- Use English ONLY. No Arabic. No Chinese. No other language.
- No tables. No images. No special characters except dashes and bullets.
- Keep it clean and ATS-friendly.
- Do not add fake experience or fake companies.
"""
        with st.spinner("جاري إعداد السيرة الذاتية..."):
            result = ask_ai(prompt)
        if result is None:
            st.stop()
        st.session_state.cv_text = result
        save_to_csv(data)

    # ── Show result ────────────────────────────────────────────────────────────
    st.markdown(f'<div class="success-banner">✓ تم إعداد سيرتك الذاتية بنجاح — {data["name"]}</div>', unsafe_allow_html=True)

    # Preview
    st.markdown('<div class="section-header">معاينة السيرة الذاتية</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="cv-result-box">{st.session_state.cv_text}</div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Generate PDF ───────────────────────────────────────────────────────────
    pdf_buffer = generate_pdf(st.session_state.cv_text, data)
    safe_name  = data['name'].replace(' ', '_')

    st.download_button(
        label="⬇  تحميل السيرة الذاتية PDF",
        data=pdf_buffer,
        file_name=f"CV_{safe_name}.pdf",
        mime="application/pdf",
        use_container_width=True,
    )

    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("بدء تقييم جديد", use_container_width=True):
        st.session_state.step = 0
        st.session_state.data = {}
        st.session_state.cv_text = None
        st.rerun()

    st.markdown(
        '<p style="text-align:center;font-size:13px;color:#9B8B7A;margin-top:16px;">سيتم التواصل معك قريباً</p>',
        unsafe_allow_html=True
    )
