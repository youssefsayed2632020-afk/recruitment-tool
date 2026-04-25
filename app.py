import streamlit as st
import requests
import csv
import os
from datetime import datetime

GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]

def ask_ai(prompt):
    try:
        response = requests.post(
            url=f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}",
            headers={"Content-Type": "application/json"},
            json={"contents": [{"parts": [{"text": prompt}]}]},
            timeout=30
        )
        result = response.json()
        return result["candidates"][0]["content"]["parts"][0]["text"]
    except Exception as e:
        st.error(f"❌ خطأ: {str(e)}")
        return None

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

st.set_page_config(page_title="فرصتك المهنية", page_icon="🚀", layout="centered")

if "step" not in st.session_state:
    st.session_state.step = 0
if "data" not in st.session_state:
    st.session_state.data = {}
if "cv_text" not in st.session_state:
    st.session_state.cv_text = None

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

elif st.session_state.step == 1:
    st.progress(33)
    st.header("📋 الخطوة 1 من 3 — بياناتك الأساسية")
    with st.form("basic_info"):
        name = st.text_input("🧑 الاسم الكامل", value=st.session_state.data.get("name",""))
        email = st.text_input("📧 البريد الإلكتروني", value=st.session_state.data.get("email",""))
        phone = st.text_input("📱 رقم الموبايل", value=st.session_state.data.get("phone",""))
        city = st.selectbox("🏙️ المدينة", ["اختر","القاهرة","الإسكندرية","الجيزة","المنصورة","أخرى"])
        education = st.selectbox("🎓 المؤهل", ["اختر","طالب جامعي","بكالوريوس","دبلوم","ماجستير","ثانوية"])
        major = st.text_input("📚 التخصص", value=st.session_state.data.get("major",""))
        submitted = st.form_submit_button("التالي ←")
        if submitted:
            if not name or not email or not phone:
                st.error("⚠️ من فضلك املأ الاسم والإيميل والموبايل")
            elif city == "اختر":
                st.error("⚠️ من فضلك اختر المدينة")
            elif education == "اختر":
                st.error("⚠️ من فضلك اختر المؤهل")
            else:
                st.session_state.data.update({"name":name,"email":email,"phone":phone,"city":city,"education":education,"major":major})
                st.session_state.step = 2
                st.rerun()

elif st.session_state.step == 2:
    st.progress(66)
    st.header("🧠 الخطوة 2 من 3 — شخصيتك المهنية")
    q1_opts = ["أحاول أفهم سبب الرفض وأعيد الشرح","أقبل الرفض وأنتقل لعميل آخر","أطلب مساعدة من زميلي","أحتاج وقت أفكر"]
    q2_opts = ["سريع التعلم ومحب للتطور","منظم ودقيق في التفاصيل","اجتماعي وبحب التعامل مع الناس","مبدع وعندي أفكار جديدة"]
    q3_opts = ["من البيت Remote","في المكتب مع الفريق","مش مهم طالما في تطور","هجين"]
    q4_opts = ["أصبر وأستمر","أطلب تدريب إضافي","أدور على طريقة أسهل","أقيّم وأقرر"]
    q5_opts = ["الفلوس والعمولات","التطور والتعلم","الاستقرار والبيئة المريحة","التأثير وإني أحس إن شغلي مهم"]
    with st.form("personality"):
        q1 = st.radio("1️⃣ لو عندك عميل رافض يشتري، هتعمل إيه؟", q1_opts)
        q2 = st.radio("2️⃣ إزاي بتوصف نفسك في الشغل؟", q2_opts)
        q3 = st.radio("3️⃣ بيئة الشغل المفضلة؟", q3_opts)
        q4 = st.radio("4️⃣ لو الشغل صعب في الأول هتعمل إيه؟", q4_opts)
        q5 = st.radio("5️⃣ إيه اللي يحفزك في الشغل؟", q5_opts)
        open_q = st.text_area("6️⃣ عرّف عن نفسك في 3 جمل", value=st.session_state.data.get("open_q",""))
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
                st.session_state.data.update({"q1":q1,"q2":q2,"q3":q3,"q4":q4,"q5":q5,"open_q":open_q})
                st.session_state.step = 3
                st.rerun()

elif st.session_state.step == 3:
    st.progress(100)
    data = st.session_state.data
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
1. تقييم من 10 مع تبرير
2. أبرز 3 نقاط قوة
3. CV احترافي كامل
4. توصية: هل يناسب Sales؟
"""
        with st.spinner("🔄 جاري التحليل..."):
            result = ask_ai(prompt)
        if result is None:
            st.stop()
        st.session_state.cv_text = result
        save_to_csv(data)

    st.success("✅ تم التحليل بنجاح!")
    st.header(f"أهلاً {data['name']} 👋")
    st.markdown("---")
    st.subheader("📄 السيرة الذاتية والتحليل:")
    st.markdown(st.session_state.cv_text)
    st.markdown("---")
    st.download_button(
        label="⬇️ تحميل CV",
        data=st.session_state.cv_text.encode("utf-8"),
        file_name=f"CV_{data['name'].replace(' ','_')}.txt",
        mime="text/plain",
        use_container_width=True
    )
    if st.button("🔄 مرشح جديد", use_container_width=True):
        st.session_state.step = 0
        st.session_state.data = {}
        st.session_state.cv_text = None
        st.rerun()
    st.info("📧 سيتم التواصل معك قريباً")
