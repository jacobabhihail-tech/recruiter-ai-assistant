import os

from dotenv import load_dotenv
from google import genai


load_dotenv()


client = genai.Client(
    api_key=os.getenv("API_KEY")
)


def create_embedding(text: str):

    response = client.models.embed_content(
        model="gemini-embedding-2",
        contents=text,
    )

    return response.embeddings[0].values

def job_to_text(job):

    return f"""
    Job Title: {job.title}
    Skills: {", ".join(job.skills)}
    Location: {job.location}
    Experience: {job.experience}
    """