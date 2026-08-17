import os

from dotenv import load_dotenv
from google import genai


load_dotenv()


client = genai.Client(
    api_key=os.getenv("API_KEY")
)


def generate_rag_response(
    candidate_profile,
    candidate_preferences,
    retrieved_jobs,
    user_query
):

    candidate_context = f"""
Candidate Profile:

Name: {candidate_profile.name}

Roles:
{", ".join(candidate_profile.roles)}

Skills:
{", ".join(candidate_profile.skills)}

Years of Experience:
{candidate_profile.years_experience}

Education:
{", ".join(candidate_profile.education)}


Candidate Preferences:

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
"""


    job_context = "\n\n".join(
        [
            f"""
Job ID: {match["job"].id}

Title:
{match["job"].title}

Skills:
{", ".join(match["job"].skills)}

Location:
{match["job"].location}

Experience:
{match["job"].experience}

Similarity Distance:
{match["distance"]:.4f}
"""
            for match in retrieved_jobs
        ]
    )


    prompt = f"""
You are an AI Recruitment Assistant.

Your job is to help a candidate understand relevant
job opportunities.

Use the candidate information and retrieved job
information provided below.

Do not invent jobs, skills, experience, or candidate
information that is not present in the context.

If information is unavailable, say so clearly.

Candidate Information:
{candidate_context}


Retrieved Jobs:
{job_context}


Candidate Question:
{user_query}


Provide a clear and concise recruiter-style answer.
"""


    response = client.models.generate_content(
        model=os.getenv("MODEL_NAME"),
        contents=prompt
    )


    return response.text