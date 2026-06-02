def planner(state):

    if not state.get("patient_text"):
        return "read_pdf"

    if not state.get("extracted_data"):
        return "extract"

    if not state.get("summary"):
        return "summarize"

    return "finish"