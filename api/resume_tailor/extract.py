# Extracting Normalizing Job Description
import re
from .vocab import SKILLS, TOOLS, FRAMEWORKS, LANGUAGES, ROLE_TERMS


def normalize_job_description(jd_text):
    text = jd_text.lower()
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def generate_ngrams(tokens, n):
    return " ".join([tokens[i:i+n] for i in range(len(tokens)-n + 1)])


def extract_job_description(jd_text):
    cleaned_text = normalize_job_description(jd_text)
    tokens = cleaned_text.split()
    unigram = set(tokens)
    bigrams = set(generate_ngrams(tokens, 2))
    trigrams = set(generate_ngrams(tokens, 3))

    all_terms = unigram | bigrams | trigrams

    return {
        "skills": sorted(SKILLS & all_terms),
        "framework": sorted(FRAMEWORKS & all_terms),
        "tools": sorted(TOOLS & all_terms),
        "languages": sorted(LANGUAGES & all_terms),
        "role_terms": sorted(ROLE_TERMS & all_terms)
    }



