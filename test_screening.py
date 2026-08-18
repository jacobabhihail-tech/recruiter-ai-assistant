from src.candidate_schema import CandidateProfile
from src.intake_schema import CandidatePreferences
from src.job_schema import Job
from src.screening_engine import calculate_screening_score


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


candidate_preferences = CandidatePreferences(
    preferred_location="Bangalore",
    salary_expectation="500000",
    interested_role="Python Developer",
    work_preference="Remote",
    notice_period="30 days"
)


job = Job(
    id=1,

    title="Python Backend Developer",

    skills=[
        "Python",
        "FastAPI",
        "Django",
        "PostgreSQL",
        "Docker"
    ],

    location="Bangalore",

    experience="3+ years"
)


result = calculate_screening_score(
    candidate_profile,
    candidate_preferences,
    job
)


print("\nScreening Result:\n")

print(
    result.model_dump()
)