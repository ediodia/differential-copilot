"""
Shared Pydantic schemas for structured agent output.

Core vocabulary lock: agents must use "consideration" and "differential
expansion" language. Never "diagnosis" or "verdict". This system never
produces a diagnosis; it expands the space of considerations a clinician
should review and flags what might be missing.
"""

from pydantic import BaseModel, Field


class Consideration(BaseModel):
    label: str = Field(description="Short name of the clinical consideration, e.g. 'cardiac ischemia'")
    category: str = Field(description="cardiac | pulmonary | musculoskeletal | psychiatric | other")
    rationale: str = Field(description="Why this consideration is being raised, in plain clinical language")
    confidence: float = Field(description="0.0-1.0 relative weight, NOT a probability of diagnosis")


class ReasoningOutput(BaseModel):
    considerations: list[Consideration]


class RetrievalSupport(BaseModel):
    label: str = Field(description="Matches a consideration label from the Reasoning Agent")
    supporting_evidence: list[str] = Field(
        default_factory=list, description="Short bullet points from guideline lookup"
    )
    contradicting_evidence: list[str] = Field(default_factory=list)
    source_ids: list[str] = Field(
        default_factory=list,
        description="Reference IDs returned by the guideline MCP tool. Use an empty list if no matching guideline was found.",
    )


class RetrievalOutput(BaseModel):
    supports: list[RetrievalSupport]


class FlaggedOmission(BaseModel):
    label: str
    reason: str = Field(description="Why this consideration may have been prematurely excluded or under-weighted")


class VerifiedOutput(BaseModel):
    differential_expansion: list[Consideration] = Field(
        description="Final reconciled set of considerations, NOT a diagnosis"
    )
    flagged_omissions: list[FlaggedOmission] = Field(
        description="Considerations the clinician should not dismiss without explicit review"
    )
    conflict_notes: list[str] = Field(
        description="Where the Reasoning and Retrieval agents disagreed and how it was resolved"
    )
