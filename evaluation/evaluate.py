import json
from difflib import SequenceMatcher
from pathlib import Path


MISSING_VALUES = {"", "MISSING", "N/A", "NA", "UNKNOWN", "NULL", "NONE"}


def is_missing(value):
    return (
        value is None
        or isinstance(value, str) and value.strip().upper() in MISSING_VALUES
    )


def normalize(value):
    if isinstance(value, str):
        return value.strip().casefold()
    return value


def flatten(obj, prefix=""):
    """Flatten nested objects while keeping lists as individual values."""
    items = {}

    if isinstance(obj, dict):
        for key, value in obj.items():
            path = f"{prefix}.{key}" if prefix else key
            items.update(flatten(value, path))
    elif isinstance(obj, list):
        items[prefix] = obj
    else:
        items[prefix] = obj

    return items


def similarity(a, b):
    """Return normalized character-level similarity between two values."""
    return SequenceMatcher(
        None, str(normalize(a)), str(normalize(b))
    ).ratio()


def calculate_metrics(gt, pred):
    """Evaluate fields with available ground truth; report unscored predictions separately."""
    gt_flat = flatten(gt)
    pred_flat = flatten(pred)

    evaluable_gt = {
        key: value for key, value in gt_flat.items()
        if not is_missing(value)
    }

    correct = sum(
        1 for key, value in evaluable_gt.items()
        if key in pred_flat
        and not is_missing(pred_flat[key])
        and normalize(pred_flat[key]) == normalize(value)
    )

    # Score only predictions at fields that have evaluable ground truth.
    scored_predictions = {
        key: pred_flat[key]
        for key in evaluable_gt
        if key in pred_flat and not is_missing(pred_flat[key])
    }

    # Predictions outside the evaluable ground-truth scope cannot be
    # judged correct or incorrect; report their count separately.
    unscored_predictions = {
        key: value for key, value in pred_flat.items()
        if not is_missing(value) and key not in evaluable_gt
    }

    total_pred = len(scored_predictions)
    total_gt = len(evaluable_gt)

    precision = correct / total_pred if total_pred else 0.0
    recall = correct / total_gt if total_gt else 0.0
    f1 = (
        2 * precision * recall / (precision + recall)
        if precision + recall else 0.0
    )

    return {
        "correct_fields": correct,
        "total_pred": total_pred,
        "total_gt": total_gt,
        "unscored_predictions": len(unscored_predictions),
        "precision": precision,
        "recall": recall,
        "f1": f1,
    }


def calculate_list_metrics(gt, pred):
    """Calculate micro-averaged exact list-item precision, recall and F1."""
    gt_flat = flatten(gt)
    pred_flat = flatten(pred)

    true_positive = 0
    total_gt = 0
    total_pred = 0

    for key, gt_value in gt_flat.items():
        if not isinstance(gt_value, list):
            continue

        # Missing prediction lists count as zero predictions, not as
        # missing ground truth.
        pred_value = pred_flat.get(key, [])
        if not isinstance(pred_value, list):
            pred_value = []

        expected = [normalize(v) for v in gt_value if not is_missing(v)]
        actual = [normalize(v) for v in pred_value if not is_missing(v)]

        remaining = list(expected)
        for item in actual:
            if item in remaining:
                true_positive += 1
                remaining.remove(item)

        total_gt += len(expected)
        total_pred += len(actual)

    # Count predicted list items for which no corresponding GT list exists.
    for key, pred_value in pred_flat.items():
        if key not in gt_flat or not isinstance(gt_flat[key], list):
            if isinstance(pred_value, list):
                total_pred += sum(
                    1 for value in pred_value if not is_missing(value)
                )

    precision = true_positive / total_pred if total_pred else 0.0
    recall = true_positive / total_gt if total_gt else 0.0
    f1 = (
        2 * precision * recall / (precision + recall)
        if precision + recall else 0.0
    )

    return {
        "correct_items": true_positive,
        "total_pred_items": total_pred,
        "total_gt_items": total_gt,
        "precision": precision,
        "recall": recall,
        "f1": f1,
    }


