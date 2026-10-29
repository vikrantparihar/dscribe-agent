import json
import sys
from pathlib import Path

from tools.pdf_tool import read_pdf
from agents.extractor import extract_information


def main():
    pdf_path = "patients/patient2.pdf"
    text = read_pdf(pdf_path)

    print("\n" + "=" * 50)
    print("TOTAL TEXT LENGTH:", len(text))
    print("=" * 50)

    result = extract_information(text)

    # Do not treat an API or extraction error as successful output.
    if isinstance(result, dict) and result.get("error"):
        print("\nExtraction failed:", result["error"], file=sys.stderr)
        details = result.get("details")
        if details:
            print("Details:", details, file=sys.stderr)
        sys.exit(1)

    output_path = Path("outputs/structured_output.json")
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with output_path.open("w", encoding="utf-8") as f:
        json.dump(result, f, indent=4, ensure_ascii=False)

    print("\nEXTRACTED DATA:\n")
    print(json.dumps(result, indent=4, ensure_ascii=False))
    print(f"\nJSON saved: {output_path}")


if __name__ == "__main__":
    main()
