from src.candidate_schema import CandidateProfile
from src.job_schema import Job
from src.interview_engine import generate_interview_questions


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


questions = generate_interview_questions(
    candidate_profile,
    job
)


print("\nInterview Questions\n")

print(
    questions.model_dump_json(
        indent=4
    )
)