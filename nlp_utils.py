import re
import subprocess
import sys

import spacy


PHRASE_LIST = [
    "rest api",
    "machine learning",
    "system design",
    "software development",
    "cloud computing",
    "ci/cd",
]

_NOISE_WORDS = {
    "template",
    "lorem",
    "ipsum",
    "january",
    "february",
    "march",
    "april",
    "may",
    "june",
    "july",
    "august",
    "september",
    "october",
    "november",
    "december",
}

_ALLOWED_POS = {"NOUN", "PROPN", "ADJ", "VERB"}
_BLOCKED_ENTITY_TYPES = {
    "PERSON",
    "GPE",
    "LOC",
    "DATE",
    "TIME",
    "MONEY",
    "PERCENT",
    "CARDINAL",
    "ORDINAL",
}


def _load_nlp():
    try:
        return spacy.load("en_core_web_sm")
    except OSError:
        subprocess.check_call([sys.executable, "-m", "spacy", "download", "en_core_web_sm"])
        return spacy.load("en_core_web_sm")


nlp = _load_nlp()


def _normalize_token_text(text: str) -> str:
    normalized = text.strip().lower()
    normalized = normalized.replace("/", "")
    normalized = re.sub(r"[^a-z0-9+#.-]", "", normalized)
    return normalized


def extract_keywords(text: str) -> dict:
    normalized_text = text.lower()
    phrases = [phrase for phrase in PHRASE_LIST if phrase in normalized_text]
    phrase_words = {word for phrase in phrases for word in phrase.split()}

    doc = nlp(text)
    keywords = []
    ignored_noise = []
    seen = set()

    for token in doc:
        token_text = _normalize_token_text(token.text)
        lemma_text = _normalize_token_text(token.lemma_)

        if not token_text:
            continue

        if token.is_space or token.is_punct:
            continue

        if token.is_stop:
            ignored_noise.append({"word": token.text, "reason": "stopword"})
            continue

        if token.ent_type_ in _BLOCKED_ENTITY_TYPES:
            ignored_noise.append({"word": token.text, "reason": "personal identifier or location/date"})
            continue

        if token.like_num:
            ignored_noise.append({"word": token.text, "reason": "numeric token"})
            continue

        if token_text in _NOISE_WORDS:
            ignored_noise.append({"word": token.text, "reason": "generic template/noise word"})
            continue

        if token_text in phrase_words or lemma_text in phrase_words:
            continue

        if token.pos_ not in _ALLOWED_POS:
            ignored_noise.append({"word": token.text, "reason": "low-signal part-of-speech"})
            continue

        candidate = lemma_text or token_text
        if len(candidate) < 3:
            ignored_noise.append({"word": token.text, "reason": "too short"})
            continue

        if not re.search(r"[a-z]", candidate):
            ignored_noise.append({"word": token.text, "reason": "non-alphabetic token"})
            continue

        if candidate in seen:
            continue

        seen.add(candidate)
        keywords.append(candidate)

    return {
        "keywords": keywords,
        "phrases": sorted(set(phrases)),
        "ignored_noise": ignored_noise,
    }