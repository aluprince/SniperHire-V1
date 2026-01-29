from pydantic import BaseModel, Field
from typing import List

class SkillMatch(BaseModel):
    skill_name: str
    is_present: bool
    evidence_quote: str = Field(description="Direct quote from resume proving the skill")
    impact_score: int = Field(description="Score 1-5 based on quantifiable results found")

class JDAnalysis(BaseModel):
    hard_skills: List[SkillMatch]
    soft_skills: List[SkillMatch]
    overall_sentiment: str

class JDExtraction(BaseModel):
    hard_skills: List[str] = Field(description="Top 5 mandatory technical skills or certifications.")
    experience_requirements: str = Field(description="Years of experience and seniority level expected.")
    key_responsibilities: List[str] = Field(description="The core 3-5 tasks the role performs.")
    nice_to_haves: List[str] = Field(description="Preferred but not mandatory skills.")
    target_keywords: List[str] = Field(description="Specific industry acronyms or tools (e.g., 'SaaS', 'CI/CD').")

    