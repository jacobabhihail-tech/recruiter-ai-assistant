import os

from dotenv import load_dotenv
from google import genai

from src.candidate_summary_schema import CandidateSummary


load_dotenv()


client = genai.Client(
    api_key=os.getenv("API_KEY")
)


def generate_candidate_summary(
    candidate_profile,
    candidate_insights,
    candidate_preferences
) -> CandidateSummary:

    prompt = f"""
You are an experienced technical recruiter.

Create a concise ATS-style candidate summary.

CANDIDATE PROFILE

Name:
{candidate_profile.name}

Skills:
{candidate_profile.skills}

Years of Experience:
{candidate_profile.years_experience}

Roles:
{candidate_profile.roles}

Education:
{candidate_profile.education}


AI CANDIDATE INSIGHTS

Likely Job Titles:
{candidate_insights.likely_job_title}

Skill Summary:
{candidate_insights.skill_summary}

Strengths:
{candidate_insights.strengths}


CANDIDATE PREFERENCES

Preferred Location:
{candidate_preferences.preferred_location}

Salary Expectation:
{candidate_preferences.salary_expectation}

Interested Role:
{candidate_preferences.interested_role}

Work Preference:
{candidate_preferences.work_preference}

Notice Period:
{candidate_preferences.notice_period}


Generate:

1. A concise professional candidate summary.
2. The candidate's strongest professional strengths.
3. Practical recruiter notes.

Rules:

- Stay grounded in the supplied information.
- Do not invent experience, skills, companies, or achievements.
- Keep the candidate summary concise.
- Make the output useful to a technical recruiter.
- Recruiter notes should highlight useful screening considerations.
- Do not make discriminatory or personal judgments.

Return structured data matching the
CandidateSummary schema.
"""

    response = client.models.generate_content(
        model=os.getenv(
            "MODEL_NAME",
            "gemini-3.1-flash-lite"
        ),

        contents=prompt,

        config={
            "temperature": 0.2,
            "response_mime_type": "application/json",
            "response_schema": CandidateSummary,
        }
    )

    return CandidateSummary.model_validate_json(
        response.text
    )