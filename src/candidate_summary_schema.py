from pydantic import BaseModel


class CandidateSummary(BaseModel):

    candidate_summary: str

    strengths: list[str]

    recruiter_notes: list[str]