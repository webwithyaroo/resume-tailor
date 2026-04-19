def _suggestion_for(keyword: str) -> str:
    suggestion_map = {
        "docker": "Add to Skills or mention in a project",
        "agile": "Include experience working in agile environments",
        "ci/cd": "Add deployment or pipeline experience",
        "debugging": "Highlight debugging experience in projects",
        "system design": "Mention system-level thinking if applicable",
        "kubernetes": "Add orchestration experience if you have it",
        "aws": "Mention specific cloud services you have used",
        "azure": "Mention specific cloud services you have used",
        "gcp": "Mention specific cloud services you have used",
    }
    return suggestion_map.get(keyword.lower(), "Add this keyword to skills or achievement bullets")


def _build_summary(score: float, missing_count: int, matched_count: int) -> str:
    if score >= 80:
        return "Your resume strongly aligns with this role, with only a few gaps to close."
    if score >= 50:
        return "Your resume matches several core requirements but still misses some important items."
    if matched_count == 0:
        return "Your resume currently does not align with the key requirements for this role."
    if missing_count > matched_count:
        return "Your resume matches some core technical requirements but is missing several important skills and concepts expected for this role."
    return "Your resume has partial alignment with this role; strengthen it by adding missing keywords and clearer impact statements."


def _render_ignored_noise(ignored_noise: dict) -> str:
    items = []
    for source in ("resume", "job"):
        for entry in ignored_noise.get(source, []):
            word = entry.get("word", "").strip()
            reason = entry.get("reason", "filtered")
            if word:
                items.append((word, reason))

    # Deduplicate while preserving order.
    deduped = []
    seen = set()
    for word, reason in items:
        key = (word.lower(), reason.lower())
        if key in seen:
            continue
        seen.add(key)
        deduped.append((word, reason))

    top_items = deduped[:5]
    if not top_items:
        return "<li>No major noise tokens detected.</li>"

    return "".join(f"<li>{word} - {reason}</li>" for word, reason in top_items)


def display(resume_job_data: dict) -> str:
    """Display result in concise recruiter-style summary format."""
    missing_items = resume_job_data["missing_keywords"] + resume_job_data["missing_phrases"]
    matched_items = resume_job_data["matched_keywords"] + resume_job_data["matched_phrases"]

    missing_top = missing_items[:5]
    matched_top = matched_items[:5]

    missing_html = (
        "".join(
            f"<li>{item} - {_suggestion_for(item)}</li>"
            for item in missing_top
        )
        if missing_top
        else "<li>No critical missing keywords found.</li>"
    )

    matched_html = (
        "".join(f"<li>{item}</li>" for item in matched_top)
        if matched_top
        else "<li>No strong matches identified yet.</li>"
    )

    ignored_noise = resume_job_data.get("ignored_noise", {"resume": [], "job": []})
    ignored_html = _render_ignored_noise(ignored_noise)

    summary = _build_summary(
        resume_job_data.get("score", 0),
        len(missing_items),
        len(matched_items),
    )

    return f"""
    <h2>Match Score: {resume_job_data.get("score", 0):.2f}%</h2>
    <h3>Summary:</h3>
    <p>{summary}</p>

    <h3>Missing (Top 5 only):</h3>
    <ul>
        {missing_html}
    </ul>

    <h3>Matched (Top 5):</h3>
    <ul>
        {matched_html}
    </ul>

    <h3>Ignored/Noise:</h3>
    <ul>
        {ignored_html}
    </ul>
    """
