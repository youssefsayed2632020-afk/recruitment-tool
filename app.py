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
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,600;0,700;1,400;1,600&family=Outfit:wght@200;300;400;500;600&display=swap');

:root {
  --ink:     #05080F;
  --navy:    #080E1C;
  --navy2:   #0C1525;
  --navy3:   #111D30;
  --gold:    #C8A45A;
  --gold2:   #E2C07E;
  --goldD:   #A0813A;
  --goldL:   rgba(200,164,90,0.10);
  --goldM:   rgba(200,164,90,0.20);
  --goldB:   rgba(200,164,90,0.35);
  --white:   #EDE9E0;
  --muted:   #6B7485;
  --soft:    #9BA5B5;
  --glass:   rgba(255,255,255,0.03);
  --glassH:  rgba(255,255,255,0.06);
  --border:  rgba(200,164,90,0.15);
  --borderW: rgba(255,255,255,0.06);
}

/* ── BASE ── */
* { box-sizing: border-box; }

.stApp {
  background: var(--ink) !important;
  font-family: 'Outfit', sans-serif !important;
  background-image:
    radial-gradient(ellipse 90% 60% at 15% -5%,  rgba(200,164,90,0.06) 0%, transparent 55%),
    radial-gradient(ellipse 70% 50% at 85% 105%, rgba(200,164,90,0.04) 0%, transparent 50%),
    radial-gradient(ellipse 50% 40% at 50%  50%, rgba(12,21,37,0.8)    0%, transparent 100%) !important;
}

#MainMenu, footer, header { visibility: hidden !important; }
.stDeployButton { display: none !important; }
.main .block-container {
  max-width: 640px !important;
  padding: 0 1.5rem 7rem !important;
  margin: 0 auto !important;
}

/* ══════════════════════════════════════
   BRAND BAR
══════════════════════════════════════ */
.brand-bar {
  padding: 32px 0 28px;
  margin-bottom: 60px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  position: relative;
}
.brand-bar::after {
  content: '';
  position: absolute;
  bottom: 0; left: 0; right: 0;
  height: 1px;
  background: linear-gradient(90deg, var(--gold) 0%, transparent 100%);
  opacity: 0.3;
}
.brand-name {
  font-family: 'Playfair Display', serif;
  font-size: 18px; font-weight: 600;
  color: var(--white); letter-spacing: 6px;
  text-transform: uppercase;
}
.brand-dot {
  width: 4px; height: 4px;
  background: var(--gold);
  border-radius: 50%;
  display: inline-block;
  margin: 0 2px 1px;
  vertical-align: middle;
}
.brand-tag {
  font-family: 'Outfit', sans-serif;
  font-size: 8px; letter-spacing: 4px;
  text-transform: uppercase;
  color: var(--gold); font-weight: 300;
}

/* ══════════════════════════════════════
   HERO
══════════════════════════════════════ */
.hero-eyebrow {
  font-size: 8px; letter-spacing: 5px;
  text-transform: uppercase; color: var(--gold);
  margin-bottom: 24px; font-weight: 400;
  display: flex; align-items: center; gap: 14px;
  opacity: 0.85;
}
.hero-eyebrow::before {
  content: '◈';
  font-size: 10px;
}
.hero-eyebrow::after {
  content: '';
  flex: 1; height: 1px;
  background: linear-gradient(90deg, var(--goldB), transparent);
}

.hero-title {
  font-family: 'Playfair Display', serif;
  font-size: 64px; font-weight: 400;
  color: var(--white); line-height: 1.0;
  margin-bottom: 8px; letter-spacing: -1.5px;
}
.hero-title em {
  color: var(--gold);
  font-style: italic;
  font-weight: 400;
}
.hero-title span {
  display: block;
  font-size: 52px;
}

.hero-sub {
  font-size: 14px; color: var(--muted);
  font-weight: 300; line-height: 1.85;
  margin: 28px 0 52px; max-width: 380px;
  letter-spacing: 0.2px;
}
.hero-sub strong {
  color: var(--soft);
  font-weight: 400;
}

