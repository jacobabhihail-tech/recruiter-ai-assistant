import os

from dotenv import load_dotenv
from google import genai

from src.candidate_schema import CandidateProfile
from src.profile_schema import CandidateInsights


load_dotenv()


client = genai.Client(
    api_key=os.getenv("API_KEY")
)


def generate_candidate_insights(
    candidate_profile: CandidateProfile,
) -> CandidateInsights:

    prompt = f"""
    Analyze the following candidate profile and generate professional
    recruitment insights.

    Candidate Profile:
    {candidate_profile.model_dump_json(indent=2)}

    Determine:

    1. Likely job titles:
       Identify 3 to 5 realistic job titles that this candidate
       appears qualified for based only on their skills, experience,
       and existing roles.

    2. Skill summary:
       Write a concise professional summary of the candidate's
       technical and professional skill set.

    3. Candidate strengths:
       Identify the candidate's strongest areas that would be
       valuable to an employer.

    Important:
    - Use only information available in the candidate profile.
    - Do not invent qualifications or experience.
    - Keep the analysis realistic and recruiter-oriented.
    """

    response = client.models.generate_content(
        model=os.getenv("MODEL_NAME"),
        contents=prompt,
        config={
            "max_output_tokens": int(
                os.getenv("MAX_TOKENS", "1000")
            ),
            "response_mime_type": "application/json",
            "response_schema": CandidateInsights,
        },
    )

    return CandidateInsights.model_validate_json(response.text)