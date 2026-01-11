SniperHire-V1: Autonomous Resume Orchestrator
SniperHire-V1 is a high-impact CLI tool designed for Backend and AI Engineers to automate the heavy lifting of resume tailoring. It treats a resume as a version-controlled data object, using Llama-3.3-70B to bridge the gap between static experience and specific Job Description (JD) requirements.

🛠 Core Engine Capabilities
Requirements Deconstruction: Leverages Llama-3.3-70B to parse raw JD text into categorized technical requirements (Required vs. Nice-to-Have).

Skill Gap Analysis: Audits your master_resume.json against the JD to identify missing keywords and technical debt before generation.

Asynchronous Orchestration: Built with AsyncIO to handle LLM calls and PDF rendering pipelines, reducing tailoring time from minutes to under 20 seconds.

Jinja2 Templating: Decouples content from presentation, ensuring clean, ATS-compliant PDF generation every time.

## 📂 Project Structure & Schema
The system relies on a structured master_resume.json. This acts as your "source of truth."

Master Resume Schema
To use the orchestrator, ensure your data follows this structure in api/resume_tailor/master_resume.json:

{
  "contact": {
    "name": "John Doe",
    "email": "johndoe@example.com",
    "location": "New York, USA",
    "github": "github.com/johndoe"
  },
  "education": [
    {
      "degree": "B.S. in Computer Science",
      "institution": "State University",
      "status": "Completed"
    }
  ],
  "experience": [
    {
      "role": "Software Engineer",
      "company": "Global Tech",
      "dates": "2021 – Present",
      "bullets": [
        "Optimized backend microservices reducing latency by 20%.",
        "Integrated AI modules for automated data processing."
      ]
    }
  ],
  "projects": [
    {
      "name": "Project Alpha",
      "bullets": ["Developed a scalable web scraper using Python and FastAPI."],
      "technologies": ["Python", "FastAPI", "Docker"]
    }
  ],
  "master_skills": {
    "languages": ["Python", "Go", "SQL"],
    "frameworks": ["FastAPI", "React"],
    "tools_devops": ["Docker", "Kubernetes", "PostgreSQL"],
    "concepts": ["REST APIs", "Microservices", "System Design"]
  }
} 

##




## ⚙️ Environment Setup
Before running the orchestrator, ensure you have your Groq API key configured:

```bash
export GROQ_API_KEY='your_api_key_here' # Linux/Mac
set GROQ_API_KEY='your_api_key_here'    # Windows


💻 Usage
Run the orchestrator directly from the terminal. The tool will extract JD requirements, calculate an initial match score, and generate a tailored PDF.

1. Install Package:
    pip install -e .

2. Resume Tailor:
    python -m cli.cli path/to/jd.txt

🚀 Roadmap: The Path to "Shock"
Phase 1 (Shipped): LLM-based JD extraction, initial scoring, and Jinja2-to-PDF rendering.

Phase 2 (Upcoming): High-Dimensional Semantic Scoring. Migrating from keyword matching to text-embedding-3-large vector similarity (3072 dimensions) to detect technical synonyms and architectural conceptual matches.

Phase 3: Autonomous Agentic Workflows for bulk processing and automated ATS feedback loops.