from app.llm.base import LLMProvider  
from pydantic import BaseModel 

class MockLLMProvider(LLMProvider):

    async def generate(self, prompt: str) -> str:

        return """
        {
            "title": "Junior Python Developer",
            "skills": [
                "Python",
                "FastAPI",
                "PostgreSQL",
                "Docker"
            ],
            "experience_level": "Junior"
        }
        """

    async def generate_structured(self, prompt: str, response_model: type[BaseModel]) -> BaseModel:

        mock_data = {
            "title": "Junior Python Developer",
            "required_skills": [
                "Python",
                "FastAPI",
                "PostgreSQL",
                "Docker"
            ],
            "experience_level": "Junior",
            "minimum_experience_years": 0
        }

        return response_model.model_validate(mock_data)
        