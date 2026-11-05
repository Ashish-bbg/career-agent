# Career Agent 🤖

Career Agent is an AI-powered job search and application assistant designed to help users discover relevant jobs, analyze job descriptions, compare jobs against their resume, and eventually assist throughout the job application process.

The project uses a **provider-independent LLM architecture**, allowing different AI providers such as Google Gemini, OpenAI, and Anthropic Claude to be integrated without changing the main business logic.

> 🚧 This project is currently under active development.

---

## 🎯 Project Goal

The long-term goal of Career Agent is to build an intelligent career assistant that can support the complete job-search workflow.

```text
Candidate Profile
        ↓
Job Discovery
        ↓
Job Analysis
        ↓
Resume Matching
        ↓
Job Ranking
        ↓
Resume Tailoring
        ↓
User Approval
        ↓
Application Assistance
        ↓
Application Tracking
        ↓
Interview Preparation
```

Important actions such as submitting a job application will keep the user in control through a human-approval step.

---

## ✅ Current Features

The current version includes:

- FastAPI backend
- Job description analysis
- Structured job information extraction
- Google Gemini integration
- Provider-independent LLM architecture
- Pydantic response validation
- Structured LLM output
- Environment-based provider configuration
- Environment-based model configuration
- Mock LLM provider for local testing

---

## 🧠 Current Job Analysis

Career Agent currently accepts a job description and converts it into structured information.

### Example Input

```json
{
  "description": "We are looking for a Robotics Software Engineer experienced in C++, Python, ROS2, computer vision, Docker and autonomous navigation. Candidates should have at least 2 years of software engineering experience."
}
```

### Example Output

```json
{
  "title": "Robotics Software Engineer",
  "required_skills": [
    "C++",
    "Python",
    "ROS2",
    "computer vision",
    "Docker",
    "autonomous navigation"
  ],
  "experience_level": "Mid-Level",
  "minimum_experience_years": 2
}
```

The response follows a predefined Pydantic schema instead of returning unpredictable free-form LLM text.

---

## 🏗️ Architecture

Career Agent separates business logic from provider-specific LLM implementations.

```text
                    .env
                     │
                     ▼
                  Config
                     │
                     ▼
                LLM Factory
                     │
                     ▼
                LLMProvider
                     │
          ┌──────────┼──────────┐
          │          │          │
          ▼          ▼          ▼
       Gemini      OpenAI     Anthropic
      Provider    Provider     Provider
          │       (planned)    (planned)
          │
          ▼
      JobAnalyzer
          │
          ▼
        FastAPI
```

### Why this architecture?

`JobAnalyzer` does not directly depend on Gemini.

Instead, it depends on the common:

```python
LLMProvider
```

interface.

For example:

```python
class LLMProvider(ABC):

    @abstractmethod
    async def generate(self, prompt: str) -> str:
        pass

    @abstractmethod
    async def generate_structured(
        self,
        prompt: str,
        response_model: type[BaseModel]
    ) -> BaseModel:
        pass
```

Provider-specific implementations implement the same contract.

For example:

```text
LLMProvider
     │
     ├── GeminiProvider
     ├── MockLLMProvider
     ├── OpenAIProvider      ← planned
     └── AnthropicProvider   ← planned
```

This makes it possible to switch AI providers without rewriting the job-analysis business logic.

---

## 💉 Dependency Injection

Career Agent currently uses manual dependency injection.

The selected LLM provider is created first:

```python
llm = get_llm_provider(settings.llm_provider)
```

The provider is then injected into the job analyzer:

```python
job_analyzer = JobAnalyzer(llm)
```

`JobAnalyzer` stores the injected provider:

```python
class JobAnalyzer:

    def __init__(self, llm: LLMProvider):
        self.llm = llm
```

The analyzer can therefore call:

```python
await self.llm.generate_structured(...)
```

without knowing whether the underlying implementation is Gemini, OpenAI, Claude, or another provider.

---

## 🤖 AI Provider

The project currently uses Google Gemini.

The provider and model are controlled through environment variables:

```env
LLM_PROVIDER=gemini
LLM_MODEL=gemini-3.5-flash-lite
```

This means the business logic does not contain hardcoded provider or model configuration.

Future providers will follow the same architecture.

---

## 📁 Project Structure

