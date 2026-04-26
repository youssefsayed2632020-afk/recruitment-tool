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
for k, v in [("step", 0), ("data", {}), ("cv_text", None), ("lang", None)]:
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
        "stat1_n": "5", "stat1_l": "دقائق فقط",
        "stat2_n": "ATS", "stat2_l": "محسّن بالكامل",
        "stat3_n": "PDF", "stat3_l": "احترافي",
        "start_btn": "ابدأ التقييم الآن",
        "step1_label": "الخطوة الأولى — البيانات الشخصية",
        "step2_label": "الخطوة الثانية — التقييم المهني",
        "full_name": "الاسم الكامل",
        "email": "البريد الإلكتروني",
        "phone": "رقم الهاتف",
        "city": "المدينة",
        "city_opts": ["اختر", "القاهرة", "الإسكندرية", "الجيزة", "المنصورة", "أسيوط", "طنطا", "أخرى"],
        "edu": "المؤهل الدراسي",
        "edu_opts": ["اختر", "طالب جامعي", "بكالوريوس", "دبلوم", "ماجستير", "ثانوية عامة"],
        "major": "التخصص / المجال الدراسي",
        "years_exp": "سنوات الخبرة في المبيعات",
        "years_opts": ["اختر", "لا يوجد (مبتدئ)", "أقل من سنة", "1 – 2 سنة", "3 – 5 سنوات", "أكثر من 5 سنوات"],
        "prev_job": "المسمى الوظيفي السابق (اختياري)",
        "next": "التالي ←",
        "back": "→ رجوع",
        "generate": "إنشاء السيرة الذاتية ✦",
        "err_required": "⚠️ من فضلك أكمل جميع الحقول المطلوبة",
        "err_city": "⚠️ من فضلك اختر المدينة",
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
        "q_learn": "كيف تكتسب مهارات جديدة في بيئة العمل؟",
        "q_learn_opts": [
            "التجربة العملية المباشرة والخطأ والتعلم",
            "مشاهدة كيف يعمل الزملاء الناجحون",
            "البحث الذاتي والتدريب عبر الإنترنت",
            "الحصول على تغذية راجعة مستمرة من المدير",
        ],
        "q_training": "إذا طُلب منك الالتزام بتدريب مكثف لمدة أسبوعين قبل البدء — ما موقفك؟",
        "q_training_opts": [
            "موافق تماماً، التدريب يُعدّني للنجاح",
            "موافق شرط أن يكون التدريب عملياً وليس نظرياً",
            "أفضل البدء فوراً والتعلم أثناء العمل",
            "أحتاج أعرف تفاصيل التدريب قبل الموافقة",
        ],
        "q_scenario": "في أول أسبوع لك، طُلب منك إقناع 10 عملاء يومياً بالهاتف. كيف ستبدأ؟",
        "q_scenario_opts": [
            "أدرس المنتج جيداً أولاً ثم أبدأ بالاتصال",
            "أبدأ فوراً وأتعلم من كل محادثة",
            "أطلب الاستماع لزميل ناجح قبل أن أبدأ",
            "أضع سكريبت واضح لنفسي وألتزم به",
        ],
        "open_q": "عرّف عن نفسك في 3 جمل (نقاط قوتك وطموحك)",
        "generating": "جاري إعداد سيرتك الذاتية...",
        "success": "تم إعداد سيرتك الذاتية بنجاح",
        "preview_label": "معاينة السيرة الذاتية",
        "download_btn": "تحميل السيرة الذاتية — PDF",
        "restart_btn": "بدء تقييم جديد",
        "footer_contact": "سيتم التواصل معك قريباً",
        "lang_label": "اختر لغتك",
        "choose_lang": "اختر اللغة للمتابعة",
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
        "stat1_n": "5", "stat1_l": "Minutes Only",
        "stat2_n": "ATS", "stat2_l": "Fully Optimized",
        "stat3_n": "PDF", "stat3_l": "Professional",
        "start_btn": "Start Assessment Now",
        "step1_label": "Step One — Personal Information",
        "step2_label": "Step Two — Professional Assessment",
        "full_name": "Full Name",
        "email": "Email Address",
        "phone": "Phone Number",
        "city": "City",
        "city_opts": ["Select", "Cairo", "Alexandria", "Giza", "Mansoura", "Asyut", "Tanta", "Other"],
        "edu": "Education Level",
        "edu_opts": ["Select", "University Student", "Bachelor's Degree", "Diploma", "Master's Degree", "High School"],
        "major": "Major / Field of Study",
        "years_exp": "Years of Sales Experience",
        "years_opts": ["Select", "No Experience (Beginner)", "Less than 1 year", "1 – 2 years", "3 – 5 years", "More than 5 years"],
        "prev_job": "Previous Job Title (Optional)",
        "next": "Next →",
        "back": "← Back",
        "generate": "Generate CV ✦",
        "err_required": "⚠️ Please complete all required fields",
        "err_city": "⚠️ Please select your city",
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
        "q_learn": "How do you acquire new skills at work?",
        "q_learn_opts": [
            "Hands-on experience, trial and error",
            "Watching how successful colleagues work",
            "Self-research and online training",
            "Getting continuous feedback from management",
        ],
        "q_training": "If required to commit to 2 weeks of intensive training before starting — your stance?",
        "q_training_opts": [
            "Fully agree — training prepares me for success",
            "Agree, as long as training is practical not theoretical",
            "I prefer starting immediately and learning on the job",
            "I need to know training details before agreeing",
        ],
        "q_scenario": "In your first week, you're asked to call 10 clients daily by phone. How do you start?",
        "q_scenario_opts": [
            "Study the product well first, then start calling",
            "Start immediately and learn from each conversation",
            "Ask to listen to a successful colleague first",
            "Prepare a clear personal script and stick to it",
        ],
        "open_q": "Describe yourself in 3 sentences (your strengths and ambitions)",
        "generating": "Preparing your CV...",
        "success": "Your CV has been prepared successfully",
        "preview_label": "CV Preview",
        "download_btn": "Download CV — PDF",
        "restart_btn": "Start New Assessment",
        "footer_contact": "We will contact you soon",
        "lang_label": "Choose Your Language",
        "choose_lang": "Choose your language to continue",
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

