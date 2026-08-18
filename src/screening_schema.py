from pydantic import BaseModel


class ScreeningResult(BaseModel):

    match_score: float

    skill_overlap: list[str]

    missing_skills: list[str]

    experience_match: bool

    location_match: bool