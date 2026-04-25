import streamlit as st
import requests
import csv
import os
from datetime import datetime
from io import BytesIO

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable, Table, TableStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT

st.set_page_config(page_title="Dawood Recruitment", page_icon="◈", layout="centered")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,500;1,300;1,400&family=DM+Sans:wght@300;400;500&display=swap');

:root {
  --navy:  #0B1629;
  --gold:  #C9A84C;
  --gold2: #E8C97A;
  --white: #FFFFFF;
  --gray:  #8A929E;
  --light: #C0C8D4;
  --line:  rgba(201,168,76,0.2);
  --card:  rgba(255,255,255,0.03);
}

.stApp { background: var(--navy); font-family: 'DM Sans', sans-serif; }
#MainMenu, footer, header { visibility: hidden; }
.stDeployButton { display: none; }
.main .block-container { max-width: 600px; padding: 0 1.5rem 5rem; margin: 0 auto; }

.brand-bar {
  border-bottom: 1px solid var(--line);
  padding: 26px 0 22px;
  margin-bottom: 52px;
  display: flex;
  align-items: center;
  justify-content: space-between;
}
.brand-name {
  font-family: 'Cormorant Garamond', serif;
  font-size: 19px; font-weight: 500;
  color: var(--white); letter-spacing: 4px; text-transform: uppercase;
}
.brand-tag {
  font-size: 9px; letter-spacing: 3px;
  text-transform: uppercase; color: var(--gold);
}

.hero-eyebrow {
  font-size: 9px; letter-spacing: 4px;
  text-transform: uppercase; color: var(--gold);
  margin-bottom: 18px;
  display: flex; align-items: center; gap: 12px;
}
.hero-eyebrow::after { content:''; flex:1; height:1px; background:var(--line); }

.hero-title {
  font-family: 'Cormorant Garamond', serif;
  font-size: 58px; font-weight: 300;
  color: var(--white); line-height: 1.05;
  margin-bottom: 6px; letter-spacing: -1px;
}
.hero-title em { color: var(--gold); font-style: italic; }

.hero-sub {
  font-size: 13.5px; color: var(--gray);
  font-weight: 300; line-height: 1.75;
  margin: 20px 0 44px; max-width: 400px;
}

.stats-grid {
  display: grid; grid-template-columns: repeat(3,1fr);
  gap: 1px; background: var(--line);
  border: 1px solid var(--line); margin-bottom: 48px;
}
.stat-cell { background: var(--navy); padding: 22px 16px; text-align: center; }
.stat-num {
  font-family: 'Cormorant Garamond', serif;
  font-size: 30px; font-weight: 400;
  color: var(--gold); line-height: 1; margin-bottom: 7px;
}
.stat-lbl { font-size: 8.5px; letter-spacing: 2.5px; text-transform: uppercase; color: var(--gray); }

.sec-label {
  font-size: 8.5px; letter-spacing: 3.5px;
  text-transform: uppercase; color: var(--gold);
  margin-bottom: 28px; padding-bottom: 12px;
  border-bottom: 1px solid var(--line);
}

.success-banner {
  border: 1px solid rgba(201,168,76,0.35);
  border-left: 3px solid var(--gold);
  background: rgba(201,168,76,0.05);
  padding: 15px 20px; border-radius: 2px;
  color: var(--gold2); font-size: 13px;
  letter-spacing: 0.3px; margin-bottom: 28px;
}

.cv-box {
  background: var(--card);
  border: 1px solid rgba(255,255,255,0.07);
  border-radius: 2px; padding: 28px 22px;
  font-size: 12.5px; line-height: 1.85;
  color: var(--light); white-space: pre-wrap;
  font-family: 'DM Sans', sans-serif; margin-bottom: 24px;
}

