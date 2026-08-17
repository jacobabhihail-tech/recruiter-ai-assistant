import streamlit as st

from src.resume_parser import extract_text_from_pdf
from src.llm import extract_candidate_profile
from src.profile_engine import generate_candidate_insights
from src.intake_schema import CandidatePreferences


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="AI Recruitment Assistant",
    page_icon="🤖",
)


# --------------------------------------------------
# WELCOME SCREEN
# --------------------------------------------------

st.title("🤖 AI Recruitment Assistant")

st.write(
    "Hi! I am your AI Recruitment Assistant. "
    "Upload your resume to get started."
)


# --------------------------------------------------
# RESUME UPLOAD
# --------------------------------------------------

uploaded_file = st.file_uploader(
    "Upload your resume",
    type=["pdf"]
)


if uploaded_file is not None:

    st.success("Resume uploaded successfully!")


    # --------------------------------------------------
    # STEP 1: EXTRACT TEXT FROM RESUME
    # --------------------------------------------------

    resume_text = extract_text_from_pdf(uploaded_file)

    st.subheader("Extracted Resume Text")

    st.text_area(
        "Resume content",
        resume_text,
        height=400
    )


    # --------------------------------------------------
    # STEP 2: EXTRACT CANDIDATE PROFILE
    # --------------------------------------------------

    with st.spinner("Analyzing your resume..."):

        candidate_profile = extract_candidate_profile(
            resume_text
        )


    st.subheader("Candidate Profile")

    st.json(
        candidate_profile.model_dump()
    )


    # --------------------------------------------------
    # STEP 3: GENERATE AI CANDIDATE INSIGHTS
    # --------------------------------------------------

    with st.spinner("Generating Candidate Insights..."):

        candidate_insights = generate_candidate_insights(
            candidate_profile
        )


    st.subheader("🤖 AI Candidate Insights")

    st.json(
        candidate_insights.model_dump()
    )


    # --------------------------------------------------
    # STEP 4: RECRUITER SCREENING
    # --------------------------------------------------

    st.subheader("💬 Recruiter Screening")


    # Initialize screening state
    if "intake_started" not in st.session_state:
        st.session_state.intake_started = False

    if "intake_step" not in st.session_state:
        st.session_state.intake_step = 0


    # Start screening
    if st.button("Start Recruiter Screening"):

        st.session_state.intake_started = True


    # --------------------------------------------------
    # QUESTION 1 — PREFERRED LOCATION
    # --------------------------------------------------

    if st.session_state.intake_started:

        if st.session_state.intake_step == 0:

            st.write(
                "What is your preferred location?"
            )

            location = st.text_input(
                "Preferred location",
                key="preferred_location"
            )

            if st.button(
                "Next",
                key="location_next"
            ):

                if location:

                    st.session_state.intake_step = 1

                    st.rerun()


    # --------------------------------------------------
    # QUESTION 2 — SALARY EXPECTATION
    # --------------------------------------------------

    if st.session_state.intake_step == 1:

        st.write(
            "What is your salary expectation?"
        )

        salary = st.text_input(
            "Salary expectation",
            key="salary_expectation"
        )

        if st.button(
            "Next",
            key="salary_next"
        ):

            if salary:

                st.session_state.intake_step = 2

                st.rerun()


    # --------------------------------------------------
    # QUESTION 3 — INTERESTED ROLE
    # --------------------------------------------------

    if st.session_state.intake_step == 2:

        st.write(
            "What role are you interested in?"
        )

        role = st.text_input(
            "Interested role",
            key="interested_role"
        )

        if st.button(
            "Next",
            key="role_next"
        ):

            if role:

                st.session_state.intake_step = 3

                st.rerun()


    # --------------------------------------------------
    # QUESTION 4 — WORK PREFERENCE
    # --------------------------------------------------

    if st.session_state.intake_step == 3:

        st.write(
            "Are you looking for remote or onsite work?"
        )

        work_preference = st.selectbox(
            "Work preference",
            [
                "Remote",
                "Onsite",
                "Hybrid",
                "Any"
            ]
        )

        if st.button(
            "Next",
            key="work_next"
        ):

            st.session_state.work_preference = (
                work_preference
            )

            st.session_state.intake_step = 4

            st.rerun()


    # --------------------------------------------------
    # QUESTION 5 — NOTICE PERIOD
    # --------------------------------------------------

    if st.session_state.intake_step == 4:

        st.write(
            "What is your notice period?"
        )

        notice_period = st.text_input(
            "Notice period",
            key="notice_period"
        )

        if st.button(
            "Finish",
            key="finish_intake"
        ):

            if notice_period:

                st.session_state.intake_step = 5

                st.rerun()


    # --------------------------------------------------
    # INTAKE COMPLETED
    # --------------------------------------------------

    if st.session_state.intake_step == 5:

        st.success(
            "Recruiter screening completed!"
        )


        # Create structured CandidatePreferences object

        candidate_preferences = CandidatePreferences(
            preferred_location=(
                st.session_state.preferred_location
            ),
            salary_expectation=(
                st.session_state.salary_expectation
            ),
            interested_role=(
                st.session_state.interested_role
            ),
            work_preference=(
                st.session_state.work_preference
            ),
            notice_period=(
                st.session_state.notice_period
            )
        )


        # Display structured candidate preferences

        st.subheader(
            "Candidate Preferences"
        )

        st.json(
            candidate_preferences.model_dump()
        )