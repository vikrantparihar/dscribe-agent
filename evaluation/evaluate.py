import json

with open("ground_truth.json") as f:
    gt = json.load(f)

with open("outputs/structured_output.json") as f:
    pred = json.load(f)

def flatten(obj, prefix=""):
    items = {}

    if isinstance(obj, dict):
        for k, v in obj.items():
            items.update(
                flatten(v, f"{prefix}.{k}" if prefix else k)
            )

    elif isinstance(obj, list):
        items[prefix] = set(map(str, obj))

    else:
        items[prefix] = str(obj)

    return items

gt_flat = flatten(gt)
pred_flat = flatten(pred)

correct = 0
total_pred = len(pred_flat)
total_gt = len(gt_flat)

for key in gt_flat:
    if key in pred_flat and pred_flat[key] == gt_flat[key]:
        correct += 1

precision = correct / total_pred
recall = correct / total_gt

if precision + recall == 0:
    f1 = 0
else:
    f1 = 2 * precision * recall / (precision + recall)

print("\n===== EVALUATION =====")
print(f"Correct Fields : {correct}")
print(f"Precision      : {precision:.2f}")
print(f"Recall         : {recall:.2f}")
print(f"F1 Score       : {f1:.2f}")
