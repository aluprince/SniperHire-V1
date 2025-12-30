from pydantic import BaseModel
from typing import List

class ResumeSection(BaseModel):
    title: str
    content: str

class Resume(BaseModel):
    summary: ResumeSection
    skills: ResumeSection
    experience: List[ResumeSection]
    projects: List[ResumeSection]
