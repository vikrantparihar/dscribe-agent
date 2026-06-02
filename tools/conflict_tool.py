def detect_conflict(value1, value2):

    if value1 != value2:

        return {
            "conflict": True,
            "details":
            f"{value1} vs {value2}"
        }

    return {
        "conflict": False
    }