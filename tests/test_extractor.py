import json
from unittest.mock import Mock

from pydantic import ValidationError

from agents import extractor


def valid_medical_record():
    return {
        "patient_demographics": {
            "full_name": "MISSING",
            "age": "MISSING",
            "gender": "MISSING",
            "mrn": "MISSING",
            "ip_no": "MISSING",
        },
        "admission_date": "MISSING",
        "discharge_date": "MISSING",
        "diagnoses": [],
        "allergies": "MISSING",
        "medications": {},
        "procedures": [],
        "pending_results": [],
        "follow_up": [],
        "discharge_condition": "MISSING",
    }


def mock_response(monkeypatch, response_text):
    response = Mock()
    response.text = response_text

    generate = Mock(return_value=response)
    monkeypatch.setattr(extractor.model, "generate_content", generate)

    return generate


def test_extract_information_valid_json(monkeypatch, tmp_path):
    monkeypatch.chdir(tmp_path)
    record = valid_medical_record()
    generate = mock_response(monkeypatch, json.dumps(record))

    result = extractor.extract_information("Sample clinical note")

    assert result == record
    generate.assert_called_once()


def test_extract_information_invalid_json(monkeypatch, tmp_path):
    monkeypatch.chdir(tmp_path)
    mock_response(monkeypatch, '{"patient_demographics": invalid}')

    result = extractor.extract_information("Sample clinical note")

    assert "error" in result


def test_extract_information_schema_validation_failure(monkeypatch, tmp_path):
    monkeypatch.chdir(tmp_path)
    record = valid_medical_record()
    del record["diagnoses"]
    mock_response(monkeypatch, json.dumps(record))

    result = extractor.extract_information("Sample clinical note")

    assert result["error"] == "Schema Validation Failed"


def test_extract_information_empty_response(monkeypatch, tmp_path):
    monkeypatch.chdir(tmp_path)
    mock_response(monkeypatch, "")

    result = extractor.extract_information("Sample clinical note")

    assert "error" in result
