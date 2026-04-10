def match_resume_to_job(resume_keywords, job_keywords):
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
    
    # converting sets to lists for better display
    converting_missing_keywords = [*missing_keywords]
    
    return converting_missing_keywords