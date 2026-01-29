from api.resume_tailor.vocab import VARIANT_TO_CANONICAL, VARIANT_TO_CONCEPT_CANONICAL
from api.resume_tailor.normalizer import atomic_normalize
from sentence_transformers import SentenceTransformer, util

# Single source of truth for mapping
MASTER_LOOKUP = {**VARIANT_TO_CANONICAL, **VARIANT_TO_CONCEPT_CANONICAL}

model = SentenceTransformer('all-MiniLM-L6-v2')


def calculate_segmented_score(jd_data, resume_json):

    all_skills = set()
    master_skill = resume_json.get("master_skills", [])
    languages = set(master_skill["languages"])
    frameworks = set(master_skill["frameworks"])
    concepts = set(master_skill["concepts"])
    devop_tools = set(master_skill["tools_devops"])

    skill_union = languages | frameworks | concepts | devop_tools

    for skill in skill_union:
        all_skills.add(skill)
    
    res_skills = ", ".join(all_skills)
    res_exp = " ".join(bullet for exp in resume_json.get("experience", []) for bullet in exp["bullets"])
    
    try: 
    #We use the try block incase catch when we are to review the llm_tailored_json output
        jd_skills = ", ".join(jd_data.hard_skills)
        jd_experience = " ".join(jd_data.key_responsibilities)
    except AttributeError: 
        jd_skills = ", ".join(jd_data["hard_skills"])
        jd_exp = " ".join(bullet for exp in jd_data["experience"] for bullet in exp["bullets"])
        jd_proj = " ".join(bullet for proj in jd_data["projects"] for bullet in proj["bullets"])
        jd_experience = jd_exp + jd_proj

    emb_res_skills = model.encode(res_skills, convert_to_tensor=True)
    emb_jd_skills = model.encode(jd_skills, convert_to_tensor=True)
    
    emb_res_exp = model.encode(res_exp, convert_to_tensor=True)
    emb_jd_exp = model.encode(jd_experience, convert_to_tensor=True)
    
    # Calculating Cosine Similarities
    skill_sim = util.cos_sim(emb_res_skills, emb_jd_skills).item()
    exp_sim = util.cos_sim(emb_res_exp, emb_jd_exp).item()
    
    final_score = (skill_sim * 0.5) + (exp_sim * 0.5)
    return round(final_score * 100, 2)



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


