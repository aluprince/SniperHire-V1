import re
import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

CANONICAL_MAP = {
    "restful apis": "rest",
    "rest api": "rest",
    "jwt-based systems": "jwt",
    "ci/cd pipelines": "ci/cd",
    "async programming": "asyncio",
    "ai-powered systems": "ai systems",
    "llm integrations": "llm"
}


client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)

def normalizing_output(json):
    lowercased_json = json.lower()
    print(lowercased_json)

    pattern = re.compile(r'\b(' + '|'.join(re.escape(k) for k in CANONICAL_MAP.keys()) + r')\b')

    # 3. Use a lambda function to look up the replacement for each match
    new_json = pattern.sub(lambda m: CANONICAL_MAP[m.group(0)], lowercased_json)

    print(new_json) 


def extract_relevant_jd(job_description, model):
    chat_completion = client.chat.completions.create(
        messages=[{
            "role" : "user",
            "content": f"""Instructions: With this job description:  {job_description},
             Give me the required for the job and the nice to have and output them in the form in only json strictly nothing else
             (e.g) {{
                    "required": {{
                        "languages": [],
                        "frameworks": [],
                        "tools": [],
                    "concepts": []
                    }},
                    "nice_to_have": {{
                    "languages": [],
                    "frameworks": [],
                    "tools": [],
                    "concepts": []
                    }}
                }}
                    Do no reinvent skills that do not exist and only output in the example provided
             """
        }],
        model=model
    )
    print(chat_completion.choices[0].message.content)

    result = chat_completion.choices[0].message.content
    return result



if __name__ == "__main__":
    print(">>> Let's goooo")
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
    normalizing_output(json_file)