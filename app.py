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
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable
from reportlab.lib.enums import TA_LEFT, TA_CENTER

st.set_page_config(page_title="Talently", page_icon="◈", layout="centered")

# ── SESSION STATE ─────────────────────────────────────────────────────────────
for k, v in [("step", 0), ("data", {}), ("cv_text", None), ("assessment_text", None), ("lang", None)]:
    if k not in st.session_state:
        st.session_state[k] = v

# ── TRANSLATIONS ──────────────────────────────────────────────────────────────
T = {
    "ar": {
        "dir": "rtl",
        "brand": "Talently",
        "brand_sub": "Deals Outsourcing.com",
        "brand_tag": "منصة التوظيف الذكي",
        "eyebrow": "Career Assessment Platform",
        "hero1": "حدّد",
        "hero2": "مسارك",
        "hero3": "المهني",
        "hero_sub": "منصة ذكية لتقييم المرشحين وإنشاء سيرة ذاتية ATS احترافية",
        "stat1_n": "في خطوة", "stat1_l": "واحدة",
        "stat2_n": "ATS", "stat2_l": "محسّن ومطابق للمعايير العالمية",
        "stat3_n": "PDF", "stat3_l": "احترافي",
        "start_btn": "ابدأ التقييم الآن",
        "step1_label": "الخطوة الأولى — البيانات الشخصية",
        "step2_label": "الخطوة الثانية — التقييم المهني",
        "full_name": "الاسم الكامل",
        "age": "السن",
        "age_opts": ["اختر"] + [str(i) for i in range(18, 56)],
        "address": "العنوان التفصيلي",
        "phone": "رقم الموبايل",
        "edu": "المؤهل الدراسي",
        "edu_opts": ["اختر", "طالب جامعي", "بكالوريوس", "دبلوم", "ماجستير", "ثانوية عامة"],
        "major": "التخصص / المجال الدراسي",
        "years_exp": "سنوات الخبرة في المبيعات",
        "years_opts": ["اختر", "لا يوجد (مبتدئ)", "أقل من سنة", "1 – 2 سنة", "3 – 5 سنوات", "أكثر من 5 سنوات"],
        "exp_section": "الخبرة العملية السابقة",
        "company_name": "اسم الشركة",
        "job_title": "المسمى الوظيفي",
        "duration": "مدة العمل",
        "duration_opts": ["اختر", "أقل من 6 شهور", "6 – 12 شهر", "1 – 2 سنة", "2 – 4 سنوات", "أكثر من 4 سنوات"],
        "add_exp": "➕ إضافة شركة أخرى",
        "next": "التالي ←",
        "back": "→ رجوع",
        "generate": "إنشاء السيرة الذاتية ✦",
        "err_required": "⚠️ من فضلك أكمل جميع الحقول المطلوبة",
        "err_age": "⚠️ من فضلك اختر السن",
        "err_edu": "⚠️ من فضلك اختر المؤهل الدراسي",
        "err_exp": "⚠️ من فضلك اختر سنوات الخبرة",
        "err_open": "⚠️ من فضلك أجب على السؤال المفتوح",
        "q_motivation": "ما الذي يدفعك للعمل في مجال المبيعات؟",
        "q_motivation_opts": [
            "الدخل المرتفع والعمولات",
            "حب التواصل وبناء العلاقات",
            "التحدي المستمر وتحقيق الأهداف",
            "التطور المهني والترقي السريع",
        ],
        "q_pressure": "كيف تتعامل مع ضغط تحقيق الأهداف الشهرية؟",
        "q_pressure_opts": [
            "أضع خطة يومية وأتابع أدائي باستمرار",
            "أركز على العملاء الأكثر احتمالاً للشراء",
            "أطلب الدعم من مديري عند الحاجة",
            "أعمل ساعات إضافية حتى أحقق الهدف",
        ],
        "q_rejection": "عميل رفض عرضك بشكل قاطع — ما ردة فعلك؟",
        "q_rejection_opts": [
            "أحاول فهم سبب الرفض وأعود بعروض أفضل",
            "أقبل الرفض وأنتقل فوراً لعميل آخر",
            "أحلل الموقف لتحسين أسلوبي في المستقبل",
            "أطلب مساعدة زميل أكثر خبرة",
        ],
        "q_ambition": "أين تريد أن تكون مهنياً بعد 3 سنوات؟",
        "q_ambition_opts": [
            "مدير مبيعات أو team leader",
            "خبير في مجال تخصصي محدد",
            "رائد أعمال أو عمل مستقل",
            "الاستمرار في التطور كموظف محترف",
        ],
        "q_work_env": "ما بيئة العمل التي تناسبك أكثر؟",
        "q_work_env_opts": [
            "بيئة تنافسية بأهداف عالية وضغط مستمر",
            "بيئة تعاونية وفريق عمل متماسك",
            "بيئة مرنة تتيح الإبداع والمبادرة",
            "بيئة منظمة بإجراءات واضحة",
        ],
        "open_q": "عرّف عن نفسك في 3 جمل (نقاط قوتك وطموحك)",
        "generating": "جاري إعداد سيرتك الذاتية...",
        "success": "تم إعداد ملفك بنجاح",
        "preview_cv": "معاينة السيرة الذاتية",
        "preview_report": "معاينة تقرير التقييم",
        "download_cv": "⬇ تحميل السيرة الذاتية — PDF",
        "download_report": "⬇ تحميل تقرير التقييم — PDF",
        "restart_btn": "بدء تقييم جديد",
        "footer_contact": "سيتم التواصل معك قريباً",
        "exp_label": "الشركة",
        "no_prev_exp": "لا توجد خبرة سابقة",
    },
    "en": {
        "dir": "ltr",
        "brand": "Talently",
        "brand_sub": "Deals Outsourcing.com",
        "brand_tag": "Smart Recruitment Platform",
        "eyebrow": "Career Assessment Platform",
        "hero1": "Define",
        "hero2": "Your Career",
        "hero3": "Path",
        "hero_sub": "Smart platform to assess candidates and build ATS-optimized professional CVs",
        "stat1_n": "One", "stat1_l": "Single Step",
        "stat2_n": "ATS", "stat2_l": "Global Standards Certified",
        "stat3_n": "PDF", "stat3_l": "Professional",
        "start_btn": "Start Assessment Now",
        "step1_label": "Step One — Personal Information",
        "step2_label": "Step Two — Professional Assessment",
        "full_name": "Full Name",
        "age": "Age",
        "age_opts": ["Select"] + [str(i) for i in range(18, 56)],
        "address": "Full Address",
        "phone": "Mobile Number",
        "edu": "Education Level",
        "edu_opts": ["Select", "University Student", "Bachelor's Degree", "Diploma", "Master's Degree", "High School"],
        "major": "Major / Field of Study",
        "years_exp": "Years of Sales Experience",
        "years_opts": ["Select", "No Experience (Beginner)", "Less than 1 year", "1 – 2 years", "3 – 5 years", "More than 5 years"],
        "exp_section": "Previous Work Experience",
        "company_name": "Company Name",
        "job_title": "Job Title",
        "duration": "Duration",
        "duration_opts": ["Select", "Less than 6 months", "6 – 12 months", "1 – 2 years", "2 – 4 years", "More than 4 years"],
        "add_exp": "➕ Add Another Company",
        "next": "Next →",
        "back": "← Back",
        "generate": "Generate CV ✦",
        "err_required": "⚠️ Please complete all required fields",
        "err_age": "⚠️ Please select your age",
        "err_edu": "⚠️ Please select your education level",
        "err_exp": "⚠️ Please select years of experience",
        "err_open": "⚠️ Please answer the open question",
        "q_motivation": "What drives you to work in sales?",
        "q_motivation_opts": [
            "High income and commissions",
            "Love of communication and building relationships",
            "Continuous challenge and achieving targets",
            "Career growth and fast promotion",
        ],
        "q_pressure": "How do you handle pressure to meet monthly targets?",
        "q_pressure_opts": [
            "I create a daily plan and track my performance",
            "I focus on the most likely-to-buy prospects",
            "I ask my manager for support when needed",
            "I work extra hours until I hit the target",
        ],
        "q_rejection": "A client firmly rejects your offer — what's your reaction?",
        "q_rejection_opts": [
            "I try to understand the reason and come back with a better offer",
            "I accept it and immediately move to the next client",
            "I analyze the situation to improve my approach",
            "I ask a more experienced colleague for help",
        ],
        "q_ambition": "Where do you want to be professionally in 3 years?",
        "q_ambition_opts": [
            "Sales manager or team leader",
            "Expert in a specific specialized field",
            "Entrepreneur or freelancer",
            "Continue growing as a professional employee",
        ],
        "q_work_env": "What work environment suits you most?",
        "q_work_env_opts": [
            "Competitive environment with high targets and pressure",
            "Collaborative team-oriented environment",
            "Flexible environment that allows creativity and initiative",
            "Structured environment with clear procedures",
        ],
        "open_q": "Describe yourself in 3 sentences (your strengths and ambitions)",
        "generating": "Preparing your files...",
        "success": "Your files have been prepared successfully",
        "preview_cv": "CV Preview",
        "preview_report": "Assessment Report Preview",
        "download_cv": "⬇ Download CV — PDF",
        "download_report": "⬇ Download Assessment Report — PDF",
        "restart_btn": "Start New Assessment",
        "footer_contact": "We will contact you soon",
        "exp_label": "Company",
        "no_prev_exp": "No previous experience",
    }
}

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,600;1,300;1,400&family=Outfit:wght@200;300;400;500;600&display=swap');

