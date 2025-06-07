#test_rpn_calculator

import unittest
from app import(
  calculate_rpn_method
  
)
from app import InvalidRPNString


class CalculateRPNTest(unittest.TestCase):

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
       result = calculate_rpn_method("5")
       self.assertEqual(result, 5.0)

    def test_single_operator_input(self):
       with self.assertRaises(InvalidRPNString) as context:
          calculate_rpn_method("+")
       self.assertEqual(str(context.exception), "too few arguments")

    def test_leading_trailing_spaces(self):
       result = calculate_rpn_method("   3 4 +   ")
       self.assertEqual(result, 7.0)


    def test_power_positive_exponent(self):
        result = calculate_rpn_method("2 3 ^")
        self.assertEqual(result, 8.0)

    def test_power_zero_exponent(self):
        result = calculate_rpn_method("5 0 ^")
        self.assertEqual(result, 1.0)

    def test_power_zero_base(self):
        result = calculate_rpn_method("0 5 ^")
        self.assertEqual(result, 0.0)

    def test_power_negative_exponent(self):
        result = calculate_rpn_method("2 -2 ^")
        self.assertEqual(result, 0.25)

    def test_mixed_arithmetic_with_power_and_division(self):
    
       result = calculate_rpn_method("3 2 + 4 * 2 2 ^ /")
       self.assertEqual(result, 5.0)

    def test_power_modulus_addition(self):
    
       result = calculate_rpn_method("2 3 ^ 5 % 1 +")
       self.assertEqual(result, 4.0)

    def test_full_operator_chain(self):
   
       result = calculate_rpn_method("10 3 % 2 + 5 3 - 2 ^ *")
       self.assertEqual(result, 12.0)

    def test_power_zero_base(self):
        self.assertEqual(calculate_rpn_method("0 5 ^"), 0.0)

    def test_power_zero_exponent(self):
        self.assertEqual(calculate_rpn_method("5 0 ^"), 1.0)

    def test_modulus_zero_result(self):
        self.assertEqual(calculate_rpn_method("9 3 %"), 0.0)

    def test_modulus_by_zero_raises(self):
        with self.assertRaises(InvalidRPNString) as context:
            calculate_rpn_method("10 0 %")
        self.assertEqual(str(context.exception), "cannot modulo by 0")

    def test_negative_base_fractional_exponent_raises(self):
        with self.assertRaises(InvalidRPNString) as context:
            calculate_rpn_method("-2 0.5 ^")
        self.assertEqual(str(context.exception), "invalid power operation")

    def test_large_power_overflow_raises(self):
        with self.assertRaises(InvalidRPNString) as context:
            calculate_rpn_method("99 130 ^")
        self.assertEqual(str(context.exception), "numerical overflow or invalid result")

    def test_operator_with_no_operands(self):
        with self.assertRaises(InvalidRPNString) as context:
            calculate_rpn_method("^")
        self.assertEqual(str(context.exception), "too few arguments")

    def test_only_one_operand_then_operator(self):
        with self.assertRaises(InvalidRPNString) as context:
            calculate_rpn_method("5 ^")
        self.assertEqual(str(context.exception), "too few arguments")

    def test_extra_values_left_on_stack(self):
        with self.assertRaises(InvalidRPNString) as context:
            calculate_rpn_method("3 4 + 2")
        self.assertEqual(str(context.exception), "too many arguments")


if __name__ == "__main__":
    unittest.main()


