import json
from pathlib import Path


def flatten(obj, prefix=""):
    items = {}

    if isinstance(obj, dict):
        for key, value in obj.items():
            path = f"{prefix}.{key}" if prefix else key
            items.update(flatten(value, path))

    elif isinstance(obj, list):
        items[prefix] = set(map(str, obj))

    else:
        items[prefix] = str(obj)

    return items


def calculate_metrics(gt, pred):
    gt_flat = flatten(gt)
    pred_flat = flatten(pred)

    correct = sum(
        1
        for key, value in gt_flat.items()
        if key in pred_flat and pred_flat[key] == value
    )

    total_pred = len(pred_flat)
    total_gt = len(gt_flat)

    precision = correct / total_pred if total_pred else 0.0
    recall = correct / total_gt if total_gt else 0.0

    f1 = (
        2 * precision * recall / (precision + recall)
        if precision + recall
        else 0.0
    )

    return {
        "correct_fields": correct,
        "total_pred": total_pred,
        "total_gt": total_gt,
        "precision": precision,
        "recall": recall,
        "f1": f1,
    }


def main():
    base_dir = Path(__file__).resolve().parent.parent

    with (base_dir / "ground_truth.json").open(encoding="utf-8") as file:
        ground_truth = json.load(file)

    with (base_dir / "outputs/structured_output.json").open(
        encoding="utf-8"
    ) as file:
        prediction = json.load(file)

    metrics = calculate_metrics(ground_truth, prediction)

    print("\n===== EVALUATION =====")
    print(f"Correct Fields : {metrics['correct_fields']}")
    print(f"Precision      : {metrics['precision']:.2f}")
    print(f"Recall         : {metrics['recall']:.2f}")
    print(f"F1 Score       : {metrics['f1']:.2f}")


if __name__ == "__main__":
    main()