:root {
  --ink:    #03050D;
  --navy:   #060918;
  --navy2:  #090D1E;
  --navy3:  #0C1124;
  --gold:   #C8A45A;
  --gold2:  #E2C07E;
  --gold3:  #F5DFA0;
  --goldD:  #9A7C38;
  --goldB:  rgba(200,164,90,0.30);
  --goldL:  rgba(200,164,90,0.07);
  --goldM:  rgba(200,164,90,0.15);
  --white:  #EDE9DF;
  --muted:  #5C6478;
  --soft:   #8E98B0;
  --mid:    #B0B8CC;
  --border: rgba(200,164,90,0.14);
  --borderW:rgba(255,255,255,0.06);
  --borderG:rgba(200,164,90,0.22);
  --glow:   rgba(200,164,90,0.18);
}

* { box-sizing: border-box; }

.stApp {
  background: var(--ink) !important;
  font-family: 'Outfit', sans-serif !important;
  background-image:
    radial-gradient(ellipse 120% 60% at 15% -5%,  rgba(200,164,90,0.10) 0%, transparent 55%),
    radial-gradient(ellipse 80%  80% at 88% 105%, rgba(200,164,90,0.07) 0%, transparent 55%),
    radial-gradient(ellipse 50%  90% at 50%  50%, rgba(6,12,30,0.95)    0%, transparent 100%) !important;
}

#MainMenu, footer, header { visibility: hidden !important; }
.stDeployButton { display: none !important; }

.main .block-container {
  max-width: 660px !important;
  padding: 0 1.5rem 8rem !important;
  margin: 0 auto !important;
}

::-webkit-scrollbar { width: 3px; }
::-webkit-scrollbar-track { background: var(--ink); }
::-webkit-scrollbar-thumb { background: linear-gradient(180deg, var(--goldD), var(--gold)); border-radius: 2px; }

@keyframes fadeUp {
  from { opacity: 0; transform: translateY(20px); }
  to   { opacity: 1; transform: translateY(0); }
}
@keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
@keyframes shimmer { 0% { left: -100%; } 100% { left: 220%; } }
@keyframes pulseGold {
  0%,100% { opacity: 0.4; transform: scale(1); }
  50%     { opacity: 1;   transform: scale(1.15); }
}
@keyframes dotBeat {
  0%,100% { transform: scale(1); opacity: 0.7; }
  50%     { transform: scale(1.9); opacity: 1; }
}
@keyframes lineGrow {
  from { width: 0; opacity: 0; }
  to   { width: 100%; opacity: 1; }
}
@keyframes glowPulse {
  0%,100% { box-shadow: 0 0 0px 0px rgba(200,164,90,0); }
  50%     { box-shadow: 0 0 28px 4px rgba(200,164,90,0.14); }
}
@keyframes textGlow {
  0%,100% { text-shadow: 0 0 20px rgba(200,164,90,0.2); }
  50%     { text-shadow: 0 0 40px rgba(200,164,90,0.5), 0 0 80px rgba(200,164,90,0.2); }
}
@keyframes orb1 {
  0%,100% { transform: translate(0,0) scale(1); opacity: 0.5; }
  33%     { transform: translate(30px,-20px) scale(1.1); opacity: 0.8; }
  66%     { transform: translate(-20px,15px) scale(0.95); opacity: 0.6; }
}
@keyframes orb2 {
  0%,100% { transform: translate(0,0) scale(1); opacity: 0.4; }
  50%     { transform: translate(-25px,20px) scale(1.12); opacity: 0.7; }
}

.orb-container { position: fixed; inset: 0; pointer-events: none; z-index: 0; overflow: hidden; }
.orb { position: absolute; border-radius: 50%; filter: blur(80px); }
.orb-1 {
  width: 500px; height: 380px;
  background: radial-gradient(ellipse, rgba(200,164,90,0.14) 0%, transparent 70%);
  top: -100px; left: -120px;
  animation: orb1 14s ease-in-out infinite;
}
.orb-2 {
  width: 400px; height: 400px;
  background: radial-gradient(ellipse, rgba(200,164,90,0.09) 0%, transparent 70%);
  bottom: 5%; right: -100px;
  animation: orb2 18s ease-in-out infinite;
}

