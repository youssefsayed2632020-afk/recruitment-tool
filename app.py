import streamlit as st
import requests
import json
import csv
import os
from datetime import datetime

# ─── API KEY ───────────────────────────────────────────────────────────────────
OPENROUTER_API_KEY = st.secrets["OPENROUTER_API_KEY"]

# ─── MODELS (fallback list) ────────────────────────────────────────────────────
MODELS = [
    "mistralai/mistral-7b-instruct:free",
    "google/gemma-3-4b-it:free",
    "meta-llama/llama-3.2-3b-instruct:free",
]

# ─── AI FUNCTION WITH FALLBACK & ERROR HANDLING ───────────────────────────────
def ask_ai(prompt):
    for model in MODELS:
        try:
            response = requests.post(
                url="https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                    "HTTP-Referer": "https://dawoodrecruitement.streamlit.app",
                    "X-Title": "Dawood Recruitment"
                },
                json={
                    "model": model,
                    "messages": [{"role": "user", "content": prompt}]
                },
                timeout=30
            )
            result = response.json()

            if "choices" in result and result["choices"]:
                return result["choices"][0]["message"]["content"]
            else:
                error_detail = result.get("error", {}).get("message", "Unknown error")
                st.warning(f"⚠️ الموديل {model} فشل: {error_detail} — بجرب الموديل التالي...")
                continue

        except requests.exceptions.Timeout:
            st.warning(f"⏱️ الموديل {model} استغرق وقت طويل — بجرب التالي...")
            continue
        except Exception as e:
            st.warning(f"❌ خطأ في {model}: {str(e)} — بجرب التالي...")
            continue

    st.error("❌ كل الموديلات فشلت. تحقق من الـ API key أو جرب مرة تانية.")
    return None