/* ═══ KEYFRAMES ═══ */
@keyframes fadeUp {
  from { opacity: 0; transform: translateY(20px); }
  to   { opacity: 1; transform: translateY(0); }
}
@keyframes fadeIn {
  from { opacity: 0; }
  to   { opacity: 1; }
}
@keyframes shimmer {
  0%   { left: -100%; }
  100% { left: 220%; }
}
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
@keyframes orb1 {
  0%,100% { transform: translate(0,0) scale(1); opacity: 0.5; }
  33%     { transform: translate(30px,-20px) scale(1.1); opacity: 0.8; }
  66%     { transform: translate(-20px,15px) scale(0.95); opacity: 0.6; }
}
@keyframes orb2 {
  0%,100% { transform: translate(0,0) scale(1); opacity: 0.4; }
  50%     { transform: translate(-25px,20px) scale(1.12); opacity: 0.7; }
}
@keyframes floatY {
  0%,100% { transform: translateY(0px); }
  50%     { transform: translateY(-8px); }
}
@keyframes scanLine {
  0%   { top: -2px; opacity: 0; }
  10%  { opacity: 0.6; }
  90%  { opacity: 0.4; }
  100% { top: 100%; opacity: 0; }
}
@keyframes borderGlow {
  0%,100% { border-color: rgba(200,164,90,0.12); }
  50%     { border-color: rgba(200,164,90,0.35); }
}

/* ═══ AMBIENT ORBS (decorative background shapes) ═══ */
.orb-container {
  position: fixed; inset: 0; pointer-events: none; z-index: 0; overflow: hidden;
}
.orb {
  position: absolute; border-radius: 50%;
  filter: blur(80px);
}
.orb-1 {
  width: 400px; height: 300px;
  background: radial-gradient(ellipse, rgba(200,164,90,0.12) 0%, transparent 70%);
  top: -80px; left: -100px;
  animation: orb1 14s ease-in-out infinite;
}
.orb-2 {
  width: 350px; height: 350px;
  background: radial-gradient(ellipse, rgba(200,164,90,0.07) 0%, transparent 70%);
  bottom: 5%; right: -80px;
  animation: orb2 18s ease-in-out infinite;
}

/* ═══ BRAND BAR ═══ */
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
  font-size: 22px; font-weight: 600;
  color: var(--white); letter-spacing: 8px;
  text-transform: uppercase;
  text-shadow: 0 0 40px rgba(200,164,90,0.25);
}
.brand-dot {
  width: 5px; height: 5px;
  background: var(--gold);
  border-radius: 50%;
  display: inline-block;
  margin: 0 2px 3px;
  vertical-align: middle;
  animation: dotBeat 2.6s ease-in-out infinite;
  box-shadow: 0 0 8px rgba(200,164,90,0.7);
}
.brand-sub-name {
  font-size: 9px; letter-spacing: 3px;
  text-transform: uppercase;
  color: var(--goldD);
  font-weight: 300;
  opacity: 0.7;
  font-family: 'Outfit', sans-serif;
  padding-left: 2px;
}
.brand-tag {
  font-size: 8px; letter-spacing: 5px;
  text-transform: uppercase;
  color: var(--gold); font-weight: 300;
  opacity: 0.55;
  margin-top: 4px;
}

/* ═══ HERO ═══ */
.hero-eyebrow {
  font-size: 8px; letter-spacing: 5px;
  text-transform: uppercase; color: var(--gold);
  margin-bottom: 28px; font-weight: 400;
  display: flex; align-items: center; gap: 14px;
  opacity: 0;
  animation: fadeUp 0.7s ease 0.3s both;
}
.hero-eyebrow::before {
  content: '◈'; font-size: 11px;
  animation: pulseGold 3s ease-in-out infinite;
  filter: drop-shadow(0 0 6px rgba(200,164,90,0.6));
}
.hero-eyebrow::after {
  content: ''; flex: 1; height: 1px;
  background: linear-gradient(90deg, var(--goldB), transparent);
}

