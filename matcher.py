def match_resume_to_job(resume_keywords, resume_phrases, job_keywords, job_phrases) -> dict:
    """
    Compares the keywords from the resume and job description and returns the missing keywords.

    Parameters:
    resume_keywords (list): A list of keywords extracted from the resume.
    job_keywords (list): A list of keywords extracted from the job description.

    Returns:
    dict: A dictionary containing the missing keywords from the resume that are present in the job description.
    """
    
    
    
    # comparing the resume and job description keywords
    missing_keywords = set(job_keywords) - set(resume_keywords)
    missing_phrases = set(job_phrases) - set(resume_phrases)

    structured_missing_keywords = sorted(missing_keywords)
    structured_missing_phrases = sorted(missing_phrases)

    # extracting the matching keywords and phrases from the resume and job
    matched_keywords = set(resume_keywords) & set(job_keywords)
    matched_phrases = set(resume_phrases) & set(job_phrases)

    structured_matched_keywords = sorted(matched_keywords)
    structured_matched_phrases = sorted(matched_phrases)

    # extracting the extra keywords and phrases from the resume that are not in the job description
    extra_keywords = set(resume_keywords) - set(job_keywords)
    extra_phrases = set(resume_phrases) - set(job_phrases)

    structured_extra_keywords = sorted(extra_keywords)
    structured_extra_phrases = sorted(extra_phrases)

    
    
    # Score calculation
    total_required = len(job_keywords) + len(job_phrases)
    total_matched = len(matched_keywords) + len(matched_phrases)
    
    
    total_score = (total_matched / total_required) * 100 if total_required > 0 else 0
    
    
    
    
    
    # structuring the result in a dictionary format
    result = {"missing_keywords": structured_missing_keywords, 
              "missing_phrases": structured_missing_phrases, 
              "extra_keywords": structured_extra_keywords,
              "extra_phrases": structured_extra_phrases, 
              "matched_keywords": structured_matched_keywords, 
              "matched_phrases": structured_matched_phrases,
              "score": total_score,
              "matched_count": total_matched,
              "total_required": total_required}

    return result