.brand-bar {
  padding: 32px 0 26px;
  margin-bottom: 60px;
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  position: relative;
  animation: fadeIn 0.9s ease both;
}
.brand-bar::after {
  content: '';
  position: absolute;
  bottom: 0; left: 0; right: 0;
  height: 1px;
  background: linear-gradient(90deg, var(--gold) 0%, rgba(200,164,90,0.25) 50%, transparent 88%);
  animation: lineGrow 1.2s cubic-bezier(0.4,0,0.2,1) 0.3s both;
}
.brand-left { display: flex; flex-direction: column; gap: 4px; }
.brand-name {
  font-family: 'Cormorant Garamond', serif;
  font-size: 28px; font-weight: 600;
  color: var(--white); letter-spacing: 10px;
  text-transform: uppercase;
  text-shadow: 0 0 50px rgba(200,164,90,0.35), 0 2px 20px rgba(0,0,0,0.5);
}
.brand-dot {
  width: 6px; height: 6px;
  background: var(--gold);
  border-radius: 50%;
  display: inline-block;
  margin: 0 2px 3px;
  vertical-align: middle;
  animation: dotBeat 2.6s ease-in-out infinite;
  box-shadow: 0 0 10px rgba(200,164,90,0.9), 0 0 20px rgba(200,164,90,0.4);
}
.brand-sub-name {
  font-size: 15px; letter-spacing: 3px;
  text-transform: uppercase;
  color: var(--gold2); font-weight: 500; opacity: 0.92;
  font-family: 'Outfit', sans-serif;
  text-shadow: 0 0 20px rgba(200,164,90,0.45);
}
.brand-tag {
  font-size: 9px; letter-spacing: 4px;
  text-transform: uppercase;
  color: var(--mid); font-weight: 300; opacity: 0.6; margin-top: 4px;
}

.hero-eyebrow {
  font-size: 8px; letter-spacing: 5px;
  text-transform: uppercase; color: var(--gold);
  margin-bottom: 28px; font-weight: 400;
  display: flex; align-items: center; gap: 14px;
  opacity: 0; animation: fadeUp 0.7s ease 0.3s both;
}
.hero-eyebrow::before { content: '◈'; font-size: 11px; animation: pulseGold 3s ease-in-out infinite; }
.hero-eyebrow::after  { content: ''; flex: 1; height: 1px; background: linear-gradient(90deg, var(--goldB), transparent); }

.hero-title {
  font-family: 'Cormorant Garamond', serif;
  font-size: 72px; font-weight: 400;
  color: var(--white); line-height: 1.0;
  margin-bottom: 8px; letter-spacing: -1px;
  opacity: 0; animation: fadeUp 0.85s ease 0.45s both;
  text-shadow: 0 4px 40px rgba(0,0,0,0.4);
}
.hero-title em   { color: var(--gold); font-style: italic; animation: textGlow 4s ease-in-out infinite; display: inline-block; }
.hero-title span { display: block; font-size: 56px; }

.hero-sub {
  font-size: 14px; color: var(--muted); font-weight: 300; line-height: 2.0;
  margin: 28px 0 52px; max-width: 400px; letter-spacing: 0.3px;
  opacity: 0; animation: fadeUp 0.85s ease 0.6s both;
}

.stats-grid {
  display: grid; grid-template-columns: repeat(3, 1fr);
  gap: 1px; background: var(--borderG);
  border: 1px solid var(--borderG); border-radius: 6px;
  overflow: hidden; margin-bottom: 52px;
  opacity: 0; animation: fadeUp 0.85s ease 0.75s both, glowPulse 5s ease 2s infinite;
}
.stat-cell {
  background: var(--navy2); padding: 32px 16px;
  text-align: center; position: relative; overflow: hidden;
  transition: background 0.4s ease;
}
.stat-cell:hover { background: var(--navy3); }
.stat-num {
  font-family: 'Cormorant Garamond', serif;
  font-size: 24px; font-weight: 600; color: var(--gold);
  line-height: 1.2; margin-bottom: 9px; letter-spacing: 1px;
  text-shadow: 0 0 20px rgba(200,164,90,0.4);
}
.stat-lbl { font-size: 7px; letter-spacing: 1.5px; text-transform: uppercase; color: var(--muted); font-weight: 400; line-height: 1.5; }

.sec-label {
  font-size: 8.5px; letter-spacing: 4px; text-transform: uppercase; color: var(--gold);
  margin-bottom: 32px; padding-bottom: 14px; border-bottom: 1px solid var(--border);
  display: flex; align-items: center; gap: 10px; font-weight: 400;
  animation: fadeIn 0.7s ease both;
}
.sec-label::before { content: '—'; opacity: 0.4; }

.success-banner {
  background: linear-gradient(135deg, rgba(200,164,90,0.11), rgba(200,164,90,0.03));
  border: 1px solid var(--goldB); border-left: 2px solid var(--gold);
  padding: 16px 22px; border-radius: 5px; color: var(--gold2);
  font-size: 13px; letter-spacing: 0.4px; margin-bottom: 32px;
  display: flex; align-items: center; gap: 12px;
  animation: fadeUp 0.6s ease both, glowPulse 3s ease 0.8s infinite;
}
.success-banner::before { content: '✦'; font-size: 13px; opacity: 0.7; animation: pulseGold 2s ease-in-out infinite; }

.cv-box {
  background: var(--navy2); border: 1px solid var(--borderW);
  border-top: 1px solid var(--borderG); border-radius: 6px;
  padding: 36px 32px; font-size: 12.5px; line-height: 2.0;
  color: var(--soft); white-space: pre-wrap;
  font-family: 'Outfit', sans-serif; font-weight: 300;
  margin-bottom: 28px;
  box-shadow: 0 28px 72px rgba(0,0,0,0.6), inset 0 1px 0 rgba(255,255,255,0.04);
}

.exp-card {
  background: var(--navy2); border: 1px solid var(--borderW);
  border-left: 2px solid var(--goldB); border-radius: 5px;
  padding: 14px 18px; margin-bottom: 10px;
  animation: fadeUp 0.4s ease both;
}
.exp-card-title { font-size: 11px; color: var(--gold2); letter-spacing: 1px; font-weight: 500; margin-bottom: 2px; }
.exp-card-sub   { font-size: 10px; color: var(--soft); }

.stProgress > div > div > div > div {
  background: linear-gradient(90deg, var(--goldD), var(--gold), var(--gold2)) !important;
  border-radius: 2px !important;
  box-shadow: 0 0 12px rgba(200,164,90,0.35) !important;
}
.stProgress > div > div { background: rgba(255,255,255,0.05) !important; border-radius: 2px !important; height: 2px !important; }

