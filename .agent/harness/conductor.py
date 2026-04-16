"""Thin conductor loop. Reads files, calls the model, logs. No reasoning here."""
import os, sys
from context_budget import build_context
from hooks.post_execution import log_execution

RESERVED = 40000
MAX_CTX = int(os.getenv("AGENT_MAX_CONTEXT", "128000"))


def _call_model(system, user):
    provider = os.getenv("AGENT_PROVIDER", "anthropic").lower()
    if provider == "anthropic":
        from anthropic import Anthropic
        c = Anthropic()
        r = c.messages.create(
            model=os.getenv("AGENT_MODEL", "claude-sonnet-4-5"),
            max_tokens=4096, temperature=0.3,
            system=system,
            messages=[{"role": "user", "content": user}],
        )
        return r.content[0].text
    if provider == "openai":
        from openai import OpenAI
        c = OpenAI()
        r = c.chat.completions.create(
            model=os.getenv("AGENT_MODEL", "gpt-4o"),
            messages=[{"role": "system", "content": system},
                      {"role": "user", "content": user}],
        )
        return r.choices[0].message.content
    raise ValueError(f"unknown provider: {provider}")


SYSTEM_PREAMBLE = (
    "You are an agent with externalized memory, skills, and protocols.\n"
    "Your memory, skills, and constraints are in the context below.\n"
    "Read them before acting. Follow constraints strictly.\n"
    "Log every action. Update memory/working/WORKSPACE.md as you go.\n\n"
)


def run(user_input: str) -> str:
    context, used = build_context(user_input, budget=MAX_CTX - RESERVED)
    system = SYSTEM_PREAMBLE + context
    try:
        result = _call_model(system, user_input)
        log_execution("conductor", user_input[:100], result[:500], True)
        return result
    except Exception as e:
        log_execution("conductor", user_input[:100], str(e), False)
        raise


if __name__ == "__main__":
    prompt = " ".join(sys.argv[1:]) or sys.stdin.read()
    print(run(prompt))
