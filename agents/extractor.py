import json

import google.generativeai as genai
from pydantic import ValidationError

from config import GEMINI_API_KEY
from schemas.medical_schema import MedicalRecord

# Configure Gemini
genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel("gemini-2.5-flash")


def extract_information(text: str) -> dict:
    """
    Extract structured medical information from clinical notes.
    """

    prompt = f"""
You are a clinical information extraction agent.

STRICT RULES:

1. Never invent information.
2. Never infer information.
3. Only extract information explicitly present in the document.
4. If information is unavailable, return "MISSING".
5. Return VALID JSON ONLY.
6. Do not include explanations.
7. Do not include markdown.
8. Do not wrap output inside ```json blocks.
9. Diagnoses, medications, procedures and dates must only come from the source text.

Extract the following fields:

{{
    "patient_demographics": {{
        "full_name": "",
        "age": "",
        "gender": "",
        "mrn": "",
        "ip_no": ""
    }},
    "admission_date": "",
    "discharge_date": "",
    "diagnoses": [],
    "allergies": "",
    "medications": {{}},
    "procedures": [],
    "pending_results": [],
    "follow_up": [],
    "discharge_condition": ""
}}

Source Notes:

{text}
"""

    try:
        response = model.generate_content(
            prompt,
            generation_config={"response_mime_type": "application/json"},
        )

        raw_output = getattr(response, "text", None)

        if not isinstance(raw_output, str) or not raw_output.strip():
            return {
                "error": "Empty Response",
                "details": "Gemini returned no text to parse.",
            }

        raw_output = raw_output.strip()

        # Accept JSON enclosed in Markdown code fences.
        if raw_output.startswith("```"):
            lines = raw_output.splitlines()
            if lines and lines[0].strip().lower() in ("```json", "```"):
                lines = lines[1:]
            if lines and lines[-1].strip() == "```":
                lines = lines[:-1]
            raw_output = "\n".join(lines).strip()

        try:
            data = json.loads(raw_output)
        except json.JSONDecodeError as e:
            return {
                "error": "Invalid JSON",
                "details": str(e),
            }

        try:
            validated_data = MedicalRecord.model_validate(data)
        except ValidationError as e:
            return {
                "error": "Schema Validation Failed",
                "details": str(e),
            }

        print("Schema validation passed")
        return validated_data.model_dump()

    except Exception as e:
        return {
            "error": "Generation Failed",
            "details": str(e),
        }