.stTextInput label, .stTextArea label, .stSelectbox label, .stRadio > label {
  font-size: 8.5px !important; letter-spacing: 3px !important;
  text-transform: uppercase !important; color: var(--muted) !important;
  font-weight: 400 !important; font-family: 'Outfit', sans-serif !important;
  margin-bottom: 8px !important;
}
.stTextInput > div > div > input {
  background: var(--navy2) !important; border: 1px solid var(--borderW) !important;
  border-radius: 5px !important; color: var(--white) !important;
  font-family: 'Outfit', sans-serif !important; font-size: 14px !important;
  font-weight: 300 !important; padding: 16px 20px !important;
  transition: border-color 0.3s ease, box-shadow 0.3s ease !important;
}
.stTextInput > div > div > input:focus {
  border-color: rgba(200,164,90,0.55) !important; background: var(--navy3) !important;
  box-shadow: 0 0 0 3px rgba(200,164,90,0.09) !important;
}
.stTextInput > div > div > input::placeholder { color: var(--muted) !important; opacity: 0.4 !important; }

.stTextArea > div > div > textarea {
  background: var(--navy2) !important; border: 1px solid var(--borderW) !important;
  border-radius: 5px !important; color: var(--white) !important;
  font-family: 'Outfit', sans-serif !important; font-size: 14px !important;
  font-weight: 300 !important; padding: 16px 20px !important; line-height: 1.8 !important;
}
.stTextArea > div > div > textarea:focus {
  border-color: rgba(200,164,90,0.55) !important;
  box-shadow: 0 0 0 3px rgba(200,164,90,0.09) !important;
}

.stSelectbox > div > div {
  background: var(--navy2) !important; border: 1px solid var(--borderW) !important;
  border-radius: 5px !important; color: var(--white) !important; padding: 4px 0 !important;
}
.stSelectbox > div > div:focus-within { border-color: rgba(200,164,90,0.55) !important; }
.stSelectbox > div > div > div { color: var(--white) !important; font-family: 'Outfit', sans-serif !important; font-weight: 300 !important; }
.stSelectbox svg { fill: var(--muted) !important; }

.stRadio > div { gap: 9px !important; flex-direction: column !important; }
.stRadio > div > label {
  background: var(--navy2) !important; border: 1px solid var(--borderW) !important;
  border-radius: 5px !important; padding: 15px 20px !important;
  color: var(--soft) !important; font-size: 13.5px !important;
  font-family: 'Outfit', sans-serif !important; font-weight: 300 !important;
  transition: border-color 0.28s ease, background 0.28s ease, transform 0.28s ease !important;
  cursor: pointer !important;
}
.stRadio > div > label:hover {
  border-color: var(--goldB) !important; color: var(--white) !important;
  background: var(--navy3) !important; transform: translateX(6px) !important;
  box-shadow: -3px 0 0 0 var(--gold) !important;
}

.stButton > button {
  background: transparent !important; border: 1px solid var(--goldB) !important;
  color: var(--gold) !important; border-radius: 5px !important;
  font-family: 'Outfit', sans-serif !important; font-size: 8.5px !important;
  font-weight: 500 !important; letter-spacing: 4px !important;
  text-transform: uppercase !important; padding: 19px 38px !important;
  transition: color 0.3s ease, border-color 0.3s ease, transform 0.3s ease, box-shadow 0.3s ease !important;
  position: relative !important; overflow: hidden !important;
}
.stButton > button:hover {
  color: var(--ink) !important; border-color: var(--gold) !important;
  background: var(--gold) !important; transform: translateY(-3px) !important;
  box-shadow: 0 14px 36px rgba(200,164,90,0.22) !important;
}

.stDownloadButton > button {
  background: linear-gradient(135deg, var(--gold) 0%, var(--goldD) 100%) !important;
  border: 1px solid transparent !important; color: var(--ink) !important;
  border-radius: 5px !important; font-family: 'Outfit', sans-serif !important;
  font-size: 8.5px !important; font-weight: 600 !important;
  letter-spacing: 4px !important; text-transform: uppercase !important;
  padding: 19px 38px !important;
  transition: transform 0.3s ease, box-shadow 0.3s ease !important;
  box-shadow: 0 8px 28px rgba(200,164,90,0.25) !important;
}
.stDownloadButton > button:hover {
  transform: translateY(-3px) !important;
  box-shadow: 0 18px 44px rgba(200,164,90,0.32) !important;
}

.stSpinner > div { border-top-color: var(--gold) !important; }

[data-testid="stForm"] {
  background: var(--navy2) !important; border: 1px solid var(--borderW) !important;
  border-top: 1px solid var(--borderG) !important; border-radius: 6px !important;
  padding: 36px 32px !important;
  box-shadow: 0 28px 72px rgba(0,0,0,0.45), inset 0 1px 0 rgba(255,255,255,0.04) !important;
  animation: fadeUp 0.75s ease both !important;
}

.stAlert {
  background: rgba(160,50,50,0.07) !important; border: 1px solid rgba(200,80,80,0.2) !important;
  border-left: 2px solid rgba(200,80,80,0.55) !important; border-radius: 5px !important;
  color: #E0A0A0 !important;
}