/* inputs */
.stTextInput label, .stTextArea label,
.stSelectbox label, .stRadio > label {
  font-size: 9.5px !important; letter-spacing: 2.5px !important;
  text-transform: uppercase !important; color: var(--gray) !important;
  font-weight: 400 !important;
}
.stTextInput > div > div > input {
  background: rgba(255,255,255,0.04) !important;
  border: 1px solid rgba(255,255,255,0.1) !important;
  border-radius: 2px !important; color: var(--white) !important;
  font-family: 'DM Sans',sans-serif !important; font-size: 14px !important;
  padding: 14px 16px !important;
}
.stTextInput > div > div > input:focus {
  border-color: var(--gold) !important;
  background: rgba(201,168,76,0.04) !important; box-shadow: none !important;
}
.stTextArea > div > div > textarea {
  background: rgba(255,255,255,0.04) !important;
  border: 1px solid rgba(255,255,255,0.1) !important;
  border-radius: 2px !important; color: var(--white) !important;
  font-family: 'DM Sans',sans-serif !important; font-size: 14px !important;
}
.stTextArea > div > div > textarea:focus {
  border-color: var(--gold) !important;
  background: rgba(201,168,76,0.04) !important; box-shadow: none !important;
}
.stSelectbox > div > div {
  background: rgba(255,255,255,0.04) !important;
  border: 1px solid rgba(255,255,255,0.1) !important;
  border-radius: 2px !important; color: var(--white) !important;
}
.stSelectbox > div > div > div { color: var(--white) !important; }
.stSelectbox svg { fill: var(--gray) !important; }

/* radio */
.stRadio > div { gap: 6px !important; }
.stRadio > div > label {
  background: rgba(255,255,255,0.03) !important;
  border: 1px solid rgba(255,255,255,0.08) !important;
  border-radius: 2px !important; padding: 12px 16px !important;
  color: var(--light) !important; font-size: 13px !important;
  transition: all 0.15s !important; cursor: pointer !important;
}
.stRadio > div > label:hover {
  border-color: var(--gold) !important; color: var(--white) !important;
  background: rgba(201,168,76,0.06) !important;
}

/* buttons */
.stButton > button {
  background: transparent !important;
  border: 1px solid var(--gold) !important; color: var(--gold) !important;
  border-radius: 2px !important; font-family: 'DM Sans',sans-serif !important;
  font-size: 9.5px !important; font-weight: 500 !important;
  letter-spacing: 3px !important; text-transform: uppercase !important;
  padding: 16px 32px !important; transition: all 0.2s !important;
}
.stButton > button:hover {
  background: var(--gold) !important; color: var(--navy) !important;
  transform: translateY(-1px) !important;
  box-shadow: 0 8px 24px rgba(201,168,76,0.2) !important;
}
.stDownloadButton > button {
  background: var(--gold) !important;
  border: 1px solid var(--gold) !important; color: var(--navy) !important;
  border-radius: 2px !important; font-family: 'DM Sans',sans-serif !important;
  font-size: 9.5px !important; font-weight: 600 !important;
  letter-spacing: 3px !important; text-transform: uppercase !important;
  padding: 16px 32px !important; transition: all 0.2s !important;
}
.stDownloadButton > button:hover {
  background: var(--gold2) !important;
  box-shadow: 0 8px 32px rgba(201,168,76,0.3) !important;
  transform: translateY(-1px) !important;
}

/* progress */
.stProgress > div > div > div > div { background: var(--gold) !important; }
.stProgress > div > div { background: rgba(255,255,255,0.06) !important; }

