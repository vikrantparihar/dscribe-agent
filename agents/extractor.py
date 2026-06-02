import json
import re

import google.generativeai as genai

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
            generation_config={
                "response_mime_type": "application/json"
            }
        )

        raw_output = response.text.strip()

        # Save raw output for debugging
        with open("gemini_raw.txt", "w", encoding="utf-8") as f:
            f.write(raw_output)

        # Remove markdown fences if present
        raw_output = (
            raw_output
            .replace("```json", "")
            .replace("```", "")
            .strip()
        )

        # Extract JSON safely
        match = re.search(r"\{.*\}", raw_output, re.DOTALL)

        if not match:
            raise ValueError("No valid JSON found in Gemini response")

        clean_json = match.group(0)

        # Parse JSON
        data = json.loads(clean_json)

        # Validate schema
        validated_data = MedicalRecord.model_validate(data)

        print("✅ Schema Validation Passed")

        return validated_data.model_dump()

    except json.JSONDecodeError as e:
        print("❌ Invalid JSON returned by Gemini")
        print(e)

        return {
            "error": "Invalid JSON",
            "details": str(e)
        }

    except Exception as e:
        print("❌ Validation Failed")
        print(e)

        return {
            "error": "Validation Failed",
            "details": str(e)
        }