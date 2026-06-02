from pydantic import BaseModel
from typing import List, Optional, Dict, Any


class PatientDemographics(BaseModel):
    full_name: str
    age: str
    gender: str
    mrn: str
    ip_no: str


class MedicalRecord(BaseModel):

    patient_demographics: PatientDemographics

    admission_date: str

    discharge_date: str

    diagnoses: List[str]

    allergies: str

    medications: Dict[str, Any]

    procedures: List[str]

    pending_results: List[str]

    follow_up: List[str]

    discharge_condition: str