import re
import subprocess
import sys
from collections import Counter

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
    "experience",
    "need",
    "needs",
    "looking",
    "seeking",
    "wanted",
    "build",
    "built",
    "work",
    "worked",
    "using",
    "use",
    "used",
    "role",
    "position",
    "job",
    "task",
    "tasks",
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

_COMPANY_SUFFIXES = {
    "inc",
    "inc.",
    "ltd",
    "ltd.",
    "corp",
    "corp.",
    "llc",
    "co",
    "co.",
    "company",
    "companies",
    "group",
    "holdings",
    "solutions",
    "innovations",
    "technologies",
    "systems",
}

_JOB_TITLE_WORDS = {
    "engineer",
    "developer",
    "analyst",
    "manager",
    "specialist",
    "architect",
    "consultant",
    "director",
    "lead",
    "principal",
    "head",
    "associate",
    "intern",
    "administrator",
    "coordinator",
    "officer",
    "executive",
    "designer",
    "scientist",
    "researcher",
}

_TITLE_MODIFIERS = {
    "software",
    "senior",
    "junior",
    "principal",
    "staff",
    "full",
    "backend",
    "frontend",
    "data",
    "product",
    "cloud",
    "platform",
    "solutions",
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

_ENTITY_REASON_MAP = {
    "PERSON": "name",
    "GPE": "location",
    "LOC": "location",
    "DATE": "date",
    "TIME": "date",
    "MONEY": "numeric/detail",
    "PERCENT": "numeric/detail",
    "CARDINAL": "numeric/detail",
    "ORDINAL": "numeric/detail",
}

_ROLE_CHUNKS = {
    "software engineer",
    "data engineer",
    "devops engineer",
    "product manager",
    "project manager",
    "business analyst",
    "systems engineer",
    "solution architect",
    "technical lead",
    "team lead",
    "cloud engineer",
    "machine learning engineer",
    "qa engineer",
}

DOMAIN_TERMS = {
    "python",
    "docker",
    "kubernetes",
    "aws",
    "azure",
    "gcp",
    "ci/cd",
    "cicd",
    "cloud",
    "deployment",
    "testing",
    "debugging",
    "system design",
    "software development",
    "microservices",
    "automation",
    "api",
    "rest api",
    "machine learning",
    "agile",
    "scrum",
    "pipeline",
    "devops",
    "git",
    "linux",
    "sql",
    "javascript",
    "typescript",
    "react",
    "node",
    "flask",
    "fastapi",
    "communication",
    "teamwork",
    "collaboration",
    "leadership",
    "bachelor",
    "degree",
    "certification",
    "university",
}

GENERIC_TERMS = {
    "apply",
    "analyze",
    "help",
    "join",
    "manage",
    "work",
    "build",
    "use",
    "make",
    "create",
    "develop",
    "support",
    "task",
    "responsibility",
    "experience",
    "skill",
    "skills",
    "solution",
    "solutions",
    "innovative",
    "modern",
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


def normalize_term(text: str) -> str:
    return _normalize_token_text(text)


def is_too_generic(term: str, frequency: int, context_hits: int, category: str) -> bool:
    normalized = normalize_term(term)

    if normalized in DOMAIN_TERMS:
        return False

    if normalized in GENERIC_TERMS:
        return True

    if category == "OTHER" and len(normalized) < 4:
        return True

    if frequency >= 2 and context_hits > 0:
        return False

    if frequency == 1 and context_hits == 0:
        return True

    return False


def _chunk_is_company(chunk) -> bool:
    chunk_text = chunk.text.lower().strip()
    if any(suffix in chunk_text for suffix in _COMPANY_SUFFIXES):
        return True
    if chunk.root.ent_type_ == "ORG":
        return True
    return False


def _chunk_is_job_title(chunk) -> bool:
    chunk_text = chunk.text.lower().strip()
    if chunk_text in _ROLE_CHUNKS:
        return True

    chunk_words = {_normalize_token_text(token.text) for token in chunk if _normalize_token_text(token.text)}
    if chunk_words & _JOB_TITLE_WORDS and chunk_words & _TITLE_MODIFIERS:
        return True

    if _normalize_token_text(chunk.root.lemma_) in _JOB_TITLE_WORDS:
        return True

    return False


def _collect_noise_spans(doc):
    noise_spans = []

    for ent in doc.ents:
        if ent.label_ == "ORG":
            if any(_normalize_token_text(token.text) in _COMPANY_SUFFIXES for token in ent):
                noise_spans.append((ent.start, ent.end, "company name"))
            else:
                noise_spans.append((ent.start, ent.end, "organization"))
        elif ent.label_ in _BLOCKED_ENTITY_TYPES:
            noise_spans.append((ent.start, ent.end, _ENTITY_REASON_MAP.get(ent.label_, "non-relevant entity")))

    for chunk in doc.noun_chunks:
        if _chunk_is_company(chunk):
            noise_spans.append((chunk.start, chunk.end, "company suffix or organization"))
        elif _chunk_is_job_title(chunk):
            noise_spans.append((chunk.start, chunk.end, "job title"))

    return noise_spans


def extract_keywords(text: str) -> dict:
    normalized_text = text.lower()
    phrase_counts = {
        phrase: normalized_text.count(phrase)
        for phrase in PHRASE_LIST
        if normalized_text.count(phrase) > 0
    }
    phrases = sorted(phrase_counts.keys())
    phrase_words = {word for phrase in phrases for word in phrase.split()}

    doc = nlp(text)
    keywords = []
    keyword_counts = Counter()
    ignored_noise = []
    seen = set()
    noise_spans = _collect_noise_spans(doc)

    span_reasons = {}
    for start, end, reason in noise_spans:
        for index in range(start, end):
            span_reasons[index] = reason

    for token in doc:
        token_text = _normalize_token_text(token.text)
        lemma_text = _normalize_token_text(token.lemma_)

        if not token_text:
            continue

        if token.is_space or token.is_punct:
            continue

        if token.i in span_reasons:
            ignored_noise.append({"word": token.text, "reason": span_reasons[token.i]})
            continue

        if token.is_stop:
            ignored_noise.append({"word": token.text, "reason": "stopword"})
            continue

        if token.ent_type_ in _BLOCKED_ENTITY_TYPES:
            ignored_noise.append(
                {
                    "word": token.text,
                    "reason": _ENTITY_REASON_MAP.get(token.ent_type_, "personal identifier or location/date"),
                }
            )
            continue

        if token.like_num:
            ignored_noise.append({"word": token.text, "reason": "numeric token"})
            continue

        if token_text in _NOISE_WORDS:
            ignored_noise.append({"word": token.text, "reason": "generic template/noise word"})
            continue

        if token_text in _COMPANY_SUFFIXES:
            ignored_noise.append({"word": token.text, "reason": "company suffix"})
            continue

        if token_text in _JOB_TITLE_WORDS:
            ignored_noise.append({"word": token.text, "reason": "job title"})
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

        context_hits = 0
        for offset in (-2, -1, 1, 2):
            neighbor_index = token.i + offset
            if 0 <= neighbor_index < len(doc):
                neighbor = doc[neighbor_index]
                neighbor_text = _normalize_token_text(neighbor.text)
                neighbor_lemma = _normalize_token_text(neighbor.lemma_)
                if neighbor_text in DOMAIN_TERMS or neighbor_lemma in DOMAIN_TERMS:
                    context_hits += 1

        if is_too_generic(candidate, keyword_counts[candidate] + 1, context_hits, token.pos_):
            ignored_noise.append({"word": token.text, "reason": "too generic without domain context"})
            continue

        keyword_counts[candidate] += 1

        if candidate in seen:
            continue

        seen.add(candidate)
        keywords.append(candidate)

    return {
        "keywords": keywords,
        "keyword_counts": dict(keyword_counts),
        "phrases": phrases,
        "phrase_counts": phrase_counts,
        "ignored_noise": ignored_noise,
    }