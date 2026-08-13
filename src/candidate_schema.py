from pydantic import BaseModel, Field

class CandidateProfile(BaseModel):
    name: str = ""
    skills: list[str] = Field(default_factory=list)
    years_experience: float=0
    roles: list[str] = Field(default_factory=list)
    education: list[str] = Field(default_factory=list)