# ─── SAVE DATA TO CSV ─────────────────────────────────────────────────────────
def save_to_csv(data):
    filename = "applicants.csv"
    fieldnames = ["timestamp", "name", "email", "phone", "city",
                  "education", "major", "q1", "q2", "q3", "q4", "q5", "open_q"]
    file_exists = os.path.isfile(filename)
    with open(filename, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()
        row = {k: data.get(k, "") for k in fieldnames}
        row["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        writer.writerow(row)

# ─── PAGE CONFIG ──────────────────────────────────────────────────────────────
st.set_page_config(page_title="فرصتك المهنية", page_icon="🚀", layout="centered")

# ─── SESSION STATE ────────────────────────────────────────────────────────────
if "step" not in st.session_state:
    st.session_state.step = 0
if "data" not in st.session_state:
    st.session_state.data = {}
if "cv_text" not in st.session_state:
    st.session_state.cv_text = None

# ══════════════════════════════════════════════════════════════════════════════
# STEP 0 — Landing
# ══════════════════════════════════════════════════════════════════════════════
if st.session_state.step == 0:
    st.title("🚀 ابدأ مسيرتك المهنية")
    st.subheader("أداة ذكية تحلل شخصيتك وتولد CV احترافي مجاناً")
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("⏱️ الوقت", "4 دقائق")
    with col2:
        st.metric("🤖 تحليل", "ذكاء اصطناعي")
    with col3:
        st.metric("📄 النتيجة", "CV جاهز")
    st.markdown("---")
    if st.button("ابدأ الآن ←", use_container_width=True):
        st.session_state.step = 1
        st.rerun()

# ══════════════════════════════════════════════════════════════════════════════
# STEP 1 — Basic Info
# ══════════════════════════════════════════════════════════════════════════════
elif st.session_state.step == 1:
    st.progress(33)
    st.header("📋 الخطوة 1 من 3 — بياناتك الأساسية")
    with st.form("basic_info"):
        name      = st.text_input("🧑 الاسم الكامل",        value=st.session_state.data.get("name", ""))
        email     = st.text_input("📧 البريد الإلكتروني",   value=st.session_state.data.get("email", ""))
        phone     = st.text_input("📱 رقم الموبايل",        value=st.session_state.data.get("phone", ""))
        city      = st.selectbox("🏙️ المدينة",
                                 ["اختر", "القاهرة", "الإسكندرية", "الجيزة", "المنصورة", "أخرى"],
                                 index=["اختر","القاهرة","الإسكندرية","الجيزة","المنصورة","أخرى"]
                                        .index(st.session_state.data.get("city","اختر")))
        education = st.selectbox("🎓 المؤهل",
                                 ["اختر","طالب جامعي","بكالوريوس","دبلوم","ماجستير","ثانوية"],
                                 index=["اختر","طالب جامعي","بكالوريوس","دبلوم","ماجستير","ثانوية"]
                                        .index(st.session_state.data.get("education","اختر")))
        major     = st.text_input("📚 التخصص",              value=st.session_state.data.get("major", ""))
        submitted = st.form_submit_button("التالي ←")
        if submitted:
            if not name or not email or not phone:
                st.error("⚠️ من فضلك املأ الاسم والإيميل والموبايل")
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
# STEP 2 — Personality
# ══════════════════════════════════════════════════════════════════════════════
elif st.session_state.step == 2:
    st.progress(66)
    st.header("🧠 الخطوة 2 من 3 — شخصيتك المهنية")

    q1_opts = ["أحاول أفهم سبب الرفض وأعيد الشرح",
               "أقبل الرفض وأنتقل لعميل آخر",
               "أطلب مساعدة من زميلي",
               "أحتاج وقت أفكر"]
    q2_opts = ["سريع التعلم ومحب للتطور",
               "منظم ودقيق في التفاصيل",
               "اجتماعي وبحب التعامل مع الناس",
               "مبدع وعندي أفكار جديدة"]
    q3_opts = ["من البيت Remote",
               "في المكتب مع الفريق",
               "مش مهم طالما في تطور",
               "هجين"]
    q4_opts = ["أصبر وأستمر",
               "أطلب تدريب إضافي",
               "أدور على طريقة أسهل",
               "أقيّم وأقرر"]
    q5_opts = ["الفلوس والعمولات",
               "التطور والتعلم",
               "الاستقرار والبيئة المريحة",
               "التأثير وإني أحس إن شغلي مهم"]

    def get_idx(opts, key):
        val = st.session_state.data.get(key, opts[0])
        return opts.index(val) if val in opts else 0

    with st.form("personality"):
        q1     = st.radio("1️⃣ لو عندك عميل رافض يشتري، هتعمل إيه؟", q1_opts, index=get_idx(q1_opts, "q1"))
        q2     = st.radio("2️⃣ إزاي بتوصف نفسك في الشغل؟",            q2_opts, index=get_idx(q2_opts, "q2"))
        q3     = st.radio("3️⃣ بيئة الشغل المفضلة؟",                   q3_opts, index=get_idx(q3_opts, "q3"))
        q4     = st.radio("4️⃣ لو الشغل صعب في الأول هتعمل إيه؟",     q4_opts, index=get_idx(q4_opts, "q4"))
        q5     = st.radio("5️⃣ إيه اللي يحفزك في الشغل؟",              q5_opts, index=get_idx(q5_opts, "q5"))
        open_q = st.text_area("6️⃣ عرّف عن نفسك في 3 جمل — ليه تستاهل الفرصة دي؟",
                              value=st.session_state.data.get("open_q", ""))
        col_back, col_next = st.columns(2)
        with col_back:
            back = st.form_submit_button("← رجوع")
        with col_next:
            submitted2 = st.form_submit_button("تحليل شخصيتي وأنشئ CV ←")

        if back:
            st.session_state.step = 1
            st.rerun()

        if submitted2:
            if not open_q.strip():
                st.error("⚠️ من فضلك اكتب عن نفسك")
            else:
                st.session_state.data.update({
                    "q1": q1, "q2": q2, "q3": q3,
                    "q4": q4, "q5": q5, "open_q": open_q
                })
                st.session_state.step = 3
                st.rerun()

# ══════════════════════════════════════════════════════════════════════════════
# STEP 3 — AI Analysis & CV
# ══════════════════════════════════════════════════════════════════════════════
elif st.session_state.step == 3:
    st.progress(100)
    data = st.session_state.data

    # Only call AI once; cache result in session_state
    if st.session_state.cv_text is None:
        st.header("🤖 جاري تحليل شخصيتك...")
        prompt = f"""
أنت خبير موارد بشرية متخصص في Sales وMarketing.
حلل هذا المرشح وأنشئ CV احترافي باللغة العربية.

الاسم: {data['name']}
المدينة: {data['city']}
المؤهل: {data['education']} - {data['major']}
التعامل مع رفض العميل: {data['q1']}
وصف نفسه: {data['q2']}
بيئة الشغل: {data['q3']}
التعامل مع الصعوبات: {data['q4']}
المحفز: {data['q5']}
عن نفسه: {data['open_q']}

المطلوب:
1. تقييم من 10 مع تبرير قصير
2. أبرز 3 نقاط قوة
3. CV احترافي كامل (معلومات شخصية، ملخص مهني، مهارات، تعليم، توصية وظيفية)
4. توصية نهائية: هل يناسب Sales؟ ولماذا؟
"""
        with st.spinner("🔄 جاري التحليل، انتظر لحظة..."):
            result = ask_ai(prompt)

        if result is None:
            st.stop()

        st.session_state.cv_text = result
        # Save applicant data to CSV
        save_to_csv(data)

    # ── Display Result ──
    st.success("✅ تم التحليل بنجاح!")
    st.header(f"أهلاً {data['name']} 👋")
    st.markdown("---")
    st.subheader("📄 السيرة الذاتية والتحليل:")
    st.markdown(st.session_state.cv_text)
    st.markdown("---")

    # ── Download CV as text file ──
    st.download_button(
        label="⬇️ تحميل CV كملف نصي",
        data=st.session_state.cv_text.encode("utf-8"),
        file_name=f"CV_{data['name'].replace(' ', '_')}.txt",
        mime="text/plain",
        use_container_width=True
    )

    st.markdown("---")

    # ── Start over ──
    if st.button("🔄 تقديم مرشح جديد", use_container_width=True):
        st.session_state.step = 0
        st.session_state.data = {}
        st.session_state.cv_text = None
        st.rerun()

    st.info("📧 سيتم التواصل معك على الإيميل المسجل قريباً")
