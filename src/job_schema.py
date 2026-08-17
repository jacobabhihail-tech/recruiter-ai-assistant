from pydantic import BaseModel


class Job(BaseModel):
    id: int
    title: str
    skills: list[str]
    location: str
    experience: str