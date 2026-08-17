from src.candidate_schema import CandidateProfile
from src.intake_schema import CandidatePreferences
from src.candidate_matcher import create_candidate_embedding


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


embedding = create_candidate_embedding(
    candidate_profile,
    candidate_preferences
)


print("Embedding type:", type(embedding))
print("Embedding dimensions:", len(embedding))
print("First 10 values:", embedding[:10])