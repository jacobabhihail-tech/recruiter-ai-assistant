from src.candidate_schema import CandidateProfile
from src.profile_schema import CandidateInsights
from src.intake_schema import CandidatePreferences

from src.candidate_summary_engine import (
    generate_candidate_summary
)


candidate_profile = CandidateProfile(
    name="John Doe",

    skills=[
        "Python",
        "Django",
        "FastAPI",
        "PostgreSQL",
        "AWS",
        "Docker"
    ],

    years_experience=4,

    roles=[
        "Python Developer",
        "Software Developer"
    ],

    education=[
        "Bachelor of Technology in Computer Science"
    ]
)


candidate_insights = CandidateInsights(
    likely_job_title=[
        "Python Backend Developer",
        "Python Software Engineer"
    ],

    skill_summary=(
        "Backend developer specializing in "
        "Python web development and cloud technologies."
    ),

    strengths=[
        "Strong Python backend development",
        "Experience with FastAPI and Django",
        "Database and cloud experience"
    ]
)


candidate_preferences = CandidatePreferences(
    preferred_location="Bangalore",
    salary_expectation="12 LPA",
    interested_role="Python Developer",
    work_preference="Remote",
    notice_period="30 days"
)


summary = generate_candidate_summary(
    candidate_profile,
    candidate_insights,
    candidate_preferences
)


print("\nCandidate Summary\n")

print(
    summary.model_dump_json(
        indent=4
    )
)