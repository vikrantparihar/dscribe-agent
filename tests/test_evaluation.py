import unittest

from evaluation.evaluate import calculate_metrics


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
            {"patient": {"age": "MISSING"}},
            {"patient": {"age": "MISSING"}},
        )
        self.assertEqual(result["correct_fields"], 1)

    def test_empty_inputs(self):
        result = calculate_metrics({}, {})
        self.assertEqual(result["precision"], 0.0)
        self.assertEqual(result["recall"], 0.0)
        self.assertEqual(result["f1"], 0.0)


if __name__ == "__main__":
    unittest.main()
