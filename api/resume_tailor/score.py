from api.resume_tailor.vocab import VARIANT_TO_CANONICAL, VARIANT_TO_CONCEPT_CANONICAL
from api.resume_tailor.normalizer import atomic_normalize

# Single source of truth for mapping
MASTER_LOOKUP = {**VARIANT_TO_CANONICAL, **VARIANT_TO_CONCEPT_CANONICAL}

def calculate_score(jd_data, master_resume):
    # --- 1. SYMMETRIC RESUME PREP ---
    resume_skills_norm = set()
    all_resume_text = "" # To catch skills mentioned in bullets but not in skills list
    
    sections = master_resume.get('experience', []) + master_resume.get('projects', [])
    for item in sections:
        # Collect skills
        for skill in item.get('skills', []):
            resume_skills_norm.add(atomic_normalize(skill, MASTER_LOOKUP))
        # Collect bullet text for the safety net
        all_resume_text += " ".join(item.get('bullets', [])).lower()

    WEIGHT_REQUIRED = 1.0
    WEIGHT_NICE = 0.3

    max_possible_score = 0
    actual_score = 0
    matches = []
    missing = []

    # --- 2. DEDUPLICATE AND NORMALIZE JD REQUIREMENTS ---
    # We use a dict to store normalized_skill -> original_display_name
    def get_clean_set(category_dict):
        clean_map = {}
        for skills in category_dict.values():
            for s in skills:
                norm = atomic_normalize(s, MASTER_LOOKUP)
                if norm not in clean_map: # Avoid double counting
                    clean_map[norm] = s
        return clean_map

    required_set = get_clean_set(jd_data.get('required', {}))
    nice_to_have_set = get_clean_set(jd_data.get('nice_to_have', {}))

    # --- 3. SCORING LOGIC ---
    # Score Required
    for norm_skill, display_name in required_set.items():
        max_possible_score += WEIGHT_REQUIRED
        
        # Primary Match: Skills List
        if norm_skill in resume_skills_norm:
            actual_score += WEIGHT_REQUIRED
            matches.append(display_name)
        # Secondary Match: Substring search in bullets (The "Safety Net")
        elif norm_skill in all_resume_text:
            actual_score += WEIGHT_REQUIRED 
            matches.append(f"{display_name} (found in text)")
        else:
            missing.append(display_name)

    # Score Nice-to-Have
    for norm_skill, display_name in nice_to_have_set.items():
        max_possible_score += WEIGHT_NICE
        
        if norm_skill in resume_skills_norm or norm_skill in all_resume_text:
            actual_score += WEIGHT_NICE
            matches.append(display_name)

    if max_possible_score == 0:
        return 0, matches, missing
    
    final_percentage = (actual_score / max_possible_score) * 100
    return round(final_percentage, 2), list(set(matches)), missing


