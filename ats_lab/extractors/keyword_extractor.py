import re

VOCAB = {
    "languages": {
        "python", "java", "javascript", "typescript", "rust", "go"
    },
    "frameworks": {
        "django", "fastapi", "flask", "react", "next.js", "node.js"
    },
    "tools": {
        "docker", "git", "github", "kubernetes", "terraform"
    },
    "databases": {
        "postgresql", "mysql", "mongodb", "redis"
    },
    "cloud": {
        "aws", "gcp", "azure"
    }
}

ALIASES = {
    "js": "javascript",
    "ts": "typescript",
    "node": "node.js",
    "postgres": "postgresql",
    "k8s": "kubernetes"
}



def clean_text(text: str) -> str:
    """ Clean the input text by removing special characters and extra spaces while also keeping them lowercase."""
    text = text.lower()
    text = re.sub(r'[^a-zA-Z0-9\s]', ' ', text)  # Remove special characters
    text = re.sub(r'\s+', ' ', text).strip()  # Remove extra spaces
    return text

def generate_ngrams(token_list: list, n: int):
    pass

def extract_keywords(text: str, nlp_model) -> list:
    """ Extract keywords from the input text using the spaCy model."""
    cleaned_text = clean_text(text)




if __name__ == "__main__":
    nlp = spacy.load("en_core_web_sm")
    sample_text = "We are looking for a Senior Software Engineer with experience in Python, SQL, and cloud technologies."
    cleaned_text = clean_text(sample_text)
    keywords = extract_keywords(cleaned_text, nlp)
    print("Extracted Keywords:", keywords)