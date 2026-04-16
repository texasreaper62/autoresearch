"""Failures are learning. High pain score + rewrite flag after repeat offenses."""
import json, datetime, os

ROOT = os.path.join(os.path.dirname(__file__), "..", "..")
EPISODIC = os.path.join(ROOT, "memory/episodic/AGENT_LEARNINGS.jsonl")
FAILURE_THRESHOLD = 3
WINDOW_DAYS = 14


def _count_recent_failures(skill_name):
    if not os.path.exists(EPISODIC):
        return 0
    cutoff = datetime.datetime.now() - datetime.timedelta(days=WINDOW_DAYS)
    count = 0
    for line in open(EPISODIC):
        line = line.strip()
        if not line:
            continue
        try:
            e = json.loads(line)
        except json.JSONDecodeError:
            continue
        if e.get("skill") != skill_name or e.get("result") != "failure":
            continue
        try:
            if datetime.datetime.fromisoformat(e["timestamp"]) > cutoff:
                count += 1
        except (KeyError, ValueError):
            continue
    return count


def on_failure(skill_name, action, error, context=""):
    entry = {
        "timestamp": datetime.datetime.now().isoformat(),
        "skill": skill_name,
        "action": action[:200],
        "result": "failure",
        "detail": str(error)[:500],
        "pain_score": 8,
        "importance": 7,
        "reflection": f"FAILURE in {skill_name}: {type(error).__name__}: "
                      f"{str(error)[:200]}",
        "context": context[:300],
    }
    recent = _count_recent_failures(skill_name)
    if recent >= FAILURE_THRESHOLD:
        entry["reflection"] += (
            f" | THIS SKILL HAS FAILED {recent} TIMES IN {WINDOW_DAYS}d. "
            f"Flag for rewrite."
        )
        entry["pain_score"] = 10
    os.makedirs(os.path.dirname(EPISODIC), exist_ok=True)
    with open(EPISODIC, "a") as f:
        f.write(json.dumps(entry) + "\n")
    return entry
