import unittest
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from tools.calculator import calculate


class TestCalculatorTool(unittest.TestCase):

    def test_basic_arithmetic(self):
        self.assertEqual(calculate("2 + 2"), "4")
        self.assertEqual(calculate("10 - 4"), "6")
        self.assertEqual(calculate("3 * 5"), "15")
        self.assertEqual(calculate("15 / 3"), "5")

    def test_operator_precedence_and_grouping(self):
        self.assertEqual(calculate("2 + 3 * 4"), "14")
        self.assertEqual(calculate("(2 + 3) * 4"), "20")
        self.assertEqual(calculate("2^3"), "8")
        self.assertEqual(calculate("2**4"), "16")

    def test_advanced_math_functions(self):
        self.assertEqual(calculate("sqrt(144)"), "12")
        self.assertEqual(calculate("factorial(5)"), "120")
        self.assertEqual(calculate("max(10, 25, 5)"), "25")
        self.assertEqual(calculate("min(10, 25, 5)"), "5")
        self.assertEqual(calculate("round(3.14159, 2)"), "3.14")
        self.assertEqual(calculate("log2(16)"), "4")

    def test_constants(self):
        result = float(calculate("pi * 2"))
        self.assertAlmostEqual(result, 6.2831853, places=4)

    def test_zero_division_guard(self):
        res = calculate("10 / 0")
        self.assertIn("Division by zero", res)

    def test_security_disallowed_syntax(self):
        # Attempt to access builtins or arbitrary code execution
        res1 = calculate("__import__('os').system('echo pwned')")
        self.assertTrue(res1.startswith("Error"))

        res2 = calculate("open('/etc/passwd')")
        self.assertTrue(res2.startswith("Error"))

        res3 = calculate("[x for x in range(10)]")
        self.assertTrue(res3.startswith("Error"))


if __name__ == "__main__":
    unittest.main()
