import json

from tools.pdf_tool import read_pdf
from agents.extractor import extract_information

pdf_path = "patients/patient2.pdf"

text = read_pdf(pdf_path)

print("\n" + "=" * 50)
print("TOTAL TEXT LENGTH:", len(text))
print("=" * 50)

result = extract_information(text)

print("\nEXTRACTED DATA:\n")
print(json.dumps(result, indent=4))

with open(
    "outputs/structured_output.json",
    "w",
    encoding="utf-8"
) as f:
    json.dump(result, f, indent=4)

print("\n✅ JSON SAVED")