.hero-title {
  font-family: 'Cormorant Garamond', serif;
  font-size: 72px; font-weight: 400;
  color: var(--white); line-height: 1.0;
  margin-bottom: 8px; letter-spacing: -1px;
  opacity: 0;
  animation: fadeUp 0.85s ease 0.45s both;
  text-shadow: 0 4px 40px rgba(0,0,0,0.4);
}
.hero-title em   { color: var(--gold); font-style: italic; filter: drop-shadow(0 0 20px rgba(200,164,90,0.35)); }
.hero-title span { display: block; font-size: 56px; }

.hero-sub {
  font-size: 14px; color: var(--muted);
  font-weight: 300; line-height: 2.0;
  margin: 28px 0 52px; max-width: 400px;
  letter-spacing: 0.3px;
  opacity: 0;
  animation: fadeUp 0.85s ease 0.6s both;
}
.hero-sub strong { color: var(--soft); font-weight: 400; }

/* ═══ STATS GRID ═══ */
.stats-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1px;
  background: var(--borderG);
  border: 1px solid var(--borderG);
  border-radius: 6px;
  overflow: hidden;
  margin-bottom: 52px;
  opacity: 0;
  animation: fadeUp 0.85s ease 0.75s both, glowPulse 5s ease 2s infinite;
}
.stat-cell {
  background: var(--navy2);
  padding: 32px 16px;
  text-align: center;
  position: relative;
  overflow: hidden;
  transition: background 0.4s ease, transform 0.3s ease;
}
.stat-cell::after {
  content: '';
  position: absolute;
  top: 0; left: -100%; width: 55%; height: 100%;
  background: linear-gradient(120deg, transparent, rgba(200,164,90,0.08), transparent);
  pointer-events: none;
}
.stat-cell::before {
  content: '';
  position: absolute;
  top: 0; left: 50%; transform: translateX(-50%);
  width: 0; height: 2px;
  background: linear-gradient(90deg, transparent, var(--gold), transparent);
  transition: width 0.45s ease;
}
.stat-cell:hover { background: var(--navy3); }
.stat-cell:hover::before { width: 60%; }
.stat-cell:hover::after { animation: shimmer 0.7s ease forwards; }

.stat-num {
  font-family: 'Cormorant Garamond', serif;
  font-size: 32px; font-weight: 600;
  color: var(--gold); line-height: 1;
  margin-bottom: 9px; letter-spacing: 1px;
  text-shadow: 0 0 20px rgba(200,164,90,0.4);
}
.stat-lbl {
  font-size: 7.5px; letter-spacing: 3px;
  text-transform: uppercase; color: var(--muted); font-weight: 400;
}

/* ═══ LANGUAGE SELECTOR ═══ */
.lang-screen {
  display: flex; flex-direction: column;
  align-items: center; justify-content: center;
  min-height: 50vh; gap: 32px;
  animation: fadeUp 0.8s ease both;
}
.lang-title {
  font-family: 'Cormorant Garamond', serif;
  font-size: 28px; font-weight: 400;
  color: var(--white); letter-spacing: 3px;
  text-align: center;
}
.lang-sub {
  font-size: 12px; color: var(--muted);
  letter-spacing: 3px; text-transform: uppercase;
  text-align: center;
}
.lang-buttons { display: flex; gap: 16px; width: 100%; max-width: 340px; }

/* ═══ SECTION LABEL ═══ */
.sec-label {
  font-size: 8.5px; letter-spacing: 4px;
  text-transform: uppercase; color: var(--gold);
  margin-bottom: 32px; padding-bottom: 14px;
  border-bottom: 1px solid var(--border);
  display: flex; align-items: center; gap: 10px;
  font-weight: 400;
  animation: fadeIn 0.7s ease both;
}
.sec-label::before { content: '—'; opacity: 0.4; }

/* ═══ SUCCESS BANNER ═══ */
.success-banner {
  background: linear-gradient(135deg, rgba(200,164,90,0.11), rgba(200,164,90,0.03));
  border: 1px solid var(--goldB);
  border-left: 2px solid var(--gold);
  padding: 16px 22px;
  border-radius: 5px;
  color: var(--gold2);
  font-size: 13px;
  letter-spacing: 0.4px;
  margin-bottom: 32px;
  display: flex; align-items: center; gap: 12px;
  animation: fadeUp 0.6s ease both, glowPulse 3s ease 0.8s infinite;
}
.success-banner::before {
  content: '✦'; font-size: 13px; opacity: 0.7;
  animation: pulseGold 2s ease-in-out infinite;
  filter: drop-shadow(0 0 5px rgba(200,164,90,0.6));
}

