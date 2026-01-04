import re

def atomic_normalize(text, mapping):
    if not text: return ""
    text = text.lower().strip()
    # Sort by length descending to prevent partial matches (e.g., 'async' in 'asyncio')
    sorted_variants = sorted(mapping.keys(), key=len, reverse=True)
    pattern = re.compile(r'\b(' + '|'.join(re.escape(v) for v in sorted_variants) + r')\b')
    
    return pattern.sub(lambda m: mapping[m.group(0)], text)