def calculate_list_similarity(gt, pred):
    """Calculate best-match character similarity; not clinical correctness."""
    gt_flat = flatten(gt)
    pred_flat = flatten(pred)

    field_results = {}
    all_gt_scores = []
    all_pred_scores = []

    for key, gt_value in gt_flat.items():
        if not isinstance(gt_value, list):
            continue

        pred_value = pred_flat.get(key, [])
        if not isinstance(pred_value, list):
            pred_value = []

        expected = [v for v in gt_value if not is_missing(v)]
        actual = [v for v in pred_value if not is_missing(v)]

        gt_scores = [
            max((similarity(item, candidate) for candidate in actual), default=0.0)
            for item in expected
        ]
        pred_scores = [
            max((similarity(item, candidate) for candidate in expected), default=0.0)
            for item in actual
        ]

        all_gt_scores.extend(gt_scores)
        all_pred_scores.extend(pred_scores)

        field_results[key] = {
            "ground_truth_items": len(expected),
            "predicted_items": len(actual),
            "ground_truth_mean_similarity": (
                sum(gt_scores) / len(gt_scores) if gt_scores else 0.0
            ),
            "prediction_mean_similarity": (
                sum(pred_scores) / len(pred_scores) if pred_scores else 0.0
            ),
        }

    return {
        "fields": field_results,
        "ground_truth_mean_similarity": (
            sum(all_gt_scores) / len(all_gt_scores) if all_gt_scores else 0.0
        ),
        "prediction_mean_similarity": (
            sum(all_pred_scores) / len(all_pred_scores) if all_pred_scores else 0.0
        ),
    }

def main():
    base_dir = Path(__file__).resolve().parent.parent
    gt_path = base_dir / "ground_truth.json"
    pred_path = base_dir / "outputs" / "structured_output.json"

    for path in (gt_path, pred_path):
        if not path.is_file():
            raise FileNotFoundError(f"Required evaluation file not found: {path}")

    with gt_path.open(encoding="utf-8") as file:
        ground_truth = json.load(file)

    with pred_path.open(encoding="utf-8") as file:
        prediction = json.load(file)

    if not isinstance(ground_truth, dict) or not isinstance(prediction, dict):
        raise ValueError("Ground truth and prediction must both be JSON objects.")

    field_metrics = calculate_metrics(ground_truth, prediction)
    list_metrics = calculate_list_metrics(ground_truth, prediction)
    similarity_metrics = calculate_list_similarity(ground_truth, prediction)

    print("\n===== FIELD-LEVEL EXACT-MATCH EVALUATION =====")
    print(f"Correct fields    : {field_metrics['correct_fields']}")
    print(f"Scored predictions: {field_metrics['total_pred']}")
    print(f"Evaluable GT fields: {field_metrics['total_gt']}")
    print(f"Unscored predictions: {field_metrics['unscored_predictions']}")
    print(f"Precision         : {field_metrics['precision']:.4f}")
    print(f"Recall            : {field_metrics['recall']:.4f}")
    print(f"F1 Score          : {field_metrics['f1']:.4f}")

    print("\n===== LIST-ITEM EXACT-MATCH EVALUATION =====")
    print(f"Correct items     : {list_metrics['correct_items']}")
    print(f"Predicted items   : {list_metrics['total_pred_items']}")
    print(f"Ground-truth items: {list_metrics['total_gt_items']}")
    print(f"Precision         : {list_metrics['precision']:.4f}")
    print(f"Recall            : {list_metrics['recall']:.4f}")
    print(f"F1 Score          : {list_metrics['f1']:.4f}")

    print("\n===== LIST CHARACTER-SIMILARITY DIAGNOSTICS =====")
    print("Warning: text similarity does not establish medical correctness.")
    for key, result in similarity_metrics["fields"].items():
        print(f"\n{key}")
        print(
            "  Ground-truth mean best-match similarity: "
            f"{result['ground_truth_mean_similarity']:.2%}"
        )
        print(
            "  Prediction mean best-match similarity:  "
            f"{result['prediction_mean_similarity']:.2%}"
        )

    print(
        "\nOverall ground-truth mean similarity: "
        f"{similarity_metrics['ground_truth_mean_similarity']:.2%}"
    )
    print(
        "Overall prediction mean similarity:  "
        f"{similarity_metrics['prediction_mean_similarity']:.2%}"
    )


if __name__ == "__main__":
    main()
