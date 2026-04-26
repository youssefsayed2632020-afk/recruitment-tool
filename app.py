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
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,600;1,300;1,400&family=Outfit:wght@200;300;400;500;600&display=swap');

:root {
  --ink:    #04060E;
  --navy:   #070A18;
  --navy2:  #0A0F20;
  --navy3:  #0E1428;
  --gold:   #C8A45A;
  --gold2:  #E2C07E;
  --gold3:  #F5DFA0;
  --goldD:  #9A7C38;
  --goldB:  rgba(200,164,90,0.28);
  --goldL:  rgba(200,164,90,0.07);
  --goldM:  rgba(200,164,90,0.14);
  --white:  #EDE9DF;
  --muted:  #5C6478;
  --soft:   #8E98B0;
  --mid:    #B0B8CC;
  --border: rgba(200,164,90,0.12);
  --borderW:rgba(255,255,255,0.05);
  --borderG:rgba(200,164,90,0.20);
}

* { box-sizing: border-box; }

.stApp {
  background: var(--ink) !important;
  font-family: 'Outfit', sans-serif !important;
  background-image:
    radial-gradient(ellipse 110% 70% at 10% -10%, rgba(200,164,90,0.055) 0%, transparent 50%),
    radial-gradient(ellipse 80%  60% at 90% 110%, rgba(200,164,90,0.035) 0%, transparent 50%),
    radial-gradient(ellipse 60%  80% at 50%  50%, rgba(10,18,40,0.9)     0%, transparent 100%) !important;
}

#MainMenu, footer, header { visibility: hidden !important; }
.stDeployButton { display: none !important; }

.main .block-container {
  max-width: 640px !important;
  padding: 0 1.5rem 8rem !important;
  margin: 0 auto !important;
}

::-webkit-scrollbar { width: 3px; }
::-webkit-scrollbar-track { background: var(--ink); }
::-webkit-scrollbar-thumb { background: linear-gradient(180deg, var(--goldD), var(--gold)); border-radius: 2px; }

/* ═══ KEYFRAMES ═══ */
@keyframes fadeUp {
  from { opacity: 0; transform: translateY(16px); }
  to   { opacity: 1; transform: translateY(0); }
}
@keyframes fadeIn {
  from { opacity: 0; }
  to   { opacity: 1; }
}
@keyframes shimmer {
  0%   { left: -100%; }
  100% { left: 200%;  }
}
@keyframes pulseGold {
  0%,100% { opacity: 0.5; }
  50%     { opacity: 1;   }
}
@keyframes dotBeat {
  0%,100% { transform: scale(1);   }
  50%     { transform: scale(1.7); }
}
@keyframes lineGrow {
  from { width: 0; opacity: 0; }
  to   { width: 100%; opacity: 1; }
}
@keyframes softGlow {
  0%,100% { box-shadow: 0 0 0 0 rgba(200,164,90,0); }
  50%     { box-shadow: 0 0 20px 2px rgba(200,164,90,0.10); }
}

/* ═══ BRAND BAR ═══ */
.brand-bar {
  padding: 34px 0 28px;
  margin-bottom: 64px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  position: relative;
  animation: fadeIn 0.8s ease both;
}
.brand-bar::after {
  content: '';
  position: absolute;
  bottom: 0; left: 0; right: 0;
  height: 1px;
  background: linear-gradient(90deg, var(--gold) 0%, rgba(200,164,90,0.2) 55%, transparent 90%);
  animation: lineGrow 1.1s cubic-bezier(0.4,0,0.2,1) 0.2s both;
}
.brand-name {
  font-family: 'Cormorant Garamond', serif;
  font-size: 20px; font-weight: 600;
  color: var(--white); letter-spacing: 7px;
  text-transform: uppercase;
}
.brand-dot {
  width: 4px; height: 4px;
  background: var(--gold);
  border-radius: 50%;
  display: inline-block;
  margin: 0 2px 2px;
  vertical-align: middle;
  animation: dotBeat 2.8s ease-in-out infinite;
}
.brand-tag {
  font-size: 8px; letter-spacing: 5px;
  text-transform: uppercase;
  color: var(--gold); font-weight: 300;
  opacity: 0.65;
}

