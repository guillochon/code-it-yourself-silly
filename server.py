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
    manual_recommended: bool
    confidence: float
    explanation: str
    recommended_action: str


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
        manual_recommended=should_human,
        confidence=round(confidence, 2),
        explanation=rationale,
        recommended_action=instruction,
    )


@mcp.tool(
    name="triage_code_request",
    description=(
        "Pre-flight task triage for coding requests. Decide if a request should be "
        "handled manually by a human or by an AI coding agent. Call before coding "
        "when a task might be tiny (rename/comment/typo/README/small formatting edits)."
    ),
)
def triage_code_request(prompt: str, code_context: str = "") -> dict:
    """
    Evaluate whether a human programmer should make the code change directly.

    Args:
      prompt: User request describing the desired code change.
      code_context: Relevant code or diff context for scope/risk estimation.
    """
    decision = _decide(prompt=prompt, code_context=code_context)
    return {
        "manual_recommended": decision.manual_recommended,
        "confidence": decision.confidence,
        "explanation": decision.explanation,
        "recommended_action": decision.recommended_action,
    }


def main() -> None:
    mcp.run()


if __name__ == "__main__":
    main()
