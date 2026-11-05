from pydantic import BaseModel 

class JobDescription(BaseModel):
    description: str

class JobAnalysis(BaseModel):
    title: str
    required_skills: list[str]
    experience_level: str
    minimum_experience_years: int | None = None 