/* spinner */
.stSpinner > div { border-top-color: var(--gold) !important; }
</style>
""", unsafe_allow_html=True)

# ── GROQ ──────────────────────────────────────────────────────────────────────
GROQ_API_KEY = st.secrets["GROQ_API_KEY"]

def ask_ai(prompt):
    try:
        response = requests.post(
            url="https://api.groq.com/openai/v1/chat/completions",
            headers={"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"},
            json={"model": "llama-3.3-70b-versatile", "messages": [{"role": "user", "content": prompt}]},
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

# ── PDF ───────────────────────────────────────────────────────────────────────
def parse_cv_sections(cv_text):
    lines = cv_text.strip().split("\n")
    sections = {"assessment":[],"summary":[],"competencies":[],"education":[],"attributes":[],"languages":[],"name_line":"","contact_line":"","score":""}
    current = None
    for line in lines:
        line = line.strip()
        if not line or line == "---": continue
        upper = line.replace(" ","").replace(",","").replace("|","")
        if upper.isupper() and len(line)>3 and sections["name_line"]=="" and "CURRICULUM" not in line and "ASSESSMENT" not in line:
            sections["name_line"] = line; continue
        if "|" in line and "@" in line and sections["contact_line"]=="":
            sections["contact_line"] = line; continue
        if "Score:" in line or "score:" in line.lower():
            sections["score"] = line; continue
        low = line.lower()
        if "assessment" in low: current="assessment"; continue
        elif "curriculum vitae" in low: current=None; continue
        elif "professional summary" in low: current="summary"; continue
        elif "core competencies" in low: current="competencies"; continue
        elif "education" in low: current="education"; continue
        elif "key attributes" in low: current="attributes"; continue
        elif "languages" in low: current="languages"; continue
        if current and line: sections[current].append(line.lstrip("-•– ").strip())
    return sections

def generate_pdf(cv_text, data):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=18*mm, leftMargin=18*mm, topMargin=14*mm, bottomMargin=14*mm)
    NAVY  = colors.HexColor("#0B1629")
    GOLD  = colors.HexColor("#C9A84C")
    WHITE = colors.white
    LIGHT = colors.HexColor("#C0C8D4")
    GRAY  = colors.HexColor("#8A929E")
    RULE  = colors.HexColor("#1E2E48")

    name_style    = ParagraphStyle("N",  fontName="Helvetica-Bold", fontSize=22, textColor=WHITE,  alignment=TA_CENTER, spaceAfter=4)
    contact_style = ParagraphStyle("C",  fontName="Helvetica",      fontSize=8.5, textColor=colors.HexColor("#9BAABF"), alignment=TA_CENTER)
    sec_style     = ParagraphStyle("S",  fontName="Helvetica-Bold", fontSize=7.5, textColor=GOLD,  spaceAfter=5, spaceBefore=14, leading=11)
    body_style    = ParagraphStyle("B",  fontName="Helvetica",      fontSize=9.5, textColor=LIGHT, spaceAfter=4, leading=15)
    bullet_style  = ParagraphStyle("BU", fontName="Helvetica",      fontSize=9.5, textColor=LIGHT, spaceAfter=3, leading=14, leftIndent=10)
    assess_style  = ParagraphStyle("A",  fontName="Helvetica",      fontSize=9,   textColor=GRAY,  spaceAfter=3, leading=14, leftIndent=8)
    score_style   = ParagraphStyle("SC", fontName="Helvetica-Bold", fontSize=10,  textColor=GOLD,  spaceAfter=6, leading=14)
    footer_style  = ParagraphStyle("F",  fontName="Helvetica",      fontSize=7,   textColor=GRAY,  alignment=TA_CENTER)

    story = []
    sections = parse_cv_sections(cv_text)
    name_text    = sections["name_line"]    or data.get("name","").upper()
    contact_text = sections["contact_line"] or f"{data.get('city','')} | {data.get('phone','')} | {data.get('email','')}"

    hd = [[Paragraph(name_text, name_style)], [Paragraph(contact_text, contact_style)]]
    ht = Table(hd, colWidths=[174*mm])
    ht.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(-1,-1),NAVY),
        ("TOPPADDING",(0,0),(-1,0),22), ("BOTTOMPADDING",(0,0),(-1,0),4),
        ("TOPPADDING",(0,1),(-1,1),0),  ("BOTTOMPADDING",(0,1),(-1,1),20),
        ("LEFTPADDING",(0,0),(-1,-1),16), ("RIGHTPADDING",(0,0),(-1,-1),16),
        ("LINEBELOW",(0,-1),(-1,-1),1.5,GOLD),
    ]))
    story.append(ht); story.append(Spacer(1,6*mm))

    if sections["assessment"] or sections["score"]:
        story.append(Paragraph("ASSESSMENT REPORT", sec_style))
        story.append(HRFlowable(width="100%", thickness=0.5, color=RULE, spaceAfter=6))
        if sections["score"]: story.append(Paragraph(sections["score"], score_style))
        for line in sections["assessment"]:
            if line: story.append(Paragraph(f"• {line}", assess_style))
        story.append(Spacer(1,4*mm))

    if sections["summary"]:
        story.append(Paragraph("PROFESSIONAL SUMMARY", sec_style))
        story.append(HRFlowable(width="100%", thickness=0.5, color=RULE, spaceAfter=6))
        story.append(Paragraph(" ".join(sections["summary"]), body_style))
        story.append(Spacer(1,4*mm))

    if sections["competencies"]:
        story.append(Paragraph("CORE COMPETENCIES", sec_style))
        story.append(HRFlowable(width="100%", thickness=0.5, color=RULE, spaceAfter=6))
        items = sections["competencies"]
        if len(items) % 2 != 0: items.append("")
        mid = len(items)//2
        td = []
        for l,r in zip(items[:mid], items[mid:]):
            td.append([
                Paragraph(f"▪  {l}", bullet_style) if l else Paragraph("", bullet_style),
                Paragraph(f"▪  {r}", bullet_style) if r else Paragraph("", bullet_style)
            ])
        ct = Table(td, colWidths=[87*mm,87*mm])
        ct.setStyle(TableStyle([("VALIGN",(0,0),(-1,-1),"TOP"),("TOPPADDING",(0,0),(-1,-1),2),("BOTTOMPADDING",(0,0),(-1,-1),2),("LEFTPADDING",(0,0),(-1,-1),0),("RIGHTPADDING",(0,0),(-1,-1),0)]))
        story.append(ct); story.append(Spacer(1,4*mm))

    if sections["education"]:
        story.append(Paragraph("EDUCATION", sec_style))
        story.append(HRFlowable(width="100%", thickness=0.5, color=RULE, spaceAfter=6))
        for line in sections["education"]:
            if line: story.append(Paragraph(line, body_style))
        story.append(Spacer(1,4*mm))

    if sections["attributes"]:
        story.append(Paragraph("KEY ATTRIBUTES", sec_style))
        story.append(HRFlowable(width="100%", thickness=0.5, color=RULE, spaceAfter=6))
        for line in sections["attributes"]:
            if line: story.append(Paragraph(f"• {line}", bullet_style))
        story.append(Spacer(1,4*mm))

    if sections["languages"]:
        story.append(Paragraph("LANGUAGES", sec_style))
        story.append(HRFlowable(width="100%", thickness=0.5, color=RULE, spaceAfter=6))
        for line in sections["languages"]:
            if line: story.append(Paragraph(f"• {line}", bullet_style))

    story.append(Spacer(1,8*mm))
    story.append(HRFlowable(width="100%", thickness=0.5, color=RULE))
    story.append(Spacer(1,2*mm))
    story.append(Paragraph(f"Prepared on {datetime.now().strftime('%B %d, %Y')}  ·  ATS-Optimized CV  ·  Dawood Recruitment", footer_style))
    doc.build(story); buffer.seek(0); return buffer

# ── SESSION STATE ─────────────────────────────────────────────────────────────
for k,v in [("step",0),("data",{}),("cv_text",None)]:
    if k not in st.session_state: st.session_state[k] = v

# ── BRAND BAR ─────────────────────────────────────────────────────────────────
st.markdown("""
<div class="brand-bar">
  <div class="brand-name">Dawood</div>
  <div class="brand-tag">Recruitment</div>
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# STEP 0 — LANDING
# ══════════════════════════════════════════════════════════════════════════════
if st.session_state.step == 0:
    st.markdown("""
    <div class="hero-eyebrow">Career Assessment Platform</div>
    <div class="hero-title">ابدأ<br><em>مسيرتك</em><br>المهنية</div>
    <div class="hero-sub">
      منصة متخصصة في تقييم المرشحين<br>
      وإعداد سيرة ذاتية احترافية جاهزة للتقديم
    </div>
    <div class="stats-grid">
      <div class="stat-cell"><div class="stat-num">4</div><div class="stat-lbl">دقائق</div></div>
      <div class="stat-cell"><div class="stat-num">ATS</div><div class="stat-lbl">محسّن</div></div>
      <div class="stat-cell"><div class="stat-num">PDF</div><div class="stat-lbl">احترافي</div></div>
    </div>
    """, unsafe_allow_html=True)

    if st.button("ابدأ التقييم الآن", use_container_width=True):
        st.session_state.step = 1
        st.rerun()