/* ═══ CV BOX ═══ */
.cv-box {
  background: var(--navy2);
  border: 1px solid var(--borderW);
  border-top: 1px solid var(--borderG);
  border-radius: 6px;
  padding: 36px 32px;
  font-size: 12.5px; line-height: 2.0;
  color: var(--soft);
  white-space: pre-wrap;
  font-family: 'Outfit', sans-serif; font-weight: 300;
  margin-bottom: 28px;
  box-shadow: 0 28px 72px rgba(0,0,0,0.6), inset 0 1px 0 rgba(255,255,255,0.04);
  animation: fadeUp 0.7s ease both;
  position: relative; overflow: hidden;
  animation: borderGlow 4s ease-in-out infinite;
}
.cv-box::before {
  content: '';
  position: absolute;
  top: 0; left: -100%; width: 55%; height: 1px;
  background: linear-gradient(90deg, transparent, rgba(200,164,90,0.6), transparent);
  animation: shimmer 2s ease 0.5s both;
}
/* scan line effect */
.cv-box::after {
  content: '';
  position: absolute;
  left: 0; right: 0; height: 2px;
  background: linear-gradient(90deg, transparent, rgba(200,164,90,0.08), transparent);
  animation: scanLine 5s linear 1s infinite;
}

/* ═══ PROGRESS ═══ */
.stProgress > div > div > div > div {
  background: linear-gradient(90deg, var(--goldD), var(--gold), var(--gold2)) !important;
  border-radius: 2px !important;
  position: relative; overflow: hidden;
  box-shadow: 0 0 12px rgba(200,164,90,0.35) !important;
}
.stProgress > div > div > div > div::after {
  content: '';
  position: absolute;
  top: 0; left: -100%; width: 55%; height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent);
  animation: shimmer 1.8s ease-in-out infinite;
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
  border-radius: 5px !important; color: var(--white) !important;
  font-family: 'Outfit', sans-serif !important;
  font-size: 14px !important; font-weight: 300 !important;
  padding: 16px 20px !important;
  transition: border-color 0.3s ease, background 0.3s ease, box-shadow 0.3s ease !important;
  letter-spacing: 0.3px !important;
}
.stTextInput > div > div > input:focus {
  border-color: rgba(200,164,90,0.55) !important; background: var(--navy3) !important;
  box-shadow: 0 0 0 3px rgba(200,164,90,0.09), 0 4px 20px rgba(0,0,0,0.3), 0 0 18px rgba(200,164,90,0.08) !important;
}
.stTextInput > div > div > input::placeholder { color: var(--muted) !important; opacity: 0.4 !important; }

.stTextArea > div > div > textarea {
  background: var(--navy2) !important;
  border: 1px solid var(--borderW) !important;
  border-radius: 5px !important; color: var(--white) !important;
  font-family: 'Outfit', sans-serif !important;
  font-size: 14px !important; font-weight: 300 !important;
  padding: 16px 20px !important;
  transition: border-color 0.3s ease, background 0.3s ease, box-shadow 0.3s ease !important;
  line-height: 1.8 !important;
}
.stTextArea > div > div > textarea:focus {
  border-color: rgba(200,164,90,0.55) !important; background: var(--navy3) !important;
  box-shadow: 0 0 0 3px rgba(200,164,90,0.09), 0 0 18px rgba(200,164,90,0.08) !important;
}

.stSelectbox > div > div {
  background: var(--navy2) !important;
  border: 1px solid var(--borderW) !important;
  border-radius: 5px !important; color: var(--white) !important;
  padding: 4px 0 !important;
  transition: border-color 0.3s ease, box-shadow 0.3s ease !important;
}
.stSelectbox > div > div:focus-within {
  border-color: rgba(200,164,90,0.55) !important;
  box-shadow: 0 0 0 3px rgba(200,164,90,0.09), 0 0 18px rgba(200,164,90,0.08) !important;
}
.stSelectbox > div > div > div { color: var(--white) !important; font-family: 'Outfit', sans-serif !important; font-weight: 300 !important; }
.stSelectbox svg { fill: var(--muted) !important; }

/* RADIO */
.stRadio > div { gap: 9px !important; flex-direction: column !important; }
.stRadio > div > label {
  background: var(--navy2) !important;
  border: 1px solid var(--borderW) !important;
  border-radius: 5px !important; padding: 15px 20px !important;
  color: var(--soft) !important; font-size: 13.5px !important;
  font-family: 'Outfit', sans-serif !important; font-weight: 300 !important;
  transition: border-color 0.28s ease, background 0.28s ease, transform 0.28s ease, color 0.28s ease, box-shadow 0.28s ease !important;
  cursor: pointer !important; letter-spacing: 0.2px !important;
  position: relative !important; overflow: hidden !important;
}
.stRadio > div > label:hover {
  border-color: var(--goldB) !important; color: var(--white) !important;
  background: var(--navy3) !important; transform: translateX(6px) !important;
  box-shadow: -3px 0 0 0 var(--gold), 0 4px 20px rgba(0,0,0,0.25) !important;
}
[data-baseweb="radio"] input:checked + div { border-color: var(--gold) !important; }

