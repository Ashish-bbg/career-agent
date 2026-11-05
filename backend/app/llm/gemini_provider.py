from google import genai
from pydantic import BaseModel
from app.llm.base import LLMProvider

class GeminiProvider(LLMProvider):

    def __init__(self, api_key: str, model: str):
        self.client = genai.Client(api_key=api_key)
        self.model = model 

    async def generate(self, prompt: str) -> str:

        response = await self.client.aio.models.generate_content(
            model = self.model,
            contents = prompt
        )
        return response.text

    async def generate_structured(self, prompt: str, response_model: type[BaseModel]) -> BaseModel:

        response = await self.client.aio.models.generate_content(
            model = self.model,
            contents = prompt,
            config = {
                "response_mime_type": "application/json",
                "response_json_schema": response_model.model_json_schema()
            }
        )

        return response_model.model_validate_json(response.text)
    