# ══════════════════════════════════════════════════════════════════════════════
# STEP 1 — BASIC INFO
# ══════════════════════════════════════════════════════════════════════════════
elif st.session_state.step == 1:
    st.progress(33)
    st.markdown('<div class="sec-label">الخطوة الأولى — البيانات الشخصية</div>', unsafe_allow_html=True)

    with st.form("basic_info"):
        name      = st.text_input("الاسم الكامل",        value=st.session_state.data.get("name",""))
        email     = st.text_input("البريد الإلكتروني",   value=st.session_state.data.get("email",""))
        phone     = st.text_input("رقم الهاتف",          value=st.session_state.data.get("phone",""))
        city      = st.selectbox("المدينة",              ["اختر","القاهرة","الإسكندرية","الجيزة","المنصورة","أخرى"])
        education = st.selectbox("المؤهل الدراسي",       ["اختر","طالب جامعي","بكالوريوس","دبلوم","ماجستير","ثانوية"])
        major     = st.text_input("التخصص",              value=st.session_state.data.get("major",""))
        submitted = st.form_submit_button("التالي", use_container_width=True)

        if submitted:
            if not name or not email or not phone:
                st.error("⚠️ من فضلك أكمل الاسم والبريد ورقم الهاتف")
            elif city == "اختر":
                st.error("⚠️ من فضلك اختر المدينة")
            elif education == "اختر":
                st.error("⚠️ من فضلك اختر المؤهل")
            else:
                st.session_state.data.update({"name":name,"email":email,"phone":phone,"city":city,"education":education,"major":major})
                st.session_state.step = 2
                st.rerun()

