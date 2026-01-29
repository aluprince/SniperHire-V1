import re
import os
from groq import Groq
from dotenv import load_dotenv
from .vocab import  CANONICAL_MAP, CONCEPT_CANONICAL_MAP
from .prompts import SEMANTIC_JD_PROMPT
from .score import calculate_score, calculate_segmented_score
from .tailor import run_tailoring_engine
from .renderer import generate_tailored_resume
from .schema import JDExtraction
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
    

def extract_jd(jd_text):
    # Convert Pydantic schema to a JSON-schema string for the prompt
    schema_json = json.dumps(JDExtraction.model_json_schema(), indent=2)
    
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": f"{SEMANTIC_JD_PROMPT.format(job_description=jd_text, schema_json=schema_json)}"
            }
        ],
        model="llama-3.3-70b-versatile", # High reasoning for extraction
        temperature=0.0, # For a Deterministic Output and reduction of hallucinations
        response_format={"type": "json_object"}
    )
    
    raw_response = chat_completion.choices[0].message.content
    normalized_response = normalize_output(raw_response)

    
    # Then validate against the Pydantic schema
    try:
        return JDExtraction.model_validate_json(json.dumps(normalized_response))
    except Exception as e:
        print(f">>> Schema Validation Error: {e}")


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
    extracted_requirements = extract_jd(jd)
    # print("Extracted JD Requirements:", extracted_requirements)
    score_before_tailoring = calculate_segmented_score(extracted_requirements, master_resume)
    print("This is before Optimization: ", score_before_tailoring)
   
    llm_tailored_json = run_tailoring_engine(master_resume=master_resume, raw_jd=jd, jd_requirements=extracted_requirements, missing_skills=score_before_tailoring)
    
    score_after_optimization = calculate_segmented_score(jd_data=llm_tailored_json, resume_json=master_resume)
    print("This is after optimization: ", score_after_optimization)
    # tailored resume 
    pdf_resume = generate_tailored_resume(llm_tailored_json, master_resume)


