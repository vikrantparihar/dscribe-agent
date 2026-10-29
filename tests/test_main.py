import json

import pytest

import main


def test_main_stops_when_extraction_fails(monkeypatch, tmp_path):
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(main, "read_pdf", lambda path: "sample text")
    monkeypatch.setattr(
        main,
        "extract_information",
        lambda text: {"error": "Generation Failed", "details": "Quota exceeded"},
    )

    with pytest.raises(SystemExit) as exc:
        main.main()

    assert exc.value.code == 1
    assert not (tmp_path / "outputs" / "structured_output.json").exists()


def test_main_saves_successful_extraction(monkeypatch, tmp_path):
    monkeypatch.chdir(tmp_path)
    expected = {"diagnoses": ["sample diagnosis"]}

    monkeypatch.setattr(main, "read_pdf", lambda path: "sample text")
    monkeypatch.setattr(main, "extract_information", lambda text: expected)

    main.main()

    output_path = tmp_path / "outputs" / "structured_output.json"
    assert output_path.exists()

    with output_path.open(encoding="utf-8") as f:
        assert json.load(f) == expected
