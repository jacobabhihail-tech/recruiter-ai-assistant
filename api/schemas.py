from pydantic import BaseModel


class MatchRequest(BaseModel):

    candidate_profile: dict

    candidate_preferences: dict

    top_k: int = 5


class ChatRequest(BaseModel):

    candidate_profile: dict

    candidate_preferences: dict

    matched_jobs: list

    query: str


class UploadResponse(BaseModel):

    filename: str

    resume_text: str

    candidate_profile: dict