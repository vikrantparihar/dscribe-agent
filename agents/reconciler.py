def reconcile_meds(admission_meds, discharge_meds):

    added = list(
        set(discharge_meds) -
        set(admission_meds)
    )

    removed = list(
        set(admission_meds) -
        set(discharge_meds)
    )

    return {
        "added": added,
        "removed": removed
    }