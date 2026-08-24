import os

from dotenv import load_dotenv
from google import genai
from google.genai import types

from src.candidate_schema import CandidateProfile


# Load local .env when running locally.
# On Render, environment variables come from Render itself.
load_dotenv()


# --------------------------------------------------
# GEMINI CONFIGURATION
# --------------------------------------------------

API_KEY = os.getenv("GOOGLE_API_KEY")

if not API_KEY:
    raise RuntimeError(
        "GOOGLE_API_KEY environment variable is not configured."
    )


client = genai.Client(api_key=API_KEY)


# Use a current Gemini model that supports structured JSON output.
MODEL_NAME = os.getenv(
    "MODEL_NAME",
    "gemini-2.5-flash"
)


# --------------------------------------------------
# CANDIDATE PROFILE EXTRACTION
# --------------------------------------------------

def extract_candidate_profile(resume_text: str) -> CandidateProfile:

    prompt = f"""
Analyze the following resume and extract the candidate's information.

Return:
- candidate name
- technical and professional skills
- total years of professional experience
- job roles/titles
- education

Use only information present in the resume.
Do not invent information.

Resume:
{resume_text}
"""

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt,
        config=types.GenerateContentConfig(
            temperature=float(
                os.getenv("TEMPERATURE", "0")
            ),
            max_output_tokens=int(
                os.getenv("MAX_TOKENS", "1000")
            ),
            response_mime_type="application/json",
            response_schema=CandidateProfile,
        ),
    )

    return CandidateProfile.model_validate_json(response.text)