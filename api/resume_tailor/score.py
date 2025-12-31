import json

with open("SniperHire-V1/api/resume_tailor/master_resume.json", "r") as file:
    master_resume = json.load(file)

def flatten_resume(master):
    units = []

    for exp in master["experience"]:
        text = " ".join(exp["bullets"]) + " " + " ".join(exp["skills"])
        units.append({
            "type": "experience",
            "role": exp["role"],
            "company": exp["company"],
            "text": text.lower(),
            "raw": exp
        })

    for proj in master["projects"]:
        text = " ".join(proj["bullets"]) + " " + " ".join(proj["skills"])
        units.append({
            "type": "project",
            "name": proj["name"],
            "text": text.lower(),
            "raw": proj
        })

    return units

def score_unit(units: str, jd_terms: set):
    return sum([1 for term in jd_terms if term in units["text"]])


def score_resume(units: list, jd_terms: set):
    scored = []

    for i in units:
        score = score_unit(i["text"], jd_terms)
        scored.append({
            "unit": i,
            "score": score
        })
    return scored


