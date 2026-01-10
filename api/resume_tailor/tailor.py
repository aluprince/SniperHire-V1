import os
import json
from .prompts import TAILORING_PROMPT
from .llm_client import get_llm_tailoring

current_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(current_dir, "master_resume.json")

with open(file_path, "r") as file:
    master_resume = json.load(file)


def run_tailoring_engine(master_resume, raw_jd, jd_requirements, missing_skills):
    # 1. Format the context for the LLM
    context = {
        "MASTER_RESUME": master_resume,
        "JOB_DESCRIPTION": raw_jd,
        "JD_REQUIREMENTS": jd_requirements,
        "MISSING_SKILLS": missing_skills
    }
    
    response = get_llm_tailoring(prompt=TAILORING_PROMPT, context=context)
    tailored_text = response.replace("```json", "").replace("```", "").strip()
    tailored_json = json.loads(tailored_text)

    if tailored_json.get("unmatched_skills"):
        print(f"The JD requires {tailored_json.get('unmatched_skills')}")
    else:
        print("seems you are an ideal candidate for this job")
    
    return tailored_json


if __name__ == "__main__":
    tailored_resume = run_tailoring_engine(master_resume=master_resume)