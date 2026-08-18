import streamlit as st

from src.resume_parser import extract_text_from_pdf
from src.llm import extract_candidate_profile
from src.profile_engine import generate_candidate_insights
from src.intake_schema import CandidatePreferences
from src.matching_engine import find_matching_jobs
from src.rag_engine import generate_rag_response
from src.screening_engine import calculate_screening_score
from src.interview_engine import generate_interview_questions


# ==================================================
# PAGE CONFIGURATION
# ==================================================

st.set_page_config(
    page_title="AI Recruitment Assistant",
    page_icon="🤖",
)


# ==================================================
# SESSION STATE INITIALIZATION
# ==================================================

if "candidate_profile" not in st.session_state:
    st.session_state.candidate_profile = None

if "candidate_insights" not in st.session_state:
    st.session_state.candidate_insights = None

if "candidate_preferences" not in st.session_state:
    st.session_state.candidate_preferences = None

if "matched_jobs" not in st.session_state:
    st.session_state.matched_jobs = None

if "screening_results" not in st.session_state:
    st.session_state.screening_results = None

if "interview_questions" not in st.session_state:
    st.session_state.interview_questions = None

if "preferred_location" not in st.session_state:
    st.session_state.preferred_location = ""

if "salary_expectation" not in st.session_state:
    st.session_state.salary_expectation = ""

if "interested_role" not in st.session_state:
    st.session_state.interested_role = ""

if "work_preference" not in st.session_state:
    st.session_state.work_preference = ""

if "notice_period" not in st.session_state:
    st.session_state.notice_period = ""

if "intake_started" not in st.session_state:
    st.session_state.intake_started = False

if "intake_step" not in st.session_state:
    st.session_state.intake_step = 0


# ==================================================
# WELCOME SCREEN
# ==================================================

st.title("🤖 AI Recruitment Assistant")

st.write(
    "Hi! I am your AI Recruitment Assistant. "
    "Upload your resume to get started."
)


# ==================================================
# RESUME UPLOAD
# ==================================================

uploaded_file = st.file_uploader(
    "Upload your resume",
    type=["pdf"]
)