# ══════════════════════════════════════════════════════════════════════════════
# STEP 2 — PERSONALITY
# ══════════════════════════════════════════════════════════════════════════════
elif st.session_state.step == 2:
    st.progress(66)
    st.markdown('<div class="sec-label">الخطوة الثانية — الملف المهني</div>', unsafe_allow_html=True)

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
            back = st.form_submit_button("رجوع", use_container_width=True)
        with col_next:
            submitted2 = st.form_submit_button("إنشاء السيرة الذاتية", use_container_width=True)

        if back:
            st.session_state.step = 1
            st.rerun()
        if submitted2:
            if not open_q.strip():
                st.error("⚠️ من فضلك اكتب عن نفسك")
            else:
                st.session_state.data.update({"q1":q1,"q2":q2,"q3":q3,"q4":q4,"q5":q5,"open_q":open_q})
                st.session_state.step = 3
                st.rerun()

# ══════════════════════════════════════════════════════════════════════════════
# STEP 3 — RESULT
# ══════════════════════════════════════════════════════════════════════════════
elif st.session_state.step == 3:
    st.progress(100)
    data = st.session_state.data

    if st.session_state.cv_text is None:
        st.markdown('<div class="sec-label">جاري إعداد سيرتك الذاتية...</div>', unsafe_allow_html=True)

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

    st.markdown(f'<div class="success-banner">✓ تم إعداد سيرتك الذاتية بنجاح — {data["name"]}</div>', unsafe_allow_html=True)
    st.markdown('<div class="sec-label">معاينة السيرة الذاتية</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="cv-box">{st.session_state.cv_text}</div>', unsafe_allow_html=True)

    pdf_buffer = generate_pdf(st.session_state.cv_text, data)
    safe_name  = data['name'].replace(' ','_')

    st.download_button(
        label="تحميل السيرة الذاتية PDF",
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
        '<p style="text-align:center;font-size:12px;color:#4A5568;margin-top:20px;letter-spacing:1px;">سيتم التواصل معك قريباً</p>',
        unsafe_allow_html=True
    )
