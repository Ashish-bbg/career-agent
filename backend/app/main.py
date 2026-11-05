from fastapi import FastAPI
from app.jobs import JobDescription, JobAnalysis
from app.job_analyzer import JobAnalyzer
from app.llm.factory import get_llm_provider
from app.config import settings

app = FastAPI(
    title = "Career Agent API",
    description = "AI powered job search and application assistant",
    version = "0.1.0"
)

llm = get_llm_provider(settings.llm_provider)
job_analyzer = JobAnalyzer(llm)

@app.get("/")
def root():
    return {
        "message": "Career Agent API is running"
    }

@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }

@app.post("/api/jobs/analyze",
          response_model = JobAnalysis
          )
async def analyze_job(job: JobDescription):
    return await job_analyzer.analyze(
        job.description
        )
    