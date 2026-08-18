from pydantic import BaseModel


class InterviewQuestions(BaseModel):

    technical_questions: list[str]

    experience_questions: list[str]

    role_specific_questions: list[str]