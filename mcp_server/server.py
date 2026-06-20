"""
Differential Co-Pilot - Guideline Lookup MCP Server

Exposes a single tool, `lookup_guidelines`, that the Retrieval Agent
calls to fetch supporting/contradicting reference material for a
candidate consideration. All data is synthetic and illustrative only,
built for the Kaggle AI Agents Capstone demo. This is NOT connected to
any real clinical database and must never be treated as medical advice.
"""

from mcp.server.fastmcp import FastMCP
from guideline_data import search_guidelines

mcp = FastMCP("guideline-lookup")


@mcp.tool()
def lookup_guidelines(symptoms: list[str], risk_factors: list[str]) -> dict:
    """
    Look up synthetic reference guidelines relevant to a set of symptoms
    and risk factors.

    Args:
        symptoms: list of patient-reported symptoms, e.g. ["chest discomfort", "fatigue"]
        risk_factors: list of patient risk factors, e.g. ["hypertension", "smoking"]

    Returns:
        dict with a `results` list of matching synthetic guideline entries,
        each including a category, summary, and the matched query terms.
    """
    query_terms = [*symptoms, *risk_factors]
    results = search_guidelines(query_terms)
    return {
        "query": {"symptoms": symptoms, "risk_factors": risk_factors},
        "results": results,
        "disclaimer": (
            "Synthetic demo data only. Not a real clinical guideline source. "
            "For illustrative use in the Differential Co-Pilot capstone project."
        ),
    }


if __name__ == "__main__":
    mcp.run(transport="stdio")