if uploaded_file is not None:

    st.success("Resume uploaded successfully!")


    # ==================================================
    # STEP 1 — RESUME TEXT EXTRACTION
    # ==================================================

    resume_text = extract_text_from_pdf(
        uploaded_file
    )

    st.subheader("📄 Extracted Resume Text")

    st.text_area(
        "Resume content",
        resume_text,
        height=400
    )


    # ==================================================
    # STEP 2 — CANDIDATE PROFILE
    # ==================================================

    if st.session_state.candidate_profile is None:

        with st.spinner(
            "Analyzing your resume..."
        ):

            candidate_profile = (
                extract_candidate_profile(
                    resume_text
                )
            )

        st.session_state.candidate_profile = (
            candidate_profile
        )

    else:

        candidate_profile = (
            st.session_state.candidate_profile
        )


    st.subheader("👤 Candidate Profile")

    st.json(
        candidate_profile.model_dump()
    )


    # ==================================================
    # STEP 3 — CANDIDATE INSIGHTS
    # ==================================================

    if st.session_state.candidate_insights is None:

        with st.spinner(
            "Generating Candidate Insights..."
        ):

            candidate_insights = (
                generate_candidate_insights(
                    candidate_profile
                )
            )

        st.session_state.candidate_insights = (
            candidate_insights
        )

    else:

        candidate_insights = (
            st.session_state.candidate_insights
        )


    st.subheader("🤖 AI Candidate Insights")

    st.json(
        candidate_insights.model_dump()
    )


    # ==================================================
    # STEP 4 — RECRUITER SCREENING
    # ==================================================

    st.subheader("💬 Recruiter Screening")


    # --------------------------------------------------
    # START SCREENING
    # --------------------------------------------------

    if st.button(
        "Start Recruiter Screening"
    ):

        st.session_state.intake_started = True


    # --------------------------------------------------
    # QUESTION 1 — LOCATION
    # --------------------------------------------------

    if st.session_state.intake_started:

        if st.session_state.intake_step == 0:

            st.write(
                "What is your preferred location?"
            )

            location = st.text_input(
                "Preferred location",
                key="location_input"
            )

            if st.button(
                "Next",
                key="location_next"
            ):

                if location:

                    st.session_state.preferred_location = (
                        location
                    )

                    st.session_state.intake_step = 1

                    st.rerun()


    # --------------------------------------------------
    # QUESTION 2 — SALARY
    # --------------------------------------------------

    if st.session_state.intake_step == 1:

        st.write(
            "What is your salary expectation?"
        )

        salary = st.text_input(
            "Salary expectation",
            key="salary_input"
        )

        if st.button(
            "Next",
            key="salary_next"
        ):

            if salary:

                st.session_state.salary_expectation = (
                    salary
                )

                st.session_state.intake_step = 2

                st.rerun()


    # --------------------------------------------------
    # QUESTION 3 — ROLE
    # --------------------------------------------------

    if st.session_state.intake_step == 2:

        st.write(
            "What role are you interested in?"
        )

        role = st.text_input(
            "Interested role",
            key="role_input"
        )

        if st.button(
            "Next",
            key="role_next"
        ):

            if role:

                st.session_state.interested_role = (
                    role
                )

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
            ],
            key="work_preference_input"
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
            key="notice_period_input"
        )

        if st.button(
            "Finish",
            key="finish_intake"
        ):

            if notice_period:

                st.session_state.notice_period = (
                    notice_period
                )

                st.session_state.intake_step = 5

                st.rerun()


    # ==================================================
    # STEP 5 — INTAKE COMPLETED
    # ==================================================

    if st.session_state.intake_step == 5:

        st.success(
            "Recruiter screening completed!"
        )


        # --------------------------------------------------
        # CREATE CANDIDATE PREFERENCES
        # --------------------------------------------------

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


        st.session_state.candidate_preferences = (
            candidate_preferences
        )


        # --------------------------------------------------
        # DISPLAY PREFERENCES
        # --------------------------------------------------

        st.subheader(
            "📋 Candidate Preferences"
        )

        st.json(
            candidate_preferences.model_dump()
        )


        # ==================================================
        # STEP 6 — JOB MATCHING
        # ==================================================

        st.subheader(
            "🎯 Recommended Jobs"
        )


        if st.button(
            "Find Matching Jobs",
            key="find_jobs"
        ):

            with st.spinner(
                "Finding the best matching jobs..."
            ):

                matched_jobs = find_matching_jobs(

                    st.session_state.candidate_profile,

                    st.session_state.candidate_preferences,

                    "data/jobs.json",

                    top_k=5
                )


            st.session_state.matched_jobs = (
                matched_jobs
            )


            # --------------------------------------------------
            # CALCULATE SCREENING RESULTS
            # --------------------------------------------------

            screening_results = []


            for match in matched_jobs:

                job = match["job"]

                screening_result = (
                    calculate_screening_score(

                        st.session_state.candidate_profile,

                        st.session_state.candidate_preferences,

                        job
                    )
                )


                screening_results.append(
                    {
                        "job": job,
                        "distance": match["distance"],
                        "screening": screening_result
                    }
                )


            st.session_state.screening_results = (
                screening_results
            )


        # ==================================================
        # STEP 7 — SCREENING RESULTS
        # ==================================================

        if st.session_state.screening_results:

            for result in st.session_state.screening_results:

                job = result["job"]

                distance = result["distance"]

                screening = result["screening"]


                st.markdown(
                    f"### 💼 {job.title}"
                )


                st.metric(
                    "🎯 Match Score",
                    f"{screening.match_score}%"
                )


                st.write(
                    f"📍 **Location:** "
                    f"{job.location}"
                )


                st.write(
                    f"💼 **Experience Required:** "
                    f"{job.experience}"
                )


                st.write(
                    f"🛠️ **Required Skills:** "
                    f"{', '.join(job.skills)}"
                )


                # --------------------------------------------------
                # MATCHING SKILLS
                # --------------------------------------------------

                if screening.skill_overlap:

                    st.write(
                        "✅ **Matching Skills:** "
                        + ", ".join(
                            screening.skill_overlap
                        )
                    )

                else:

                    st.write(
                        "✅ **Matching Skills:** None"
                    )


                # --------------------------------------------------
                # MISSING SKILLS
                # --------------------------------------------------

                if screening.missing_skills:

                    st.write(
                        "⚠️ **Missing Skills:** "
                        + ", ".join(
                            screening.missing_skills
                        )
                    )

                else:

                    st.write(
                        "⚠️ **Missing Skills:** None"
                    )


                # --------------------------------------------------
                # EXPERIENCE MATCH
                # --------------------------------------------------

                experience_status = (
                    "Yes"
                    if screening.experience_match
                    else "No"
                )

                st.write(
                    f"📊 **Experience Match:** "
                    f"{experience_status}"
                )


                # --------------------------------------------------
                # LOCATION MATCH
                # --------------------------------------------------

                location_status = (
                    "Yes"
                    if screening.location_match
                    else "No"
                )

                st.write(
                    f"📍 **Location Match:** "
                    f"{location_status}"
                )


                # --------------------------------------------------
                # FAISS DISTANCE
                # --------------------------------------------------

                st.write(
                    f"🔎 **Semantic Distance:** "
                    f"{distance:.4f}"
                )


                st.divider()


            # ==================================================
            # STEP 8 — RAG RECRUITER ASSISTANT
            # ==================================================

            st.subheader(
                "🤖 Ask the AI Recruiter"
            )


            user_query = st.text_input(
                "Ask a question about your job matches",

                placeholder=(
                    "Example: Why am I a good fit "
                    "for these jobs?"
                ),

                key="rag_question"
            )


            if user_query:

                with st.spinner(
                    "AI Recruiter is analyzing "
                    "your profile..."
                ):

                    response = generate_rag_response(

                        st.session_state.candidate_profile,

                        st.session_state.candidate_preferences,

                        st.session_state.matched_jobs,

                        user_query
                    )


                st.subheader(
                    "💬 AI Recruiter Response"
                )

                st.write(response)


            # ==================================================
            # STEP 9 — INTERVIEW QUESTION GENERATOR
            # ==================================================

            st.subheader(
                "🎤 Interview Question Generator"
            )


            st.write(
                "Select a recommended job and generate "
                "personalized interview questions based "
                "on the candidate profile and job requirements."
            )


            job_options = [
                result["job"]
                for result
                in st.session_state.screening_results
            ]


            selected_job = st.selectbox(
                "Select a job",

                job_options,

                format_func=lambda job: (
                    f"{job.title} | "
                    f"{job.location} | "
                    f"{job.experience}"
                ),

                key="selected_interview_job"
            )


            if st.button(
                "🎤 Generate Interview Questions",
                key="generate_interview_questions"
            ):

                with st.spinner(
                    "Generating personalized interview questions..."
                ):

                    interview_questions = (
                        generate_interview_questions(

                            st.session_state.candidate_profile,

                            selected_job
                        )
                    )


                st.session_state.interview_questions = (
                    interview_questions
                )


            # --------------------------------------------------
            # DISPLAY INTERVIEW QUESTIONS
            # --------------------------------------------------

            if st.session_state.interview_questions:

                interview_questions = (
                    st.session_state.interview_questions
                )


                st.subheader(
                    "🧠 Personalized Interview Questions"
                )


                st.markdown(
                    "### 💻 Technical Questions"
                )

                for index, question in enumerate(
                    interview_questions.technical_questions,
                    start=1
                ):

                    st.write(
                        f"**{index}. {question}**"
                    )


                st.markdown(
                    "### 👔 Experience-Based Questions"
                )

                for index, question in enumerate(
                    interview_questions.experience_questions,
                    start=1
                ):

                    st.write(
                        f"**{index}. {question}**"
                    )


                st.markdown(
                    "### 🎯 Role-Specific Questions"
                )

                for index, question in enumerate(
                    interview_questions.role_specific_questions,
                    start=1
                ):

                    st.write(
                        f"**{index}. {question}**"
                    )