/* BUTTONS */
.stButton > button {
  background: transparent !important;
  border: 1px solid var(--goldB) !important;
  color: var(--gold) !important; border-radius: 5px !important;
  font-family: 'Outfit', sans-serif !important;
  font-size: 8.5px !important; font-weight: 500 !important;
  letter-spacing: 4px !important; text-transform: uppercase !important;
  padding: 19px 38px !important;
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
  background: linear-gradient(120deg, transparent, rgba(255,255,255,0.12), transparent) !important;
}
.stButton > button:hover {
  color: var(--ink) !important; border-color: var(--gold) !important;
  transform: translateY(-3px) !important;
  box-shadow: 0 14px 36px rgba(200,164,90,0.22), 0 4px 12px rgba(0,0,0,0.28), 0 0 0 1px rgba(200,164,90,0.2) !important;
}
.stButton > button:hover::before { opacity: 1 !important; }
.stButton > button:hover::after  { animation: shimmer 0.55s ease forwards !important; }
.stButton > button span { position: relative; z-index: 1; }

.stDownloadButton > button {
  background: linear-gradient(135deg, var(--gold) 0%, var(--goldD) 100%) !important;
  border: 1px solid transparent !important; color: var(--ink) !important;
  border-radius: 5px !important; font-family: 'Outfit', sans-serif !important;
  font-size: 8.5px !important; font-weight: 600 !important;
  letter-spacing: 4px !important; text-transform: uppercase !important;
  padding: 19px 38px !important;
  transition: transform 0.3s ease, box-shadow 0.3s ease !important;
  position: relative !important; overflow: hidden !important;
  box-shadow: 0 8px 28px rgba(200,164,90,0.25) !important;
}
.stDownloadButton > button::after {
  content: '' !important; position: absolute !important;
  top: 0; left: -100%; width: 55%; height: 100% !important;
  background: linear-gradient(120deg, transparent, rgba(255,255,255,0.2), transparent) !important;
}
.stDownloadButton > button:hover {
  background: linear-gradient(135deg, var(--gold2) 0%, var(--gold) 100%) !important;
  box-shadow: 0 18px 44px rgba(200,164,90,0.32), 0 4px 14px rgba(0,0,0,0.28) !important;
  transform: translateY(-3px) !important;
}
.stDownloadButton > button:hover::after { animation: shimmer 0.55s ease forwards !important; }

/* SPINNER */
.stSpinner > div { border-top-color: var(--gold) !important; }

/* FORM CONTAINER */
[data-testid="stForm"] {
  background: var(--navy2) !important;
  border: 1px solid var(--borderW) !important;
  border-top: 1px solid var(--borderG) !important;
  border-radius: 6px !important; padding: 36px 32px !important;
  box-shadow: 0 28px 72px rgba(0,0,0,0.45), inset 0 1px 0 rgba(255,255,255,0.04) !important;
  animation: fadeUp 0.75s ease both !important;
  position: relative !important; overflow: hidden !important;
}
[data-testid="stForm"]::before {
  content: '' !important; position: absolute !important;
  top: 0; left: -100%; width: 55%; height: 1px !important;
  background: linear-gradient(90deg, transparent, rgba(200,164,90,0.5), transparent) !important;
  animation: shimmer 1.5s ease 0.3s both !important;
}

/* ERROR */
.stAlert {
  background: rgba(160,50,50,0.07) !important;
  border: 1px solid rgba(200,80,80,0.2) !important;
  border-left: 2px solid rgba(200,80,80,0.55) !important;
  border-radius: 5px !important; color: #E0A0A0 !important;
  animation: fadeUp 0.4s ease both !important;
}

