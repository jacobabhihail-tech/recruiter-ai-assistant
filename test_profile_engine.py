from src.candidate_schema import CandidateProfile
from src.profile_schema import CandidateInsights
from src.profile_engine import generate_candidate_insights

candidate = CandidateProfile(
    name="John Doe",
    skills=[
        "Python",
        "Django",
        "FastAPI",
        "SQL",
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

insights = generate_candidate_insights(candidate)

print("\n Candidate Insights")
print(insights.model_dump_json(indent=4))
