from nlp_utils import normalize_term


def match_resume_to_job(
    resume_keywords,
    resume_phrases,
    job_keywords,
    job_phrases,
    resume_ignored_noise=None,
    job_ignored_noise=None,
    resume_keyword_counts=None,
    job_keyword_counts=None,
    resume_phrase_counts=None,
    job_phrase_counts=None,
) -> dict:
    """
    Compares the keywords from the resume and job description and returns the missing keywords.

    Parameters:
    resume_keywords (list): A list of keywords extracted from the resume.
    job_keywords (list): A list of keywords extracted from the job description.

    Returns:
    dict: A dictionary containing the missing keywords from the resume that are present in the job description.
    """
    
    
    
    resume_keyword_counts = resume_keyword_counts or {}
    job_keyword_counts = job_keyword_counts or {}
    resume_phrase_counts = resume_phrase_counts or {}
    job_phrase_counts = job_phrase_counts or {}

    def _normalize(term: str) -> str:
        return normalize_term(term)

    def _is_meaningful(term: str, category: str) -> bool:
        normalized = _normalize(term)

        stop_terms = {
            "design",
            "engineer",
            "solution",
            "solutions",
            "innovation",
            "innovations",
            "inc",
            "ltd",
            "corp",
            "company",
            "role",
            "position",
            "experience",
            "need",
            "needs",
            "looking",
            "seeking",
            "worked",
            "work",
            "using",
            "used",
            "built",
        }

        if normalized in stop_terms:
            return False

        if category == "OTHER" and len(normalized) < 4:
            return False

        return True

    def _is_requirement(term: str) -> bool:
        normalized = _normalize(term)
        requirement_terms = {
            "bachelor",
            "degree",
            "masters",
            "phd",
            "certification",
            "diploma",
            "university",
        }
        return normalized in requirement_terms

    def term_weight(term: str) -> int:
        normalized = _normalize(term)
        return job_phrase_counts.get(normalized, job_keyword_counts.get(normalized, 1))

    def categorize(term: str) -> str:
        tech_terms = {
            "python", "docker", "kubernetes", "aws", "azure", "gcp", "ci/cd", "cicd",
            "git", "rest api", "machine learning", "cloud", "deployment", "testing",
            "debugging", "system design", "software development", "microservices",
        }
        soft_terms = {
            "communication", "teamwork", "leadership", "collaboration", "stakeholder",
            "ownership", "mentoring", "adaptability", "agile",
        }
        education_terms = {
            "bachelor", "masters", "degree", "phd", "university", "certification", "diploma",
        }

        normalized = _normalize(term)
        if normalized in tech_terms:
            return "TECH"
        if normalized in soft_terms:
            return "SOFT"
        if normalized in education_terms:
            return "EDUCATION"
        return "OTHER"

    def prioritize(items: list[str]) -> list[dict]:
        ranked = []
        for item in items:
            category = categorize(item)
            if not _is_meaningful(item, category):
                continue
            ranked.append(
                {
                    "term": item,
                    "weight": term_weight(item),
                    "category": category,
                }
            )
        return sorted(ranked, key=lambda x: (-x["weight"], x["category"], x["term"]))

    def _canonical_map(items, counts=None):
        canonical = {}
        counts = counts or {}
        for item in items:
            normalized = _normalize(item)
            if not normalized:
                continue
            if normalized not in canonical:
                canonical[normalized] = item
            else:
                existing = canonical[normalized]
                if len(item) > len(existing):
                    canonical[normalized] = item
        return canonical

    def _validated_split(job_items, resume_items):
        job_set = {_normalize(item) for item in job_items if _normalize(item)}
        resume_set = {_normalize(item) for item in resume_items if _normalize(item)}
        missing = sorted(job_set - resume_set)
        matched = sorted(job_set & resume_set)
        return missing, matched

    resume_keyword_map = _canonical_map(resume_keywords, resume_keyword_counts)
    job_keyword_map = _canonical_map(job_keywords, job_keyword_counts)
    resume_phrase_map = _canonical_map(resume_phrases, resume_phrase_counts)
    job_phrase_map = _canonical_map(job_phrases, job_phrase_counts)

    resume_term_set = set(resume_keyword_map) | set(resume_phrase_map)
    job_term_set = set(job_keyword_map) | set(job_phrase_map)

    # comparing the resume and job description keywords
    missing_terms = job_term_set - resume_term_set
    matched_terms = job_term_set & resume_term_set

    validated_missing_terms, validated_matched_terms = _validated_split(job_term_set, resume_term_set)
    missing_terms = set(validated_missing_terms)
    matched_terms = set(validated_matched_terms)

    missing_keywords = [job_keyword_map[item] for item in missing_terms if item in job_keyword_map]
    missing_phrases = [job_phrase_map[item] for item in missing_terms if item in job_phrase_map]

    structured_missing_keywords = sorted(missing_keywords)
    structured_missing_phrases = sorted(missing_phrases)

    # extracting the matching keywords and phrases from the resume and job
    matched_keywords = [job_keyword_map[item] for item in matched_terms if item in job_keyword_map]
    matched_phrases = [job_phrase_map[item] for item in matched_terms if item in job_phrase_map]

    structured_matched_keywords = sorted(matched_keywords)
    structured_matched_phrases = sorted(matched_phrases)

    # extracting the extra keywords and phrases from the resume that are not in the job description
    extra_keywords = set(resume_keywords) - set(job_keywords)
    extra_phrases = set(resume_phrases) - set(job_phrases)

    structured_extra_keywords = sorted(extra_keywords)
    structured_extra_phrases = sorted(extra_phrases)

    
    
    ranked_missing = prioritize(structured_missing_keywords + structured_missing_phrases)
    ranked_matched = prioritize(structured_matched_keywords + structured_matched_phrases)

    requirement_gaps = []
    for item in ranked_missing:
        if _is_requirement(item["term"]):
            requirement_gaps.append(item)
    ranked_missing = [item for item in ranked_missing if item not in requirement_gaps]

    # Weighted score calculation
    total_required = sum(job_keyword_counts.get(_normalize(k), 1) for k in set(job_keywords)) + sum(
        job_phrase_counts.get(_normalize(p), 1) for p in set(job_phrases)
    )
    total_matched = sum(job_keyword_counts.get(_normalize(k), 1) for k in matched_keywords) + sum(
        job_phrase_counts.get(_normalize(p), 1) for p in matched_phrases
    )
    
    
    total_score = (total_matched / total_required) * 100 if total_required > 0 else 0
    
    
    
    
    
    # structuring the result in a dictionary format
    result = {
        "missing_keywords": structured_missing_keywords,
        "missing_phrases": structured_missing_phrases,
        "extra_keywords": structured_extra_keywords,
        "extra_phrases": structured_extra_phrases,
        "matched_keywords": structured_matched_keywords,
        "matched_phrases": structured_matched_phrases,
        "score": total_score,
        "matched_count": total_matched,
        "total_required": total_required,
        "ranked_missing": ranked_missing,
        "ranked_matched": ranked_matched,
        "requirement_gaps": requirement_gaps,
        "ignored_noise": {
            "resume": resume_ignored_noise or [],
            "job": job_ignored_noise or [],
        },
    }

    return result