/* ══════════════════════════════════════
   STATS GRID
══════════════════════════════════════ */
.stats-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1px;
  background: var(--border);
  border: 1px solid var(--border);
  border-radius: 4px;
  overflow: hidden;
  margin-bottom: 52px;
}
.stat-cell {
  background: var(--navy2);
  padding: 28px 16px;
  text-align: center;
  position: relative;
  transition: background 0.3s;
}
.stat-cell::before {
  content: '';
  position: absolute;
  top: 0; left: 50%; transform: translateX(-50%);
  width: 30px; height: 1px;
  background: var(--gold);
  opacity: 0;
  transition: opacity 0.3s;
}
.stat-cell:hover { background: var(--navy3); }
.stat-cell:hover::before { opacity: 1; }

.stat-num {
  font-family: 'Playfair Display', serif;
  font-size: 28px; font-weight: 600;
  color: var(--gold); line-height: 1;
  margin-bottom: 8px; letter-spacing: 1px;
}
.stat-lbl {
  font-size: 7.5px; letter-spacing: 3px;
  text-transform: uppercase; color: var(--muted);
  font-weight: 400;
}

/* ══════════════════════════════════════
   SECTION LABEL
══════════════════════════════════════ */
.sec-label {
  font-size: 8px; letter-spacing: 4px;
  text-transform: uppercase; color: var(--gold);
  margin-bottom: 32px; padding-bottom: 14px;
  border-bottom: 1px solid var(--border);
  display: flex; align-items: center; gap: 10px;
  font-weight: 400;
}
.sec-label::before { content: '—'; opacity: 0.5; }

/* ══════════════════════════════════════
   SUCCESS BANNER
══════════════════════════════════════ */
.success-banner {
  background: linear-gradient(135deg, rgba(200,164,90,0.08), rgba(200,164,90,0.03));
  border: 1px solid var(--goldB);
  border-left: 2px solid var(--gold);
  padding: 16px 20px;
  border-radius: 3px;
  color: var(--gold2);
  font-size: 13px;
  letter-spacing: 0.5px;
  margin-bottom: 32px;
  display: flex;
  align-items: center;
  gap: 12px;
}
.success-banner::before { content: '✦'; font-size: 12px; opacity: 0.7; }

/* ══════════════════════════════════════
   CV BOX
══════════════════════════════════════ */
.cv-box {
  background: var(--navy2);
  border: 1px solid var(--borderW);
  border-top: 1px solid var(--border);
  border-radius: 4px;
  padding: 32px 28px;
  font-size: 12.5px;
  line-height: 1.9;
  color: var(--soft);
  white-space: pre-wrap;
  font-family: 'Outfit', sans-serif;
  font-weight: 300;
  margin-bottom: 28px;
  box-shadow: 0 20px 60px rgba(0,0,0,0.4), inset 0 1px 0 rgba(255,255,255,0.04);
}

/* ══════════════════════════════════════
   INPUTS
══════════════════════════════════════ */
.stTextInput label, .stTextArea label,
.stSelectbox label, .stRadio > label {
  font-size: 8.5px !important;
  letter-spacing: 3px !important;
  text-transform: uppercase !important;
  color: var(--muted) !important;
  font-weight: 400 !important;
  font-family: 'Outfit', sans-serif !important;
  margin-bottom: 8px !important;
}

.stTextInput > div > div > input {
  background: var(--navy2) !important;
  border: 1px solid var(--borderW) !important;
  border-radius: 3px !important;
  color: var(--white) !important;
  font-family: 'Outfit', sans-serif !important;
  font-size: 14px !important;
  font-weight: 300 !important;
  padding: 15px 18px !important;
  transition: all 0.25s !important;
  letter-spacing: 0.3px !important;
}
.stTextInput > div > div > input:focus {
  border-color: var(--gold) !important;
  background: var(--navy3) !important;
  box-shadow: 0 0 0 3px rgba(200,164,90,0.08) !important;
}
.stTextInput > div > div > input::placeholder { color: var(--muted) !important; opacity: 0.5 !important; }

