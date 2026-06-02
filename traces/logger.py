import json

def log_step(step):

    with open(
        "traces/trace.json",
        "a"
    ) as f:

        f.write(
            json.dumps(step)
        )

        f.write("\n")