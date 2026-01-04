import os
import json
from .prompts import TAILORING_PROMPT
from .llm_client import get_llm

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
    
    # 2. Call the LLM (Ensuring JSON mode is ON)
    # response = llm.generate(prompt=TAILORING_PROMPT, context=context)

    response = get_llm(prompt=TAILORING_PROMPT, context=context)
    
    # 3. Validation Logic
    # check if 'unmatched_skills' has data. If yes, print a warning for the user.
    # "Warning: The JD requires AWS, but we couldn't find it in your resume. 
    # It has been moved to the Cover Letter strategy."
    
    return response_json


if __name__ == "__main__":
    tailored_resume = run_tailoring_engine(master_resume=master_resume)