/* ═══ HERO ═══ */
.hero-eyebrow {
  font-size: 8px; letter-spacing: 5px;
  text-transform: uppercase; color: var(--gold);
  margin-bottom: 26px; font-weight: 400;
  display: flex; align-items: center; gap: 14px;
  opacity: 0;
  animation: fadeUp 0.7s ease 0.25s both;
}
.hero-eyebrow::before {
  content: '◈'; font-size: 10px;
  animation: pulseGold 3s ease-in-out infinite;
}
.hero-eyebrow::after {
  content: ''; flex: 1; height: 1px;
  background: linear-gradient(90deg, var(--goldB), transparent);
}

.hero-title {
  font-family: 'Cormorant Garamond', serif;
  font-size: 68px; font-weight: 400;
  color: var(--white); line-height: 1.0;
  margin-bottom: 8px; letter-spacing: -1px;
  opacity: 0;
  animation: fadeUp 0.8s ease 0.4s both;
}
.hero-title em   { color: var(--gold); font-style: italic; }
.hero-title span { display: block; font-size: 54px; }

.hero-sub {
  font-size: 14px; color: var(--muted);
  font-weight: 300; line-height: 1.9;
  margin: 28px 0 52px; max-width: 380px;
  letter-spacing: 0.2px;
  opacity: 0;
  animation: fadeUp 0.8s ease 0.55s both;
}
.hero-sub strong { color: var(--soft); font-weight: 400; }

/* ═══ STATS GRID ═══ */
.stats-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1px;
  background: var(--border);
  border: 1px solid var(--border);
  border-radius: 5px;
  overflow: hidden;
  margin-bottom: 52px;
  opacity: 0;
  animation: fadeUp 0.8s ease 0.7s both;
}
.stat-cell {
  background: var(--navy2);
  padding: 30px 16px;
  text-align: center;
  position: relative;
  overflow: hidden;
  transition: background 0.35s ease;
}
/* shimmer sweep */
.stat-cell::after {
  content: '';
  position: absolute;
  top: 0; left: -100%; width: 55%; height: 100%;
  background: linear-gradient(120deg, transparent, rgba(200,164,90,0.06), transparent);
  transition: none;
  pointer-events: none;
}
.stat-cell:hover::after { animation: shimmer 0.65s ease forwards; }
/* top accent line */
.stat-cell::before {
  content: '';
  position: absolute;
  top: 0; left: 50%; transform: translateX(-50%);
  width: 0; height: 1px;
  background: var(--gold);
  transition: width 0.4s ease;
}
.stat-cell:hover { background: var(--navy3); }
.stat-cell:hover::before { width: 48%; }

.stat-num {
  font-family: 'Cormorant Garamond', serif;
  font-size: 30px; font-weight: 600;
  color: var(--gold); line-height: 1;
  margin-bottom: 8px; letter-spacing: 1px;
}
.stat-lbl {
  font-size: 7.5px; letter-spacing: 3px;
  text-transform: uppercase; color: var(--muted); font-weight: 400;
}

/* ═══ SECTION LABEL ═══ */
.sec-label {
  font-size: 8px; letter-spacing: 4px;
  text-transform: uppercase; color: var(--gold);
  margin-bottom: 32px; padding-bottom: 14px;
  border-bottom: 1px solid var(--border);
  display: flex; align-items: center; gap: 10px;
  font-weight: 400;
  animation: fadeIn 0.6s ease both;
}
.sec-label::before { content: '—'; opacity: 0.45; }

/* ═══ SUCCESS BANNER ═══ */
.success-banner {
  background: linear-gradient(135deg, rgba(200,164,90,0.09), rgba(200,164,90,0.03));
  border: 1px solid var(--goldB);
  border-left: 2px solid var(--gold);
  padding: 16px 20px;
  border-radius: 4px;
  color: var(--gold2);
  font-size: 13px;
  letter-spacing: 0.4px;
  margin-bottom: 32px;
  display: flex; align-items: center; gap: 12px;
  animation: fadeUp 0.6s ease both, softGlow 3.5s ease 0.8s infinite;
}
.success-banner::before {
  content: '✦'; font-size: 12px; opacity: 0.65;
  animation: pulseGold 2.2s ease-in-out infinite;
}

