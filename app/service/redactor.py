from faker import Faker

fake = Faker()

FAKE_GENERATORS = {
    "PERSON": lambda: fake.name(),
    "ORG": lambda: fake.company(),
    "GPE": lambda: fake.city(),
    "EMAIL": lambda: fake.email(),
    "PHONE": lambda: fake.phone_number(),
    "ID": lambda: fake.ssn(),
    "LOC": lambda: fake.address()
}


def apply_redaction(text, entities, method="pseudonym"):
    for original, tag in entities.items():
        label = tag.strip("[]")
        if method == "tag":
            replacement = tag
        elif method == "pseudonym":
            replacement = FAKE_GENERATORS.get(label, lambda: "[REDACTED]")()
        else:
            replacement = "[REDACTED]"
        text = text.replace(original, replacement)
    return text
