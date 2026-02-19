"""Maps trial conditions into one standard therapeutic area."""

TA_KEYWORDS = [
    ("Oncology", ["cancer", "carcinoma", "tumor", "tumour", "lymphoma", "leukemia", "melanoma", "myeloma"]),
    ("Cardiology", ["cardio", "heart", "myocardial", "hypertension", "arrhythmia", "stroke"]),
    ("Neurology", ["neuro", "alzheimer", "parkinson", "epilepsy", "multiple sclerosis", "migraine"]),
    ("Immunology", ["immune", "autoimmune", "lupus", "rheumatoid", "psoriasis", "crohn", "colitis"]),
    ("Infectious Diseases", ["infection", "viral", "bacterial", "hiv", "hepatitis", "covid", "influenza", "tuberculosis"]),
    ("Endocrinology", ["diabetes", "thyroid", "metabolic", "obesity", "hormone"]),
    ("Respiratory", ["asthma", "copd", "pulmonary", "respiratory", "lung"]),
    ("Gastroenterology", ["gastro", "liver", "hepatic", "pancrea", "intestinal"]),
    ("Rare Diseases", ["rare disease", "orphan"]),
]


def map_therapeutic_area(conditions: list[str]) -> str:
    text = " ".join(conditions or []).lower()
    for ta, keywords in TA_KEYWORDS:
        if any(keyword in text for keyword in keywords):
            return ta
    return "General Medicine"


def map_indication_class(conditions: list[str]) -> str:
    text = " ".join(conditions or []).lower()
    if any(x in text for x in ["cancer", "lymphoma", "leukemia", "tumor", "tumour"]):
        return "Oncologic"
    if any(x in text for x in ["infection", "viral", "bacterial", "hiv", "covid", "flu", "hepatitis"]):
        return "Infectious"
    if any(x in text for x in ["diabetes", "hypertension", "copd", "asthma", "heart", "alzheimer", "parkinson"]):
        return "Chronic"
    if any(x in text for x in ["acute", "trauma", "sepsis", "injury"]):
        return "Acute"
    return "Other"
