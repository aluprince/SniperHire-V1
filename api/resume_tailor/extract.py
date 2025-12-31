import re
from .vocab import SKILLS, TOOLS, FRAMEWORKS, LANGUAGES, ROLE_TERMS, SKILL_ALIASES, CONCEPTS


def normalize_job_description(jd_text):
    text = jd_text.lower()
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text

STOPWORDS = {"and", "or", "to", "for", "in", "a", "we", "are"}

def valid_ngram(ngram):
    words = ngram.split()
    return words[0] not in STOPWORDS and words[-1] not in STOPWORDS

def generate_ngrams(tokens: list, n):
    ngrams = []
    for i in range(len(tokens) - n + 1):
        ngram = " ".join(tokens[i:i + n])
        ngrams.append(ngram)
    return ngrams


def extract_job_description(jd_text):
    cleaned_text = normalize_job_description(jd_text)
    tokens = cleaned_text.split()
    unigram = set(tokens)
    bigrams = set(generate_ngrams(tokens, 2))
    trigrams = set(generate_ngrams(tokens, 3))
    all_terms = unigram | bigrams | trigrams
    all_terms = [term for term in all_terms if valid_ngram(term)]

    print(all_terms)

    return all_terms

def normalize_terms(text: str, aliases: dict, jd_list) -> set[str]:
    """
    Converts free text into a set of canonical skill tokens.
    """
    text = text.lower()
    found = set()

    for canonical, variants in aliases.items():
        for v in variants:
            if v in text:
                found.add(canonical)
                break  # stop after first match
    
    for term in jd_list:
        if term in SKILLS:
            found.add(term)
        if term in FRAMEWORKS:
            found.add(term)
        if term in TOOLS:
            found.add(term)
        if term in ROLE_TERMS:
            found.add(term)
        if term in CONCEPTS:
            found.add(term)
        
    print("FOUND: ", found)

    return found


def classify_terms(terms: list) -> dict:

    classified = {
        "skills": [],
        "frameworks": [],
        "tools": [],
        "languages": [],
        "role_terms": [],
        "concepts": []
    }


    for term in terms:
        print(term)
        if term in SKILLS:
            print("found in skills: ", term)
            classified["skills"].append(term)
        if term in FRAMEWORKS:
            print("found in framework: ", term)
            classified["frameworks"].append(term)
        if term in TOOLS:
            print("found in tools: ", term)
            classified["tools"].append(term)
        if term in LANGUAGES:
            print("found in languages: ", term)
            classified["languages"].append(term)
        if term in ROLE_TERMS:
            print("found in role_terms: ", term)
            classified["role_terms"].append(term)
        if term in CONCEPTS:
            print('found in concepts: ', term)
            classified["concepts"].append(terms)

        print("new classified: ", classified)

    return classified


if __name__ == "__main__":

    jd = """We are looking for a backend developer skilled in Python, Django, and AWS to build scalable APIs."""
    terms = extract_job_description(jd)
    print("Extracted Terms:", terms)
    normalized = normalize_terms(jd, SKILL_ALIASES, jd_list=terms)
    print("Normalized Terms:", normalized)
    classified = classify_terms(normalized)
    print("Classified Terms:", classified)



