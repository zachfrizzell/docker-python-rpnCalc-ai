#test_ai_rpn_calculator

import unittest
from app import(
  calculate_rpn_method
  
)
from ai_rpn_calculator import InvalidRPNString


# Assuming calculate_rpn_method is implemented like in previous messages
# from your_rpn_module import calculate_rpn_method, InvalidRPNString

class CalculateRPNTest(unittest.TestCase):

    # === BASIC FUNCTIONALITY TESTS ===
    #Test
    def test_addition_string(self):
        result = calculate_rpn_method("2 2 +")
        self.assertAlmostEqual(result, 4.0, places=2)

    def test_subtraction(self):
        result = calculate_rpn_method("2 2 -")
        self.assertAlmostEqual(result, 0.0, places=2)

    def test_multiplication(self):
        result = calculate_rpn_method("2 2 *")
        self.assertAlmostEqual(result, 4.0, places=2)

    def test_division(self):
        result = calculate_rpn_method("2 2 /")
        self.assertAlmostEqual(result, 1.0, places=2)

    # === ERROR HANDLING TESTS ===

    def test_divide_by_zero(self):
        with self.assertRaises(InvalidRPNString) as context:
            calculate_rpn_method("2 0 /")
        self.assertEqual(str(context.exception), "cannot divide by 0")

    def test_not_enough_numbers(self):
        with self.assertRaises(InvalidRPNString) as context:
            calculate_rpn_method("2 2 2 + - *")
        self.assertEqual(str(context.exception), "too few arguments")

    def test_too_many_numbers(self):
        with self.assertRaises(InvalidRPNString) as context:
            calculate_rpn_method("3 2 2 + - 5")
        self.assertEqual(str(context.exception), "too many arguments")

    def test_invalid_character(self):
        with self.assertRaises(InvalidRPNString) as context:
            calculate_rpn_method("2 2 a +")
        self.assertEqual(str(context.exception), "invalid character")

    def test_empty_string(self):
        with self.assertRaises(InvalidRPNString) as context:
            calculate_rpn_method("")
        self.assertEqual(str(context.exception), "empty")

    def test_multiple_operand_rpn_string(self):
        result = calculate_rpn_method("2 3 4 + *")
        self.assertAlmostEqual(result, 14.0, places=2)

    # === ADVANCED AND EDGE CASES ===

    def test_floating_point_addition(self):
        result = calculate_rpn_method("3.5 2.2 +")
        self.assertAlmostEqual(result, 5.7, places=2)

    def test_long_rpn_expression(self):
        result = calculate_rpn_method("1 2 + 3 + 4 + 5 + 6 + 7 + 8 + 9 +")
        self.assertAlmostEqual(result, 45.0, places=2)

    def test_negative_numbers(self):
        result = calculate_rpn_method("-2 4 *")
        self.assertAlmostEqual(result, -8.0, places=2)

    def test_irregular_whitespace(self):
        result = calculate_rpn_method("2    3\t+")
        self.assertAlmostEqual(result, 5.0, places=2)

    def test_unsupported_operator(self):
        with self.assertRaises(InvalidRPNString) as context:
            calculate_rpn_method("4 2 %")
        self.assertEqual(str(context.exception), "invalid character")

    def test_consecutive_operators(self):
        with self.assertRaises(InvalidRPNString) as context:
            calculate_rpn_method("2 + +")
        self.assertEqual(str(context.exception), "too few arguments")

    def test_negative_zero_division(self):
        with self.assertRaises(InvalidRPNString) as context:
            calculate_rpn_method("2 -0 /")
        self.assertEqual(str(context.exception), "cannot divide by 0")

    def test_garbage_input(self):
        with self.assertRaises(InvalidRPNString) as context:
            calculate_rpn_method("banana 3 +")
        self.assertEqual(str(context.exception), "invalid character")

    def test_deep_nested_expression(self):
        result = calculate_rpn_method("5 1 2 + 4 * + 3 -")
        self.assertAlmostEqual(result, 14.0, places=2)

    def test_multiple_sequential_calculations(self):
        result1 = calculate_rpn_method("3 4 +")
        result2 = calculate_rpn_method("5 6 +")
        self.assertAlmostEqual(result1, 7.0, places=2)
        self.assertAlmostEqual(result2, 11.0, places=2)

    def test_numerical_overflow(self):
       with self.assertRaises(InvalidRPNString) as context:
          calculate_rpn_method("1e308 1e308 +")
       self.assertEqual(str(context.exception), "numerical overflow or invalid result")

    def test_rpn_expression_too_long(self):
       long_expression = "1 " * 1001 + "+ " * 1000  # 2001 tokens
       with self.assertRaises(InvalidRPNString) as context:
          calculate_rpn_method(long_expression.strip())
       self.assertEqual(str(context.exception), "input too long")

    def test_whitespace_only_string(self):
       with self.assertRaises(InvalidRPNString) as context:
          calculate_rpn_method("      \t\n  ")
       self.assertEqual(str(context.exception), "empty")

    def test_single_number_input(self):
       with self.assertRaises(InvalidRPNString) as context:
          calculate_rpn_method("5")
       self.assertEqual(str(context.exception), "too many arguments")

    def test_single_operator_input(self):
       with self.assertRaises(InvalidRPNString) as context:
          calculate_rpn_method("+")
       self.assertEqual(str(context.exception), "too few arguments")

    def test_leading_trailing_spaces(self):
       result = calculate_rpn_method("   3 4 +   ")
       self.assertEqual(result, 7.0)




if __name__ == "__main__":
    unittest.main()

