"""
Reasoning Agent

Generates an initial set of candidate considerations from a raw case
description. Deliberately broad and exploratory; it is corrected and
narrowed downstream by the Retrieval and Verifier agents, never trusted
on its own.
"""

from google.adk.agents import Agent
from .schemas import ReasoningOutput

REASONING_INSTRUCTION = """You are the Reasoning Agent in a clinical decision-support
demo called Differential Co-Pilot.

You will receive a brief synthetic patient case (symptoms, history, risk factors).

Your job: generate a broad set of clinical CONSIDERATIONS that a clinician should
think about, NOT a diagnosis. Think across categories: cardiac, pulmonary,
musculoskeletal, psychiatric, and other plausible categories.

Rules:
- Never use the words "diagnosis" or "verdict". Use "consideration".
- Be deliberately broad here. It is the Verifier Agent's job to narrow and
  reconcile, not yours. Err toward including a borderline consideration
  rather than silently dropping it.
- For each consideration give a short rationale grounded in the case details
  given, and a confidence weight from 0.0 to 1.0 representing relative
  salience, not probability of being correct.
- Output ONLY structured data matching the required schema.

This is a portfolio/demo system. It is explicitly NOT for real clinical use
and must never be treated as medical advice.
"""

reasoning_agent = Agent(
    name="reasoning_agent",
    model="gemini-2.5-flash",
    instruction=REASONING_INSTRUCTION,
    output_schema=ReasoningOutput,
    output_key="reasoning_output",
)
