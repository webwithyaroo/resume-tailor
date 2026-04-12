def display(missing: dict) -> str:
    """
    Display the missing, extra, matched keywords and phrases in a user-friendly format.
    """

    extra_keywords_html = ""
    extra_phrases_html = ""
    if missing['extra_keywords']:
        extra_keywords_html = f"""
        <h2>Extra keywords in resume:</h2>
        <ul>
            {"".join(f"<li>{keyword}</li>" for keyword in missing['extra_keywords'])}
        </ul>"""

    if missing['extra_phrases']:
        extra_phrases_html = f"""
        <h2>Extra phrases in resume:</h2>
        <ul>
            {"".join(f"<li>{phrase}</li>" for phrase in missing['extra_phrases'])}
        </ul>"""

    missing_keywords_html = ""
    missing_phrases_html = ""

    if missing['missing_keywords']:
        missing_keywords_html = f"""
        <h2>Missing keywords:</h2>
        <ul>
            {"".join(f"<li>{keyword}</li>" for keyword in missing['missing_keywords'])}
        </ul>"""

    if missing['missing_phrases']:
        missing_phrases_html = f"""
        <h2>Missing phrases:</h2>
        <ul>
            {"".join(f"<li>{phrase}</li>" for phrase in missing['missing_phrases'])}
        </ul>"""

    matched_keywords_html = ""
    matched_phrases_html = ""

    if missing['matched_keywords']:
        matched_keywords_html = f"""
        <h2>Matched keywords:</h2>
        <ul>
            {"".join(f"<li>{keyword}</li>" for keyword in missing['matched_keywords'])}
        </ul>"""

    if missing['matched_phrases']:
        matched_phrases_html = f"""
        <h2>Matched phrases:</h2>
        <ul>
            {"".join(f"<li>{phrase}</li>" for phrase in missing['matched_phrases'])}
        </ul>"""

    if not missing['missing_keywords'] and not missing['missing_phrases']:
        return "<h2>Congratulations! Your resume matches the job description perfectly.</h2>"

    return extra_keywords_html + extra_phrases_html + missing_keywords_html + missing_phrases_html + matched_keywords_html + matched_phrases_html
