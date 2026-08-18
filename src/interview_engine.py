import os

from dotenv import load_dotenv
from google import genai

from src.interview_schema import InterviewQuestions

load_dotenv()

client = genai.Client(
    api_key=os.getenv("API_KEY")
)


def generate_interview_questions(
    candidate_profile,
    job
) -> InterviewQuestions:

    prompt = f"""
You are an experienced technical recruiter.

Generate personalized interview questions
for a candidate applying for a specific job.

CANDIDATE PROFILE:

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


JOB:

Title:
{job.title}

Required Skills:
{job.skills}

Location:
{job.location}

Required Experience:
{job.experience}


Generate interview questions that are:

1. Based on the candidate's actual skills
2. Relevant to the job requirements
3. Appropriate for the candidate's experience
4. Useful for a technical recruiter/interviewer

Return:

- 5 technical questions
- 3 experience-based questions
- 3 role-specific questions

Do not generate generic questions unrelated
to the candidate or job.
"""


    response = client.models.generate_content(
        model=os.getenv(
            "MODEL_NAME",
            "gemini-3.1-flash-lite"
        ),

        contents=prompt,

        config={
            "temperature": 0.4,
            "response_mime_type": "application/json",
            "response_schema": InterviewQuestions,
        }
    )


    return InterviewQuestions.model_validate_json(
        response.text
    )