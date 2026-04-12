def display(resume_job_data: dict) -> str:
    """
    Display the missing, extra, matched keywords and phrases in a user-friendly format.
    """

    extra_keywords_html = ""
    extra_phrases_html = ""
    if resume_job_data['extra_keywords']:
        extra_keywords_html = f"""
        <h2>Extra keywords in resume:</h2>
        <ul>
            {"".join(f"<li>{keyword}</li>" for keyword in resume_job_data['extra_keywords'])}
        </ul>"""

    if resume_job_data['extra_phrases']:
        extra_phrases_html = f"""
        <h2>Extra phrases in resume:</h2>
        <ul>
            {"".join(f"<li>{phrase}</li>" for phrase in resume_job_data['extra_phrases'])}
        </ul>"""

    missing_keywords_html = ""
    missing_phrases_html = ""

    if resume_job_data['missing_keywords']:
        missing_keywords_html = f"""
        <h2>Missing keywords:</h2>
        <ul>
            {"".join(f"<li>{keyword}</li>" for keyword in resume_job_data['missing_keywords'])}
        </ul>"""

    if resume_job_data['missing_phrases']:
        missing_phrases_html = f"""
        <h2>Missing phrases:</h2>
        <ul>
            {"".join(f"<li>{phrase}</li>" for phrase in resume_job_data['missing_phrases'])}
        </ul>"""

    matched_keywords_html = ""
    matched_phrases_html = ""

    if resume_job_data['matched_keywords']:
        matched_keywords_html = f"""
        <h2>Matched keywords:</h2>
        <ul>
            {"".join(f"<li>{keyword}</li>" for keyword in resume_job_data['matched_keywords'])}
        </ul>"""

    if resume_job_data['matched_phrases']:
        matched_phrases_html = f"""
        <h2>Matched phrases:</h2>
        <ul>
            {"".join(f"<li>{phrase}</li>" for phrase in resume_job_data['matched_phrases'])}
        </ul>"""

    if not resume_job_data['missing_keywords'] and not resume_job_data['missing_phrases']:
        return "<h2>Congratulations! Your resume matches the job description perfectly.</h2>"

    
    score = ""
    if resume_job_data['score'] > 0:
        score = f"<p>You matched {resume_job_data['matched_count']} out of {resume_job_data['total_required']} requirements. {resume_job_data['score']:.2f}%</p>"
        
    
    return extra_keywords_html + extra_phrases_html + missing_keywords_html + missing_phrases_html + matched_keywords_html + matched_phrases_html + score
