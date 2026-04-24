from __future__ import annotations

import re
from dataclasses import dataclass

from mcp.server.fastmcp import FastMCP


mcp = FastMCP("code it yourself silly")


SIMPLE_PATTERNS = [
    r"\brename\b",
    r"\btypo\b",
    r"\bcomment\b",
    r"\bdocstring\b",
    r"\breadme\b",
    r"\bformat\b",
    r"\blint\b",
    r"\bone[- ]line\b",
    r"\bsmall\b",
    r"\bquick\b",
    r"\bjust\b",
]

COMPLEX_PATTERNS = [
    r"\barchitecture\b",
    r"\brefactor\b",
    r"\bmigration\b",
    r"\bdatabase\b",
    r"\bauth\b",
    r"\bsecurity\b",
    r"\bperformance\b",
    r"\bapi\b",
    r"\basync\b",
    r"\bconcurrency\b",
    r"\bdistributed\b",
]


@dataclass
class Decision:
    should_human_do_it: bool
    confidence: float
    rationale: str
    agent_instruction: str


def _count_patterns(text: str, patterns: list[str]) -> int:
    return sum(1 for pattern in patterns if re.search(pattern, text, flags=re.IGNORECASE))


def _estimate_scope(code_context: str) -> int:
    if not code_context.strip():
        return 0
    changed_lines = [line for line in code_context.splitlines() if line.strip()]
    # Rough proxy: few non-empty lines usually means tiny edits.
    return len(changed_lines)


def _decide(prompt: str, code_context: str) -> Decision:
    prompt_lc = prompt.strip()
    combined = f"{prompt_lc}\n{code_context}"

    simple_hits = _count_patterns(combined, SIMPLE_PATTERNS)
    complex_hits = _count_patterns(combined, COMPLEX_PATTERNS)
    scope = _estimate_scope(code_context)

    # Bias toward "human should do it" only for tiny/obvious tasks.
    score = simple_hits - (complex_hits * 2)
    if scope <= 20:
        score += 1
    if scope > 80:
        score -= 2

    should_human = score >= 2
    confidence = 0.6 + min(abs(score), 4) * 0.08
    confidence = max(0.51, min(confidence, 0.95))

    if should_human:
        rationale = "Low-scope, low-risk request detected."
        # Intentionally token-thrifty and human-readable.
        instruction = "Do manually: edit file, run tests, commit."
    else:
        rationale = "Task appears non-trivial or higher risk."
        instruction = "Proceed with normal agent workflow."

    return Decision(
        should_human_do_it=should_human,
        confidence=round(confidence, 2),
        rationale=rationale,
        agent_instruction=instruction,
    )


@mcp.tool(
    name="should_a_human_do_it",
    description=(
        "Decide if a code task is simple enough that a human should do it directly. "
        "Returns a terse instruction for the agent."
    ),
)
def should_a_human_do_it(prompt: str, code_context: str = "") -> dict:
    """
    Evaluate whether a human programmer should make the code change directly.

    Args:
      prompt: User request describing the desired code change.
      code_context: Relevant code or diff context for scope/risk estimation.
    """
    decision = _decide(prompt=prompt, code_context=code_context)
    return {
        "should_human_do_it": decision.should_human_do_it,
        "confidence": decision.confidence,
        "rationale": decision.rationale,
        "agent_instruction": decision.agent_instruction,
    }


def main() -> None:
    mcp.run()


if __name__ == "__main__":
    main()
