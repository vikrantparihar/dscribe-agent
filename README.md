# Medical Discharge Summary Extraction Agent

## Overview

This project extracts structured medical discharge summaries from clinical PDF documents using:

- PDF Text Extraction
- Gemini 2.5 Flash
- Pydantic Schema Validation
- Structured JSON Output
- Ground Truth Evaluation

The goal is to convert unstructured clinical notes into safe, structured discharge summaries while minimizing hallucinations.

---

## Features

- Multi-page PDF Processing
- Clinical Information Extraction
- Hallucination Prevention
- Structured JSON Output
- Pydantic Validation
- Evaluation Metrics
- Error Handling

---

## Project Structure

.
├── agents/
├── evaluation/
├── outputs/
├── patients/
├── schemas/
├── tools/
├── main.py
├── config.py
├── ground_truth.json
├── requirements.txt
├── README.md
└── Dockerfile

---

## Architecture

PDF
↓
Text Extraction
↓
Gemini 2.5 Flash
↓
Structured Information Extraction
↓
Pydantic Validation
↓
JSON Output
↓
Evaluation

---

## Installation

Create virtual environment:

python -m venv venv

Activate:

source venv/bin/activate

Install dependencies:

pip install -r requirements.txt

---

## Run

Process a PDF:

python main.py

Output:

outputs/structured_output.json

---

## Evaluation

Run:

python evaluation/evaluate.py

Metrics:

- Precision
- Recall
- F1 Score

---

## Example Output

{
  "diagnoses": [
    "ACUTE GASTROENTERITIS WITH DEHYDRATION",
    "URINARY TRACT INFECTION"
  ]
}

---

## Future Improvements

- Migration to google-genai SDK
- Batch Processing
- Confidence Scores
- Better OCR Post-processing
- Human Review Workflow

## Evaluation Results

Latest local evaluation run:

### Field-Level Exact Match

- Correct fields: 4
- Scored predictions: 6
- Evaluable ground-truth fields: 6
- Additional unscored predictions: 11
- Precision: 0.6667
- Recall: 0.6667
- F1 Score: 0.6667

### List-Item Exact Match

- Correct items: 4
- Predicted items: 6
- Ground-truth items: 6
- Precision: 0.6667
- Recall: 0.6667
- F1 Score: 0.6667

### Text Similarity Diagnostics

- Mean best-match character similarity: 96.21%

Character similarity is a diagnostic measure only; it does not establish
clinical correctness. These results describe the current sample and are not
evidence of a generalizable model accuracy.

### Limitations

- OCR noise can affect clinical information, especially medication extraction.
- Ground truth was manually created from source notes.
- Only fields with available ground-truth values are scored by the field-level
  metric; additional predictions are reported separately as unscored.
- List-item metrics use exact normalized text matching.
- Evaluation on additional manually verified records is needed before drawing
  broader conclusions about extraction performance.
- Future improvements include confidence scoring, OCR normalization, and human
  review.

