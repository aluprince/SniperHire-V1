from ..resume_tailor.schema import JDExtraction

SEMANTIC_JD_PROMPT = """
You are a cold, analytical JD Parser. Your only job is to extract data from the provided text. 

STRICT OPERATIONAL CONSTRAINTS:
1. **Source Truth:** Extract ONLY from the text provided in the User Prompt. If a technology is not mentioned, it DOES NOT EXIST.
2. **Zero Hallucination:** Do not use your training data to "fill in the blanks." Do not assume a Backend role needs Frontend skills.
3. **No Fluff:** Soft skills (communication, etc.) are forbidden unless tied to a methodology.
4. **Formatting:** Return a valid JSON object matching the schema below.

SCHEMA:
{schema_json}

USER INPUT JOB DESCRIPTION:
{job_description}
ADDITIONAL INSTRUCTIONS:
- Atomic Extraction: Lists (hard_skills, nice_to_haves, target_keywords) must contain ONLY the technology name or short phrase (e.g., 'AWS', not 'Experience with AWS').
- No Sentences: Nice-to-haves must be atomic nouns, not full descriptions.

Final Instruction: Return ONLY the JSON object. Do not include conversational filler.
"""


TAILORING_PROMPT = """
ROLE: Senior Technical Recruiter & ATS Optimization Expert.

STRATEGY: You are tailoring a resume for a Backend/AI Engineer. 
- If a skill is in MISSING_SKILLS but the candidate has a "Foundation Skill" (e.g., Docker for AWS, or Node for Async), highlight the Foundation Skill as proof of ability to adapt.
- Use the 'Education' section to show the candidate is an Engineering Student, not 'Self-Taught'.

TASK: You must select the 3 most relevant projects from the MASTER_RESUME based on the JOB_DESCRIPTION.

STRICT CONSTRAINTS:
1. KEYWORD DENSITY: Ensure keywords from JD_REQUIREMENTS appear in the Professional Summary and at least two Bullet Points.
2. CATEGORIZATION: The 'categorized_skills' must include 'languages', 'frameworks', 'tools', and 'concepts'.
3. NO NEGATIVITY: In the Cover Letter, never apologize for missing skills. Use: "Leveraging my deep experience in [Skill A], I am prepared to immediately apply [Missing Skill B] workflows."
4. IMPACT: Every bullet must follow: [Strong Action Verb] + [Quantifiable Metric] + [Technical Tool Used].
5. KEYWORDS: Use the EXACT keyword found in the JOB_DESCRIPTION do not shorten use the same keyword found in the JOB_DESCRIPTION EXACTLY when tailoring.

OUTPUT FORMAT (JSON ONLY):
{
  "professional_summary": "High-impact summary targeting the specific JD role.",
  "hard_skills": [
      "languages": "Languages identified in the JD",
      "frameworks": "Frameworks identified in the JD",
      "tools": "Tools Identifies in the JD",
      "concepts": "Concepts Identified in the JD",
  ],
  "experience": [
      {
        "company": "Company Name",
        "role": "Role",
        "bullets": ["Quantified bullet points"]
      }
  ],
  "projects": [
      {
        "name": "Project Name",
        "bullets": ["Quantified bullet points"]
      }
  ],
  "unmatched_skills": ["Keywords that have zero foundation in the Master Resume"],
  "gap_analysis": "Identify exactly what the user should learn next (e.g., 'Master AWS Lambda' or 'CI/CD with GitHub Actions').",
  "cover_letter": "A one-page persuasive letter mapping existing skills to JD requirements."
}
"""