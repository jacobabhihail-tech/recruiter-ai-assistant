from pydantic import BaseModel


class CandidatePreferences(BaseModel):
    preferred_location: str = ""
    salary_expectation: str = ""
    interested_role: str = ""
    work_preference: str = ""
    notice_period: str = ""