```text
career-agent/
│
├── backend/
│   │
│   ├── app/
│   │   │
│   │   ├── llm/
│   │   │   ├── base.py
│   │   │   ├── factory.py
│   │   │   ├── gemini_provider.py
│   │   │   └── mock_provider.py
│   │   │
│   │   ├── config.py
│   │   ├── job_analyzer.py
│   │   ├── jobs.py
│   │   └── main.py
│   │
│   ├── .env.example
│   ├── .gitignore
│   └── requirements.txt
│
└── README.md
```

The project structure will expand as resume processing, databases, authentication, job discovery, and application tracking are added.

---

# 🚀 Getting Started

## Prerequisites

Make sure you have:

- Python installed
- Git installed
- A Gemini API key
- VS Code or another Python IDE/editor

---

## 1. Clone the Repository

```bash
git clone https://github.com/Ashish-bbg/career-agent.git
```

Enter the project:

```bash
cd career-agent
```

Then enter the backend:

```bash
cd backend
```

---

## 2. Create a Virtual Environment

Create the environment:

```bash
python -m venv .venv
```

### Windows Command Prompt

```bash
.venv\Scripts\activate
```

### Windows PowerShell

```powershell
.\.venv\Scripts\Activate.ps1
```

After activation, the terminal should show something similar to:

```text
(.venv)
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Configure Environment Variables

Create a `.env` file inside the `backend` directory.

Example:

```env
LLM_PROVIDER=gemini
LLM_MODEL=gemini-3.5-flash-lite

GEMINI_API_KEY=your_gemini_api_key_here
```

Never commit the actual `.env` file to GitHub.

Use `.env.example` to document the required variables:

```env
LLM_PROVIDER=gemini
LLM_MODEL=gemini-3.5-flash-lite

GEMINI_API_KEY=
```

---

## 5. Start the FastAPI Server

From the `backend` directory:

```bash
uvicorn app.main:app --reload
```

The server should start at:

```text
http://127.0.0.1:8000
```

---

## 📖 API Documentation

FastAPI automatically generates interactive Swagger documentation.

After starting the server, open:

```text
http://127.0.0.1:8000/docs
```

---

# 🔌 API Endpoints

## Health Check

```http
GET /health
```

Example response:

```json
{
  "status": "healthy"
}
```

---

## Analyze Job

```http
POST /api/jobs/analyze
```

### Request

```json
{
  "description": "We need a Python backend developer experienced with FastAPI, PostgreSQL and Docker."
}
```

### Response

The API returns structured job information such as:

```json
{
  "title": "Python Backend Developer",
  "required_skills": ["Python", "FastAPI", "PostgreSQL", "Docker"],
  "experience_level": "Not specified",
  "minimum_experience_years": null
}
```

---

# 🔄 How Job Analysis Works

When a request is sent to:

```text
POST /api/jobs/analyze
```

the request flows through the application like this:

```text
Job Description
      │
      ▼
FastAPI Endpoint
      │
      ▼
JobDescription
Pydantic Validation
      │
      ▼
JobAnalyzer
      │
      ▼
LLMProvider
      │
      ▼
GeminiProvider
      │
      ▼
Gemini API
      │
      ▼
Structured JSON
      │
      ▼
JobAnalysis
Pydantic Validation
      │
      ▼
FastAPI Response
```

This ensures the API receives predictable structured data instead of free-form AI responses.

---

# 🗺️ Roadmap

## Phase 1: Job Understanding

- [x] Create FastAPI backend
- [x] Create job-analysis endpoint
- [x] Create LLM abstraction
- [x] Implement provider factory
- [x] Add Mock LLM provider
- [x] Integrate Google Gemini
- [x] Add structured output
- [x] Add Pydantic validation
- [x] Configure provider through environment variables
- [x] Configure model through environment variables

---

## Phase 2: Resume Intelligence

- [ ] Resume upload
- [ ] PDF resume parsing
- [ ] DOCX resume parsing
- [ ] Candidate profile extraction
- [ ] Skill extraction
- [ ] Work-experience extraction
- [ ] Education extraction
- [ ] Structured candidate profile

---

## Phase 3: Job Matching

- [ ] Compare candidate profile with job requirements
- [ ] Calculate job match score
- [ ] Identify matching skills
- [ ] Identify missing skills
- [ ] Analyze experience match
- [ ] Explain why a job is a good or poor match
- [ ] Generate apply/skip recommendation

Example future result:

```json
{
  "match_score": 82,
  "matching_skills": ["Python", "FastAPI", "Docker"],
  "missing_skills": ["Kubernetes"],
  "recommendation": "APPLY"
}
```

---

## Phase 4: Job Discovery

- [ ] Define job-search preferences
- [ ] Search supported job sources
- [ ] Filter by role
- [ ] Filter by location
- [ ] Filter by experience
- [ ] Filter by candidate preferences
- [ ] Analyze discovered job descriptions
- [ ] Rank jobs by candidate fit

---

## Phase 5: Application Assistant

- [ ] Tailor resume for selected jobs
- [ ] Generate cover letters
- [ ] Generate job-application answers
- [ ] Prevent fabricated qualifications
- [ ] Human approval before application submission
- [ ] Track submitted applications

---

## Phase 6: Application Tracking

- [ ] PostgreSQL database
- [ ] Save discovered jobs
- [ ] Save match results
- [ ] Save application status
- [ ] Track application history
- [ ] Track interview stages
- [ ] Application dashboard

Potential statuses:

```text
Discovered
    ↓