.stTextArea > div > div > textarea {
  background: var(--navy2) !important;
  border: 1px solid var(--borderW) !important;
  border-radius: 3px !important;
  color: var(--white) !important;
  font-family: 'Outfit', sans-serif !important;
  font-size: 14px !important;
  font-weight: 300 !important;
  padding: 15px 18px !important;
  transition: all 0.25s !important;
  line-height: 1.7 !important;
}
.stTextArea > div > div > textarea:focus {
  border-color: var(--gold) !important;
  background: var(--navy3) !important;
  box-shadow: 0 0 0 3px rgba(200,164,90,0.08) !important;
}

.stSelectbox > div > div {
  background: var(--navy2) !important;
  border: 1px solid var(--borderW) !important;
  border-radius: 3px !important;
  color: var(--white) !important;
  padding: 4px 0 !important;
  transition: all 0.25s !important;
}
.stSelectbox > div > div:focus-within {
  border-color: var(--gold) !important;
  box-shadow: 0 0 0 3px rgba(200,164,90,0.08) !important;
}
.stSelectbox > div > div > div { color: var(--white) !important; font-family: 'Outfit', sans-serif !important; font-weight: 300 !important; }
.stSelectbox svg { fill: var(--muted) !important; }

/* ── RADIO ── */
.stRadio > div { gap: 8px !important; flex-direction: column !important; }
.stRadio > div > label {
  background: var(--navy2) !important;
  border: 1px solid var(--borderW) !important;
  border-radius: 3px !important;
  padding: 14px 18px !important;
  color: var(--soft) !important;
  font-size: 13.5px !important;
  font-family: 'Outfit', sans-serif !important;
  font-weight: 300 !important;
  transition: all 0.2s !important;
  cursor: pointer !important;
  letter-spacing: 0.2px !important;
}
.stRadio > div > label:hover {
  border-color: var(--goldB) !important;
  color: var(--white) !important;
  background: var(--navy3) !important;
  transform: translateX(4px) !important;
}
[data-baseweb="radio"] input:checked + div { border-color: var(--gold) !important; }

/* ── BUTTONS ── */
.stButton > button {
  background: transparent !important;
  border: 1px solid var(--goldB) !important;
  color: var(--gold) !important;
  border-radius: 3px !important;
  font-family: 'Outfit', sans-serif !important;
  font-size: 8.5px !important;
  font-weight: 500 !important;
  letter-spacing: 4px !important;
  text-transform: uppercase !important;
  padding: 18px 36px !important;
  transition: all 0.25s !important;
  position: relative !important;
  overflow: hidden !important;
}
.stButton > button::before {
  content: '' !important;
  position: absolute !important;
  inset: 0 !important;
  background: linear-gradient(135deg, var(--gold), var(--goldD)) !important;
  opacity: 0 !important;
  transition: opacity 0.25s !important;
}
.stButton > button:hover {
  color: var(--ink) !important;
  border-color: var(--gold) !important;
  transform: translateY(-2px) !important;
  box-shadow: 0 12px 32px rgba(200,164,90,0.2), 0 4px 12px rgba(0,0,0,0.3) !important;
}
.stButton > button:hover::before { opacity: 1 !important; }
.stButton > button span { position: relative; z-index: 1; }

.stDownloadButton > button {
  background: linear-gradient(135deg, var(--gold), var(--goldD)) !important;
  border: 1px solid transparent !important;
  color: var(--ink) !important;
  border-radius: 3px !important;
  font-family: 'Outfit', sans-serif !important;
  font-size: 8.5px !important;
  font-weight: 600 !important;
  letter-spacing: 4px !important;
  text-transform: uppercase !important;
  padding: 18px 36px !important;
  transition: all 0.25s !important;
}
.stDownloadButton > button:hover {
  background: linear-gradient(135deg, var(--gold2), var(--gold)) !important;
  box-shadow: 0 16px 40px rgba(200,164,90,0.3), 0 4px 16px rgba(0,0,0,0.3) !important;
  transform: translateY(-2px) !important;
}