hr { border-color: var(--border) !important; opacity: 0.35 !important; }
</style>
""", unsafe_allow_html=True)

# ── AMBIENT ORBS ──────────────────────────────────────────────────────────────
st.markdown('<div class="orb-container"><div class="orb orb-1"></div><div class="orb orb-2"></div></div>', unsafe_allow_html=True)

# ── GROQ ──────────────────────────────────────────────────────────────────────
GROQ_API_KEY = st.secrets["GROQ_API_KEY"]

def ask_ai(prompt):
    try:
        response = requests.post(
            url="https://api.groq.com/openai/v1/chat/completions",
            headers={"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"},
            json={"model": "llama-3.3-70b-versatile", "messages": [{"role": "user", "content": prompt}]},
            timeout=45
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
        "timestamp","lang","name","email","phone","city","education","major",
        "years_exp","prev_job","q_motivation","q_pressure","q_rejection",
        "q_learn","q_training","q_scenario","open_q"
    ]
    file_exists = os.path.isfile(filename)
    with open(filename, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()
        row = {k: data.get(k, "") for k in fieldnames}
        row["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        writer.writerow(row)

# ── PDF (ATS-Clean) ───────────────────────────────────────────────────────────
def generate_pdf_ats(cv_text, data):
    """Pure ATS-optimized PDF — plain text, no images, no tables, no special chars."""
    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer, pagesize=A4,
        rightMargin=22*mm, leftMargin=22*mm,
        topMargin=18*mm, bottomMargin=18*mm
    )

    BLACK  = colors.HexColor("#0D0D0D")
    DGRAY  = colors.HexColor("#1A1A1A")
    MGRAY  = colors.HexColor("#444444")
    LGRAY  = colors.HexColor("#666666")
    RULE   = colors.HexColor("#CCCCCC")

    name_s    = ParagraphStyle("N",  fontName="Helvetica-Bold", fontSize=18, textColor=BLACK, alignment=TA_CENTER, spaceAfter=3, leading=22)
    contact_s = ParagraphStyle("C",  fontName="Helvetica",      fontSize=9,  textColor=LGRAY,  alignment=TA_CENTER, spaceAfter=10, leading=13)
    sec_s     = ParagraphStyle("S",  fontName="Helvetica-Bold", fontSize=10, textColor=BLACK, spaceAfter=4, spaceBefore=14, leading=14)
    body_s    = ParagraphStyle("B",  fontName="Helvetica",      fontSize=10, textColor=DGRAY, spaceAfter=4, leading=16)
    bullet_s  = ParagraphStyle("BU", fontName="Helvetica",      fontSize=10, textColor=DGRAY, spaceAfter=3, leading=15, leftIndent=14, firstLineIndent=-8)
    assess_s  = ParagraphStyle("A",  fontName="Helvetica",      fontSize=9,  textColor=MGRAY, spaceAfter=3, leading=14, leftIndent=12)
    score_s   = ParagraphStyle("SC", fontName="Helvetica-Bold", fontSize=11, textColor=BLACK, spaceAfter=6, leading=16)
    footer_s  = ParagraphStyle("F",  fontName="Helvetica",      fontSize=7.5,textColor=LGRAY, alignment=TA_CENTER, leading=11)

    story = []
    lines = cv_text.strip().split("\n")

    current_section = None
    name_done = False
    contact_done = False
    assessment_lines = []
    score_line = ""
    sections_data = {}
    current_key = None

    for line in lines:
        line = line.strip()
        if not line or line == "---": continue
        low = line.lower()

        # Name (all caps line, not a section header keyword)
        if not name_done and line.isupper() and len(line) > 3 and not any(k in low for k in ["assessment","curriculum","summary","competencies","education","attributes","languages"]):
            story.append(Paragraph(line, name_s))
            name_done = True
            continue

        # Contact line
        if not contact_done and "|" in line and ("@" in line or any(c.isdigit() for c in line)):
            story.append(Paragraph(line.replace("|", "  |  "), contact_s))
            story.append(HRFlowable(width="100%", thickness=0.8, color=RULE, spaceAfter=8, spaceBefore=2))
            contact_done = True
            continue

        # Score
        if "score:" in low:
            score_line = line
            continue

        # Section headers
        if "assessment report" in low:
            current_section = "assessment"
            continue
        elif "professional summary" in low:
            if assessment_lines or score_line:
                story.append(Paragraph("ASSESSMENT", sec_s))
                story.append(HRFlowable(width="100%", thickness=0.5, color=RULE, spaceAfter=5))
                if score_line:
                    story.append(Paragraph(score_line, score_s))
                for al in assessment_lines:
                    story.append(Paragraph(f"- {al}", assess_s))
                story.append(Spacer(1, 5*mm))
            current_section = "summary"
            story.append(Paragraph("PROFESSIONAL SUMMARY", sec_s))
            story.append(HRFlowable(width="100%", thickness=0.5, color=RULE, spaceAfter=5))
            continue
        elif "core competencies" in low:
            current_section = "competencies"
            story.append(Paragraph("CORE COMPETENCIES", sec_s))
            story.append(HRFlowable(width="100%", thickness=0.5, color=RULE, spaceAfter=5))
            continue
        elif "education" in low and len(line) < 20:
            current_section = "education"
            story.append(Paragraph("EDUCATION", sec_s))
            story.append(HRFlowable(width="100%", thickness=0.5, color=RULE, spaceAfter=5))
            continue
        elif "key attributes" in low:
            current_section = "attributes"
            story.append(Paragraph("KEY ATTRIBUTES", sec_s))
            story.append(HRFlowable(width="100%", thickness=0.5, color=RULE, spaceAfter=5))
            continue
        elif "languages" in low and len(line) < 15:
            current_section = "languages"
            story.append(Paragraph("LANGUAGES", sec_s))
            story.append(HRFlowable(width="100%", thickness=0.5, color=RULE, spaceAfter=5))
            continue
        elif "curriculum vitae" in low:
            current_section = None
            continue

        # Content
        if current_section == "assessment":
            clean = line.lstrip("-•– ").strip()
            if clean:
                assessment_lines.append(clean)
        elif current_section == "summary":
            if line:
                story.append(Paragraph(line, body_s))
        elif current_section in ("competencies", "attributes", "languages"):
            clean = line.lstrip("-•– ").strip()
            if clean:
                story.append(Paragraph(f"- {clean}", bullet_s))
        elif current_section == "education":
            if line:
                story.append(Paragraph(line, body_s))

    story.append(Spacer(1, 10*mm))
    story.append(HRFlowable(width="100%", thickness=0.5, color=RULE))
    story.append(Spacer(1, 2*mm))
    story.append(Paragraph(
        f"Generated: {datetime.now().strftime('%B %d, %Y')}  |  ATS-Optimized  |  Talently - Deals Outsourcing.com",
        footer_s
    ))

    doc.build(story)
    buffer.seek(0)
    return buffer

# ── BRAND BAR ─────────────────────────────────────────────────────────────────
def render_brand():
    lang = st.session_state.lang or "en"
    t = T[lang]
    st.markdown(f"""
    <div class="brand-bar">
      <div class="brand-left">
        <div class="brand-name">{t['brand']}<span class="brand-dot"></span></div>
        <div class="brand-sub-name">{t['brand_sub']}</div>
      </div>
      <div class="brand-tag">{t['brand_tag']}</div>
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

    st.markdown("""
    <p style="text-align:center; font-size:10px; color:#3A4558; margin-top:24px; letter-spacing:2px; font-family:Outfit,sans-serif;">
      Powered by Deals Outsourcing.com
    </p>
    """, unsafe_allow_html=True)
    st.stop()

