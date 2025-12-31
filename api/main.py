from fastapi import FASTAPI
from .resume_tailor.extract import extract_job_description,normalize_terms
from .resume_tailor.score import flatten_resume, score_resume
from .resume_tailor.vocab import SKILLS, TOOLS, FRAMEWORKS, LANGUAGES, ROLE_TERMS, SKILL_ALIASES
from .resume_tailor.score import master_resume

app = FASTAPI()

extracted_data = extract_job_description("We are looking for a backend developer skilled in Python, Django, and AWS to build scalable APIs.")

resume_text = flatten_resume(master_resume)
resume_skills = normalize_terms(resume_text, SKILL_ALIASES)




@app.get("/")
def home():
    return {"message": "Welcome to SniperHire ATSLAB"}










if __name__ == "__main__":
    app.run()