import streamlit as st
import google.generativeai as genai

# --- 1. الإعدادات الأساسية (الذكاء الاصطناعي) ---
# حط الـ API Key بتاعك هنا مكان الكلمة اللي تحت
API_KEY = "PASTE_YOUR_API_KEY_HERE"
genai.configure(api_key=API_KEY)

# --- 2. تصميم الواجهة (الديزاين القديم بتاعك) ---
st.set_page_config(page_title="Talently AI", page_icon="🚀", layout="centered")

# ده الجزء المسؤول عن المؤثرات البصرية والألوان اللي كانت عندك
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stButton>button { width: 100%; border-radius: 20px; height: 3em; background-color: #2e7d32; color: white; }
    .title-text { text-align: center; color: #00d4ff; font-family: 'Arial'; }
    </style>
    """, unsafe_allow_html=True)

if "step" not in st.session_state:
    st.session_state.step = 1
if "user_data" not in st.session_state:
    st.session_state.user_data = {}

# --- 3. المرحلة الأولى: إدخال البيانات (نفس شكلك القديم مع إضافات) ---
if st.session_state.step == 1:
    st.markdown("<h1 class='title-text'>🚀 Talently AI - تجربة احترافية جديدة</h1>", unsafe_allow_html=True)
    st.write("---")
    
    with st.container():
        name = st.text_input("الاسم بالكامل / Full Name", placeholder="Youssef Sayed")
        col1, col2 = st.columns(2)
        with col1:
            email = st.text_input("البريد الإلكتروني / Email")
        with col2:
            city = st.text_input("المدينة / City")
            
        path = st.selectbox("المسار الوظيفي المستهدف / Career Path", 
                            ["Sales", "Customer Service", "Recruitment", "Operations"])
        
        skills = st.text_area("المهارات والخبرات السابقة / Skills & Experience")
        
        if st.button("الاستمرار للتقييم / Next Step ➡️"):
            if name and email and city:
                st.session_state.user_data = {
                    "name": name, "email": email, "city": city, "path": path, "skills": skills
                }
                st.session_state.step = 2
                st.experimental_rerun()
            else:
                st.warning("برجاء إكمال البيانات الأساسية أولاً.")

# --- 4. المرحلة الثانية: التقييم والبرومبت المطور ---
elif st.session_state.step == 2:
    st.title(f"🧠 تقييم مسار: {st.session_state.user_data['path']}")
    
    q1 = st.radio("كيف تتعامل مع ضغط العمل المرتفع؟", 
                 ["أقوم بترتيب الأولويات والبدء بالأهم", "أعمل بسرعة أكبر لإنهاء كل شيء", "أطلب المساعدة فوراً"])
    
    english = st.select_slider("مستوى اللغة الإنجليزية", options=["Basic", "Intermediate", "Advanced"])

    if st.button("إصدار التقرير والـ CV وخطوة الطريق 🚀"):
        with st.spinner("جاري تحليل بياناتك بأعلى دقة..."):
            
            # --- البرومبت المطور (المخ الجديد) ---
            master_prompt = f"""
            System: Act as an Expert Career Coach & ATS Optimizer.
            Candidate Name: {st.session_state.user_data['name']}
            Target Role: {st.session_state.user_data['path']}
            Skills: {st.session_state.user_data['skills']}
            Assessment Answers: {q1}, English Level: {english}

            Provide a 3-part response in professional English:
            1. ATS-FRIENDLY CV: Professional summary, Skills list, and Experience section.
            2. RECRUITMENT REPORT: Assessment score (out of 10), Key strengths, and areas for improvement.
            3. 2-YEAR ROADMAP: A step-by-step career development plan for the next 24 months.
            """
            
            try:
                model = genai.GenerativeModel('gemini-pro')
                response = model.generate_content(master_prompt)
                st.session_state.final_result = response.text
                st.session_state.step = 3
                st.experimental_rerun()
            except Exception as e:
                st.error("حدث خطأ في الاتصال بالذكاء الاصطناعي. تأكد من الـ API Key.")

# --- 5. المرحلة الثالثة: عرض النتائج (بنفس أسلوبك) ---
elif st.session_state.step == 3:
    st.success("✅ تم استخراج ملفك الاحترافي بنجاح!")
    st.markdown("### نتائج التحليل والـ CV المطور:")
    st.text_area("", st.session_state.final_result, height=500)
    
    if st.button("بدء تحليل جديد 🔄"):
        st.session_state.step = 1
        st.experimental_rerun()