# ── Active language
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
      <div class="stat-cell">
        <div class="stat-num">{t['stat1_n']}</div>
        <div class="stat-lbl">{t['stat1_l']}</div>
      </div>
      <div class="stat-cell">
        <div class="stat-num">{t['stat2_n']}</div>
        <div class="stat-lbl">{t['stat2_l']}</div>
      </div>
      <div class="stat-cell">
        <div class="stat-num">{t['stat3_n']}</div>
        <div class="stat-lbl">{t['stat3_l']}</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    if st.button(t["start_btn"], use_container_width=True):
        st.session_state.step = 1
        st.rerun()

# ══════════════════════════════════════════════════════════════════════════════
# STEP 1 — BASIC INFO
# ══════════════════════════════════════════════════════════════════════════════
elif st.session_state.step == 1:
    render_brand()
    st.progress(33)
    st.markdown(f'<div class="sec-label">{t["step1_label"]}</div>', unsafe_allow_html=True)

    d = st.session_state.data
    with st.form("basic_info"):
        name      = st.text_input(t["full_name"],  value=d.get("name",""))
        email     = st.text_input(t["email"],      value=d.get("email",""))
        phone     = st.text_input(t["phone"],      value=d.get("phone",""))

        city_opts = t["city_opts"]
        city_idx  = city_opts.index(d["city"]) if d.get("city") in city_opts else 0
        city      = st.selectbox(t["city"], city_opts, index=city_idx)

        edu_opts  = t["edu_opts"]
        edu_idx   = edu_opts.index(d["education"]) if d.get("education") in edu_opts else 0
        education = st.selectbox(t["edu"], edu_opts, index=edu_idx)

        major     = st.text_input(t["major"],      value=d.get("major",""))

        years_opts = t["years_opts"]
        years_idx  = years_opts.index(d["years_exp"]) if d.get("years_exp") in years_opts else 0
        years_exp  = st.selectbox(t["years_exp"], years_opts, index=years_idx)

        prev_job  = st.text_input(t["prev_job"],   value=d.get("prev_job",""))

        submitted = st.form_submit_button(t["next"], use_container_width=True)
        if submitted:
            if not name.strip() or not email.strip() or not phone.strip():
                st.error(t["err_required"])
            elif city == city_opts[0]:
                st.error(t["err_city"])
            elif education == edu_opts[0]:
                st.error(t["err_edu"])
            elif years_exp == years_opts[0]:
                st.error(t["err_exp"])
            else:
                st.session_state.data.update({
                    "name": name, "email": email, "phone": phone,
                    "city": city, "education": education, "major": major,
                    "years_exp": years_exp, "prev_job": prev_job
                })
                st.session_state.step = 2
                st.rerun()

