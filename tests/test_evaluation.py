import unittest

from evaluation.evaluate import calculate_list_metrics, calculate_metrics


class TestEvaluation(unittest.TestCase):
    def test_exact_match(self):
        result = calculate_metrics(
            {"name": "Vikrant"},
            {"name": "Vikrant"},
        )
        self.assertEqual(result["correct_fields"], 1)
        self.assertEqual(result["f1"], 1.0)

    def test_mismatch(self):
        result = calculate_metrics(
            {"gender": "female"},
            {"gender": "MISSING"},
        )
        self.assertEqual(result["correct_fields"], 0)
        self.assertEqual(result["f1"], 0.0)

    def test_nested_match(self):
        result = calculate_metrics(
            {"patient": {"age": "42"}},
            {"patient": {"age": "42"}},
        )
        self.assertEqual(result["correct_fields"], 1)

    def test_empty_inputs(self):
        result = calculate_metrics({}, {})
        self.assertEqual(result["precision"], 0.0)
        self.assertEqual(result["recall"], 0.0)
        self.assertEqual(result["f1"], 0.0)

    def test_ground_truth_missing_is_not_evaluable(self):
        result = calculate_metrics(
            {"age": "MISSING", "gender": "female"},
            {"age": "MISSING", "gender": "female"},
        )
        self.assertEqual(result["correct_fields"], 1)
        self.assertEqual(result["total_gt"], 1)
        self.assertEqual(result["f1"], 1.0)

    def test_case_and_whitespace_normalization(self):
        result = calculate_metrics(
            {"name": " Vikrant "},
            {"name": "vikrant"},
        )
        self.assertEqual(result["correct_fields"], 1)

    def test_extra_prediction_is_reported_as_unscored(self):
        result = calculate_metrics(
            {"name": "Vikrant"},
            {"name": "Vikrant", "extra": "unexpected"},
        )
        self.assertEqual(result["correct_fields"], 1)
        self.assertAlmostEqual(result["precision"], 1.0)
        self.assertEqual(result["recall"], 1.0)
        self.assertEqual(result["unscored_predictions"], 1)

    def test_missing_prediction_counts_as_false_negative(self):
        result = calculate_metrics(
            {"name": "Vikrant", "gender": "female"},
            {"name": "Vikrant"},
        )
        self.assertEqual(result["correct_fields"], 1)
        self.assertEqual(result["total_gt"], 2)
        self.assertAlmostEqual(result["recall"], 0.5)

    def test_empty_ground_truth_reports_predictions_as_unscored(self):
        result = calculate_metrics(
            {"medications": {}},
            {"medications": {"example": {"frequency": "daily"}}},
        )
        self.assertEqual(result["total_gt"], 0)
        self.assertEqual(result["total_pred"], 0)
        self.assertEqual(result["unscored_predictions"], 1)

    def test_list_item_metrics_partial_match(self):
        result = calculate_list_metrics(
            {"diagnoses": ["A", "B"]},
            {"diagnoses": ["A", "C"]},
        )
        self.assertEqual(result["correct_items"], 1)
        self.assertAlmostEqual(result["precision"], 0.5)
        self.assertAlmostEqual(result["recall"], 0.5)
        self.assertAlmostEqual(result["f1"], 0.5)

    def test_list_metrics_handle_duplicates(self):
        result = calculate_list_metrics(
            {"diagnoses": ["A", "A"]},
            {"diagnoses": ["A"]},
        )
        self.assertEqual(result["correct_items"], 1)
        self.assertEqual(result["precision"], 1.0)
        self.assertEqual(result["recall"], 0.5)


if __name__ == "__main__":
    unittest.main()


def test_missing_predicted_list_counts_ground_truth_items():
    from evaluation.evaluate import calculate_list_metrics

    result = calculate_list_metrics(
        {"diagnoses": ["A", "B"]},
        {},
    )

    assert result["correct_items"] == 0
    assert result["total_gt_items"] == 2
    assert result["total_pred_items"] == 0
    assert result["recall"] == 0.0


def test_extra_predicted_list_items_are_counted():
    from evaluation.evaluate import calculate_list_metrics

    result = calculate_list_metrics(
        {"diagnoses": ["A"]},
        {"diagnoses": ["A"], "procedures": ["X"]},
    )

    assert result["correct_items"] == 1
    assert result["total_gt_items"] == 1
    assert result["total_pred_items"] == 2
    assert result["precision"] == 0.5
    assert result["recall"] == 1.0
