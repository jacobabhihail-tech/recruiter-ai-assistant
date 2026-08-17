from src.candidate_schema import CandidateProfile
from src.intake_schema import CandidatePreferences
from src.matching_engine import find_matching_jobs
from src.rag_engine import generate_rag_response


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
    salary_expectation="12 LPA",
    interested_role="Python Developer",
    work_preference="Remote",
    notice_period="30 days"
)


retrieved_jobs = find_matching_jobs(
    candidate_profile,
    candidate_preferences,
    "data/jobs.json",
    top_k=5
)


question = "What are my main skill gaps for the most relevant jobs?"


response = generate_rag_response(
    candidate_profile,
    candidate_preferences,
    retrieved_jobs,
    question
)


print("\nAI Recruiter Response:\n")
print(response)