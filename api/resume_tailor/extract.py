import re
import os
from groq import Groq
from dotenv import load_dotenv
from .vocab import  CANONICAL_MAP, CONCEPT_CANONICAL_MAP
from .prompts import JD_REQUIREMENTS_PROMPT
from .score import calculate_score
from .tailor import run_tailoring_engine
from .renderer import generate_tailored_resume
import json


load_dotenv()

current_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(current_dir, "master_resume.json")

with open(file_path, "r") as file: 
    master_resume = json.load(file)


VARIANT_TO_CANONICAL = {
    variant: canonical
    for canonical, variants in CANONICAL_MAP.items()
    for variant in variants
}

VARIANT_TO_CONCEPT_CANONICAL = {
    variant: canonical
    for canonical, variants in CONCEPT_CANONICAL_MAP.items()
    for variant in variants
}



client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)

import re
import json



def normalize_output(raw_text: str):
    text = raw_text.lower().replace("```json", "").replace("```", "").strip()

    # Combine both maps for a single pass or handle them sequentially
    # We use VARIANT_TO_CANONICAL (mapping "py" -> "python")
    
    # CRITICAL: Sort variants by length descending
    # This ensures "restful api" is caught before "rest"
    all_variants = sorted(VARIANT_TO_CANONICAL.keys(), key=len, reverse=True)
    
    for variant in all_variants:
        canonical = VARIANT_TO_CANONICAL[variant]
        # \b ensures we don't match 'py' inside 'happy'
        # re.escape ensures characters like '+' in 'C++' don't break the regex
        pattern = r'\b' + re.escape(variant) + r'\b'
        text = re.sub(pattern, canonical, text)

    concept_variants = sorted(VARIANT_TO_CONCEPT_CANONICAL.keys(), key=len, reverse=True)
    for variant in concept_variants:
        canonical = VARIANT_TO_CONCEPT_CANONICAL[variant]
        pattern = r'\b' + re.escape(variant) + r'\b'
        text = re.sub(pattern, canonical, text)

    try:
        return json.loads(text)
    except json.JSONDecodeError as e:
        print(f"Failed to parse JSON. Text was: {text}")
        raise e
    

def extract_relevant_jd(job_description, model):
    chat_completion = client.chat.completions.create(
        messages=[{
            "role" : "user",
            "content": f"""{JD_REQUIREMENTS_PROMPT.format(job_description=job_description)}"""
        }],
        model=model
    )
    print(chat_completion.choices[0].message.content)

    result = chat_completion.choices[0].message.content
    return result



if __name__ == "__main__":
    print(">>> Extracting JD Requirements <<< ")
    jd = """We are looking for a Backend Software Engineer to build and maintain scalable APIs for our core platform.

The ideal candidate must have strong experience with Python and FastAPI for building production-grade backend services.
You must be comfortable designing RESTful APIs and working with PostgreSQL databases in a production environment.
Experience with Docker for containerization is required.
You are expected to write clean, maintainable code and collaborate with frontend engineers and product managers.
You must have a solid understanding of authentication and authorization mechanisms such as JWT-based systems.

Experience with cloud platforms such as AWS is a strong plus.
Familiarity with asynchronous programming using AsyncIO is nice to have.
Experience working with CI/CD pipelines is considered a bonus.
Previous experience with AI-powered systems or LLM integrations is not required but would be an advantage.
"""
    model=model="llama-3.3-70b-versatile"
    json_file = extract_relevant_jd(jd, model)
    normalized = normalize_output(json_file)
    score = calculate_score(normalized, master_resume)
    print(f"Resume Match Score: {score[0]}%, {score[1]} matched skills, {score[2]} missing skills")
    llm_tailored_json = run_tailoring_engine(master_resume=master_resume, raw_jd=jd, jd_requirements=normalized, missing_skills=score)
    # tailored resume 
    pdf_resume = generate_tailored_resume(llm_tailored_json, master_resume)
    print(pdf_resume)


