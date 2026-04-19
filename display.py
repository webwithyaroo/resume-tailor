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
        "design": "Mention system or API design in a project",
        "engineer": "Focus on role-specific skills instead of the title",
        "communication": "Show communication through teamwork or stakeholder work",
        "team": "Use team collaboration or cross-functional examples",
        "testing": "Mention unit, integration, or end-to-end testing",
        "cloud": "Name the specific cloud platform or service you used",
    }
    return suggestion_map.get(keyword.lower(), "Connect it to a concrete skill, project, or outcome")


def _pretty_term(term: str) -> str:
    exact = {
        "ci/cd": "CI/CD",
        "cicd": "CI/CD",
        "aws": "AWS",
        "gcp": "GCP",
        "ml": "ML",
        "api": "API",
    }
    lower = term.lower()
    if lower in exact:
        return exact[lower]
    return term.title()


def _reason_from_weight(weight: int) -> str:
    if weight >= 3:
        return "required multiple times"
    if weight == 2:
        return "mentioned more than once"
    return "required in this role"


def _build_summary(score: float, missing_count: int, matched_count: int) -> str:
    if score >= 80:
        return "Your resume strongly aligns with this role, with only a few gaps to close."
    if score >= 50:
        return "Your resume matches several core requirements but still misses some important items."
    if matched_count == 0:
        return "Your resume currently does not align with the key requirements for this role."
    if missing_count > matched_count:
        return "Your resume shows some alignment with the role but lacks several key technical and workflow-related requirements."
    return "Your resume has partial alignment with this role; strengthen it with more specific technical impact and role-aligned terms."


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

    return "".join(f"<li>{word.title()} ({reason})</li>" for word, reason in top_items)


def _filter_matched_items(items: list[dict]) -> list[dict]:
    blocked = {
        "design",
        "engineer",
        "solution",
        "solutions",
        "innovations",
        "innovation",
        "inc",
        "ltd",
        "corp",
        "team",
        "problem",
        "solve",
        "software",
        "development",
    }
    meaningful = []
    for item in items:
        normalized = item["term"].lower().strip()
        if normalized in blocked:
            continue
        if item["category"] == "OTHER" and len(normalized) < 4:
            continue
        meaningful.append(item)
    return meaningful


def display(resume_job_data: dict) -> str:
    """Display result in concise recruiter-style summary format."""
    missing_ranked = _filter_matched_items(resume_job_data.get("ranked_missing", []))
    matched_ranked = _filter_matched_items(resume_job_data.get("ranked_matched", []))

    missing_top = missing_ranked[:5]
    matched_top = matched_ranked[:5]

    missing_html = (
        "".join(
            f"<li>{_pretty_term(item['term'])} - {_suggestion_for(item['term'])} ({_reason_from_weight(item['weight'])})</li>"
            for item in missing_top
        )
        if missing_top
        else "<li>No critical missing keywords found.</li>"
    )

    matched_html = (
        "".join(f"<li>{_pretty_term(item['term'])}</li>" for item in matched_top)
        if matched_top
        else "<li>No strong matches identified yet.</li>"
    )

    ignored_noise = resume_job_data.get("ignored_noise", {"resume": [], "job": []})
    ignored_html = _render_ignored_noise(ignored_noise)

    summary = _build_summary(
        resume_job_data.get("score", 0),
        len(missing_ranked),
        len(matched_ranked),
    )

    return f"""
    <h2>Match Score: {resume_job_data.get("score", 0):.2f}%</h2>
    <h3>Summary:</h3>
    <p>{summary}</p>

    <h3>🔴 Top Missing (High Impact):</h3>
    <ul>
        {missing_html}
    </ul>

    <h3>🟢 Matched:</h3>
    <ul>
        {matched_html}
    </ul>

    <h3>⚪ Ignored (Non-relevant):</h3>
    <ul>
        {ignored_html}
    </ul>
    """
