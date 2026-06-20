# Differential Co-Pilot
### A multi-agent system that expands clinical considerations instead of narrowing to a diagnosis

**Track:** Agents for Good

---

## The problem

Clinical decision-support tools have a specific, well-documented failure
mode: they narrow too fast. Ask a single model "what's wrong with this
patient" and it tends to commit to a likely answer, quietly dropping
plausible alternatives along the way. That's exactly the moment a clinician
most needs to be reminded of what they might be missing, not handed a
confident-sounding single answer.

This isn't a hypothetical concern for me. I'm the lead engineer and
co-founder of a hospital-focused clinical AI platform, and the core design
problem we've spent the most time on is this exact one: how do you build a
system that genuinely helps without quietly narrowing a clinician's
thinking? Differential Co-Pilot is a clean-room, public, synthetic-data-only
exploration of that problem, built for this capstone.

## Why agents, specifically

A single LLM call optimized end-to-end for "give me the answer" has no
structural incentive to preserve disagreement. It will produce a coherent,
well-written response that happens to have silently dropped the
second-most-likely consideration somewhere in its reasoning, and there's no
way to see that it happened.

Splitting the problem across agents with genuinely different jobs changes
that. One agent's only job is to be broad. Another's only job is to check
evidence honestly, including evidence that contradicts the first agent. A
third agent's only job is to reconcile the two without collapsing them into
a single winner, and to write down, explicitly, where they disagreed and
why. None of these constraints are reliably enforceable inside one model
call optimized for a single best answer. They become enforceable when
they're separate agents with separate, narrow instructions and structured
output schemas. The architecture itself is what creates the bias toward
not narrowing prematurely.

## The solution

A clinician (or in this demo, anyone) enters a short synthetic patient
case. Before anything touches an LLM, the input passes through a security
screen that redacts PII patterns and detects prompt-injection attempts. If
the input is clean, it flows through a three-agent pipeline:

**Reasoning agent** reads the case and generates a deliberately broad set
of candidate clinical considerations, spanning multiple categories (e.g.
cardiac, pulmonary, musculoskeletal, psychiatric). It is explicitly
instructed to err toward including borderline considerations rather than
silently dropping them. Narrowing is not its job.

**Retrieval agent** takes those considerations and calls an MCP server
exposing a synthetic guideline-lookup tool, checking each consideration
against reference data for supporting and contradicting evidence. It's
instructed to surface weak or contradicting evidence honestly rather than
omit it, since that's information the clinician should see, not grounds
for quiet deletion.

**Verifier agent** is the final, conservative checkpoint. It reconciles the
two upstream agents into a final differential expansion, explicitly flags
any consideration that was under-weighted or contradicted but still
clinically plausible, and writes conflict notes describing every place the
Reasoning and Retrieval agents disagreed and how that was resolved. It is
hard-instructed never to collapse the list down to one dominant answer,
genuine reconciliation reweights and contextualizes, it doesn't eliminate.

The system's vocabulary is locked at the schema level: every output uses
"consideration" and "differential expansion," never "diagnosis" or
"verdict." This isn't cosmetic. It's a constraint on what the system is
allowed to claim about itself.

The result a user sees is not a single answer. It's a reconciled list of
considerations, a list of flagged omissions, and a transparent record of
where the agents disagreed, the contestability layer. A clinician can push
back on this output because they can see how it was built, instead of
trusting a black box.

## Architecture

```
Synthetic case input
        |
        v
Pre-LLM security screen  (PII redaction, prompt-injection block)
        |
        v
+----------------------------------------+
|   Sequential ADK pipeline               |
|                                          |
|   Reasoning agent                       |
|        |                                |
|        v                                |
|   Retrieval agent  -- calls -->  MCP server (synthetic guidelines)
|        |                                |
|        v                                |
|   Verifier agent                        |
|                                          |
+----------------------------------------+
        |
        v
Differential expansion + flagged omissions + conflict notes
```

The three agents are wired as a `SequentialAgent` in Google ADK, each
agent's output written to shared session state via `output_key` and read by
the next agent automatically. The Retrieval agent connects to the MCP
server over stdio using `McpToolset`. All structured outputs are enforced
via Pydantic schemas, which is also how the "never say diagnosis"
constraint is made structurally reliable rather than just instructed and
hoped for.

## Course concepts demonstrated

**Multi-agent system (ADK).** Three agents (Reasoning, Retrieval, Verifier)
with distinct, narrow responsibilities, wired into a `SequentialAgent`
pipeline with shared session state.

**MCP server.** A purpose-built MCP server exposing one tool,
`lookup_guidelines`, over a small synthetic reference dataset. The
Retrieval agent calls it directly via ADK's `McpToolset`, this is the
piece of the system that actually grounds the Reasoning agent's broad
output in something other than the model's own priors.

**Security features.** A pre-LLM screen runs before any input reaches an
agent or model call; it redacts PII patterns (emails, phone numbers, SSNs,
medical record numbers) and detects prompt-injection patterns, blocking
and escalating rather than silently processing or silently failing. This
follows the "shift security left" pattern from the course, screening at
the point of input rather than trying to filter output after the fact.

**Deployability.** Built and iterated using Antigravity and Agents CLI to
scaffold, lint, and test the ADK agents locally, then deployed publicly so
the demo is reachable without any setup on the judge's end.

## The build

I built this as a clean-room rebuild of architecture concepts from my
clinical AI platform, not an export of its code. Everything here is new:
new prompts, a new synthetic dataset, a simplified three-agent structure
instead of the full production pipeline, and no proprietary RAG sources or
production prompt engineering. The goal was to demonstrate the underlying
design pattern, multi-agent deliberation with an explicit contestability
layer, in a form that's honest, public, and fully reproducible by anyone
who clones the repo.

The stack is Google ADK 2.0 for the agent framework, the official MCP
Python SDK for the guideline-lookup server, Pydantic for structured output
enforcement, and Streamlit for the demo UI. I used Antigravity as my
agentic IDE for the build and Agents CLI to scaffold and test the ADK
project locally, which is also where I caught the deprecated
`StdioServerParameters` pattern in favor of the current `McpToolset` API.

## What I'd build next

The most interesting open problem isn't technical, it's evaluative. Right
now the Verifier agent's instruction to "never collapse to one dominant
answer" is enforced by prompting, not by a measurable property of the
output. A real next step would be building an eval harness that
specifically scores omission prevention: given a case with a known set of
plausible alternatives, does the system's final output actually preserve
the ones a single-shot model would have dropped? That's the kind of
question this architecture was built to make answerable, and it's the
natural extension of this project beyond the capstone.

---

*This is a demo system using synthetic data only. It is not a real
clinical tool, is not connected to any real guideline database, and must
never be used for actual medical decisions.*
