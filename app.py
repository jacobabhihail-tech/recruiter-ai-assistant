import streamlit as st

from src.resume_parser import extract_text_from_pdf
from src.llm import CandidateProfile, extract_candidate_profile


st.set_page_config(
    page_title="AI Recruitment Assistant",
    page_icon="🤖",
)

st.title("🤖 AI Recruitment Assistant")

st.write(
    "Hi! I’m your AI Recruitment Assistant. "
    "Upload your resume to get started."
)

uploaded_file =  st.file_uploader(
    'Upload your resume',
    type=["pdf"]
)

if uploaded_file is not None:

    st.success("Resume uploaded successfully!")

    resume_text = extract_text_from_pdf(uploaded_file)

    st.subheader("Extracted Resume Text")
    st.text_area(
        "Resume content",
        resume_text,
        height=400
    )

    with st.spinner("Analyzing your resume..."):

        candidate_profile = extract_candidate_profile(
            resume_text
        )

    st.subheader("Candidate Profile")

    st.json(candidate_profile.model_dump())