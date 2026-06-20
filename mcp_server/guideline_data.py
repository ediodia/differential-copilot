"""
Synthetic, illustrative reference data only.
This is NOT sourced from any real clinical guideline database.
Built for demo purposes for the Kaggle AI Agents Capstone.
"""

GUIDELINES = [
    {
        "id": "ref-001",
        "topic": "chest_discomfort_cardiac",
        "summary": (
            "Chest discomfort with exertional component, risk factors such as "
            "hypertension and smoking history, and associated fatigue may warrant "
            "consideration of cardiac etiology. Common associated findings can "
            "include dyspnea on exertion and diaphoresis."
        ),
        "associated_symptoms": ["chest discomfort", "shortness of breath", "fatigue", "diaphoresis"],
        "risk_factors": ["hypertension", "smoking", "diabetes", "family history"],
        "category": "cardiac",
    },
    {
        "id": "ref-002",
        "topic": "chest_discomfort_pulmonary",
        "summary": (
            "Chest discomfort accompanied by shortness of breath may also reflect "
            "pulmonary causes such as bronchospasm or pleuritic processes, "
            "particularly in patients with smoking history or recent respiratory illness."
        ),
        "associated_symptoms": ["shortness of breath", "chest discomfort", "cough"],
        "risk_factors": ["smoking", "recent respiratory infection", "asthma history"],
        "category": "pulmonary",
    },
    {
        "id": "ref-003",
        "topic": "chest_discomfort_musculoskeletal",
        "summary": (
            "Musculoskeletal chest pain is typically reproducible on palpation or "
            "movement and is not usually accompanied by systemic symptoms such as "
            "fatigue or dyspnea unless coincidental."
        ),
        "associated_symptoms": ["chest discomfort", "pain with movement"],
        "risk_factors": ["recent physical strain", "prior musculoskeletal injury"],
        "category": "musculoskeletal",
    },
    {
        "id": "ref-004",
        "topic": "chest_discomfort_anxiety",
        "summary": (
            "Anxiety-related chest discomfort can present with shortness of breath "
            "and fatigue, often situational, and may co-occur with or mimic cardiac "
            "presentations, which is why exclusionary workup is typically recommended "
            "rather than assumption."
        ),
        "associated_symptoms": ["chest discomfort", "shortness of breath", "fatigue", "palpitations"],
        "risk_factors": ["history of anxiety", "recent stressor"],
        "category": "psychiatric",
    },
    {
        "id": "ref-005",
        "topic": "smoking_hypertension_risk_amplification",
        "summary": (
            "Concurrent smoking and hypertension history are commonly cited as "
            "compounding risk factors that amplify the pretest likelihood of "
            "cardiovascular causes for new chest symptoms, supporting a lower "
            "threshold for cardiac-focused workup."
        ),
        "associated_symptoms": [],
        "risk_factors": ["hypertension", "smoking"],
        "category": "risk_amplifier",
    },
]


def search_guidelines(query_terms: list[str]) -> list[dict]:
    """Simple keyword-overlap search over the synthetic guideline set."""
    query_terms_lower = {t.lower() for t in query_terms}
    results = []
    for g in GUIDELINES:
        haystack = set(
            [s.lower() for s in g["associated_symptoms"]]
            + [r.lower() for r in g["risk_factors"]]
            + [g["topic"].lower()]
        )
        overlap = query_terms_lower & haystack
        if overlap:
            results.append({**g, "matched_terms": sorted(overlap)})
    results.sort(key=lambda r: len(r["matched_terms"]), reverse=True)
    return results
