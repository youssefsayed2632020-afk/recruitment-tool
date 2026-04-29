import streamlit as st
import google.generativeai as genai
import time

# --- CONFIG & AI SETUP ---
API_KEY = "PASTE_YOUR_API_KEY_HERE"
genai.configure(api_key=API_KEY)

st.set_page_config(page_title="Talently Infinity", page_icon="♾️", layout="wide")

# --- ULTRA UI CUSTOM CSS ---
st.markdown("""
    <style>
    /* تحسين الخلفية وتأثير الجزيئات */
    .main {
        background: radial-gradient(circle at center, #1b2735 0%, #090a0f 100%);
        color: #e0e0e0;
    }
    
    /* تصميم الكروت المضيئة */
    .stTextInput>div>div>input, .stSelectbox>div>div>div, .stTextArea>div>div>textarea {
        background: rgba(255, 255, 255, 0.03) !important;
        border: 1px solid rgba(0, 212, 255, 0.3) !important;
        border-radius: 15px !important;
        color: white !important;
        transition: 0.4s;
    }
    
    .stTextInput>div>div>input:focus {
        border-color: #00d4ff !important;
        box-shadow: 0 0 15px rgba(0, 212, 255, 0.5) !important;
    }

    /* أزرار النيون */
    .stButton>button {
        background: linear-gradient(45deg, #00c6ff, #0072ff) !important;
        border: none !important;
        border-radius: 30px !important;
        color: white !important;
        font-weight: 800 !important;
        padding: 1rem 2rem !important;
        box-shadow: 0 4px 15px rgba(0, 114, 255, 0.4) !important;
        width: 100%;
    }
    
    .stButton>button:hover {
        transform: scale(1.02) translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(0, 114, 255, 0.6) !important;
    }

    /* أنيميشن التحميل */
    @keyframes pulse {
        0% { opacity: 0.5; }
        50% { opacity: 1; }
        100% { opacity: 0.5; }
    }
    .analyzing-text { animation: pulse 1.5s infinite; color: #00d4ff; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

# --- SESSION LOGIC ---
if "step" not in st.session_state: st.session_state.step = 1
if "data" not in st.session_state: st.session_state.data = {}

# --- STEP 1: IDENTITY & TARGET ---
if st.session_state.step == 1:
    st.markdown("<h1 style='text-align: center; color: #00d4ff; font-size: 3.5rem;'>♾️ TALENTLY <span style='color: white;'>INFINITY</span></h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 1.2rem; opacity: 0.7;'>The Future of AI Recruitment Career Coaching</p>", unsafe_allow_html=True)
    
    st.write("---")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("### 📝 الأساسيات")
        name = st.text_input("الاسم بالكامل")
        email = st.text_input("الإيميل")
        path = st.selectbox("المسار المستهدف", ["Technical Sales", "Customer Success", "IT Operations", "HR Specialist"])
        
        if st.button("تأكيد وحجز مكانك في المستقبل ⚡"):
            if name and email:
                st.session_state.data.update({"name": name, "email": email, "path": path})
                st.session_state.step = 2
                st.rerun()
            else: st.error("من فضلك أدخل بياناتك لنبدأ.")

# --- STEP 2: BRAIN SCAN (SKILLS) ---
elif st.session_state.step == 2:
    st.markdown(f"<h2 style='text-align: center;'>🧠 تحليل مهارات: {st.session_state.data['name']}</h2>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        skills = st.text_area("أدخل كل مهاراتك (حتى البسيطة منها) - الذكاء الاصطناعي سيعيد صياغتها باحترافية:")
        experience = st.select_slider("سنوات الخبرة", options=["0 (Junior)", "1-3", "3-5", "5-10", "10+ (Expert)"])
        
        if st.button("بدء عملية التحليل العميق 🛡️"):
            st.session_state.data.update({"skills": skills, "exp": experience})
            
            # محاكاة تحليل ذكاء اصطناعي "بصري"
            placeholder = st.empty()
            for i in range(1, 101, 20):
                placeholder.markdown(f"<p class='analyzing-text'>Scanning Data... {i}%</p>", unsafe_allow_html=True)
                time.sleep(0.3)
            
            # --- THE INFINITY PROMPT ---
            prompt = f"""
            System: You are 'Talently Infinity AI', the most advanced career architect.
            User: {st.session_state.data['name']} | Target: {st.session_state.data['path']}
            Experience: {st.session_state.data['exp']} | Skills: {st.session_state.data['skills']}

            Task: Create a masterpiece output in English with 3 distinct blocks:
            1. [VIP_CV]: A high-end, executive-level CV structure. Use power verbs.
            2. [INSIGHTS]: A psychological evaluation of their profile, a score (0-100), and a secret 'Interview Hack' specific to {st.session_state.data['path']}.
            3. [TIMELINE]: A 24-month aggressive growth plan to double their salary.
            """
            
            model = genai.GenerativeModel('gemini-pro')
            response = model.generate_content(prompt)
            st.session_state.result = response.text
            st.session_state.step = 3
            st.rerun()

# --- STEP 3: THE INFINITY REVEAL ---
elif st.session_state.step == 3:
    st.markdown("<h1 style='text-align: center; color: #00d4ff;'>✨ النتائج النهائية</h1>", unsafe_allow_html=True)
    
    c1, c2 = st.columns([1.5, 1])
    
    with c1:
        st.markdown("### 📄 Professional ATS CV")
        cv_text = st.session_state.result.split("[INSIGHTS]")[0].replace("[VIP_CV]", "")
        st.text_area("", cv_text, height=500)
        
    with c2:
        st.markdown("### 📊 AI Insights & Score")
        insights = st.session_state.result.split("[INSIGHTS]")[1].split("[TIMELINE]")[0]
        st.info(insights)
        
        st.markdown("### 🗺️ Your Roadmap")
        roadmap = st.session_state.result.split("[TIMELINE]")[1]
        st.success(roadmap)

    if st.button("إعادة المحاكاة 🔄"):
        st.session_state.step = 1
        st.rerun()
