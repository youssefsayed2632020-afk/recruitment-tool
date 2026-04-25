import streamlit as st

st.set_page_config(page_title="فرصتك المهنية", page_icon="🚀", layout="centered")

if "step" not in st.session_state:
    st.session_state.step = 0
if "data" not in st.session_state:
    st.session_state.data = {}

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
        name = st.text_input("🧑 الاسم الكامل")
        email = st.text_input("📧 البريد الإلكتروني")
        phone = st.text_input("📱 رقم الموبايل")
        city = st.selectbox("🏙️ المدينة", ["اختر", "القاهرة", "الإسكندرية", "الجيزة", "المنصورة", "أخرى"])
        education = st.selectbox("🎓 المؤهل", ["اختر", "طالب جامعي", "بكالوريوس", "دبلوم", "ماجستير", "ثانوية"])
        major = st.text_input("📚 التخصص")
        submitted = st.form_submit_button("التالي ←")
        if submitted:
            if not name or not email or not phone:
                st.error("⚠️ من فضلك املأ الاسم والإيميل والموبايل")
            else:
                st.session_state.data["name"] = name
                st.session_state.data["email"] = email
                st.session_state.data["phone"] = phone
                st.session_state.data["city"] = city
                st.session_state.data["education"] = education
                st.session_state.data["major"] = major
                st.session_state.step = 2
                st.rerun()

elif st.session_state.step == 2:
    st.progress(66)
    st.header("🧠 الخطوة 2 من 3 — شخصيتك المهنية")
    with st.form("personality"):
        q1 = st.radio("1️⃣ لو عندك عميل رافض يشتري، هتعمل إيه؟", [
            "أحاول أفهم سبب الرفض وأعيد الشرح",
            "أقبل الرفض وأنتقل لعميل آخر",
            "أطلب مساعدة من زميلي",
            "أحتاج وقت أفكر"])
        q2 = st.radio("2️⃣ إزاي بتوصف نفسك في الشغل؟", [
            "سريع التعلم ومحب للتطور",
            "منظم ودقيق في التفاصيل",
            "اجتماعي وبحب التعامل مع الناس",
            "مبدع وعندي أفكار جديدة"])
        q3 = st.radio("3️⃣ بيئة الشغل المفضلة؟", [
            "من البيت Remote",
            "في المكتب مع الفريق",
            "مش مهم طالما في تطور",
            "هجين"])
        q4 = st.radio("4️⃣ لو الشغل صعب في الأول هتعمل إيه؟", [
            "أصبر وأستمر",
            "أطلب تدريب إضافي",
            "أدور على طريقة أسهل",
            "أقيّم وأقرر"])
        q5 = st.radio("5️⃣ إيه اللي يحفزك في الشغل؟", [
            "الفلوس والعمولات",
            "التطور والتعلم",
            "الاستقرار والبيئة المريحة",
            "التأثير وإني أحس إن شغلي مهم"])
        open_q = st.text_area("6️⃣ عرّف عن نفسك في 3 جمل — ليه تستاهل الفرصة دي؟")
        submitted2 = st.form_submit_button("التالي ←")
        if submitted2:
            if not open_q:
                st.error("⚠️ من فضلك اكتب عن نفسك")
            else:
                st.session_state.data["q1"] = q1
                st.session_state.data["q2"] = q2
                st.session_state.data["q3"] = q3
                st.session_state.data["q4"] = q4
                st.session_state.data["q5"] = q5
                st.session_state.data["open_q"] = open_q
                st.session_state.step = 3
                st.rerun()

elif st.session_state.step == 3:
    st.progress(100)
    st.header("🎉 تم! بياناتك اتسجلت بنجاح")
    st.success("✅ شكراً " + st.session_state.data.get("name", "") + "! هنتواصل معاك قريباً")
    st.balloons()
    st.info("📧 هيوصلك CV احترافي على إيميلك خلال 24 ساعة")
