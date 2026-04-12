def match_resume_to_job(job_keywords, resume_keywords, job_phrases, resume_phrases) -> dict:
    """
    Compares the keywords from the resume and job description and returns the missing keywords.
    
    Parameters:
    resume_keywords (list): A list of keywords extracted from the resume.
    job_keywords (list): A list of keywords extracted from the job description.
    
    Returns:
    dict: A dictionary containing the missing keywords from the resume that are present in the job description.
    """
    
    
    # extracting the keywords and phrases from the resume and job description
    
    # comparing the resume and job description keywords
    missing_keywords = set(job_keywords) - set(resume_keywords)
    
    # comparing the resume and job description phrases
    missing_phrases = set(job_phrases) - set(resume_phrases)
    
    # converting sets to lists for better display
    converting_missing_keywords = [*missing_keywords]
    converting_missing_phrases = [*missing_phrases]
    
    result = {"keywords": converting_missing_keywords, "phrases": converting_missing_phrases}
    
    return result