"""
Differential Co-Pilot - Demo Runner

Usage:
    export GOOGLE_API_KEY=your_key_here
    python3 demo/run_demo.py

Runs the full Reasoning -> Retrieval -> Verifier pipeline against a
synthetic, illustrative patient case and prints the final differential
expansion, flagged omissions, and conflict notes.

This is a portfolio/demo system using synthetic data only. It is
explicitly NOT for real clinical use and must never be treated as
medical advice.
"""

import asyncio
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from google.adk.runners import InMemoryRunner
from google.genai import types

from agents.pipeline import root_agent
from agents.security_screen import screen_input

SYNTHETIC_CASE = """\
Synthetic demo case (not a real patient):

Patient: 54-year-old male
Presenting symptoms: chest discomfort, mild shortness of breath, fatigue, \
duration 3 days
History: hypertension, current smoker
"""


async def main():
    if not os.environ.get("GOOGLE_API_KEY"):
        print(
            "GOOGLE_API_KEY not set. Set it before running:\n"
            "  export GOOGLE_API_KEY=your_key_here\n"
        )
        return

    runner = InMemoryRunner(agent=root_agent, app_name="differential_copilot")
    session = await runner.session_service.create_session(
        app_name="differential_copilot", user_id="demo_user"
    )

    screen_result = screen_input(SYNTHETIC_CASE)
    print("=== Pre-LLM Security Screen ===")
    print(f"Allowed: {screen_result.allowed}")
    if screen_result.redactions:
        print(f"Redactions applied: {screen_result.redactions}")
    if not screen_result.allowed:
        print(f"Blocked. Reasons: {screen_result.block_reasons}")
        print("Escalating to human review instead of forwarding to agent pipeline.")
        return
    print()

    user_message = types.Content(
        role="user", parts=[types.Part(text=screen_result.cleaned_text)]
    )

    final_state = None
    async for event in runner.run_async(
        user_id="demo_user", session_id=session.id, new_message=user_message
    ):
        if event.is_final_response() and event.content and event.content.parts:
            final_state = event.content.parts[0].text

    print("\n=== Differential Co-Pilot: Final Output ===\n")
    if final_state:
        try:
            parsed = json.loads(final_state)
            print(json.dumps(parsed, indent=2))
        except json.JSONDecodeError:
            print(final_state)
    else:
        print("No final output captured. Check session state for intermediate results.")

    refreshed = await runner.session_service.get_session(
        app_name="differential_copilot", user_id="demo_user", session_id=session.id
    )
    print("\n=== Full Pipeline State (all agent outputs) ===\n")
    for key in ("reasoning_output", "retrieval_output", "verified_output"):
        if key in refreshed.state:
            print(f"--- {key} ---")
            print(json.dumps(refreshed.state[key], indent=2, default=str))
            print()


if __name__ == "__main__":
    asyncio.run(main())
