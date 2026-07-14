import math
import unittest

from text_editor_tool_main import calculate_pi


class TestCalculatePi(unittest.TestCase):
    def test_value_equals_pi_to_5_digits(self):
        """calculate_pi should return pi rounded to 5 decimal places."""
        self.assertEqual(calculate_pi(), 3.14159)

    def test_matches_math_pi_rounded(self):
        """Result should match math.pi rounded to 5 decimals."""
        self.assertEqual(calculate_pi(), round(math.pi, 5))

    def test_return_type_is_float(self):
        """The function should return a float."""
        self.assertIsInstance(calculate_pi(), float)

    def test_close_to_math_pi(self):
        """Result should be within 1e-5 of the true value of pi."""
        self.assertAlmostEqual(calculate_pi(), math.pi, places=5)


if __name__ == "__main__":
    unittest.main()
