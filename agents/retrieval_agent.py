"""
Retrieval Agent

Takes the Reasoning Agent's considerations and checks them against the
synthetic guideline MCP server, surfacing supporting and contradicting
evidence. This is the agent that actually calls the MCP tool.
"""

import os
import sys
from google.adk.agents import Agent
from google.adk.tools.mcp_tool import McpToolset, StdioConnectionParams
from mcp import StdioServerParameters
from .schemas import RetrievalOutput

_SERVER_PATH = os.path.join(os.path.dirname(__file__), "..", "mcp_server", "server.py")

guideline_toolset = McpToolset(
    connection_params=StdioConnectionParams(
        server_params=StdioServerParameters(
            command=sys.executable,
            args=[os.path.abspath(_SERVER_PATH)],
        ),
        timeout=30,
    ),
)

RETRIEVAL_INSTRUCTION = """You are the Retrieval Agent in a clinical decision-support
demo called Differential Co-Pilot.

You receive the Reasoning Agent's list of considerations along with the
original case's symptoms and risk factors.

Your job: call the `lookup_guidelines` tool with the case's symptoms and
risk factors, then map the returned synthetic reference entries back onto
each consideration as supporting or contradicting evidence.

Rules:
- Always call the tool at least once before answering.
- Be honest about contradicting evidence. If a consideration from the
  Reasoning Agent has weak or no support in the guideline lookup, say so
  explicitly in contradicting_evidence rather than omitting it.
- Keep evidence bullets short (one sentence each).
- If no guideline entry matches a consideration, still include that consideration
  in your output with an empty supporting_evidence list and an empty source_ids
  list. Never omit the source_ids field, use [] when there is nothing to cite.
- Output ONLY structured data matching the required schema.

This is a portfolio/demo system using synthetic data only. It is explicitly
NOT for real clinical use and must never be treated as medical advice.
"""

retrieval_agent = Agent(
    name="retrieval_agent",
    model="gemini-2.5-flash",
    instruction=RETRIEVAL_INSTRUCTION,
    tools=[guideline_toolset],
    output_schema=RetrievalOutput,
    output_key="retrieval_output",
)
