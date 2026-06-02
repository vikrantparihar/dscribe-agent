def check_interactions(meds):

    interactions = []

    if (
        "Warfarin" in meds
        and
        "Aspirin" in meds
    ):

        interactions.append(
            "Potential bleeding risk"
        )

    return interactions