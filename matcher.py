def match_resume_to_job(job_keywords, resume_keywords, job_phrases, resume_phrases) -> dict:
    """
    Compares the keywords from the resume and job description and returns the missing keywords.

    Parameters:
    resume_keywords (list): A list of keywords extracted from the resume.
    job_keywords (list): A list of keywords extracted from the job description.

    Returns:
    dict: A dictionary containing the missing keywords from the resume that are present in the job description.
    """

    # extracting the matching keywords and phrases from the resume and job
    matched_keywords = set(resume_keywords) & set(job_keywords)
    matched_phrases = set(resume_phrases) & set(job_phrases)

    structured_matched_keywords = [*matched_keywords]
    structured_matched_phrases = [*matched_phrases]

    # extracting the extra keywords and phrases from the resume that are not in the job description
    extra_keywords = set(resume_keywords) - set(job_keywords)
    extra_phrases = set(resume_phrases) - set(job_phrases)

    structured_extra_keywords = [*extra_keywords]
    structured_extra_phrases = [*extra_phrases]

    # comparing the resume and job description keywords
    missing_keywords = set(job_keywords) - set(resume_keywords)
    missing_phrases = set(job_phrases) - set(resume_phrases)

    structured_missing_keywords = [*missing_keywords]
    structured_missing_phrases = [*missing_phrases]

    result = {"missing_keywords": structured_missing_keywords, "missing_phrases": structured_missing_phrases, "extra_keywords": structured_extra_keywords,
              "extra_phrases": structured_extra_phrases, "matched_keywords": structured_matched_keywords, "matched_phrases": structured_matched_phrases}

    return result
