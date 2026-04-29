import streamlit as st
import google.generativeai as genai

# --- 1. CONFIGURATION (AI Brain) ---
# تأكد من وضع مفتاح الـ API الخاص بك هنا
genai.configure(api_key="AIzaSyB8sEgnmdUJhlp7Qa9--Wd--NWdvIKXRuA")

st.set_page_config(page_title="Talently AI v2", page_icon="🚀", layout="centered")

# --- 2. SESSION STATE MANAGEMENT ---
if "step" not in st.session_state:
    st.session_state.step = 1
if "user_data" not in st.session_state:
    st.session_state.user_data = {}

# --- 3. UI - STEP 1: DATA COLLECTION ---
if st.session_state.step == 1:
    st.title("🚀 Talently AI - Version 2")
    st.info("Let's build your professional future. Complete your profile below.")
    
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("Full Name", placeholder="e.g. Youssef Sayed")
        email = st.text_input("Email Address")
    with col2:
        city = st.text_input("City")
        status = st.selectbox("Current Job Status", ["Unemployed", "Employed", "Student"])

    path = st.selectbox("Choose your Target Career Path", 
                        ["Sales", "Customer Service", "Recruitment", "Operations", "Not Sure / Help Me Choose"])
    
    # Career Routing Logic
    if path == "Not Sure / Help Me Choose":
        interest = st.radio("What do you enjoy most?", 
                           ["Talking to people & hitting targets", "Solving problems & helping customers"])
        path = "Sales" if "targets" in interest else "Customer Service"

    exp = st.select_slider("Years of Experience", options=["0-1", "1-3", "3-5", "5+"])
    skills = st.text_area("List your skills (e.g. Excel, Communication, Teamwork)")

    if st.button("Next: Skill Assessment ➡️"):
        if name and email and city:
            st.session_state.user_data = {
                "name": name, "email": email, "city": city, 
                "status": status, "path": path, "exp": exp, "skills": skills
            }
            st.session_state.step = 2
            st.rerun()
        else:
            st.error("Please fill in your Name, Email, and City to continue.")

# --- 4. UI - STEP 2: ASSESSMENT ---
elif st.session_state.step == 2:
    st.title(f"🧠 {st.session_state.user_data['path']} Assessment")
    st.write("Answer these questions to help the AI evaluate your level.")
    
    q1 = st.radio("How do you respond to a difficult or angry client?", 
                 ["Stay calm and listen", "Explain the company rules strictly", "Transfer to manager immediately"])
    q2 = st.radio("If you have a high workload, how do you manage it?", 
                 ["Prioritize urgent tasks first", "Work faster on everything", "Ask colleagues for help"])
    english = st.select_slider("Rate your English level", options=["Basic", "Intermediate", "Very Good", "Fluent"])

    if st.button("Generate My Professional Package 🚀"):
        with st.spinner("Analyzing your profile... this takes about 10 seconds."):
            # --- THE MASTER PROMPT (Layered Architecture) ---
            master_prompt = f"""
            You are 'Talently AI v2'. Analyze the candidate and output 3 SECTIONS in English.
            
            CANDIDATE INFO:
            - Name: {st.session_state.user_data['name']} | City: {st.session_state.user_data['city']}
            - Target Path: {st.session_state.user_data['path']}
            - Exp: {st.session_state.user_data['exp']} | Skills: {st.session_state.user_data['skills']}
            - English: {english} | Situational Answers: {q1}, {q2}

            SECTION 1: ATS CV (Plain Text Only)
            Create a professional CV for the {st.session_state.user_data['path']} role. 
            Include: Summary, Skills, Experience, and Education. NO Markdown. NO Bold.

            SECTION 2: RECRUITMENT REPORT
            - Score: Assign a score out of 10.
            - Status: [Highly Recommended / Recommended / Needs Development]
            - Feedback: 2 Strengths and 1 Growth area.

            SECTION 3: 2-YEAR CAREER ROADMAP
            - Next Job Title: The best role for them now.
            - Roadmap: Step-by-step plan for the next 2 years in {st.session_state.user_data['path']}.
            """
            
            try:
                model = genai.GenerativeModel('gemini-pro')
                response = model.generate_content(master_prompt)
                st.session_state.final_result = response.text
                st.session_state.step = 3
                st.rerun()
            except Exception as e:
                st.error(f"Error: {e}. Check your API Key.")

# --- 5. UI - STEP 3: RESULTS ---
elif st.session_state.step == 3:
    st.title("🎁 Your Professional Package")
    st.success("Analysis Complete!")
    
    st.text_area("Your CV & Career Report", st.session_state.final_result, height=500)
    
    if st.button("⬅️ Start New Analysis"):
        st.session_state.step = 1
        st.rerun()
