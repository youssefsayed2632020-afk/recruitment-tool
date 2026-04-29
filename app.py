import streamlit as st
import google.generativeai as genai

# --- 1. CONFIGURATION ---
# حط الـ API Key بتاعك هنا
API_KEY = "PASTE_YOUR_API_KEY_HERE"
genai.configure(api_key=API_KEY)

st.set_page_config(page_title="Talently AI VIP", page_icon="💎", layout="wide")

# --- 2. ADVANCED UI (THE LOOK) ---
st.markdown("""
    <style>
    /* خلفية متدرجة احترافية */
    .main {
        background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
        color: white;
    }
    
    /* تصميم البطاقات الزجاجية */
    .glass-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 25px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        margin-bottom: 20px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
    }
    
    /* الزراير الذكية */
    .stButton>button {
        background: linear-gradient(90deg, #00d2ff 0%, #3a7bd5 100%);
        color: white;
        border: none;
        padding: 15px 30px;
        border-radius: 50px;
        font-weight: bold;
        transition: all 0.3s ease;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .stButton>button:hover {
        transform: translateY(-3px);
        box-shadow: 0 10px 20px rgba(0, 210, 255, 0.4);
        color: #fff;
    }

    /* عناوين النصوص */
    h1, h2, h3 {
        font-family: 'Inter', sans-serif;
        background: -webkit-linear-gradient(#eee, #333);
        -webkit-background-clip: text;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. SESSION STATE ---
if "step" not in st.session_state: st.session_state.step = 1
if "user_data" not in st.session_state: st.session_state.user_data = {}

# --- 4. STEP 1: SMART INPUT ---
if st.session_state.step == 1:
    st.markdown("<h1 style='text-align: center;'>💎 Talently AI <span style='color:#00d2ff'>VIP Edition</span></h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; opacity: 0.8;'>مستقبلك المهني يبدأ هنا بلمسة ذكاء اصطناعي</p>", unsafe_allow_html=True)
    
    with st.container():
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("👤 الاسم الكامل", placeholder="مثال: يوسف سيد")
            email = st.text_input("📧 البريد الإلكتروني")
        with col2:
            city = st.text_input("📍 المدينة")
            path = st.selectbox("🎯 المسار الوظيفي", ["Sales", "Customer Service", "Recruitment", "Operations", "Marketing"])
        
        skills = st.text_area("🛠️ مهاراتك وخبراتك (اكتب كل ما يميزك)")
        
        if st.button("انتقل للتقييم الذكي 🚀"):
            if name and email and path:
                st.session_state.user_data = {"name": name, "email": email, "city": city, "path": path, "skills": skills}
                st.session_state.step = 2
                st.rerun()
            else:
                st.error("من فضلك أكمل البيانات الأساسية لنبهرك بالنتائج!")
        st.markdown('</div>', unsafe_allow_html=True)

# --- 5. STEP 2: ASSESSMENT ---
elif st.session_state.step == 2:
    st.markdown(f"<h2>🧠 تقييم القدرات لـ {st.session_state.user_data['path']}</h2>", unsafe_allow_html=True)
    
    with st.container():
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        q1 = st.select_slider("ما مدى قدرتك على العمل تحت ضغط؟", options=["ضعيف", "متوسط", "ممتاز", "خارق"])
        q2 = st.radio("كيف تتعامل مع العملاء الصعوب؟", ["بالصبر والاستماع", "بالحزم والوضوح", "بتصعيد الأمر للمدير"])
        english = st.select_slider("مستواك في الإنجليزية", options=["Beginner", "Intermediate", "Advanced", "Fluent"])
        
        if st.button("توليد ملف المستقبل 🚀"):
            with st.spinner("⚡ يتم الآن تحليل بياناتك وصياغة مستقبلك..."):
                master_prompt = f"""
                You are a World-Class Career Strategist. Analyze {st.session_state.user_data['name']}.
                Role: {st.session_state.user_data['path']} | Skills: {st.session_state.user_data['skills']}
                Location: {st.session_state.user_data['city']} | Pressure: {q1} | English: {english}

                Provide 3 separate sections in English:
                1. [ATS_CV]: A modern, high-impact CV structure (Summary, Skills, Exp). No formatting.
                2. [REPORT]: Recruitment score (0-10), 3 Strengths, 1 Weakness, and 'Interview Tip'.
                3. [ROADMAP]: 2-year growth plan with specific milestones.
                """
                try:
                    model = genai.GenerativeModel('gemini-pro')
                    response = model.generate_content(master_prompt)
                    st.session_state.final_result = response.text
                    st.session_state.step = 3
                    st.rerun()
                except Exception as e:
                    st.error("تأكد من الـ API Key الخاص بك.")
        st.markdown('</div>', unsafe_allow_html=True)

# --- 6. STEP 3: THE RESULTS ---
elif st.session_state.step == 3:
    st.markdown("<h1>✨ ملفك الاحترافي الجاهز</h1>", unsafe_allow_html=True)
    
    # تقسيم الرد لسهولة القراءة
    res = st.session_state.final_result
    
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.subheader("📄 الـ CV المقترح (ATS Ready)")
    st.text_area("", res.split('[REPORT]')[0].replace('[ATS_CV]', ''), height=300)
    st.markdown('</div>', unsafe_allow_html=True)
    
    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.subheader("📊 تقرير التقييم")
        # عرض الجزء الخاص بالتقرير
        report_part = res.split('[REPORT]')[1].split('[ROADMAP]')[0] if '[ROADMAP]' in res else res
        st.write(report_part)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col_b:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.subheader("🛤️ خريطة الطريق (24 شهر)")
        roadmap_part = res.split('[ROADMAP]')[1] if '[ROADMAP]' in res else "Roadmap pending..."
        st.write(roadmap_part)
        st.markdown('</div>', unsafe_allow_html=True)

    if st.button("ابدأ من جديد 🔄"):
        st.session_state.step = 1
        st.rerun()
