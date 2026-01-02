import os
import json


current_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(current_dir, "master_resume.json")


with open(file_path, "r") as file:
    master_resume = json.load(file)


def calculate_score(jd_data, master_resume):
    # 1. Extract all unique skills from your master resume
    resume_skills = set()
    for exp in master_resume.get('experience', []):
        resume_skills.update([s.lower() for s in exp.get('skills', [])])
    for proj in master_resume.get('projects', []):
        resume_skills.update([s.lower() for s in proj.get('skills', [])])

    WEIGHT_REQUIRED = 1.0
    WEIGHT_NICE = 0.3

    max_possible_score = 0
    actual_score = 0
    
    matches = []
    missing = []

    # 3. Score Required Skills
    # Flatten all categories (languages, frameworks, etc.) into one list
    required_categories = jd_data.get('required', {})
    for category, skills in required_categories.items():
        for skill in skills:
            skill_lower = skill.lower()
            max_possible_score += WEIGHT_REQUIRED
            if skill_lower in resume_skills:
                actual_score += WEIGHT_REQUIRED
                matches.append(skill)
            else:
                missing.append(skill)

    # 4. Score Nice-to-have Skills
    nice_categories = jd_data.get('nice_to_have', {})
    for category, skills in nice_categories.items():
        for skill in skills:
            skill_lower = skill.lower()
            max_possible_score += WEIGHT_NICE
            if skill_lower in resume_skills:
                actual_score += WEIGHT_NICE
                matches.append(skill)
            # We don't necessarily penalize missing "nice-to-have" 
            # but they contribute to the denominator to keep the score realistic

    if max_possible_score == 0:
        return 0, matches, missing
    
    final_percentage = (actual_score / max_possible_score) * 100
    return round(final_percentage, 2), matches, missing



if __name__ == "__main__":
    print(">>> Loaded master resume")
    print(master_resume)