hr { border-color: var(--border) !important; opacity: 0.35 !important; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="orb-container"><div class="orb orb-1"></div><div class="orb orb-2"></div></div>', unsafe_allow_html=True)

# ── GROQ ──────────────────────────────────────────────────────────────────────
GROQ_API_KEY = st.secrets["GROQ_API_KEY"]

def ask_ai(prompt):
    try:
        response = requests.post(
            url="https://api.groq.com/openai/v1/chat/completions",
            headers={"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"},
            json={"model": "llama-3.3-70b-versatile", "messages": [{"role": "user", "content": prompt}]},
            timeout=60
        )
        result = response.json()
        if "choices" in result:
            return result["choices"][0]["message"]["content"]
        else:
            st.error(f"API Error: {result}")
            return None
    except Exception as e:
        st.error(f"Connection Error: {str(e)}")
        return None

# ── CSV ───────────────────────────────────────────────────────────────────────
def save_to_csv(data):
    filename = "applicants.csv"
    fieldnames = [
        "timestamp","lang","name","age","address","phone","education","major",
        "years_exp","companies","q_motivation","q_pressure","q_rejection",
        "q_ambition","q_work_env","open_q"
    ]
    file_exists = os.path.isfile(filename)
    with open(filename, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()
        row = {k: data.get(k, "") for k in fieldnames}
        row["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # flatten companies list
        companies_str = " | ".join([
            f"{c.get('company','')} / {c.get('title','')} / {c.get('duration','')}"
            for c in data.get("companies", [])
        ])
        row["companies"] = companies_str
        writer.writerow(row)

# ── PDF: CLEAN CV ─────────────────────────────────────────────────────────────
def generate_cv_pdf(cv_text, data):
    buffer = BytesIO()

    INK   = colors.HexColor("#111111")
    DARK  = colors.HexColor("#222222")
    SOFT  = colors.HexColor("#666666")
    GOLD  = colors.HexColor("#B8933F")
    NAVY  = colors.HexColor("#0F1B35")
    GRULE = colors.HexColor("#E8E8E8")

    def sty(name, **kw):
        return ParagraphStyle(name, **kw)

    NAME_S  = sty("NM", fontName="Helvetica-Bold",   fontSize=22, textColor=NAVY,  leading=26, alignment=TA_CENTER, spaceAfter=3)
    ROLE_S  = sty("RL", fontName="Helvetica",         fontSize=10, textColor=GOLD,  leading=14, alignment=TA_CENTER, spaceAfter=2)
    CONT_S  = sty("CT", fontName="Helvetica",         fontSize=8.5,textColor=SOFT,  leading=13, alignment=TA_CENTER, spaceAfter=1)
    SECH_S  = sty("SH", fontName="Helvetica-Bold",   fontSize=9,  textColor=NAVY,  leading=13, spaceBefore=14, spaceAfter=5, letterSpacing=2)
    BODY_S  = sty("BD", fontName="Helvetica",         fontSize=9.5,textColor=DARK,  leading=15, spaceAfter=4)
    BULL_S  = sty("BL", fontName="Helvetica",         fontSize=9,  textColor=DARK,  leading=14, leftIndent=12, firstLineIndent=-8, spaceAfter=3)
    CO_NM_S = sty("CN", fontName="Helvetica-Bold",   fontSize=10, textColor=INK,   leading=14, spaceAfter=1)
    CO_TL_S = sty("CL", fontName="Helvetica-Bold",   fontSize=9,  textColor=GOLD,  leading=13, spaceAfter=1)
    CO_DT_S = sty("CD", fontName="Helvetica",         fontSize=8,  textColor=SOFT,  leading=12, spaceAfter=6)
    FOOT_S  = sty("FT", fontName="Helvetica",         fontSize=7,  textColor=colors.HexColor("#AAAAAA"), leading=10, alignment=TA_CENTER)

    doc = SimpleDocTemplate(
        buffer, pagesize=A4,
        leftMargin=20*mm, rightMargin=20*mm,
        topMargin=14*mm, bottomMargin=12*mm,
    )
    story = []

    # Parse cv_text sections
    lines = cv_text.strip().split("\n")
    current_section = None
    parsed = {
        "summary": [],
        "competencies": [],
        "education": [],
        "languages": [],
        "experience_raw": [],
    }

    for line in lines:
        line = line.strip()
        if not line or line == "---": continue
        low = line.lower()

        if "professional summary" in low:      current_section = "summary";        continue
        elif "work experience" in low:          current_section = "experience_raw"; continue
        elif "core competencies" in low:        current_section = "competencies";   continue
        elif "education" in low and len(line)<20: current_section = "education";   continue
        elif "languages" in low and len(line)<15: current_section = "languages";   continue
        elif "assessment" in low:               current_section = None;             continue
        elif "curriculum vitae" in low:         current_section = None;             continue

        if current_section and current_section in parsed:
            parsed[current_section].append(line.lstrip("-•▸– ").strip())

    # ── NAME & CONTACT
    story.append(Paragraph(data["name"].upper(), NAME_S))
    story.append(Paragraph("Sales Professional  |  Egypt", ROLE_S))
    story.append(Paragraph(
        f"{data['phone']}   |   {data.get('email','')}   |   {data['address']}   |   Age: {data['age']}",
        CONT_S
    ))
    story.append(Spacer(1, 2*mm))
    story.append(HRFlowable(width="100%", thickness=2,   color=GOLD,  spaceAfter=0))
    story.append(HRFlowable(width="100%", thickness=0.4, color=GRULE, spaceAfter=0))

    # ── PROFESSIONAL SUMMARY
    story.append(Paragraph("PROFESSIONAL SUMMARY", SECH_S))
    story.append(HRFlowable(width="100%", thickness=0.8, color=NAVY, spaceAfter=6))
    for line in parsed["summary"]:
        if line:
            story.append(Paragraph(line, BODY_S))

    # ── WORK EXPERIENCE
    story.append(Paragraph("WORK EXPERIENCE", SECH_S))
    story.append(HRFlowable(width="100%", thickness=0.8, color=NAVY, spaceAfter=6))

    companies = data.get("companies", [])
    if companies:
        for i, exp in enumerate(companies):
            if exp.get("company") and exp["company"] != t.get("no_prev_exp",""):
                story.append(Paragraph(exp.get("company", ""), CO_NM_S))
                story.append(Paragraph(exp.get("title", ""), CO_TL_S))
                story.append(Paragraph(f"Duration: {exp.get('duration','')}", CO_DT_S))
                if i < len(companies) - 1:
                    story.append(HRFlowable(width="100%", thickness=0.3, color=GRULE, spaceBefore=2, spaceAfter=4))
    else:
        story.append(Paragraph("No previous experience — Entry Level Candidate", BODY_S))

    # ── CORE COMPETENCIES
    story.append(Paragraph("CORE COMPETENCIES", SECH_S))
    story.append(HRFlowable(width="100%", thickness=0.8, color=NAVY, spaceAfter=6))
    for comp in parsed["competencies"]:
        if comp:
            story.append(Paragraph(f"  ▸   {comp}", BULL_S))

    # ── EDUCATION
    story.append(Paragraph("EDUCATION", SECH_S))
    story.append(HRFlowable(width="100%", thickness=0.8, color=NAVY, spaceAfter=6))
    for line in parsed["education"]:
        if line:
            story.append(Paragraph(line, BODY_S))

    # ── LANGUAGES
    story.append(Paragraph("LANGUAGES", SECH_S))
    story.append(HRFlowable(width="100%", thickness=0.8, color=NAVY, spaceAfter=6))
    for line in parsed["languages"]:
        if line:
            story.append(Paragraph(f"  ▸   {line}", BULL_S))

    # ── FOOTER
    story.append(Spacer(1, 4*mm))
    story.append(HRFlowable(width="100%", thickness=0.4, color=GRULE, spaceAfter=3))
    story.append(Paragraph(
        f"Generated {datetime.now().strftime('%B %d, %Y')}   |   ATS-Optimized CV   |   Talently — Deals Outsourcing.com",
        FOOT_S
    ))

    doc.build(story)
    buffer.seek(0)
    return buffer

# ── PDF: ASSESSMENT REPORT ────────────────────────────────────────────────────
def generate_report_pdf(assessment_text, data):
    buffer = BytesIO()

    INK   = colors.HexColor("#111111")
    DARK  = colors.HexColor("#222222")
    SOFT  = colors.HexColor("#666666")
    GOLD  = colors.HexColor("#B8933F")
    NAVY  = colors.HexColor("#0F1B35")
    GRULE = colors.HexColor("#E8E8E8")

    def sty(name, **kw):
        return ParagraphStyle(name, **kw)

    TITLE_S = sty("TL", fontName="Helvetica-Bold",   fontSize=18, textColor=NAVY,  leading=22, alignment=TA_CENTER, spaceAfter=4)
    SUB_S   = sty("SB", fontName="Helvetica",         fontSize=9,  textColor=SOFT,  leading=13, alignment=TA_CENTER, spaceAfter=2)
    SECH_S  = sty("SH", fontName="Helvetica-Bold",   fontSize=9,  textColor=NAVY,  leading=13, spaceBefore=16, spaceAfter=6, letterSpacing=2)
    BODY_S  = sty("BD", fontName="Helvetica",         fontSize=9.5,textColor=DARK,  leading=15, spaceAfter=4)
    BULL_S  = sty("BL", fontName="Helvetica",         fontSize=9,  textColor=DARK,  leading=14, leftIndent=12, firstLineIndent=-8, spaceAfter=3)
    SCORE_S = sty("SC", fontName="Helvetica-Bold",   fontSize=28, textColor=GOLD,  leading=32, alignment=TA_CENTER, spaceAfter=2)
    REC_S   = sty("RC", fontName="Helvetica-Bold",   fontSize=10, textColor=NAVY,  leading=14, alignment=TA_CENTER, spaceAfter=4)
    LBL_S   = sty("LB", fontName="Helvetica-Bold",   fontSize=8,  textColor=SOFT,  leading=12, spaceAfter=1)
    VAL_S   = sty("VL", fontName="Helvetica",         fontSize=9.5,textColor=DARK,  leading=14, spaceAfter=6)
    FOOT_S  = sty("FT", fontName="Helvetica",         fontSize=7,  textColor=colors.HexColor("#AAAAAA"), leading=10, alignment=TA_CENTER)

    doc = SimpleDocTemplate(
        buffer, pagesize=A4,
        leftMargin=20*mm, rightMargin=20*mm,
        topMargin=14*mm, bottomMargin=12*mm,
    )
    story = []

    # ── HEADER
    story.append(Paragraph("CANDIDATE ASSESSMENT REPORT", TITLE_S))
    story.append(Paragraph(f"Talently — Deals Outsourcing.com   |   {datetime.now().strftime('%B %d, %Y')}", SUB_S))
    story.append(Spacer(1, 2*mm))
    story.append(HRFlowable(width="100%", thickness=2,   color=GOLD,  spaceAfter=0))
    story.append(HRFlowable(width="100%", thickness=0.4, color=GRULE, spaceAfter=0))

    # ── CANDIDATE INFO
    story.append(Paragraph("CANDIDATE INFORMATION", SECH_S))
    story.append(HRFlowable(width="100%", thickness=0.8, color=NAVY, spaceAfter=6))
    info_pairs = [
        ("Full Name",   data.get("name", "")),
        ("Age",         data.get("age", "")),
        ("Address",     data.get("address", "")),
        ("Phone",       data.get("phone", "")),
        ("Education",   data.get("education", "") + " — " + data.get("major", "")),
        ("Experience",  data.get("years_exp", "")),
    ]
    for lbl, val in info_pairs:
        if val.strip(" —"):
            story.append(Paragraph(lbl, LBL_S))
            story.append(Paragraph(val, VAL_S))

    # ── SCORE (parsed from assessment_text)
    lines = assessment_text.strip().split("\n")
    score_line = ""
    findings   = []
    rec_line   = ""
    fit_line   = ""
    answers_section = False
    answers    = []

    for line in lines:
        line = line.strip()
        if not line: continue
        low = line.lower()
        if "score:" in low:
            score_line = line.split(":",1)[1].strip()
        elif "recommendation:" in low:
            rec_line = line.split(":",1)[1].strip()
        elif "best fit" in low or "fit role" in low:
            fit_line = line.split(":",1)[1].strip() if ":" in line else line
        elif "candidate answers" in low or "assessment answers" in low:
            answers_section = True
        elif answers_section and line.startswith("-"):
            answers.append(line.lstrip("-• ").strip())
        elif line.startswith("-") and not answers_section:
            findings.append(line.lstrip("-•▸ ").strip())

    story.append(Paragraph("ASSESSMENT SCORE", SECH_S))
    story.append(HRFlowable(width="100%", thickness=0.8, color=NAVY, spaceAfter=6))
    if score_line:
        story.append(Paragraph(score_line, SCORE_S))
    if fit_line:
        story.append(Paragraph(f"Best Fit Role: {fit_line}", REC_S))
    if rec_line:
        story.append(Paragraph(rec_line, sty("RC2", fontName="Helvetica-Bold", fontSize=9, textColor=GOLD, leading=13, alignment=TA_CENTER, spaceAfter=4)))

    # ── KEY FINDINGS
    if findings:
        story.append(Paragraph("KEY FINDINGS", SECH_S))
        story.append(HRFlowable(width="100%", thickness=0.8, color=NAVY, spaceAfter=6))
        for f in findings:
            if f:
                story.append(Paragraph(f"  ▸   {f}", BULL_S))

    # ── CANDIDATE ANSWERS
    story.append(Paragraph("CANDIDATE RESPONSES", SECH_S))
    story.append(HRFlowable(width="100%", thickness=0.8, color=NAVY, spaceAfter=6))

    qa_pairs = [
        ("Motivation for Sales",          data.get("q_motivation", "")),
        ("Handling Monthly Pressure",     data.get("q_pressure", "")),
        ("Response to Client Rejection",  data.get("q_rejection", "")),
        ("Career Ambition (3 Years)",     data.get("q_ambition", "")),
        ("Preferred Work Environment",    data.get("q_work_env", "")),
        ("Self-Description",              data.get("open_q", "")),
    ]
    for q, a in qa_pairs:
        if a:
            story.append(Paragraph(q, LBL_S))
            story.append(Paragraph(a, VAL_S))

    # ── FOOTER
    story.append(Spacer(1, 4*mm))
    story.append(HRFlowable(width="100%", thickness=0.4, color=GRULE, spaceAfter=3))
    story.append(Paragraph(
        f"Confidential Assessment Report   |   Generated {datetime.now().strftime('%B %d, %Y')}   |   Talently — Deals Outsourcing.com",
        FOOT_S
    ))

    doc.build(story)
    buffer.seek(0)
    return buffer

# ── BRAND BAR ─────────────────────────────────────────────────────────────────
def render_brand():
    lang = st.session_state.lang or "en"
    t_local = T[lang]
    st.markdown(f"""
    <div class="brand-bar">
      <div class="brand-left">
        <div class="brand-name">{t_local['brand']}<span class="brand-dot"></span></div>
        <div class="brand-sub-name">{t_local['brand_sub']}</div>
      </div>
      <div class="brand-tag">{t_local['brand_tag']}</div>
    </div>
    """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# LANGUAGE SELECTION
# ══════════════════════════════════════════════════════════════════════════════
if st.session_state.lang is None:
    render_brand()
    st.markdown("""
    <div style="text-align:center; padding: 40px 0 20px; animation: fadeUp 0.8s ease both;">
      <div style="font-family:'Cormorant Garamond',serif; font-size:36px; color:#EDE9DF; letter-spacing:2px; margin-bottom:12px;">
        Welcome to <em style="color:#C8A45A;">Talently</em>
      </div>
      <div style="font-size:11px; color:#5C6478; letter-spacing:4px; text-transform:uppercase; margin-bottom:40px;">
        Choose your language to continue
      </div>
    </div>
    """, unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🇸🇦  العربية", use_container_width=True):
            st.session_state.lang = "ar"
            st.rerun()
    with col2:
        if st.button("🇬🇧  English", use_container_width=True):
            st.session_state.lang = "en"
            st.rerun()
    st.markdown('<p style="text-align:center;font-size:10px;color:#3A4558;margin-top:24px;letter-spacing:2px;">Powered by Deals Outsourcing.com</p>', unsafe_allow_html=True)
    st.stop()

t = T[st.session_state.lang]

# ══════════════════════════════════════════════════════════════════════════════
# STEP 0 — LANDING
# ══════════════════════════════════════════════════════════════════════════════
if st.session_state.step == 0:
    render_brand()
    st.markdown(f"""
    <div class="hero-eyebrow">{t['eyebrow']}</div>
    <div class="hero-title">
      {t['hero1']}
      <span><em>{t['hero2']}</em></span>
      {t['hero3']}
    </div>
    <div class="hero-sub">{t['hero_sub']}</div>
    <div class="stats-grid">
      <div class="stat-cell"><div class="stat-num">{t['stat1_n']}</div><div class="stat-lbl">{t['stat1_l']}</div></div>
      <div class="stat-cell"><div class="stat-num">{t['stat2_n']}</div><div class="stat-lbl">{t['stat2_l']}</div></div>
      <div class="stat-cell"><div class="stat-num">{t['stat3_n']}</div><div class="stat-lbl">{t['stat3_l']}</div></div>
    </div>
    """, unsafe_allow_html=True)
    if st.button(t["start_btn"], use_container_width=True):
        st.session_state.step = 1
        st.rerun()

# ══════════════════════════════════════════════════════════════════════════════
# STEP 1 — PERSONAL INFO
# ══════════════════════════════════════════════════════════════════════════════
elif st.session_state.step == 1:
    render_brand()
    st.progress(33)
    st.markdown(f'<div class="sec-label">{t["step1_label"]}</div>', unsafe_allow_html=True)

    d = st.session_state.data

    # Init companies list in session state
    if "companies" not in st.session_state:
        st.session_state.companies = [{"company": "", "title": "", "duration": t["duration_opts"][0]}]

    with st.form("basic_info"):
        name    = st.text_input(t["full_name"],  value=d.get("name", ""))
        phone   = st.text_input(t["phone"],      value=d.get("phone", ""))
        address = st.text_input(t["address"],    value=d.get("address", ""))

        age_opts = t["age_opts"]
        age_idx  = age_opts.index(d["age"]) if d.get("age") in age_opts else 0
        age      = st.selectbox(t["age"], age_opts, index=age_idx)

        edu_opts  = t["edu_opts"]
        edu_idx   = edu_opts.index(d["education"]) if d.get("education") in edu_opts else 0
        education = st.selectbox(t["edu"], edu_opts, index=edu_idx)

        major   = st.text_input(t["major"], value=d.get("major", ""))

        years_opts = t["years_opts"]
        years_idx  = years_opts.index(d["years_exp"]) if d.get("years_exp") in years_opts else 0
        years_exp  = st.selectbox(t["years_exp"], years_opts, index=years_idx)

        # ── Work Experience entries
        st.markdown(f'<div style="font-size:8.5px;letter-spacing:3px;text-transform:uppercase;color:#5C6478;margin:20px 0 12px;">{t["exp_section"]}</div>', unsafe_allow_html=True)

        company_entries = []
        for i, comp in enumerate(st.session_state.companies):
            st.markdown(f'<div style="font-size:10px;color:#C8A45A;margin:8px 0 4px;">— {t["exp_label"]} {i+1}</div>', unsafe_allow_html=True)
            col1, col2 = st.columns(2)
            with col1:
                co_name = st.text_input(t["company_name"], value=comp.get("company",""), key=f"co_{i}")
            with col2:
                co_title = st.text_input(t["job_title"], value=comp.get("title",""), key=f"tl_{i}")
            dur_opts = t["duration_opts"]
            dur_idx  = dur_opts.index(comp.get("duration", dur_opts[0])) if comp.get("duration") in dur_opts else 0
            co_dur   = st.selectbox(t["duration"], dur_opts, index=dur_idx, key=f"du_{i}")
            company_entries.append({"company": co_name, "title": co_title, "duration": co_dur})

        submitted = st.form_submit_button(t["next"], use_container_width=True)

        if submitted:
            errors = []
            if not name.strip() or not phone.strip() or not address.strip():
                errors.append(t["err_required"])
            if age == age_opts[0]:
                errors.append(t["err_age"])
            if education == edu_opts[0]:
                errors.append(t["err_edu"])
            if years_exp == years_opts[0]:
                errors.append(t["err_exp"])
            if errors:
                for e in errors:
                    st.error(e)
            else:
                st.session_state.data.update({
                    "name": name, "phone": phone, "address": address,
                    "age": age, "education": education, "major": major,
                    "years_exp": years_exp,
                    "companies": company_entries,
                    "lang": st.session_state.lang,
                })
                st.session_state.companies = company_entries
                st.session_state.step = 2
                st.rerun()

    # Add company button (outside form)
    if st.button(t["add_exp"], use_container_width=False):
        st.session_state.companies.append({"company": "", "title": "", "duration": t["duration_opts"][0]})
        st.rerun()

# ══════════════════════════════════════════════════════════════════════════════
# STEP 2 — ASSESSMENT
# ══════════════════════════════════════════════════════════════════════════════
elif st.session_state.step == 2:
    render_brand()
    st.progress(66)
    st.markdown(f'<div class="sec-label">{t["step2_label"]}</div>', unsafe_allow_html=True)

    d = st.session_state.data

    with st.form("assessment"):
        q_motivation = st.radio(
            t["q_motivation"], t["q_motivation_opts"],
            index=t["q_motivation_opts"].index(d["q_motivation"]) if d.get("q_motivation") in t["q_motivation_opts"] else 0
        )
        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

        q_pressure = st.radio(
            t["q_pressure"], t["q_pressure_opts"],
            index=t["q_pressure_opts"].index(d["q_pressure"]) if d.get("q_pressure") in t["q_pressure_opts"] else 0
        )
        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

        q_rejection = st.radio(
            t["q_rejection"], t["q_rejection_opts"],
            index=t["q_rejection_opts"].index(d["q_rejection"]) if d.get("q_rejection") in t["q_rejection_opts"] else 0
        )
        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

        q_ambition = st.radio(
            t["q_ambition"], t["q_ambition_opts"],
            index=t["q_ambition_opts"].index(d["q_ambition"]) if d.get("q_ambition") in t["q_ambition_opts"] else 0
        )
        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

        q_work_env = st.radio(
            t["q_work_env"], t["q_work_env_opts"],
            index=t["q_work_env_opts"].index(d["q_work_env"]) if d.get("q_work_env") in t["q_work_env_opts"] else 0
        )
        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

        open_q = st.text_area(t["open_q"], value=d.get("open_q", ""), height=120)

        col_back, col_next = st.columns(2)
        with col_back:
            back = st.form_submit_button(t["back"], use_container_width=True)
        with col_next:
            submitted2 = st.form_submit_button(t["generate"], use_container_width=True)

        if back:
            st.session_state.step = 1
            st.rerun()

        if submitted2:
            if not open_q.strip():
                st.error(t["err_open"])
            else:
                st.session_state.data.update({
                    "q_motivation": q_motivation,
                    "q_pressure":   q_pressure,
                    "q_rejection":  q_rejection,
                    "q_ambition":   q_ambition,
                    "q_work_env":   q_work_env,
                    "open_q":       open_q,
                })
                st.session_state.step = 3
                st.rerun()

# ══════════════════════════════════════════════════════════════════════════════
# STEP 3 — RESULT
# ══════════════════════════════════════════════════════════════════════════════
elif st.session_state.step == 3:
    render_brand()
    st.progress(100)
    data = st.session_state.data

    companies_text = "\n".join([
        f"  - {c.get('company','')} | {c.get('title','')} | {c.get('duration','')}"
        for c in data.get("companies", []) if c.get("company","").strip()
    ]) or "  - No previous experience (Entry Level)"

    if st.session_state.cv_text is None:
        with st.spinner(t["generating"]):

            # ── PROMPT 1: CV only
            cv_prompt = f"""
You are a senior ATS-certified resume writer. Write a professional ATS-optimized CV in ENGLISH ONLY.

Candidate:
- Name: {data['name']}
- Age: {data['age']}
- Address: {data['address']}, Egypt
- Phone: {data['phone']}
- Education: {data['education']} in {data.get('major','')}
- Years of Sales Experience: {data['years_exp']}
- Previous Companies:
{companies_text}

Self-Description: {data['open_q']}

Write EXACTLY in this format. Plain text only. No markdown. No bold markers. No special characters. ATS clean:

PROFESSIONAL SUMMARY
Write 3 strong action-verb sentences tailored for a Sales professional in Egypt. Be specific, not generic.

CORE COMPETENCIES
- Competency 1
- Competency 2
- Competency 3
- Competency 4
- Competency 5
- Competency 6
- Competency 7
- Competency 8

EDUCATION
{data['education']} in {data.get('major','')}
Egypt

LANGUAGES
- Arabic: Native
- English: Intermediate

RULES:
- English ONLY. No Arabic.
- No fake data. No fabricated companies or dates.
- Plain text, ATS must parse perfectly.
- Do NOT include contact info or name (handled separately).
- Do NOT include assessment or score.
"""

            # ── PROMPT 2: Assessment only
            exp_level = data['years_exp']
            assessment_prompt = f"""
You are a senior HR specialist and talent assessor. Write a confidential assessment report in ENGLISH ONLY.

Candidate:
- Name: {data['name']}
- Age: {data['age']}
- Education: {data['education']} in {data.get('major','')}
- Years of Experience: {data['years_exp']}
- Companies:
{companies_text}
- Motivation: {data['q_motivation']}
- Handles Pressure: {data['q_pressure']}
- Handles Rejection: {data['q_rejection']}
- Career Ambition: {data['q_ambition']}
- Work Environment Preference: {data['q_work_env']}
- Self Description: {data['open_q']}

Write EXACTLY in this format. Plain text. No markdown. No bold:

Score: X/10
Best Fit Role: (suggest 1-2 specific roles based on profile)
Recommendation: HIGHLY RECOMMENDED / RECOMMENDED / NEEDS DEVELOPMENT / NOT SUITABLE

Key Findings:
- (finding 1 — be specific and honest)
- (finding 2)
- (finding 3)

Candidate Answers:
- Motivation for Sales: {data['q_motivation']}
- Handles Pressure by: {data['q_pressure']}
- Response to Rejection: {data['q_rejection']}
- Career Ambition: {data['q_ambition']}
- Work Environment: {data['q_work_env']}

RULES:
- Be honest. Give realistic score based on answers.
- If entry level, suggest roles they CAN learn and grow into.
- English ONLY. No Arabic.
- Plain text, no markdown.
"""

            cv_result         = ask_ai(cv_prompt)
            assessment_result = ask_ai(assessment_prompt)

        if cv_result is None or assessment_result is None:
            st.stop()

        st.session_state.cv_text         = cv_result
        st.session_state.assessment_text = assessment_result
        save_to_csv(data)

    # ── DISPLAY RESULTS
    st.markdown(f'<div class="success-banner">{t["success"]} — {data["name"]}</div>', unsafe_allow_html=True)

    # CV Preview
    st.markdown(f'<div class="sec-label">{t["preview_cv"]}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="cv-box">{st.session_state.cv_text}</div>', unsafe_allow_html=True)

    cv_pdf = generate_cv_pdf(st.session_state.cv_text, data)
    safe_name = data['name'].replace(' ', '_')
    st.download_button(
        label=t["download_cv"],
        data=cv_pdf,
        file_name=f"CV_{safe_name}_Talently.pdf",
        mime="application/pdf",
        use_container_width=True,
    )

    st.markdown("<br>", unsafe_allow_html=True)

    # Assessment Preview
    st.markdown(f'<div class="sec-label">{t["preview_report"]}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="cv-box">{st.session_state.assessment_text}</div>', unsafe_allow_html=True)

    report_pdf = generate_report_pdf(st.session_state.assessment_text, data)
    st.download_button(
        label=t["download_report"],
        data=report_pdf,
        file_name=f"Assessment_{safe_name}_Talently.pdf",
        mime="application/pdf",
        use_container_width=True,
    )

    st.markdown("<br>", unsafe_allow_html=True)

    if st.button(t["restart_btn"], use_container_width=True):
        st.session_state.step = 0
        st.session_state.data = {}
        st.session_state.cv_text = None
        st.session_state.assessment_text = None
        if "companies" in st.session_state:
            del st.session_state.companies
        st.rerun()

    st.markdown(
        f'<p style="text-align:center;font-size:11px;color:#2A3448;margin-top:32px;letter-spacing:3px;">{t["footer_contact"]}</p>',
        unsafe_allow_html=True
    )
