"""
Pre-LLM Security Screen

Implements the "shift security left" pattern from the course: input is
screened BEFORE it ever reaches an LLM call, not after. Two jobs:

1. PII REDACTION - strip obvious real-world identifiers (names patterns,
   phone numbers, emails, SSNs, MRNs) from input before it reaches any
   agent. This demo only ever uses synthetic data internally, but a real
   intake surface would receive arbitrary user input, so the screen must
   exist regardless of what the bundled demo case looks like.

2. PROMPT INJECTION SHORT-CIRCUIT - detect common injection patterns
   (e.g. "ignore previous instructions", attempts to extract system
   prompts, attempts to make the agent claim something is a diagnosis)
   and refuse to forward the input to the pipeline, escalating to a
   human-review state instead of silently complying or silently failing.

This is a deliberately simple, transparent, rule-based screen, not an ML
classifier. That is intentional: a security gate should be auditable and
predictable, not itself a black box the user has to trust blindly.
"""

import re
from dataclasses import dataclass, field


PII_PATTERNS = {
    "email": re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"),
    "phone": re.compile(r"\b(\+?1[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b"),
    "ssn": re.compile(r"\b\d{3}-\d{2}-\d{4}\b"),
    "mrn": re.compile(r"\bMRN[:\s#]*\d{4,}\b", re.IGNORECASE),
    "full_name_label": re.compile(r"\b(patient name|name)\s*:\s*[A-Z][a-z]+\s+[A-Z][a-z]+", re.IGNORECASE),
}

INJECTION_PATTERNS = [
    re.compile(r"ignore (all )?(previous|prior|above) instructions", re.IGNORECASE),
    re.compile(r"disregard (your|the) (system )?prompt", re.IGNORECASE),
    re.compile(r"you are now (a|an) ", re.IGNORECASE),
    re.compile(r"reveal (your|the) (system )?prompt", re.IGNORECASE),
    re.compile(r"act as (if|though) you (are|were) (a doctor|unrestricted)", re.IGNORECASE),
    re.compile(r"output (the word |the term )?[\"']?diagnosis[\"']?", re.IGNORECASE),
    re.compile(r"this is (not|no longer) a (demo|test)", re.IGNORECASE),
]


@dataclass
class ScreenResult:
    allowed: bool
    cleaned_text: str
    redactions: list[str] = field(default_factory=list)
    block_reasons: list[str] = field(default_factory=list)


def screen_input(raw_text: str) -> ScreenResult:
    """
    Runs PII redaction and prompt-injection detection on raw input BEFORE
    it is passed to any agent or LLM call.

    Returns a ScreenResult. If `allowed` is False, the caller must NOT
    forward `cleaned_text` (or the original) to the pipeline. Instead it
    should surface block_reasons to the user/clinician as an escalation,
    not a silent failure.
    """
    block_reasons: list[str] = []
    for pattern in INJECTION_PATTERNS:
        if pattern.search(raw_text):
            block_reasons.append(f"Potential prompt injection pattern matched: '{pattern.pattern}'")

    redactions: list[str] = []
    cleaned = raw_text
    for label, pattern in PII_PATTERNS.items():
        matches = pattern.findall(cleaned)
        if matches:
            redactions.append(f"{label} ({len(pattern.findall(cleaned))} instance(s))")
            cleaned = pattern.sub(f"[REDACTED_{label.upper()}]", cleaned)

    allowed = len(block_reasons) == 0

    return ScreenResult(
        allowed=allowed,
        cleaned_text=cleaned if allowed else raw_text,
        redactions=redactions,
        block_reasons=block_reasons,
    )