# ══════════════════════════════════════════════════════════════════════════════
# STEP 2 — ASSESSMENT QUESTIONS
# ══════════════════════════════════════════════════════════════════════════════
elif st.session_state.step == 2:
    render_brand()
    st.progress(66)
    st.markdown(f'<div class="sec-label">{t["step2_label"]}</div>', unsafe_allow_html=True)

    d = st.session_state.data
    with st.form("assessment"):
        q_motivation = st.radio(t["q_motivation"], t["q_motivation_opts"],
                                index=t["q_motivation_opts"].index(d["q_motivation"]) if d.get("q_motivation") in t["q_motivation_opts"] else 0)
        st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)

        q_pressure   = st.radio(t["q_pressure"],   t["q_pressure_opts"],
                                index=t["q_pressure_opts"].index(d["q_pressure"]) if d.get("q_pressure") in t["q_pressure_opts"] else 0)
        st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)

        q_rejection  = st.radio(t["q_rejection"],  t["q_rejection_opts"],
                                index=t["q_rejection_opts"].index(d["q_rejection"]) if d.get("q_rejection") in t["q_rejection_opts"] else 0)
        st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)

        q_learn      = st.radio(t["q_learn"],      t["q_learn_opts"],
                                index=t["q_learn_opts"].index(d["q_learn"]) if d.get("q_learn") in t["q_learn_opts"] else 0)
        st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)

        q_training   = st.radio(t["q_training"],   t["q_training_opts"],
                                index=t["q_training_opts"].index(d["q_training"]) if d.get("q_training") in t["q_training_opts"] else 0)
        st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)

        q_scenario   = st.radio(t["q_scenario"],   t["q_scenario_opts"],
                                index=t["q_scenario_opts"].index(d["q_scenario"]) if d.get("q_scenario") in t["q_scenario_opts"] else 0)
        st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)

        open_q = st.text_area(t["open_q"], value=d.get("open_q",""), height=120)

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
                    "q_learn":      q_learn,
                    "q_training":   q_training,
                    "q_scenario":   q_scenario,
                    "open_q":       open_q,
                    "lang":         st.session_state.lang,
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

    if st.session_state.cv_text is None:
        st.markdown(f'<div class="sec-label">{t["generating"]}</div>', unsafe_allow_html=True)

        lang_instruction = "Arabic" if st.session_state.lang == "ar" else "English"

        prompt = f"""
You are a senior HR specialist and ATS-certified resume writer with expertise in Sales & Marketing roles in Egypt.

Your task: Write a professional ATS-optimized CV in ENGLISH ONLY (regardless of candidate language). No Arabic. No other language.

Candidate Profile:
- Full Name: {data['name']}
- Phone: {data['phone']}
- Email: {data['email']}
- City: {data['city']}, Egypt
- Education: {data['education']} in {data['major']}
- Years of Sales Experience: {data['years_exp']}
- Previous Job Title: {data.get('prev_job','N/A')}
- Motivation for Sales: {data['q_motivation']}
- Handles pressure by: {data['q_pressure']}
- Handles rejection by: {data['q_rejection']}
- Learning style: {data['q_learn']}
- Training commitment: {data['q_training']}
- First-week scenario: {data['q_scenario']}
- Self-description: {data['open_q']}

Write the CV in EXACTLY this format (no markdown, no bold, no special chars, ATS clean):

## ASSESSMENT REPORT
Score: X/10
Strengths:
- (strength 1 based on answers)
- (strength 2 based on answers)
- (strength 3 based on answers)
Recommendation: Suitable for Sales Role / Needs Development / Not Suitable at This Time

---

## CURRICULUM VITAE

{data['name'].upper()}
{data['city']}, Egypt | {data['phone']} | {data['email']}

PROFESSIONAL SUMMARY
Write 3 strong sentences. Use action verbs. Tailor for a Sales professional in Egypt. ATS-friendly. No fluff.

CORE COMPETENCIES
- Competency 1
- Competency 2
- Competency 3
- Competency 4
- Competency 5
- Competency 6

EDUCATION
{data['education']} in {data['major']}
Egypt

KEY ATTRIBUTES
- Attribute based on answers (be specific, not generic)
- Attribute based on answers
- Attribute based on answers

LANGUAGES
- Arabic: Native
- English: Intermediate

IMPORTANT RULES:
- English ONLY. No Arabic. No other languages. No markdown. No bold markers.
- No fake experience, no fake companies, no fabricated dates.
- Plain text only — ATS must parse this perfectly.
- Be honest in assessment, give realistic score based on candidate's answers.
"""
        with st.spinner(t["generating"]):
            result = ask_ai(prompt)

        if result is None:
            st.stop()

        st.session_state.cv_text = result
        save_to_csv(data)

    st.markdown(f'<div class="success-banner">{t["success"]} — {data["name"]}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="sec-label">{t["preview_label"]}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="cv-box">{st.session_state.cv_text}</div>', unsafe_allow_html=True)

    pdf_buffer = generate_pdf_ats(st.session_state.cv_text, data)
    safe_name  = data['name'].replace(' ', '_')

    st.download_button(
        label=t["download_btn"],
        data=pdf_buffer,
        file_name=f"CV_{safe_name}_Talently.pdf",
        mime="application/pdf",
        use_container_width=True,
    )

    st.markdown("<br>", unsafe_allow_html=True)

    if st.button(t["restart_btn"], use_container_width=True):
        st.session_state.step = 0
        st.session_state.data = {}
        st.session_state.cv_text = None
        st.rerun()

    st.markdown(
        f'<p style="text-align:center;font-size:11px;color:#2A3448;margin-top:32px;letter-spacing:3px;font-family:Outfit,sans-serif;">{t["footer_contact"]}</p>',
        unsafe_allow_html=True
    )
