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

    # --- Abdominal ---
    {
        "id": "ref-006",
        "topic": "abdominal_pain_appendicitis",
        "summary": (
            "Periumbilical pain migrating to the right lower quadrant, accompanied "
            "by nausea, vomiting, and low-grade fever, is a classic pattern warranting "
            "consideration of appendicitis, particularly in younger patients."
        ),
        "associated_symptoms": ["abdominal pain", "nausea", "vomiting", "fever", "loss of appetite"],
        "risk_factors": ["young age", "no prior appendectomy"],
        "category": "gastrointestinal",
    },
    {
        "id": "ref-007",
        "topic": "abdominal_pain_gallbladder",
        "summary": (
            "Right upper quadrant abdominal pain, often after fatty meals, with "
            "nausea and vomiting may suggest biliary etiology such as cholecystitis "
            "or cholelithiasis, particularly in patients with known risk factors."
        ),
        "associated_symptoms": ["abdominal pain", "nausea", "vomiting", "pain after eating"],
        "risk_factors": ["obesity", "female sex", "prior gallstones", "rapid weight loss"],
        "category": "gastrointestinal",
    },
    {
        "id": "ref-008",
        "topic": "abdominal_pain_gastroenteritis",
        "summary": (
            "Diffuse abdominal cramping with nausea, vomiting, and diarrhea, often "
            "of acute onset, is commonly associated with viral or bacterial "
            "gastroenteritis, especially with a history of recent exposure to "
            "contaminated food or sick contacts."
        ),
        "associated_symptoms": ["abdominal pain", "nausea", "vomiting", "diarrhea", "fever"],
        "risk_factors": ["recent travel", "sick contacts", "food exposure"],
        "category": "infectious",
    },

    # --- Neurological ---
    {
        "id": "ref-009",
        "topic": "headache_migraine",
        "summary": (
            "Unilateral, throbbing headache associated with nausea, light "
            "sensitivity, or visual aura, particularly with a personal or family "
            "history of similar episodes, is consistent with migraine."
        ),
        "associated_symptoms": ["headache", "nausea", "light sensitivity", "visual aura"],
        "risk_factors": ["family history of migraine", "female sex", "hormonal triggers"],
        "category": "neurological",
    },
    {
        "id": "ref-010",
        "topic": "headache_red_flags",
        "summary": (
            "Sudden-onset 'worst headache of life,' headache with fever and neck "
            "stiffness, or headache with new neurological deficits are red-flag "
            "presentations warranting urgent evaluation for causes such as "
            "subarachnoid hemorrhage or meningitis, regardless of overall pretest "
            "probability."
        ),
        "associated_symptoms": ["sudden severe headache", "neck stiffness", "fever", "neurological deficit"],
        "risk_factors": ["hypertension", "anticoagulant use"],
        "category": "neurological_red_flag",
    },
    {
        "id": "ref-011",
        "topic": "dizziness_vestibular",
        "summary": (
            "Episodic spinning dizziness triggered by head position changes, "
            "without associated neurological deficits, is commonly associated with "
            "benign vestibular causes, though central causes should be excluded "
            "when other symptoms are present."
        ),
        "associated_symptoms": ["dizziness", "vertigo", "nausea", "imbalance"],
        "risk_factors": ["prior vestibular episodes", "recent viral illness"],
        "category": "neurological",
    },

    # --- Pregnancy / reproductive ---
    {
        "id": "ref-012",
        "topic": "pregnancy_early_symptoms",
        "summary": (
            "Nausea, vomiting, fatigue, mood changes, and a missed or delayed "
            "menstrual period in a patient of reproductive age with recent sexual "
            "activity should prompt consideration of pregnancy as a primary "
            "differential, alongside pregnancy testing as an early step."
        ),
        "associated_symptoms": ["nausea", "vomiting", "fatigue", "mood changes", "missed period", "moody"],
        "risk_factors": ["reproductive age", "sexually active", "no reliable contraception"],
        "category": "reproductive",
    },
    {
        "id": "ref-013",
        "topic": "pregnancy_ectopic_red_flag",
        "summary": (
            "Lower abdominal pain with a missed period and vaginal spotting in a "
            "patient with a positive or unknown pregnancy status is a red flag for "
            "ectopic pregnancy and warrants urgent evaluation, as this is a "
            "potentially life-threatening 'can't miss' diagnosis."
        ),
        "associated_symptoms": ["abdominal pain", "missed period", "vaginal spotting", "dizziness"],
        "risk_factors": ["prior ectopic pregnancy", "pelvic inflammatory disease history", "IUD use"],
        "category": "reproductive_red_flag",
    },

    # --- Infectious / systemic ---
    {
        "id": "ref-014",
        "topic": "fever_viral_syndrome",
        "summary": (
            "Fever with fatigue, body aches, and mild upper respiratory symptoms "
            "in the absence of localizing findings is commonly consistent with a "
            "self-limited viral syndrome, though duration and severity should guide "
            "further workup."
        ),
        "associated_symptoms": ["fever", "fatigue", "body aches", "cough", "sore throat"],
        "risk_factors": ["sick contacts", "recent travel"],
        "category": "infectious",
    },
    {
        "id": "ref-015",
        "topic": "fatigue_thyroid",
        "summary": (
            "Persistent fatigue accompanied by weight change, mood changes, and "
            "temperature intolerance may reflect thyroid dysfunction, particularly "
            "in patients with a personal or family history of thyroid disease."
        ),
        "associated_symptoms": ["fatigue", "weight change", "mood changes", "moody"],
        "risk_factors": ["family history of thyroid disease", "female sex"],
        "category": "endocrine",
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
