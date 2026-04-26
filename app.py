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

# ── INIT LANGUAGE FIRST (before any rendering) ────────────────────────────────
if "lang" not in st.session_state:
    st.session_state.lang = None  # None = language not chosen yet

# ── SESSION STATE ─────────────────────────────────────────────────────────────
for k, v in [("step", 0), ("data", {}), ("cv_text", None)]:
    if k not in st.session_state:
        st.session_state[k] = v

# ── TRANSLATIONS ──────────────────────────────────────────────────────────────
T = {
    "ar": {
        "brand": "Talently",
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
        "step2_label": "الخطوة الثانية — المعلومات الوظيفية",
        "step3_label": "الخطوة الثالثة — التقييم والتحليل",
        "full_name": "الاسم الكامل",
        "email": "البريد الإلكتروني",
        "phone": "رقم الهاتف",
        "city": "المدينة",
        "city_opts": ["اختر", "القاهرة", "الإسكندرية", "الجيزة", "المنصورة", "أسيوط", "طنطا", "أخرى"],
        "edu": "المؤهل الدراسي",
        "edu_opts": ["اختر", "طالب جامعي", "بكالوريوس", "دبلوم", "ماجستير", "ثانوية عامة"],
        "major": "التخصص / المجال الدراسي",
        "years_exp": "سنوات الخبرة في المبيعات",
        "years_opts": ["اختر", "لا يوجد خبرة (مبتدئ)", "أقل من سنة", "1 - 2 سنة", "3 - 5 سنوات", "أكثر من 5 سنوات"],
        "prev_job": "المسمى الوظيفي السابق (إن وجد)",
        "next": "التالي ←",
        "back": "→ رجوع",
        "generate": "إنشاء السيرة الذاتية ✦",
        "err_required": "⚠️ من فضلك أكمل جميع الحقول المطلوبة",
        "err_city": "⚠️ من فضلك اختر المدينة",
        "err_edu": "⚠️ من فضلك اختر المؤهل الدراسي",
        "err_exp": "⚠️ من فضلك اختر سنوات الخبرة",
        "err_open": "⚠️ من فضلك أجب على السؤال المفتوح",
        # Step 2 questions
        "q_motivation": "ما الذي يدفعك للعمل في مجال المبيعات؟",
        "q_motivation_opts": [
            "الدخل المرتفع والعمولات",
            "حب التواصل مع الناس وبناء العلاقات",
            "التحدي المستمر وتحقيق الأهداف",
            "التطور المهني والترقي السريع",
        ],
        "q_pressure": "كيف تتعامل مع ضغط العمل وتحقيق الأهداف الشهرية؟",
        "q_pressure_opts": [
            "أضع خطة يومية وأتابع أدائي باستمرار",
            "أركز على أكثر العملاء احتمالاً للشراء",
            "أطلب الدعم من مديري عند الحاجة",
            "أعمل ساعات إضافية حتى أحقق الهدف",
        ],
        "q_rejection": "عميل رفض عرضك بشكل قاطع — ما ردة فعلك؟",
        "q_rejection_opts": [
            "أحاول فهم سبب الرفض وأعود بعروض أفضل",
            "أقبل الرفض وأنتقل فوراً لعميل آخر",
            "أطلب وقتاً للتفكير وأعاود التواصل لاحقاً",
            "أحلل الموقف لتحسين أسلوبي في المستقبل",
        ],
        "q_learn": "كيف تتعلم مهارات جديدة في العمل؟",
        "q_learn_opts": [
            "من خلال التدريب العملي والتجربة المباشرة",
            "أشاهد مقا