Analyzed
    ↓
Shortlisted
    ↓
Application Prepared
    ↓
User Approved
    ↓
Applied
    ↓
Interview
    ↓
Offer / Rejected
```

---

## Phase 7: Agentic AI

- [ ] Tool calling
- [ ] Job-search tools
- [ ] Resume tools
- [ ] Application tools
- [ ] MCP integration
- [ ] Multi-step agent workflows
- [ ] Agent state management
- [ ] Human-in-the-loop approval

---

## Phase 8: Multi-Provider AI

- [x] Provider-independent architecture
- [x] Gemini provider
- [x] Mock provider
- [ ] OpenAI provider
- [ ] Anthropic Claude provider
- [ ] Provider fallback
- [ ] Provider-specific capability detection

The goal is to eventually make switching providers as simple as changing:

```env
LLM_PROVIDER=gemini
```

to:

```env
LLM_PROVIDER=openai
```

or:

```env
LLM_PROVIDER=anthropic
```

without modifying the application's job-analysis logic.

---

## Phase 9: Interview Assistant

Future Career Agent capabilities may include:

- [ ] Generate interview questions from job descriptions
- [ ] Compare job requirements with candidate experience
- [ ] Technical interview preparation
- [ ] Behavioral interview preparation
- [ ] Recommendation of areas to study
- [ ] Interview progress tracking

---

# 🛠️ Technology Stack

### Backend

- Python
- FastAPI
- Pydantic

### AI

- Google Gemini
- Provider-independent LLM abstraction

Planned:

- OpenAI
- Anthropic Claude
- Tool calling
- MCP

### Database

Planned:

- PostgreSQL
- pgvector where semantic search is useful

### Frontend

Planned:

- React

### Infrastructure

Planned:

- Docker
- Cloud deployment

---

# 🔐 Security

API keys and other secrets must never be committed to the repository.

The `.gitignore` should contain:

```gitignore
.env
.venv/
__pycache__/
*.pyc
```

Only configuration templates such as `.env.example` should be committed.

Example:

```env
LLM_PROVIDER=gemini
LLM_MODEL=gemini-3.5-flash-lite

GEMINI_API_KEY=
```

---

# 🧪 Development Status

Career Agent is currently under active development.

### Current Milestone

✅ FastAPI backend  
✅ Provider-independent AI architecture  
✅ Gemini integration  
✅ Structured job-description extraction  
✅ Pydantic response validation

### Next Milestone

📄 **Resume Upload & Resume Parsing**

The next goal is to convert a user's resume into a structured candidate profile that can be compared against the structured job information.

After this milestone, Career Agent will be able to start answering the key question:

> **How well does this job match this candidate?**

---

# 🤝 Contributing

The project is currently in early development.

Issues, ideas, and contributions are welcome as the architecture and feature set evolve.

---

# ⚠️ Disclaimer

Career Agent is intended to assist users with job searching and application preparation.

AI-generated recommendations should be reviewed by the user before important actions are taken.

The system should not fabricate qualifications, work experience, education, skills, or other candidate information when tailoring applications.

---

## ⭐ Project Vision

The goal is not simply to create another job-search tool.

The goal is to build an AI career agent that can understand:

```text
Who is the candidate?
        +
What does the job require?
        ↓
How good is the match?
        ↓
Is the job worth applying for?
        ↓
How should the candidate prepare?
```

Eventually, Career Agent aims to help manage the journey from **job discovery to interview preparation**, while keeping the user in control of important decisions.