/* ═══ CV BOX ═══ */
.cv-box {
  background: var(--navy2);
  border: 1px solid var(--borderW);
  border-top: 1px solid var(--borderG);
  border-radius: 5px;
  padding: 34px 30px;
  font-size: 12.5px; line-height: 1.95;
  color: var(--soft);
  white-space: pre-wrap;
  font-family: 'Outfit', sans-serif; font-weight: 300;
  margin-bottom: 28px;
  box-shadow: 0 24px 64px rgba(0,0,0,0.5), inset 0 1px 0 rgba(255,255,255,0.03);
  animation: fadeUp 0.7s ease both;
  position: relative; overflow: hidden;
}
/* entry shimmer across the top border */
.cv-box::before {
  content: '';
  position: absolute;
  top: 0; left: -100%; width: 55%; height: 1px;
  background: linear-gradient(90deg, transparent, rgba(200,164,90,0.55), transparent);
  animation: shimmer 2s ease 0.4s both;
}

/* ═══ PROGRESS ═══ */
.stProgress > div > div > div > div {
  background: linear-gradient(90deg, var(--goldD), var(--gold), var(--gold2)) !important;
  border-radius: 2px !important;
  position: relative; overflow: hidden;
}
.stProgress > div > div > div > div::after {
  content: '';
  position: absolute;
  top: 0; left: -100%; width: 55%; height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255,255,255,0.25), transparent);
  animation: shimmer 1.6s ease-in-out infinite;
}
.stProgress > div > div {
  background: rgba(255,255,255,0.05) !important;
  border-radius: 2px !important; height: 2px !important;
}

/* ═══ INPUTS ═══ */
.stTextInput label, .stTextArea label,
.stSelectbox label, .stRadio > label {
  font-size: 8.5px !important; letter-spacing: 3px !important;
  text-transform: uppercase !important; color: var(--muted) !important;
  font-weight: 400 !important; font-family: 'Outfit', sans-serif !important;
  margin-bottom: 8px !important;
}

.stTextInput > div > div > input {
  background: var(--navy2) !important;
  border: 1px solid var(--borderW) !important;
  border-radius: 4px !important; color: var(--white) !important;
  font-family: 'Outfit', sans-serif !important;
  font-size: 14px !important; font-weight: 300 !important;
  padding: 15px 18px !important;
  transition: border-color 0.3s ease, background 0.3s ease, box-shadow 0.3s ease !important;
  letter-spacing: 0.3px !important;
}
.stTextInput > div > div > input:focus {
  border-color: var(--gold) !important; background: var(--navy3) !important;
  box-shadow: 0 0 0 3px rgba(200,164,90,0.07), 0 4px 18px rgba(0,0,0,0.28) !important;
}
.stTextInput > div > div > input::placeholder { color: var(--muted) !important; opacity: 0.45 !important; }

.stTextArea > div > div > textarea {
  background: var(--navy2) !important;
  border: 1px solid var(--borderW) !important;
  border-radius: 4px !important; color: var(--white) !important;
  font-family: 'Outfit', sans-serif !important;
  font-size: 14px !important; font-weight: 300 !important;
  padding: 15px 18px !important;
  transition: border-color 0.3s ease, background 0.3s ease, box-shadow 0.3s ease !important;
  line-height: 1.75 !important;
}
.stTextArea > div > div > textarea:focus {
  border-color: var(--gold) !important; background: var(--navy3) !important;
  box-shadow: 0 0 0 3px rgba(200,164,90,0.07), 0 4px 18px rgba(0,0,0,0.28) !important;
}

.stSelectbox > div > div {
  background: var(--navy2) !important;
  border: 1px solid var(--borderW) !important;
  border-radius: 4px !important; color: var(--white) !important;
  padding: 4px 0 !important;
  transition: border-color 0.3s ease, box-shadow 0.3s ease !important;
}
.stSelectbox > div > div:focus-within {
  border-color: var(--gold) !important;
  box-shadow: 0 0 0 3px rgba(200,164,90,0.07) !important;
}
.stSelectbox > div > div > div { color: var(--white) !important; font-family: 'Outfit', sans-serif !important; font-weight: 300 !important; }
.stSelectbox svg { fill: var(--muted) !important; }

/* ─── RADIO ─── */
.stRadio > div { gap: 8px !important; flex-direction: column !important; }
.stRadio > div > label {
  background: var(--navy2) !important;
  border: 1px solid var(--borderW) !important;
  border-radius: 4px !important; padding: 14px 18px !important;
  color: var(--soft) !important; font-size: 13.5px !important;
  font-family: 'Outfit', sans-serif !important; font-weight: 300 !important;
  transition: border-color 0.25s ease, background 0.25s ease, transform 0.25s ease, color 0.25s ease !important;
  cursor: pointer !important; letter-spacing: 0.2px !important;
}
.stRadio > div > label:hover {
  border-color: var(--goldB) !important; color: var(--white) !important;
  background: var(--navy3) !important; transform: translateX(5px) !important;
}
[data-baseweb="radio"] input:checked + div { border-color: var(--gold) !important; }

