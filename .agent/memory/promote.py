"""Detect recurring patterns and promote high-salience entries to semantic memory."""
import os, datetime
from collections import defaultdict
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "harness"))
from salience import salience_score


def find_recurring_patterns(entries):
    """Cluster by (skill, action-prefix); entries appearing 2+ times get boosted."""
    groups = defaultdict(list)
    for e in entries:
        key = f"{e.get('skill','general')}::{e.get('action','')[:50]}"
        groups[key].append(e)

    recurring = {}
    for key, group in groups.items():
        if len(group) < 2:
            continue
        best = max(group, key=salience_score)
        best["recurrence_count"] = len(group)
        best["_salience"] = salience_score(best)
        recurring[key] = best
    return recurring


def promote_to_semantic(entries, semantic_dir):
    """Append lessons that aren't already present. Returns count promoted."""
    if not entries:
        return 0
    lessons_path = os.path.join(semantic_dir, "LESSONS.md")
    existing = open(lessons_path).read() if os.path.exists(lessons_path) else ""
    new = []
    for e in entries:
        line = f"- {e.get('reflection') or e.get('action') or 'unknown'}"
        if line.strip() and line not in existing:
            new.append(line)
    if not new:
        return 0
    os.makedirs(semantic_dir, exist_ok=True)
    with open(lessons_path, "a") as f:
        f.write(f"\n## Auto-promoted {datetime.date.today().isoformat()}\n")
        for line in new:
            f.write(line + "\n")
    return len(new)
