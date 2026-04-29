import streamlit as st
import google.generativeai as genai
import time
import json
import random

# ═══════════════════════════════════════════════════
#  CONFIG
# ═══════════════════════════════════════════════════
API_KEY = "PASTE_YOUR_GEMINI_API_KEY_HERE"
genai.configure(api_key=API_KEY)

st.set_page_config(
    page_title="Talently Infinity ♾️",
    page_icon="♾️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ═══════════════════════════════════════════════════
#  MASTER CSS
# ═══════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@300;400;600;700;800&family=Space+Mono:wght@400;700&display=swap');

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, .main, .block-container {
    background: #020408 !important;
    color: #e8eaf0 !important;
    font-family: 'Sora', sans-serif !important;
}

.block-container { padding: 0 !important; max-width: 100% !important; }

/* ── CANVAS BACKGROUND ── */
.bg-canvas {
    position: fixed; inset: 0; z-index: 0; overflow: hidden; pointer-events: none;
    background: radial-gradient(ellipse 80% 60% at 20% 10%, rgba(0,200,255,0.07) 0%, transparent 60%),
                radial-gradient(ellipse 60% 80% at 80% 90%, rgba(120,0,255,0.07) 0%, transparent 60%),
                radial-gradient(ellipse 40% 40% at 50% 50%, rgba(0,255,160,0.04) 0%, transparent 70%),
                #020408;
}

.grid-overlay {
    position: fixed; inset: 0; z-index: 0; pointer-events: none;
    background-image:
        linear-gradient(rgba(0,200,255,0.04) 1px, transparent 1px),
        linear-gradient(90deg, rgba(0,200,255,0.04) 1px, transparent 1px);
    background-size: 60px 60px;
    animation: gridShift 20s linear infinite;
}
@keyframes gridShift { to { background-position: 60px 60px; } }

/* ── WRAP ALL CONTENT ── */
.app-wrapper {
    position: relative; z-index: 1;
    max-width: 960px; margin: 0 auto;
    padding: 40px 24px 80px;
}

/* ── HERO ── */
.hero { text-align: center; padding: 60px 0 40px; }
.hero-badge {
    display: inline-block;
    background: rgba(0,200,255,0.08);
    border: 1px solid rgba(0,200,255,0.25);
    border-radius: 100px;
    padding: 6px 20px;
    font-size: 11px;
    letter-spacing: 3px;
    text-transform: uppercase;
    color: #00c8ff;
    margin-bottom: 24px;
    font-family: 'Space Mono', monospace;
}
.hero-title {
    font-size: clamp(2.8rem, 6vw, 5rem);
    font-weight: 800;
    line-height: 1.05;
    letter-spacing: -2px;
    background: linear-gradient(135deg, #ffffff 0%, #00c8ff 50%, #7b00ff 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 16px;
}
.hero-sub {
    font-size: 1rem;
    color: rgba(255,255,255,0.45);
    letter-spacing: 0.5px;
    font-weight: 300;
}

/* ── GLASS CARDS ── */
.glass-card {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 24px;
    padding: 36px;
    margin: 28px 0;
    backdrop-filter: blur(20px);
    position: relative;
    overflow: hidden;
}
.glass-card::before {
    content: '';
    position: absolute;
    inset: 0;
    border-radius: 24px;
    padding: 1px;
    background: linear-gradient(135deg, rgba(0,200,255,0.2), transparent 50%, rgba(123,0,255,0.2));
    -webkit-mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
    mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
    -webkit-mask-composite: xor;
    mask-composite: exclude;
    pointer-events: none;
}

.card-label {
    font-family: 'Space Mono', monospace;
    font-size: 10px;
    letter-spacing: 3px;
    text-transform: uppercase;
    color: #00c8ff;
    margin-bottom: 20px;
    display: flex;
    align-items: center;
    gap: 8px;
}
.card-label::after {
    content: '';
    flex: 1;
    height: 1px;
    background: linear-gradient(90deg, rgba(0,200,255,0.3), transparent);
}

/* ── STEP INDICATOR ── */
.step-bar {
    display: flex;
    justify-content: center;
    gap: 12px;
    margin: 32px 0;
}
.step-dot {
    width: 10px; height: 10px;
    border-radius: 50%;
    background: rgba(255,255,255,0.1);
    border: 1px solid rgba(255,255,255,0.15);
    transition: all 0.4s;
}
.step-dot.active {
    background: #00c8ff;
    box-shadow: 0 0 12px #00c8ff;
    transform: scale(1.3);
}
.step-dot.done {
    background: rgba(0,200,255,0.4);
}

/* ── INPUTS ── */
div[data-testid="stTextInput"] input,
div[data-testid="stTextArea"] textarea,
div[data-testid="stSelectbox"] div[data-baseweb="select"] {
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    border-radius: 14px !important;
    color: #fff !important;
    font-family: 'Sora', sans-serif !important;
    font-size: 0.9rem !important;
    padding: 14px 18px !important;
    transition: all 0.3s !important;
}
div[data-testid="stTextInput"] input:focus,
div[data-testid="stTextArea"] textarea:focus {
    border-color: rgba(0,200,255,0.5) !important;
    box-shadow: 0 0 0 3px rgba(0,200,255,0.08), 0 0 20px rgba(0,200,255,0.15) !important;
    outline: none !important;
}
div[data-testid="stTextInput"] label,
div[data-testid="stTextArea"] label,
div[data-testid="stSelectbox"] label {
    color: rgba(255,255,255,0.6) !important;
    font-size: 0.8rem !important;
    letter-spacing: 0.5px !important;
    font-family: 'Space Mono', monospace !important;
}

/* ── SLIDER ── */
div[data-testid="stSlider"] { padding: 8px 0; }
div[data-testid="stSlider"] .rc-slider-track { background: linear-gradient(90deg, #00c8ff, #7b00ff) !important; }
div[data-testid="stSlider"] .rc-slider-handle {
    background: #00c8ff !important;
    border-color: #00c8ff !important;
    box-shadow: 0 0 12px rgba(0,200,255,0.6) !important;
}

/* ── BUTTONS ── */
div[data-testid="stButton"] button {
    background: linear-gradient(135deg, #00c8ff 0%, #0062ff 50%, #7b00ff 100%) !important;
    border: none !important;
    border-radius: 16px !important;
    color: #fff !important;
    font-family: 'Sora', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.95rem !important;
    padding: 16px 32px !important;
    width: 100% !important;
    cursor: pointer !important;
    transition: all 0.3s !important;
    letter-spacing: 0.5px !important;
    box-shadow: 0 4px 30px rgba(0,100,255,0.35) !important;
    position: relative !important;
    overflow: hidden !important;
}
div[data-testid="stButton"] button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 40px rgba(0,100,255,0.5) !important;
}
div[data-testid="stButton"] button:active { transform: translateY(0px) !important; }

/* ── PROGRESS BAR ── */
.progress-wrap {
    background: rgba(255,255,255,0.05);
    border-radius: 100px;
    height: 6px;
    overflow: hidden;
    margin: 12px 0 4px;
}
.progress-fill {
    height: 100%;
    border-radius: 100px;
    background: linear-gradient(90deg, #00c8ff, #7b00ff);
    transition: width 0.4s ease;
    position: relative;
}
.progress-fill::after {
    content: '';
    position: absolute;
    right: 0; top: 50%;
    transform: translateY(-50%);
    width: 12px; height: 12px;
    background: #fff;
    border-radius: 50%;
    box-shadow: 0 0 10px #00c8ff;
}

/* ── SCAN ANIMATION ── */
@keyframes scanLine {
    0% { top: -5%; opacity: 0; }
    10% { opacity: 1; }
    90% { opacity: 1; }
    100% { top: 105%; opacity: 0; }
}
.scan-container {
    position: relative;
    background: rgba(0,200,255,0.03);
    border: 1px solid rgba(0,200,255,0.15);
    border-radius: 16px;
    padding: 40px 24px;
    text-align: center;
    overflow: hidden;
}
.scan-line {
    position: absolute;
    left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, transparent, #00c8ff, transparent);
    animation: scanLine 2s linear infinite;
    box-shadow: 0 0 20px rgba(0,200,255,0.8);
}
.scan-text {
    font-family: 'Space Mono', monospace;
    font-size: 0.85rem;
    color: #00c8ff;
    letter-spacing: 2px;
}
@keyframes blink { 0%,100% { opacity: 1; } 50% { opacity: 0.2; } }
.cursor { animation: blink 1s infinite; }

/* ── RESULT BLOCKS ── */
.result-header {
    font-family: 'Space Mono', monospace;
    font-size: 10px;
    letter-spacing: 3px;
    color: #00c8ff;
    text-transform: uppercase;
    margin-bottom: 16px;
    padding-bottom: 12px;
    border-bottom: 1px solid rgba(0,200,255,0.15);
}

.score-ring-wrap {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 24px 0;
}
.score-number {
    font-size: 4rem;
    font-weight: 800;
    background: linear-gradient(135deg, #00c8ff, #7b00ff);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    line-height: 1;
}
.score-label {
    font-size: 0.75rem;
    letter-spacing: 2px;
    color: rgba(255,255,255,0.4);
    font-family: 'Space Mono', monospace;
    margin-top: 8px;
}

div[data-testid="stTextArea"] textarea {
    font-family: 'Space Mono', monospace !important;
    font-size: 0.8rem !important;
    line-height: 1.7 !important;
    color: #c8fffe !important;
}

/* HIDE streamlit chrome */
#MainMenu, footer, header { display: none !important; }
div[data-testid="stDecoration"] { display: none !important; }
.stDeployButton { display: none !important; }
</style>

<div class="bg-canvas"></div>
<div class="grid-overlay"></div>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════
#  SESSION STATE
# ═══════════════════════════════════════════════════
defaults = {
    "step": 1,
    "data": {},
    "result": {},
    "progress": 0,
    "scanning": False,
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ═══════════════════════════════════════════════════
#  PATHS CONFIG
# ═══════════════════════════════════════════════════
PATHS = {
    "💻 Software Engineering": {"icon": "💻", "keywords": "Python, system design, APIs, scalability"},
    "📊 Data Science / AI": {"icon": "📊", "keywords": "ML, analytics, Python, statistical modeling"},
    "🚀 Technical Sales": {"icon": "🚀", "keywords": "B2B, SaaS, pipeline, quota, demos"},
    "🎯 Product Management": {"icon": "🎯", "keywords": "roadmap, agile, stakeholders, OKRs"},
    "🤝 Customer Success": {"icon": "🤝", "keywords": "NPS, churn, onboarding, SLA, retention"},
    "⚙️ IT Operations / DevOps": {"icon": "⚙️", "keywords": "cloud, CI/CD, infrastructure, SRE"},
    "📣 Digital Marketing": {"icon": "📣", "keywords": "SEO, SEM, funnels, analytics, CRO"},
    "👥 HR / Talent Acquisition": {"icon": "👥", "keywords": "recruitment, employer brand, HRIS, culture"},
    "💰 Finance / Accounting": {"icon": "💰", "keywords": "FP&A, reporting, compliance, forecasting"},
    "🎨 UX / Product Design": {"icon": "🎨", "keywords": "Figma, user research, prototyping, accessibility"},
}

LEVELS = {
    "🌱 Fresher (0 yrs)": 0,
    "⚡ Junior (1–3 yrs)": 1,
    "🔥 Mid-Level (3–6 yrs)": 3,
    "💎 Senior (6–10 yrs)": 6,
    "👑 Executive (10+ yrs)": 10,
}

# ═══════════════════════════════════════════════════
#  STEP INDICATOR
# ═══════════════════════════════════════════════════
def render_steps(current):
    dots = ""
    for i in range(1, 5):
        cls = "active" if i == current else ("done" if i < current else "step-dot")
        if i == current:
            dots += f'<div class="step-dot active"></div>'
        elif i < current:
            dots += f'<div class="step-dot done"></div>'
        else:
            dots += f'<div class="step-dot"></div>'
    st.markdown(f'<div class="step-bar">{dots}</div>', unsafe_allow_html=True)

# ═══════════════════════════════════════════════════
#  THE MEGA PROMPT
# ═══════════════════════════════════════════════════
def build_prompt(data):
    return f"""
You are TALENTLY INFINITY — the world's most advanced AI career architect.
Respond ONLY with valid JSON. No markdown, no extra text. Use this exact structure:

{{
  "cv": {{
    "name": "{data['name']}",
    "title": "<Powerful professional title for {data['path']}>",
    "summary": "<3-sentence executive summary with power verbs, quantified value, and ATS keywords for {data['path']}>",
    "experience": [
      {{
        "title": "<Role title>",
        "company": "<Company type e.g. Series B SaaS startup>",
        "period": "20XX – 20XX",
        "bullets": [
          "<Achievement 1: Action verb + what + quantified result>",
          "<Achievement 2: Action verb + what + quantified result>",
          "<Achievement 3: Action verb + what + quantified result>"
        ]
      }},
      {{
        "title": "<Previous role>",
        "company": "<Company>",
        "period": "20XX – 20XX",
        "bullets": [
          "<Achievement>",
          "<Achievement>"
        ]
      }}
    ],
    "skills": {{
      "technical": ["<skill1>", "<skill2>", "<skill3>", "<skill4>", "<skill5>", "<skill6>"],
      "soft": ["<skill1>", "<skill2>", "<skill3>", "<skill4>"],
      "tools": ["<tool1>", "<tool2>", "<tool3>", "<tool4>"]
    }},
    "certifications": ["<cert1>", "<cert2>"],
    "education": "<Degree, University, Year>"
  }},
  "insights": {{
    "score": <integer 0-100 based on skills and experience match to {data['path']}>,
    "score_label": "<e.g. Strong Candidate / Rising Star / Top 5% Profile>",
    "strengths": ["<strength1>", "<strength2>", "<strength3>"],
    "gaps": ["<gap1>", "<gap2>"],
    "interview_hack": "<One powerful insider tip specific to {data['path']} interviews>",
    "salary_range": "<Realistic range in USD for {data['exp']} years in {data['path']}>",
    "personality_archetype": "<e.g. The Strategist / The Builder / The Connector>",
    "linkedin_headline": "<Optimized LinkedIn headline for {data['path']}>"
  }},
  "roadmap": [
    {{"month": "Month 1-3", "focus": "<Focus area>", "actions": ["<action1>", "<action2>", "<action3>"], "milestone": "<Target outcome>"}},
    {{"month": "Month 4-6", "focus": "<Focus area>", "actions": ["<action1>", "<action2>", "<action3>"], "milestone": "<Target outcome>"}},
    {{"month": "Month 7-12", "focus": "<Focus area>", "actions": ["<action1>", "<action2>"], "milestone": "<Target outcome>"}},
    {{"month": "Month 13-24", "focus": "<Focus area>", "actions": ["<action1>", "<action2>"], "milestone": "<Salary/role target>"}}
  ],
  "interview_qa": [
    {{"q": "<Common {data['path']} interview question 1>", "a": "<STAR-format model answer tailored to their profile>"}},
    {{"q": "<Question 2>", "a": "<Model answer>"}},
    {{"q": "<Question 3>", "a": "<Model answer>"}},
    {{"q": "<Tough behavioral question>", "a": "<Model answer>"}},
    {{"q": "<Technical/situational question for {data['path']}>", "a": "<Model answer>"}}
  ]
}}

Candidate Profile:
- Name: {data['name']}
- Target Role: {data['path']}
- Experience: {data['exp']}
- Skills provided: {data.get('skills', 'Not specified')}
- Achievements: {data.get('achievements', 'Not specified')}
- Target companies: {data.get('target', 'Top-tier companies')}

Make everything specific, powerful, and ATS-optimized. Use industry keywords for {data['path']}.
"""

# ═══════════════════════════════════════════════════
#  CALL GEMINI
# ═══════════════════════════════════════════════════
def call_ai(data):
    model = genai.GenerativeModel(
        'gemini-1.5-flash',
        generation_config={"temperature": 0.8, "max_output_tokens": 4096}
    )
    response = model.generate_content(build_prompt(data))
    raw = response.text.strip()
    # Clean JSON fences if present
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
    return json.loads(raw.strip())

# ═══════════════════════════════════════════════════
#  RENDER FUNCTIONS
# ═══════════════════════════════════════════════════
def render_cv(cv):
    text = f"""{cv['name'].upper()}
{cv['title']}
{'─'*60}

PROFESSIONAL SUMMARY
{cv['summary']}

{'─'*60}
WORK EXPERIENCE
{'─'*60}
"""
    for job in cv.get('experience', []):
        text += f"\n{job['title']}  |  {job['company']}  |  {job['period']}\n"
        for b in job['bullets']:
            text += f"  • {b}\n"
    text += f"\n{'─'*60}\nSKILLS\n{'─'*60}\n"
    text += f"Technical  :  {' | '.join(cv['skills']['technical'])}\n"
    text += f"Soft       :  {' | '.join(cv['skills']['soft'])}\n"
    text += f"Tools      :  {' | '.join(cv['skills']['tools'])}\n"
    text += f"\n{'─'*60}\nCERTIFICATIONS\n{'─'*60}\n"
    for c in cv.get('certifications', []):
        text += f"  • {c}\n"
    text += f"\n{'─'*60}\nEDUCATION\n{'─'*60}\n  {cv['education']}\n"
    return text

# ═══════════════════════════════════════════════════
#  STEP 1 — IDENTITY
# ═══════════════════════════════════════════════════
if st.session_state.step == 1:
    st.markdown('<div class="app-wrapper">', unsafe_allow_html=True)

    st.markdown("""
    <div class="hero">
        <div class="hero-badge">◈ AI Career Intelligence Platform</div>
        <div class="hero-title">TALENTLY<br>INFINITY</div>
        <div class="hero-sub">From raw skills → Executive-level career profile in 60 seconds</div>
    </div>
    """, unsafe_allow_html=True)

    render_steps(1)

    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<div class="card-label">◈ Step 01 — Identity & Target</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("Full Name", placeholder="e.g. Ahmed Al-Rashid")
        email = st.text_input("Professional Email", placeholder="ahmed@example.com")
    with col2:
        phone = st.text_input("Phone / WhatsApp", placeholder="+20 100 000 0000")
        location = st.text_input("Location", placeholder="Cairo, Egypt")

    path = st.selectbox("🎯 Target Career Path", list(PATHS.keys()))
    target_companies = st.text_input("Dream Companies (optional)", placeholder="e.g. Google, Vodafone, McKinsey")

    st.markdown('</div>', unsafe_allow_html=True)

    col_btn, _ = st.columns([1, 2])
    with col_btn:
        if st.button("Continue → Skills Deep-Dive ⚡"):
            if name and email:
                st.session_state.data.update({
                    "name": name, "email": email,
                    "phone": phone, "location": location,
                    "path": path, "target": target_companies
                })
                st.session_state.step = 2
                st.rerun()
            else:
                st.error("Please enter your name and email to continue.")

    st.markdown('</div>', unsafe_allow_html=True)

# ═══════════════════════════════════════════════════
#  STEP 2 — SKILLS & BACKGROUND
# ═══════════════════════════════════════════════════
elif st.session_state.step == 2:
    st.markdown('<div class="app-wrapper">', unsafe_allow_html=True)

    st.markdown(f"""
    <div class="hero" style="padding: 40px 0 24px;">
        <div class="hero-badge">◈ Skills Intelligence Scan</div>
        <div class="hero-title" style="font-size: 2.5rem;">Profile Analysis</div>
        <div class="hero-sub">Tell us everything — AI will craft it into gold</div>
    </div>
    """, unsafe_allow_html=True)

    render_steps(2)

    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<div class="card-label">◈ Step 02 — Skills & Experience</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        exp_level = st.selectbox("Experience Level", list(LEVELS.keys()))
        industry = st.text_input("Current / Last Industry", placeholder="e.g. FinTech, Healthcare, E-commerce")
    with col2:
        edu = st.text_input("Education", placeholder="e.g. BSc Computer Science, Cairo University")
        certs = st.text_input("Certifications (if any)", placeholder="e.g. PMP, AWS, CCNA")

    skills = st.text_area(
        "🧠 All Your Skills (list everything — soft, technical, tools)",
        placeholder="e.g. Python, Excel, leadership, public speaking, customer service, Salesforce, data analysis...",
        height=100
    )

    achievements = st.text_area(
        "🏆 Top Achievements / Projects (the more detail the better)",
        placeholder="e.g. Led a team of 5 and reduced costs by 20% | Built an app with 10K users | Closed $500K in sales...",
        height=100
    )

    languages = st.text_input("Languages", placeholder="e.g. Arabic (Native), English (C1), French (B1)")

    st.markdown('</div>', unsafe_allow_html=True)

    col1, col2 = st.columns([1, 3])
    with col1:
        if st.button("← Back"):
            st.session_state.step = 1
            st.rerun()
    with col2:
        if st.button("🚀 Generate My Infinity Profile"):
            if skills:
                st.session_state.data.update({
                    "exp": exp_level, "skills": skills,
                    "achievements": achievements, "edu": edu,
                    "certs": certs, "industry": industry,
                    "languages": languages,
                })
                st.session_state.step = 3
                st.rerun()
            else:
                st.error("Please enter at least your skills to continue.")

    st.markdown('</div>', unsafe_allow_html=True)

# ═══════════════════════════════════════════════════
#  STEP 3 — AI PROCESSING (SCAN ANIMATION)
# ═══════════════════════════════════════════════════
elif st.session_state.step == 3:
    st.markdown('<div class="app-wrapper">', unsafe_allow_html=True)

    render_steps(3)

    scan_ph = st.empty()
    prog_ph = st.empty()
    status_ph = st.empty()

    stages = [
        (5,  "INITIALIZING NEURAL NETWORK..."),
        (15, "SCANNING SKILLS MATRIX..."),
        (30, "CROSS-REFERENCING INDUSTRY DATA..."),
        (45, "CRAFTING ATS-OPTIMIZED CV..."),
        (60, "RUNNING PSYCHOLOGICAL PROFILE..."),
        (75, "BUILDING 24-MONTH ROADMAP..."),
        (88, "GENERATING INTERVIEW Q&A..."),
        (95, "COMPILING INFINITY PROFILE..."),
        (100,"COMPLETE ✓"),
    ]

    scan_ph.markdown("""
    <div class="glass-card scan-container">
        <div class="scan-line"></div>
        <div style="font-size:3rem; margin-bottom:16px;">♾️</div>
        <div class="scan-text">TALENTLY INFINITY AI<span class="cursor">█</span></div>
        <div style="font-size:0.75rem; color:rgba(255,255,255,0.3); margin-top:8px; font-family:'Space Mono',monospace;">
            Generating your executive career profile...
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Start progress animation
    for pct, label in stages[:-2]:
        prog_ph.markdown(f"""
        <div style="margin: 0 0 8px;">
            <div class="progress-wrap">
                <div class="progress-fill" style="width:{pct}%"></div>
            </div>
            <div style="font-family:'Space Mono',monospace; font-size:10px; color:rgba(0,200,255,0.7); letter-spacing:2px; margin-top:6px;">
                {label}
            </div>
        </div>
        """, unsafe_allow_html=True)
        time.sleep(0.4)

    # Call AI
    try:
        result = call_ai(st.session_state.data)
        st.session_state.result = result

        for pct, label in stages[-2:]:
            prog_ph.markdown(f"""
            <div style="margin: 0 0 8px;">
                <div class="progress-wrap">
                    <div class="progress-fill" style="width:{pct}%"></div>
                </div>
                <div style="font-family:'Space Mono',monospace; font-size:10px; color:rgba(0,200,255,0.7); letter-spacing:2px; margin-top:6px;">
                    {label}
                </div>
            </div>
            """, unsafe_allow_html=True)
            time.sleep(0.3)

        time.sleep(0.5)
        st.session_state.step = 4
        st.rerun()

    except Exception as e:
        scan_ph.error(f"AI Error: {str(e)[:200]}")
        st.markdown("**Debug:** Check your API key and that `gemini-1.5-flash` is enabled.")
        if st.button("← Try Again"):
            st.session_state.step = 2
            st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

# ═══════════════════════════════════════════════════
#  STEP 4 — RESULTS
# ═══════════════════════════════════════════════════
elif st.session_state.step == 4:
    r = st.session_state.result
    cv = r.get("cv", {})
    ins = r.get("insights", {})
    roadmap = r.get("roadmap", [])
    qa = r.get("interview_qa", [])

    st.markdown('<div class="app-wrapper">', unsafe_allow_html=True)

    st.markdown(f"""
    <div class="hero" style="padding: 40px 0 24px;">
        <div class="hero-badge">◈ Infinity Profile Complete</div>
        <div class="hero-title" style="font-size:2.2rem;">{cv.get('name','Your Profile')}</div>
        <div class="hero-sub">{cv.get('title','')}</div>
    </div>
    """, unsafe_allow_html=True)

    render_steps(4)

    # ── ROW 1: SCORE + STATS ──
    col_score, col_stats = st.columns([1, 2])

    with col_score:
        score = ins.get('score', 0)
        color = "#00ff9d" if score >= 75 else "#00c8ff" if score >= 50 else "#ff6b6b"
        st.markdown(f"""
        <div class="glass-card" style="text-align:center; padding: 32px 20px;">
            <div class="result-header">◈ ATS Match Score</div>
            <div class="score-number" style="background: linear-gradient(135deg, {color}, #7b00ff); -webkit-background-clip:text; background-clip:text; -webkit-text-fill-color:transparent;">
                {score}
            </div>
            <div class="score-label">/ 100 — {ins.get('score_label','')}</div>
            <div style="margin-top:20px; padding:12px; background:rgba(255,255,255,0.04); border-radius:12px;">
                <div style="font-family:'Space Mono',monospace; font-size:9px; color:rgba(255,255,255,0.4); letter-spacing:2px; margin-bottom:6px;">ARCHETYPE</div>
                <div style="font-weight:700; color:#00c8ff;">{ins.get('personality_archetype','')}</div>
            </div>
            <div style="margin-top:12px; padding:12px; background:rgba(255,255,255,0.04); border-radius:12px;">
                <div style="font-family:'Space Mono',monospace; font-size:9px; color:rgba(255,255,255,0.4); letter-spacing:2px; margin-bottom:6px;">SALARY RANGE</div>
                <div style="font-weight:700; color:#00ff9d; font-size:0.9rem;">{ins.get('salary_range','')}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col_stats:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown('<div class="result-header">◈ Profile Intelligence</div>', unsafe_allow_html=True)

        st.markdown("**✅ Strengths**")
        for s in ins.get('strengths', []):
            st.markdown(f"&nbsp;&nbsp;&nbsp;▸ {s}")

        st.markdown("**⚠️ Gaps to Close**")
        for g in ins.get('gaps', []):
            st.markdown(f"&nbsp;&nbsp;&nbsp;▸ {g}")

        st.markdown(f"""
        <div style="margin-top:16px; padding:14px; background:rgba(0,200,255,0.05); border:1px solid rgba(0,200,255,0.2); border-radius:12px;">
            <div style="font-family:'Space Mono',monospace; font-size:9px; color:#00c8ff; letter-spacing:2px; margin-bottom:8px;">◈ INTERVIEW HACK</div>
            <div style="font-size:0.85rem; line-height:1.6; color:rgba(255,255,255,0.8);">{ins.get('interview_hack','')}</div>
        </div>
        <div style="margin-top:12px; padding:14px; background:rgba(123,0,255,0.05); border:1px solid rgba(123,0,255,0.2); border-radius:12px;">
            <div style="font-family:'Space Mono',monospace; font-size:9px; color:#a855f7; letter-spacing:2px; margin-bottom:8px;">◈ LINKEDIN HEADLINE</div>
            <div style="font-size:0.85rem; font-style:italic; color:rgba(255,255,255,0.7);">{ins.get('linkedin_headline','')}</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

    # ── ATS CV ──
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<div class="result-header">◈ ATS-Optimized CV — Copy & Export</div>', unsafe_allow_html=True)
    st.text_area("", render_cv(cv), height=520, label_visibility="collapsed")
    st.markdown('</div>', unsafe_allow_html=True)

    # ── ROADMAP ──
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<div class="result-header">◈ 24-Month Growth Roadmap</div>', unsafe_allow_html=True)
    cols = st.columns(len(roadmap))
    for i, (col, phase) in enumerate(zip(cols, roadmap)):
        with col:
            colors = ["#00c8ff", "#7b00ff", "#00ff9d", "#ff6b6b"]
            c = colors[i % len(colors)]
            st.markdown(f"""
            <div style="padding:16px; background:rgba(255,255,255,0.03); border:1px solid rgba(255,255,255,0.08); border-radius:14px; height:100%;">
                <div style="font-family:'Space Mono',monospace; font-size:8px; color:{c}; letter-spacing:2px; margin-bottom:10px;">{phase['month']}</div>
                <div style="font-weight:700; font-size:0.85rem; margin-bottom:10px; color:white;">{phase['focus']}</div>
                {"".join(f'<div style="font-size:0.75rem; color:rgba(255,255,255,0.55); margin-bottom:5px; padding-left:8px; border-left:2px solid {c}40;">▸ {a}</div>' for a in phase['actions'])}
                <div style="margin-top:12px; padding:8px; background:{c}11; border-radius:8px; font-size:0.75rem; color:{c}; font-weight:600;">🎯 {phase['milestone']}</div>
            </div>
            """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # ── INTERVIEW Q&A ──
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<div class="result-header">◈ Interview Questions & Model Answers</div>', unsafe_allow_html=True)
    for i, item in enumerate(qa):
        with st.expander(f"Q{i+1}: {item['q']}"):
            st.markdown(f"""
            <div style="padding:14px; background:rgba(0,200,255,0.04); border-left:3px solid #00c8ff; border-radius:0 10px 10px 0; line-height:1.7; font-size:0.88rem; color:rgba(255,255,255,0.82);">
                {item['a']}
            </div>
            """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # ── RESTART ──
    col_btn, _ = st.columns([1, 3])
    with col_btn:
        if st.button("🔄 Generate New Profile"):
            for k in ["step","data","result"]:
                st.session_state[k] = defaults[k]
            st.session_state.step = 1
            st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)
