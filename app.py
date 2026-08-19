import streamlit as st

from src.resume_parser import extract_text_from_pdf
from src.llm import extract_candidate_profile
from src.profile_engine import generate_candidate_insights
from src.intake_schema import CandidatePreferences
from src.matching_engine import find_matching_jobs
from src.rag_engine import generate_rag_response
from src.screening_engine import calculate_screening_score
from src.interview_engine import generate_interview_questions
from src.candidate_summary_engine import generate_candidate_summary


# ==================================================
# PAGE CONFIGURATION
# ==================================================

st.set_page_config(
    page_title="AI Recruitment Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# ==================================================
# CUSTOM CSS — DAY 13 UI POLISH
# ==================================================

st.html(
    """
    <style>

    /* -----------------------------------------------
       GLOBAL
    ----------------------------------------------- */

    .block-container {
        max-width: 1200px;
        padding-top: 2rem;
        padding-bottom: 4rem;
    }

    h1, h2, h3 {
        letter-spacing: -0.02em;
    }

    /* -----------------------------------------------
       HERO HEADER
    ----------------------------------------------- */

    .hero {
        padding: 2rem 2.2rem;
        border-radius: 20px;
        background: linear-gradient(
            135deg,
            #eef2ff 0%,
            #f8fafc 55%,
            #ecfeff 100%
        );
        border: 1px solid #e2e8f0;
        margin-bottom: 2rem;
    }

    .hero-title {
        font-size: 2.3rem;
        font-weight: 800;
        margin-bottom: 0.4rem;
    }

    .hero-subtitle {
        color: #64748b;
        font-size: 1.05rem;
        margin-bottom: 0;
    }

    /* -----------------------------------------------
       SECTION HEADERS
    ----------------------------------------------- */

    .section-header {
        font-size: 1.45rem;
        font-weight: 750;
        margin-top: 1.8rem;
        margin-bottom: 0.8rem;
    }

    .section-description {
        color: #64748b;
        margin-bottom: 1rem;
    }

    /* -----------------------------------------------
       PROFILE CARD
    ----------------------------------------------- */

    .profile-card {
        padding: 1.4rem;
        border-radius: 16px;
        border: 1px solid #e2e8f0;
        background: white;
        min-height: 180px;
        box-shadow: 0 4px 16px rgba(15, 23, 42, 0.05);
    }

    .profile-name {
        font-size: 1.35rem;
        font-weight: 750;
        margin-bottom: 0.25rem;
    }

    .profile-role {
        color: #6366f1;
        font-weight: 600;
        margin-bottom: 1rem;
    }

    .profile-label {
        color: #64748b;
        font-size: 0.82rem;
        text-transform: uppercase;
        letter-spacing: 0.06em;
    }

    .profile-value {
        font-weight: 650;
        margin-bottom: 0.75rem;
    }

    /* -----------------------------------------------
       SKILL PILLS
    ----------------------------------------------- */

    .skill-pill {
        display: inline-block;
        padding: 0.3rem 0.65rem;
        margin: 0.18rem;
        border-radius: 999px;
        background: #eef2ff;
        color: #4338ca;
        font-size: 0.82rem;
        font-weight: 600;
        border: 1px solid #c7d2fe;
    }

    .missing-pill {
        display: inline-block;
        padding: 0.3rem 0.65rem;
        margin: 0.18rem;
        border-radius: 999px;
        background: #fff7ed;
        color: #c2410c;
        font-size: 0.82rem;
        font-weight: 600;
        border: 1px solid #fed7aa;
    }

    /* -----------------------------------------------
       JOB CARD
    ----------------------------------------------- */

    .job-card {
        padding: 1.4rem;
        border-radius: 18px;
        border: 1px solid #e2e8f0;
        background: white;
        margin-bottom: 1rem;
        box-shadow: 0 5px 18px rgba(15, 23, 42, 0.05);
    }

    .job-title {
        font-size: 1.3rem;
        font-weight: 750;
        margin-bottom: 0.5rem;
    }

    .job-meta {
        color: #64748b;
        font-size: 0.92rem;
    }

    .match-label {
        color: #64748b;
        font-size: 0.82rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }

    .match-score {
        font-size: 2rem;
        font-weight: 800;
        color: #4f46e5;
    }

    /* -----------------------------------------------
       INSIGHT CARD
    ----------------------------------------------- */

    .insight-card {
        padding: 1.3rem;
        border-radius: 16px;
        border: 1px solid #e2e8f0;
        background: #f8fafc;
        margin-bottom: 1rem;
    }

    /* -----------------------------------------------
       CHAT
    ----------------------------------------------- */

    .chat-intro {
        padding: 1rem 1.2rem;
        border-radius: 14px;
        background: #f8fafc;
        border: 1px solid #e2e8f0;
        margin-bottom: 1rem;
        color: #475569;
    }

    /* -----------------------------------------------
       STATUS BADGES
    ----------------------------------------------- */

    .status-good {
        color: #15803d;
        font-weight: 700;
    }

    .status-warning {
        color: #c2410c;
        font-weight: 700;
    }

    /* -----------------------------------------------
       FOOTER
    ----------------------------------------------- */

    .footer {
        text-align: center;
        color: #94a3b8;
        margin-top: 3rem;
        padding-top: 1rem;
        border-top: 1px solid #e2e8f0;
        font-size: 0.85rem;
    }

    </style>
    """
)


# ==================================================
# SESSION STATE INITIALIZATION
# ==================================================

DEFAULT_STATE = {
    "candidate_profile": None,
    "candidate_insights": None,
    "candidate_summary": None,
    "candidate_preferences": None,
    "matched_jobs": None,
    "screening_results": None,
    "interview_questions": None,
    "resume_text": None,
    "uploaded_filename": None,
    "preferred_location": "",
    "salary_expectation": "",
    "interested_role": "",
    "work_preference": "",
    "notice_period": "",
    "intake_started": False,
    "intake_step": 0,
    "chat_history": [],
}


for key, default_value in DEFAULT_STATE.items():

    if key not in st.session_state:
        st.session_state[key] = default_value


# ==================================================
# HERO HEADER
# ==================================================

st.html(
    """
    <div class="hero">

        <div class="hero-title">
            🤖 AI Recruitment Assistant
        </div>

        <p class="hero-subtitle">
            AI-powered resume screening, job matching,
            interview preparation and recruiter assistance.
        </p>

    </div>
    """
)


# ==================================================
# RESUME UPLOAD
# ==================================================

st.html(
    '<div class="section-header">📄 Start with your resume</div>'
)

st.html(
    '<div class="section-description">'
    'Upload a PDF resume and let the AI recruiter analyze your profile.'
    '</div>'
)

uploaded_file = st.file_uploader(
    "Upload your resume",
    type=["pdf"],
    label_visibility="collapsed",
)


# ==================================================
# HANDLE NEW RESUME
# ==================================================

if uploaded_file is not None:

    # Detect a different uploaded resume
    if (
        st.session_state.uploaded_filename
        != uploaded_file.name
    ):

        # Reset candidate-specific state
        st.session_state.candidate_profile = None
        st.session_state.candidate_insights = None
        st.session_state.candidate_summary = None
        st.session_state.candidate_preferences = None
        st.session_state.matched_jobs = None
        st.session_state.screening_results = None
        st.session_state.interview_questions = None
        st.session_state.resume_text = None

        st.session_state.preferred_location = ""
        st.session_state.salary_expectation = ""
        st.session_state.interested_role = ""
        st.session_state.work_preference = ""
        st.session_state.notice_period = ""

        st.session_state.intake_started = False
        st.session_state.intake_step = 0
        st.session_state.chat_history = []

        st.session_state.uploaded_filename = (
            uploaded_file.name
        )


    st.success(
        f"Resume uploaded: {uploaded_file.name}"
    )


    # ==================================================
    # STEP 1 — RESUME EXTRACTION
    # ==================================================

    if st.session_state.resume_text is None:

        with st.spinner(
            "Extracting resume information..."
        ):

            try:

                st.session_state.resume_text = (
                    extract_text_from_pdf(
                        uploaded_file
                    )
                )

            except Exception as e:

                st.error(
                    f"Unable to extract resume text: {e}"
                )

                st.stop()


    resume_text = st.session_state.resume_text


    # ==================================================
    # RESUME PREVIEW
    # ==================================================

    with st.expander(
        "📄 View extracted resume text"
    ):

        st.text_area(
            "Resume content",
            resume_text,
            height=350,
            disabled=True,
        )


    # ==================================================
    # STEP 2 — CANDIDATE PROFILE
    # ==================================================

    if st.session_state.candidate_profile is None:

        with st.spinner(
            "Analyzing your resume with AI..."
        ):

            try:

                candidate_profile = (
                    extract_candidate_profile(
                        resume_text
                    )
                )

                st.session_state.candidate_profile = (
                    candidate_profile
                )

            except Exception as e:

                st.error(
                    f"Candidate profile generation failed: {e}"
                )

                st.stop()

    else:

        candidate_profile = (
            st.session_state.candidate_profile
        )


    # ==================================================
    # CANDIDATE PROFILE PANEL
    # ==================================================

    st.html(
        '<div class="section-header">'
        '👤 Candidate Profile'
        '</div>'
    )


    profile_col1, profile_col2 = st.columns(
        [1, 2],
        gap="large",
    )


    # --------------------------------------------------
    # PROFILE SUMMARY
    # --------------------------------------------------

    with profile_col1:

        name = getattr(
            candidate_profile,
            "name",
            "Candidate"
        )

        years_experience = getattr(
            candidate_profile,
            "years_experience",
            0
        )

        roles = getattr(
            candidate_profile,
            "roles",
            []
        )

        primary_role = (
            roles[0]
            if roles
            else "Professional"
        )


        st.html(
            f"""
            <div class="profile-card">

                <div class="profile-name">
                    {name}
                </div>

                <div class="profile-role">
                    {primary_role}
                </div>

                <div class="profile-label">
                    Experience
                </div>

                <div class="profile-value">
                    {years_experience}+ years
                </div>

            </div>
            """
        )


    # --------------------------------------------------
    # SKILLS
    # --------------------------------------------------

    with profile_col2:

        skills = getattr(
            candidate_profile,
            "skills",
            []
        )

        skill_html = ""

        for skill in skills:

            skill_html += (
                f'<span class="skill-pill">'
                f'{skill}'
                f'</span>'
            )


        st.html(
            f"""
            <div class="profile-card">

                <div class="profile-label">
                    Core Skills
                </div>

                <div style="margin-top: 0.6rem;">
                    {skill_html}
                </div>

            </div>
            """
        )


    # ==================================================
    # STEP 3 — AI CANDIDATE INSIGHTS
    # ==================================================

    if st.session_state.candidate_insights is None:

        with st.spinner(
            "Generating candidate insights..."
        ):

            try:

                candidate_insights = (
                    generate_candidate_insights(
                        candidate_profile
                    )
                )

                st.session_state.candidate_insights = (
                    candidate_insights
                )

            except Exception as e:

                st.warning(
                    f"Candidate insights unavailable: {e}"
                )

                candidate_insights = None

    else:

        candidate_insights = (
            st.session_state.candidate_insights
        )


    # ==================================================
    # AI INSIGHTS
    # ==================================================

    if candidate_insights:

        st.html(
            '<div class="section-header">'
            '🧠 AI Candidate Insights'
            '</div>'
        )


        insight_col1, insight_col2 = st.columns(
            [1, 2],
            gap="large",
        )


        # --------------------------------------------------
        # LIKELY ROLE
        # --------------------------------------------------

        with insight_col1:

            likely_titles = getattr(
                candidate_insights,
                "likely_job_title",
                []
            )

            titles_text = (
                ", ".join(likely_titles)
                if likely_titles
                else "Not available"
            )


            st.html(
                f"""
                <div class="insight-card">

                    <div class="profile-label">
                        Likely Job Titles
                    </div>

                    <div class="profile-value">
                        {titles_text}
                    </div>

                </div>
                """
            )


        # --------------------------------------------------
        # SKILL SUMMARY
        # --------------------------------------------------

        with insight_col2:

            skill_summary = getattr(
                candidate_insights,
                "skill_summary",
                ""
            )


            st.html(
                f"""
                <div class="insight-card">

                    <div class="profile-label">
                        AI Skill Summary
                    </div>

                    <div style="margin-top:0.5rem;">
                        {skill_summary}
                    </div>

                </div>
                """
            )


        # --------------------------------------------------
        # STRENGTHS
        # --------------------------------------------------

        strengths = getattr(
            candidate_insights,
            "strengths",
            []
        )


        if strengths:

            with st.expander(
                "💪 Candidate Strengths"
            ):

                for strength in strengths:

                    st.markdown(
                        f"✅ {strength}"
                    )


    # ==================================================
    # STEP 4 — RECRUITER SCREENING
    # ==================================================

    st.html(
        '<div class="section-header">'
        '💬 Recruiter Screening'
        '</div>'
    )


    st.html(
        '<div class="section-description">'
        'Tell the recruiter what you are looking for so job '
        'matching can consider your preferences.'
        '</div>'
    )


    if not st.session_state.intake_started:

        if st.button(
            "🚀 Start Recruiter Screening",
            type="primary",
            use_container_width=False,
        ):

            st.session_state.intake_started = True
            st.rerun()


    # ==================================================
    # QUESTION 1 — LOCATION
    # ==================================================

    if st.session_state.intake_started:

        if st.session_state.intake_step == 0:

            st.info(
                "📍 What is your preferred job location?"
            )

            location = st.text_input(
                "Preferred location",
                placeholder="Example: Bangalore",
                key="location_input",
            )


            if st.button(
                "Continue →",
                key="location_next",
            ):

                if location.strip():

                    st.session_state.preferred_location = (
                        location.strip()
                    )

                    st.session_state.intake_step = 1

                    st.rerun()

                else:

                    st.warning(
                        "Please enter a preferred location."
                    )


    # ==================================================
    # QUESTION 2 — SALARY
    # ==================================================

    if st.session_state.intake_step == 1:

        st.info(
            "💰 What is your salary expectation?"
        )

        salary = st.text_input(
            "Salary expectation",
            placeholder="Example: 12 LPA",
            key="salary_input",
        )


        if st.button(
            "Continue →",
            key="salary_next",
        ):

            if salary.strip():

                st.session_state.salary_expectation = (
                    salary.strip()
                )

                st.session_state.intake_step = 2

                st.rerun()

            else:

                st.warning(
                    "Please enter your salary expectation."
                )


    # ==================================================
    # QUESTION 3 — ROLE
    # ==================================================

    if st.session_state.intake_step == 2:

        st.info(
            "🎯 What role are you interested in?"
        )

        role = st.text_input(
            "Interested role",
            placeholder="Example: Python Developer",
            key="role_input",
        )


        if st.button(
            "Continue →",
            key="role_next",
        ):

            if role.strip():

                st.session_state.interested_role = (
                    role.strip()
                )

                st.session_state.intake_step = 3

                st.rerun()

            else:

                st.warning(
                    "Please enter the role you are interested in."
                )


    # ==================================================
    # QUESTION 4 — WORK PREFERENCE
    # ==================================================

    if st.session_state.intake_step == 3:

        st.info(
            "🏢 What is your preferred work arrangement?"
        )

        work_preference = st.selectbox(
            "Work preference",
            [
                "Remote",
                "Onsite",
                "Hybrid",
                "Any",
            ],
            key="work_preference_input",
        )


        if st.button(
            "Continue →",
            key="work_next",
        ):

            st.session_state.work_preference = (
                work_preference
            )

            st.session_state.intake_step = 4

            st.rerun()


    # ==================================================
    # QUESTION 5 — NOTICE PERIOD
    # ==================================================

    if st.session_state.intake_step == 4:

        st.info(
            "⏳ What is your notice period?"
        )

        notice_period = st.text_input(
            "Notice period",
            placeholder="Example: 30 days",
            key="notice_period_input",
        )


        if st.button(
            "Finish Screening ✓",
            key="finish_intake",
        ):

            if notice_period.strip():

                st.session_state.notice_period = (
                    notice_period.strip()
                )

                st.session_state.intake_step = 5

                st.rerun()

            else:

                st.warning(
                    "Please enter your notice period."
                )


    # ==================================================
    # STEP 5 — INTAKE COMPLETED
    # ==================================================

    if st.session_state.intake_step == 5:

        st.success(
            "✅ Recruiter screening completed!"
        )


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
            ),
        )


        st.session_state.candidate_preferences = (
            candidate_preferences
        )


        # ==================================================
        # PREFERENCE CARD
        # ==================================================

        pref1, pref2, pref3, pref4, pref5 = st.columns(
            5
        )


        with pref1:

            st.metric(
                "📍 Location",
                candidate_preferences.preferred_location,
            )


        with pref2:

            st.metric(
                "💼 Role",
                candidate_preferences.interested_role,
            )


        with pref3:

            st.metric(
                "🏢 Work",
                candidate_preferences.work_preference,
            )


        with pref4:

            st.metric(
                "💰 Salary",
                candidate_preferences.salary_expectation,
            )


        with pref5:

            st.metric(
                "⏳ Notice",
                candidate_preferences.notice_period,
            )


        # ==================================================
        # STEP 6 — ATS CANDIDATE SUMMARY
        # ==================================================

        st.html(
            '<div class="section-header">📝 ATS Candidate Summary</div>'
        )

        st.html(
            '<div class="section-description">'
            'Recruiter-ready summary generated from the candidate profile, '
            'AI insights and screening preferences.'
            '</div>'
        )

        if st.session_state.candidate_summary is None:

            with st.spinner("Generating ATS candidate summary..."):

                try:
                    candidate_summary = generate_candidate_summary(
                        st.session_state.candidate_profile,
                        st.session_state.candidate_insights,
                        st.session_state.candidate_preferences,
                    )

                    st.session_state.candidate_summary = candidate_summary

                except Exception as e:
                    st.warning(
                        f"ATS candidate summary unavailable: {e}"
                    )
                    candidate_summary = None

        else:
            candidate_summary = st.session_state.candidate_summary

        if candidate_summary:

            summary_col, strengths_col = st.columns(
                [3, 2],
                gap="large",
            )

            with summary_col:
                st.html(
                    '<div class="insight-card">'
                    '<div class="profile-label">Candidate Summary</div>'
                )

                st.write(candidate_summary.candidate_summary)

                st.html('</div>')

            with strengths_col:
                st.html(
                    '<div class="insight-card">'
                    '<div class="profile-label">Key Strengths</div>'
                )

                for strength in candidate_summary.strengths:
                    st.markdown(f"✅ {strength}")

                st.html('</div>')

            if candidate_summary.recruiter_notes:
                with st.expander("📝 Recruiter Notes"):
                    for note in candidate_summary.recruiter_notes:
                        st.markdown(f"• {note}")


        # ==================================================
        # STEP 7 — JOB MATCHING
        # ==================================================

        st.html(
            '<div class="section-header">'
            '🎯 Recommended Jobs'
            '</div>'
        )


        st.html(
            '<div class="section-description">'
            'AI-ranked opportunities based on your technical '
            'profile and recruiter preferences.'
            '</div>'
        )


        if st.button(
            "🔎 Find Matching Jobs",
            key="find_jobs",
            type="primary",
        ):

            with st.spinner(
                "Finding the best matching jobs..."
            ):

                try:

                    matched_jobs = find_matching_jobs(

                        st.session_state.candidate_profile,

                        st.session_state.candidate_preferences,

                        "data/jobs.json",

                        top_k=5,
                    )


                    st.session_state.matched_jobs = (
                        matched_jobs
                    )


                    # --------------------------------------------------
                    # SCREENING RESULTS
                    # --------------------------------------------------

                    screening_results = []


                    for match in matched_jobs:

                        job = match["job"]


                        screening_result = (
                            calculate_screening_score(

                                st.session_state.candidate_profile,

                                st.session_state.candidate_preferences,

                                job,
                            )
                        )


                        screening_results.append(
                            {
                                "job": job,
                                "distance": match["distance"],
                                "screening": screening_result,
                            }
                        )


                    st.session_state.screening_results = (
                        screening_results
                    )


                    # Clear old interview questions
                    st.session_state.interview_questions = None


                    # Clear chat history
                    st.session_state.chat_history = []


                    st.success(
                        f"Found {len(screening_results)} matching opportunities."
                    )


                except Exception as e:

                    st.error(
                        f"Job matching failed: {e}"
                    )


        # ==================================================
        # STEP 7 — JOB CARDS
        # ==================================================

        if st.session_state.screening_results:

            for index, result in enumerate(
                st.session_state.screening_results,
                start=1,
            ):

                job = result["job"]
                distance = result["distance"]
                screening = result["screening"]


                match_score = float(
                    screening.match_score
                )


                # Clamp score for progress bar
                progress_value = max(
                    0.0,
                    min(
                        match_score / 100,
                        1.0
                    )
                )


                st.html(
                    '<div class="job-card">'
                )


                job_col1, job_col2 = st.columns(
                    [3, 1],
                    gap="large",
                )


                # --------------------------------------------------
                # JOB INFORMATION
                # --------------------------------------------------

                with job_col1:

                    st.html(
                        f"""
                        <div class="job-title">
                            💼 {job.title}
                        </div>

                        <div class="job-meta">
                            📍 {job.location}
                            &nbsp;&nbsp; • &nbsp;&nbsp;
                            💼 {job.experience}
                        </div>
                        """,
                    )


                # --------------------------------------------------
                # MATCH SCORE
                # --------------------------------------------------

                with job_col2:

                    st.html(
                        '<div class="match-label">'
                        'Match Score'
                        '</div>',
                    )

                    st.html(
                        f"""
                        <div class="match-score">
                            {match_score:.0f}%
                        </div>
                        """,
                    )


                st.progress(
                    progress_value
                )


                # --------------------------------------------------
                # MATCH / MISSING SKILLS
                # --------------------------------------------------

                skill_col1, skill_col2 = st.columns(
                    2,
                    gap="large",
                )


                with skill_col1:

                    st.markdown(
                        "**✅ Matching Skills**"
                    )


                    if screening.skill_overlap:

                        skill_html = ""


                        for skill in screening.skill_overlap:

                            skill_html += (
                                f'<span class="skill-pill">'
                                f'{skill}'
                                f'</span>'
                            )


                        st.html(
                            skill_html,
                        )

                    else:

                        st.caption(
                            "No direct skill overlap identified."
                        )


                with skill_col2:

                    st.markdown(
                        "**⚠️ Missing Skills**"
                    )


                    if screening.missing_skills:

                        missing_html = ""


                        for skill in screening.missing_skills:

                            missing_html += (
                                f'<span class="missing-pill">'
                                f'{skill}'
                                f'</span>'
                            )


                        st.html(
                            missing_html,
                        )

                    else:

                        st.html(
                            '<span class="status-good">'
                            '✓ No significant missing skills'
                            '</span>',
                        )


                # --------------------------------------------------
                # MATCH DETAILS
                # --------------------------------------------------

                with st.expander(
                    "View match details"
                ):

                    detail_col1, detail_col2 = st.columns(
                        2
                    )


                    with detail_col1:

                        st.write(
                            f"📊 **Experience Match:** "
                            f"{'Yes' if screening.experience_match else 'No'}"
                        )

                        st.write(
                            f"📍 **Location Match:** "
                            f"{'Yes' if screening.location_match else 'No'}"
                        )


                    with detail_col2:

                        st.write(
                            f"🔎 **Semantic Distance:** "
                            f"{distance:.4f}"
                        )

                        st.write(
                            "**Required Skills:** "
                            + ", ".join(job.skills)
                        )


                st.html(
                    "</div>"
                )
        # ==================================================
        # STEP 8 — AI RECRUITER CHAT
        # ==================================================

        if st.session_state.screening_results:

            st.html(
                """
                <div class="section-header">
                    🤖 Ask the AI Recruiter
                </div>
                """
            )

            st.html(
                """
                <div class="chat-intro">
                    <b>AI Recruiter Assistant</b><br>
                    Ask about job matches, skill gaps, suitability,
                    locations, experience requirements or interview preparation.
                </div>
                """
            )

            # --------------------------------------------------
            # DISPLAY CHAT HISTORY
            # --------------------------------------------------

            if st.session_state.chat_history:

                for message in st.session_state.chat_history:

                    with st.chat_message(message["role"]):

                        st.markdown(
                            message["content"]
                        )

            # --------------------------------------------------
            # INLINE CHAT INPUT
            # --------------------------------------------------

            with st.form(
                key="recruiter_chat_form",
                clear_on_submit=True
            ):

                user_query = st.text_input(
                    "Ask the AI Recruiter",
                    placeholder=(
                        "Example: Why am I a good fit for the top job?"
                    ),
                    label_visibility="collapsed"
                )

                send_button = st.form_submit_button(
                    "➤ Send",
                    type="primary"
                )

            # --------------------------------------------------
            # PROCESS MESSAGE
            # --------------------------------------------------

            if send_button and user_query.strip():

                user_query = user_query.strip()

                # Add user message
                st.session_state.chat_history.append(
                    {
                        "role": "user",
                        "content": user_query
                    }
                )

                # Generate AI response
                with st.spinner(
                    "🤖 AI Recruiter is thinking..."
                ):

                    try:

                        response = generate_rag_response(
                            st.session_state.candidate_profile,
                            st.session_state.candidate_preferences,
                            st.session_state.matched_jobs,
                            user_query
                        )

                        st.session_state.chat_history.append(
                            {
                                "role": "assistant",
                                "content": response
                            }
                        )

                    except Exception as e:

                        st.session_state.chat_history.append(
                            {
                                "role": "assistant",
                                "content": (
                                    "I couldn't generate a response "
                                    "right now. Please try again in a moment."
                                )
                            }
                        )

                        st.error(
                            f"AI Recruiter error: {e}"
                        )

                st.rerun()


        # ==================================================
        # STEP 9 — INTERVIEW QUESTION GENERATOR
        # ==================================================

        if st.session_state.screening_results:

            st.html(
                """
                <div class="section-header">
                    🎤 Interview Preparation
                </div>
                """
            )

            st.html(
                """
                <div class="section-description">
                    Generate personalized interview questions based on
                    the candidate profile and selected job.
                </div>
                """
            )

            # --------------------------------------------------
            # JOB SELECTION
            # --------------------------------------------------

            job_options = [
                result["job"]
                for result in st.session_state.screening_results
            ]

            selected_job = st.selectbox(
                "Select a job to prepare for",
                job_options,
                format_func=lambda job: (
                    f"{job.title} • "
                    f"{job.location} • "
                    f"{job.experience}"
                ),
                key="selected_interview_job"
            )

            # --------------------------------------------------
            # GENERATE QUESTIONS
            # --------------------------------------------------

            if st.button(
                "🎤 Generate Interview Questions",
                key="generate_interview_questions",
                type="primary"
            ):

                with st.spinner(
                    "Generating personalized interview questions..."
                ):

                    try:

                        interview_questions = (
                            generate_interview_questions(
                                st.session_state.candidate_profile,
                                selected_job
                            )
                        )

                        st.session_state.interview_questions = (
                            interview_questions
                        )

                    except Exception as e:

                        st.session_state.interview_questions = None

                        st.error(
                            f"Interview question generation failed: {e}"
                        )

            # --------------------------------------------------
            # DISPLAY GENERATED QUESTIONS
            # --------------------------------------------------

            if st.session_state.interview_questions:

                interview_questions = (
                    st.session_state.interview_questions
                )

                st.html(
                    """
                    <div class="section-description">
                        Personalized interview questions for the selected role.
                    </div>
                    """
                )

                q1, q2, q3 = st.tabs(
                    [
                        "💻 Technical",
                        "👔 Experience",
                        "🎯 Role Specific"
                    ]
                )

                # --------------------------------------------------
                # TECHNICAL QUESTIONS
                # --------------------------------------------------

                with q1:

                    if interview_questions.technical_questions:

                        for index, question in enumerate(
                            interview_questions.technical_questions,
                            start=1
                        ):

                            st.markdown(
                                f"**{index}. {question}**"
                            )

                            st.divider()

                    else:

                        st.info(
                            "No technical questions were generated."
                        )

                # --------------------------------------------------
                # EXPERIENCE QUESTIONS
                # --------------------------------------------------

                with q2:

                    if interview_questions.experience_questions:

                        for index, question in enumerate(
                            interview_questions.experience_questions,
                            start=1
                        ):

                            st.markdown(
                                f"**{index}. {question}**"
                            )

                            st.divider()

                    else:

                        st.info(
                            "No experience questions were generated."
                        )

                # --------------------------------------------------
                # ROLE-SPECIFIC QUESTIONS
                # --------------------------------------------------

                with q3:

                    if interview_questions.role_specific_questions:

                        for index, question in enumerate(
                            interview_questions.role_specific_questions,
                            start=1
                        ):

                            st.markdown(
                                f"**{index}. {question}**"
                            )

                            st.divider()

                    else:

                        st.info(
                            "No role-specific questions were generated."
                        )