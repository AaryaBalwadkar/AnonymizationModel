import spacy
import re

PII_ENTITIES = {"PERSON", "ORG", "GPE", "LOC", "EMAIL", "PHONE", "ID"}
nlp = spacy.load("en_core_web_lg")

REGEX_PATTERNS = {
    "EMAIL": r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b",
    "PHONE": r"\b(\+?\d{1,4}[\s-])?(?:\(?\d{3}\)?[\s.-])?\d{3}[\s.-]?\d{4}\b",
    "ID": r"\b[A-Z]{2}\d{6,}\b"  # e.g., IN12345678
}


def detect_pii(text):
    entities = {}

    # NLP entities
    doc = nlp(text)
    for ent in doc.ents:
        if ent.label_ in PII_ENTITIES:
            entities[ent.text] = f"[{ent.label_}]"

    # Regex fallback
    for label, pattern in REGEX_PATTERNS.items():
        for match in re.findall(pattern, text):
            entities[match] = f"[{label}]"

    return entities
