from pydantic import BaseModel, Field

class CandidateInsights(BaseModel):
    likely_job_title: list[str] = Field(default_factory=list)
    skill_summary: str = ""
    strengths: list[str] = Field(default_factory=list)
