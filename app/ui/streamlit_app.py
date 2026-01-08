import os
import streamlit as st
import json
from  api.resume_tailor.extract import extract_jd_requirements # Your extraction logic
from api.resume_tailor.score import calculate_score          # Your scoring logic
from api.resume_tailor.renderer import generate_tailored_resume         # The cleaned renderer

st.set_page_config(page_title="SniperHire-V1", layout="wide")

st.title("🎯 SniperHire-V1: Autonomous Resume Tailoring")
st.markdown("---")

# --- SIDEBAR: INPUTS ---
with st.sidebar:
    st.header("1. Data Upload")
    master_resume_file = st.file_uploader("Upload Master Resume (JSON)", type=['json'])
    jd_text = st.text_area("Paste Job Description", height=300)
    
    if st.button("🚀 Analyze & Tailor"):
        if master_resume_file and jd_text:
            with open("temp_resume.json", "wb") as f:
                f.write(master_resume_file.getbuffer())
            st.session_state.ready = True
        else:
            st.error("Please provide both a resume and a JD.")

# --- MAIN INTERFACE ---
if 'ready' in st.session_state:
    # Load data
    with open("temp_resume.json", "r") as f:
        master_resume = json.load(f)
    
    # Run the Engine
    with st.spinner("Targeting requirements..."):
        # 1. Extract Requirements
        jd_requirements = extract_jd_requirements(jd_text) 
        
        # 2. Calculate Score
        score, matches, missing = calculate_score(jd_requirements, master_resume)
        
    # --- DISPLAY METRICS ---
    col1, col2, col3 = st.columns(3)
    col1.metric("Match Score", f"{score}%")
    col2.write("**Matched Skills:**")
    col2.caption(", ".join(matches))
    col3.write("**Missing Keywords:**")
    col3.error(", ".join(missing))

    st.markdown("---")

    # --- TAILORING & GAP ANALYSIS ---
    with st.spinner("Injecting keywords & generating content..."):
        # Assuming you have a function run_tailor_llm() in your tailor.py
        # result = run_tailor_llm(master_resume, jd_requirements, jd_text, missing)
        # For now, we'll use your last output logic
        tailored_data = {} # This comes from your LLM call
        
    st.subheader("💡 Gap Analysis (How to hit 100%)")
    st.warning(tailored_data.get("gap_analysis", "No analysis available."))

    # --- THE GENERATOR ---
    st.subheader("📄 Final Documents")
    
    if st.button("🔨 Build Tailored PDF"):
        pdf_file = generate_pdf(tailored_data, master_resume)
        if pdf_file and os.path.exists(pdf_file):
            with open(pdf_file, "rb") as f:
                st.download_button("📥 Download Tailored Resume", f, file_name=pdf_file)
        else:
            st.error("LaTeX build failed. Check if MiKTeX is installed and in PATH.")

    with st.expander("View Tailored Cover Letter"):
        st.write(tailored_data.get("cover_letter", ""))