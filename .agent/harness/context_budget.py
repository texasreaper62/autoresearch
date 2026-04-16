"""Assemble context from memory + matched skills + protocols within a token budget."""
import json, os
from salience import salience_score

ROOT = os.path.join(os.path.dirname(__file__), "..")


def _read(path, limit=None):
    full = os.path.join(ROOT, path)
    if not os.path.exists(full):
        return ""
    content = open(full).read()
    return content[:limit] if limit else content


def _tokens(text):
    return len(text) // 4


def _top_episodes(k=5):
    path = os.path.join(ROOT, "memory/episodic/AGENT_LEARNINGS.jsonl")
    if not os.path.exists(path):
        return ""
    entries = []
    for line in open(path):
        line = line.strip()
        if not line:
            continue
        try:
            entries.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    entries.sort(key=salience_score, reverse=True)
    top = entries[:k]
    return "\n".join(
        f"- [{e.get('timestamp','')[:10]}] {e.get('action','')}: "
        f"{e.get('reflection', e.get('detail',''))}"
        for e in top
    )


def build_context(user_input: str, budget: int = 88000):
    """Returns (context_string, tokens_used). Lean by design."""
    from skill_loader import progressive_load  # lazy to avoid cycles
    parts, used = [], 0

    # always load: personal preferences + live workspace
    for rel in ("memory/personal/PREFERENCES.md", "memory/working/WORKSPACE.md"):
        text = _read(rel)
        if text:
            parts.append(f"# {rel}\n{text}")
            used += _tokens(text)

    # semantic lessons, truncated
    lessons = _read("memory/semantic/LESSONS.md", limit=8000)
    if lessons:
        parts.append(f"# LESSONS\n{lessons}")
        used += _tokens(lessons)

    # top episodic by salience
    episodes = _top_episodes(k=5)
    if episodes:
        parts.append(f"# RECENT EPISODES (top by salience)\n{episodes}")
        used += _tokens(episodes)

    # matched skills only
    try:
        skills = progressive_load(user_input)
    except Exception:
        skills = []
    for s in skills:
        block = f"## Skill: {s['name']}\n{s['content']}"
        t = _tokens(block)
        if used + t < budget:
            parts.append(block)
            used += t

    # permissions always last, small, safety-critical
    perms = _read("protocols/permissions.md")
    if perms:
        parts.append(f"# PERMISSIONS\n{perms}")
        used += _tokens(perms)

    return "\n\n---\n\n".join(parts), used
