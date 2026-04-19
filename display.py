def _suggestion_for(keyword: str) -> str:
    suggestion_map = {
        "docker": "Add to Skills or mention in a project",
        "ci/cd": "Add deployment or pipeline experience",
        "kubernetes": "Add orchestration experience if you have it",
        "aws": "Mention specific cloud services you have used",
        "azure": "Mention specific cloud services you have used",
        "gcp": "Mention specific cloud services you have used",
        "design": "Mention system or API design in a project",
        "engineer": "Focus on role-specific skills instead of the title",
        "communication": "Show communication through teamwork or stakeholder work",
        "team": "Show collaboration with teammates to deliver a feature or solve an issue",
        "teamwork": "Show collaboration (e.g., worked with 3 engineers to deliver a feature)",
        "testing": "Mention unit, integration, or end-to-end testing",
        "cloud": "Name the specific cloud platform or service you used",
        "python": "Add a Python project, API, automation script, or data task",
        "automation": "Mention a workflow you automated, such as testing or deployment",
        "deployment": "Describe a deployment pipeline, release flow, or production rollout",
        "debugging": "Show how you diagnosed and fixed issues in a real project",
        "debug": "Show how you diagnosed and fixed issues in a real project",
        "system design": "Add an example of designing an API, service, or scalable workflow",
        "agile": "Reference sprint planning, standups, or iterative delivery",
        "bachelor": "Mention your degree if the role requires one",
        "degree": "Mention your degree if the role requires one",
        "bachelors_degree": "Mention your degree if the role requires one",
    }
    return suggestion_map.get(keyword.lower(), "Tie it to a specific skill, project, or outcome")


def _pretty_term(term: str) -> str:
    exact = {
        "ci/cd": "CI/CD",
        "cicd": "CI/CD",
        "aws": "AWS",
        "gcp": "GCP",
        "ml": "ML",
        "api": "API",
        "debug": "Debugging",
    }
    lower = term.lower()
    if lower in exact:
        return exact[lower]
    return term.title()


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


def _render_requirement_gaps(items: list[dict]) -> str:
    if not items:
        return "<li>No explicit requirement gaps detected.</li>"

    return "".join(
        f"<li>{item.get('label', _pretty_term(item['term']))} → {_suggestion_for(item['term'])}</li>"
        for item in items[:5]
    )


def _render_missing_by_category(items: list[dict], category: str, limit: int = 5) -> str:
    selected = [item for item in items if item.get("category") == category][:limit]
    if not selected:
        return "<li>No high-impact gaps found.</li>"

    return "".join(
        f"<li>{_pretty_term(item['term'])} - {_suggestion_for(item['term'])}</li>"
        for item in selected
    )


def _top_matched(items: list[dict], limit: int = 5) -> list[dict]:
    preferred_order = {"TECH": 0, "WORKFLOW": 1, "SOFT": 2, "EDUCATION": 3, "OTHER": 4}
    return sorted(
        items,
        key=lambda x: (preferred_order.get(x.get("category", "OTHER"), 4), -x.get("priority", 0), x.get("term", "")),
    )[:limit]


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
    requirement_gaps = resume_job_data.get("requirement_gaps", [])

    missing_technical_html = _render_missing_by_category(missing_ranked, "TECH", limit=5)
    missing_workflow_html = _render_missing_by_category(missing_ranked, "WORKFLOW", limit=5)
    missing_soft_html = _render_missing_by_category(missing_ranked, "SOFT", limit=5)

    matched_top = _top_matched(matched_ranked, limit=5)

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

    <h3>🔴 Missing Technical Skills:</h3>
    <ul>
        {missing_technical_html}
    </ul>

    <h3>🟡 Missing Workflow Skills:</h3>
    <ul>
        {missing_workflow_html}
    </ul>

    <h3>🟡 Missing Soft Skills:</h3>
    <ul>
        {missing_soft_html}
    </ul>

    <h3>📌 Requirement Gaps:</h3>
    <ul>
        {_render_requirement_gaps(requirement_gaps)}
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
