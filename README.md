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

Sample Run:

Precision: 0.36
Recall: 0.92
F1 Score: 0.52

Limitations:
- OCR noise affects medication extraction.
- Ground truth was manually created from source notes.
- Future improvements include confidence scoring and OCR normalization.

