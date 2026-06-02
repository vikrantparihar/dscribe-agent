def generate_summary(data):

    diagnoses = "\n".join(data.get("diagnoses", []))

    medications = []

    for med in data.get("medications", []):
        medications.append(
            f"- {med.get('name')} "
            f"{med.get('dosage', '')}"
        )

    meds_text = "\n".join(medications)

    followup = "\n".join(
        data.get("follow_up", [])
    )

    summary = f"""
DISCHARGE SUMMARY

Diagnosis:
{diagnoses}

Discharge Condition:
{data.get('discharge_condition')}

Medications:
{meds_text}

Pending Results:
{', '.join(data.get('pending_results', []))}

Follow Up:
{followup}
"""

    return summary