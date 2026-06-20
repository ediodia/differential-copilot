"""
Differential Co-Pilot - Root Pipeline

Sequential pipeline: Reasoning -> Retrieval -> Verifier.

Each agent writes to ADK session state via output_key, and the next agent
in the sequence reads prior state automatically through ADK's shared
session context. This mirrors (in simplified, clean-room form) the
multi-agent deliberation + conflict resolution pattern used in the
Differential Co-Pilot's parent project, adapted here for a public,
synthetic-data-only capstone demo.
"""

from google.adk.agents import SequentialAgent
from .reasoning_agent import reasoning_agent
from .retrieval_agent import retrieval_agent
from .verifier_agent import verifier_agent

root_agent = SequentialAgent(
    name="differential_copilot_pipeline",
    description=(
        "Multi-agent pipeline that expands a synthetic clinical case into a "
        "reconciled set of considerations, with explicit omission flagging "
        "and contestability notes. Demo system, synthetic data only, not for "
        "real clinical use."
    ),
    sub_agents=[reasoning_agent, retrieval_agent, verifier_agent],
)
