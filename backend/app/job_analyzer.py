from app.llm.base import LLMProvider
from app.jobs import JobAnalysis 

class JobAnalyzer:

    def __init__(self, llm: LLMProvider):
        self.llm = llm

    async def analyze(  self, job_description: str) -> str:

        prompt = f"""
        Analyze the following job description.

        Extract:
        - Job title
        - Required skills
        - Experience level

        Job Description:
        {job_description}
        """

        response = await self.llm.generate_structured(
            prompt = prompt,
            response_model=JobAnalysis
            
            )

        return response