/* ─── BUTTONS ─── */
.stButton > button {
  background: transparent !important;
  border: 1px solid var(--goldB) !important;
  color: var(--gold) !important; border-radius: 4px !important;
  font-family: 'Outfit', sans-serif !important;
  font-size: 8.5px !important; font-weight: 500 !important;
  letter-spacing: 4px !important; text-transform: uppercase !important;
  padding: 18px 36px !important;
  transition: color 0.3s ease, border-color 0.3s ease, transform 0.3s ease, box-shadow 0.3s ease !important;
  position: relative !important; overflow: hidden !important;
}
.stButton > button::before {
  content: '' !important; position: absolute !important; inset: 0 !important;
  background: linear-gradient(135deg, var(--gold) 0%, var(--goldD) 100%) !important;
  opacity: 0 !important; transition: opacity 0.3s ease !important;
}
.stButton > button::after {
  content: '' !important; position: absolute !important;
  top: 0; left: -100%; width: 55%; height: 100% !important;
  background: linear-gradient(120deg, transparent, rgba(255,255,255,0.10), transparent) !important;
}
.stButton > button:hover {
  color: var(--ink) !important; border-color: var(--gold) !important;
  transform: translateY(-2px) !important;
  box-shadow: 0 10px 28px rgba(200,164,90,0.18), 0 4px 10px rgba(0,0,0,0.25) !important;
}
.stButton > button:hover::before { opacity: 1 !important; }
.stButton > button:hover::after  { animation: shimmer 0.55s ease forwards !important; }
.stButton > button span { position: relative; z-index: 1; }

.stDownloadButton > button {
  background: linear-gradient(135deg, var(--gold) 0%, var(--goldD) 100%) !important;
  border: 1px solid transparent !important; color: var(--ink) !important;
  border-radius: 4px !important; font-family: 'Outfit', sans-serif !important;
  font-size: 8.5px !important; font-weight: 600 !important;
  letter-spacing: 4px !important; text-transform: uppercase !important;
  padding: 18px 36px !important;
  transition: transform 0.3s ease, box-shadow 0.3s ease, background 0.3s ease !important;
  position: relative !important; overflow: hidden !important;
}
.stDownloadButton > button::after {
  content: '' !important; position: absolute !important;
  top: 0; left: -100%; width: 55%; height: 100% !important;
  background: linear-gradient(120deg, transparent, rgba(255,255,255,0.18), transparent) !important;
}
.stDownloadButton > button:hover {
  background: linear-gradient(135deg, var(--gold2) 0%, var(--gold) 100%) !important;
  box-shadow: 0 14px 36px rgba(200,164,90,0.28), 0 4px 12px rgba(0,0,0,0.25) !important;
  transform: translateY(-2px) !important;
}
.stDownloadButton > button:hover::after { animation: shimmer 0.55s ease forwards !important; }

/* ─── SPINNER ─── */
.stSpinner > div { border-top-color: var(--gold) !important; }

/* ─── FORM CONTAINER ─── */
[data-testid="stForm"] {
  background: var(--navy2) !important;
  border: 1px solid var(--borderW) !important;
  border-top: 1px solid var(--borderG) !important;
  border-radius: 5px !important; padding: 34px 30px !important;
  box-shadow: 0 24px 64px rgba(0,0,0,0.4), inset 0 1px 0 rgba(255,255,255,0.03) !important;
  animation: fadeUp 0.7s ease both !important;
  position: relative !important; overflow: hidden !important;
}
[data-testid="stForm"]::before {
  content: '' !important; position: absolute !important;
  top: 0; left: -100%; width: 55%; height: 1px !important;
  background: linear-gradient(90deg, transparent, rgba(200,164,90,0.45), transparent) !important;
  animation: shimmer 1.4s ease 0.25s both !important;
}

/* ─── ERROR ─── */
.stAlert {
  background: rgba(160,50,50,0.07) !important;
  border: 1px solid rgba(200,80,80,0.2) !important;
  border-left: 2px solid rgba(200,80,80,0.55) !important;
  border-radius: 4px !important; color: #E0A0A0 !important;
  animation: fadeUp 0.4s ease both !important;
}

hr { border-color: var(--border) !important; opacity: 0.4 !important; }
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
