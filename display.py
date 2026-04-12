def display(missing: dict) -> str:
    """
    Display the missing keywords and phrases in a user-friendly format.
    """
    
    missing['missing_keywords'] = missing.get('missing_keywords', [])
    missing['missing_phrases'] = missing.get('missing_phrases', [])
    
    
    
    return f"""
    <h1>Missing Keywords and Phrases</h1>
    <h2>Missing Keywords:</h2>
    <ul>
        {"".join(f"<li>{keyword}</li>" for keyword in missing['missing_keywords'])}
    </ul>
    <h2>Missing Phrases:</h2>
    <ul>
        {"".join(f"<li>{phrase}</li>" for phrase in missing['missing_phrases'])}
    </ul>
    """