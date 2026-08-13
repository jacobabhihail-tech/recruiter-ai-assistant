import os

from dotenv import load_dotenv

from google import genai

from src.candidate_schema import CandidateProfile

load_dotenv()

client = genai.Client(api_key= os.getenv("API_KEY"))

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
        model = os.getenv("MODEL_NAME"),
        contents= prompt,
        config={
            "temperature": float(os.getenv("TEMPERATURE", "0")),
            "max_output_tokens": int(os.getenv("MAX_TOKENS", "1000")),
            "response_mime_type": "application/json",
            "response_schema": CandidateProfile,
        }

    )

    return CandidateProfile.model_validate_json(response.text)