/* ── PROGRESS ── */
.stProgress > div > div > div > div {
  background: linear-gradient(90deg, var(--goldD), var(--gold), var(--gold2)) !important;
  border-radius: 2px !important;
}
.stProgress > div > div {
  background: rgba(255,255,255,0.05) !important;
  border-radius: 2px !important;
  height: 3px !important;
}

/* ── SPINNER ── */
.stSpinner > div { border-top-color: var(--gold) !important; }

/* ── FORM CONTAINER ── */
[data-testid="stForm"] {
  background: var(--navy2) !important;
  border: 1px solid var(--borderW) !important;
  border-top: 1px solid var(--border) !important;
  border-radius: 4px !important;
  padding: 32px 28px !important;
  box-shadow: 0 24px 64px rgba(0,0,0,0.35) !important;
}

/* ── ERROR ── */
.stAlert {
  background: rgba(180,60,60,0.08) !important;
  border: 1px solid rgba(200,80,80,0.25) !important;
  border-left: 2px solid rgba(200,80,80,0.6) !important;
  border-radius: 3px !important;
  color: #E0A0A0 !important;
}

/* ── DIVIDER ── */
hr { border-color: var(--border) !important; opacity: 0.4 !important; }

/* ── SCROLLBAR ── */
::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: var(--navy); }
::-webkit-scrollbar-thumb { background: var(--goldD); border-radius: 2px; }
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
  <div class="brand-name">Dawood<span class="brand-dot"></span></div>
  <div class="brand-tag">Recruitment</div>
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# STEP 0 — LANDING
# ══════════════════════════════════════════════════════════════════════════════
if st.session_state.step == 0:
    st.markdown("""
    <div class="hero-eyebrow">Career Assessment Platform</div>
    <div class="hero-title">
      ابدأ
      <span><em>مسيرتك</em></span>
      المهنية
    </div>
    <div class="hero-sub">
      منصة متخصصة في تقييم المرشحين<br>
      وإعداد <strong>سيرة ذاتية احترافية</strong> جاهزة للتقديم
    </div>
    <div class="stats-grid">
      <div class="stat-cell">
        <div class="stat-num">4</div>
        <div class="stat-lbl">دقائق فقط</div>
      </div>
      <div class="stat-cell">
        <div class="stat-num">ATS</div>
        <div class="stat-lbl">محسّن بالكامل</div>
      </div>
      <div class="stat-cell">
        <div class="stat-num">PDF</div>
        <div class="stat-lbl">احترافي</div>
      </div>
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
        submitted = st.form_submit_button("التالي ←", use_container_width=True)

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
        open_q = st.text_area("عرّف عن نفسك في 3 جمل", value=st.session_state.data.get("open_q",""), height=110)

        col_back, col_next = st.columns(2)
        with col_back:
            back = st.form_submit_button("← رجوع", use_container_width=True)
        with col_next:
            submitted2 = st.form_submit_button("إنشاء السيرة الذاتية ✦", use_container_width=True)

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

    st.markdown(f'<div class="success-banner">تم إعداد سيرتك الذاتية بنجاح — {data["name"]}</div>', unsafe_allow_html=True)
    st.markdown('<div class="sec-label">معاينة السيرة الذاتية</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="cv-box">{st.session_state.cv_text}</div>', unsafe_allow_html=True)

    pdf_buffer = generate_pdf(st.session_state.cv_text, data)
    safe_name  = data['name'].replace(' ','_')

    st.download_button(
        label="تحميل السيرة الذاتية — PDF",
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
        '<p style="text-align:center;font-size:11px;color:#3A4558;margin-top:28px;letter-spacing:2px;font-family:Outfit,sans-serif;">سيتم التواصل معك قريباً</p>',
        unsafe_allow_html=True
    )
