JD_REQUIREMENTS_PROMPT = """
You are a strict information extraction engine.

From the job description below:
1. Extract REQUIRED skills
2. Extract NICE-TO-HAVE skills

Return valid JSON only, No other message only the JSON SCHEMA REQUIRED.

Schema:
{{
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

Job Description:
{job_description}
"""
