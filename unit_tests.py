import unittest
from app import evaluate
from app import ExpressionError

class TestEvaluate(unittest.TestCase):
    def test_whitespace_basic(self):
        self.assertEqual(evaluate("2+2"), 4)

    def test_whitespace_spaces(self):
        self.assertEqual(evaluate(" 2 + 2 "), 4)

    def test_whitespace_tabs_newlines(self):
        self.assertEqual(evaluate("\t2 +\n2"), 4)

    def test_empty_input(self):
        with self.assertRaises(ExpressionError) as context:
            evaluate("")
        self.assertEqual(str(context.exception), "Expression is empty")

    def test_malformed_operator_only(self):
        with self.assertRaises(ExpressionError) as context:
            evaluate("+")
        self.assertEqual(str(context.exception), "Missing operand")

    def test_malformed_incomplete_expression(self):
        with self.assertRaises(ExpressionError) as context:
            evaluate("2 +")
        self.assertEqual(str(context.exception), "Missing operand")

    def test_invalid_character_letter(self):
        with self.assertRaises(ExpressionError) as context:
            evaluate("2 + a")
        self.assertEqual(str(context.exception), "Invalid character in expression")

    def test_invalid_character_symbol(self):
        with self.assertRaises(ExpressionError) as context:
            evaluate("2 + #3")
        self.assertEqual(str(context.exception), "Invalid character in expression")

    def test_consecutive_operators_plus(self):
        with self.assertRaises(ExpressionError) as context:
            evaluate("2 ++ 2")
        self.assertEqual(str(context.exception), "Missing operand")

    def test_consecutive_operators_mix(self):
        with self.assertRaises(ExpressionError) as context:
            evaluate("2 +* 3")
        self.assertEqual(str(context.exception), "Missing operand")

    # NEGATIVE NUMBERS TESTS ENFORCING RULE

    # Only negative numbers inside parentheses allowed.

    def test_negative_number_prefix(self):
        # -5 alone is invalid
        with self.assertRaises(ExpressionError) as context:
            evaluate("-5 + 3")
        self.assertEqual(str(context.exception), "Missing operand")

    def test_negative_after_operator(self):
        # 2 * -3 invalid
        with self.assertRaises(ExpressionError) as context:
            evaluate("2 * -3")
        self.assertEqual(str(context.exception), "Missing operand")

    def test_negative_in_parens(self):
        # -(3) invalid
        with self.assertRaises(ExpressionError) as context:
            evaluate("-(3)")
        self.assertEqual(str(context.exception), "Missing operand")

    def test_double_negative(self):
        # -(-3) invalid
        with self.assertRaises(ExpressionError) as context:
            evaluate("-(-3)")
        self.assertEqual(str(context.exception), "Missing operand")

    # These are valid:
    def test_negative_inside_parens(self):
        self.assertEqual(evaluate("2 + (-3)"), -1)

    def test_single_negative_paren(self):
        self.assertEqual(evaluate("(-3)"), -3)

    # Floating point tests

    def test_floating_point_basic(self):
        self.assertAlmostEqual(evaluate("3.14 + 2.0"), 5.14, places=9)

    def test_floating_point_small_times_large(self):
        self.assertAlmostEqual(evaluate("0.0000001 * 10000000"), 1.0, places=9)

    def test_floating_point_no_leading_zero(self):
        self.assertAlmostEqual(evaluate(".5 + .5"), 1.0, places=9)

    # Operator precedence

    def test_precedence_mult_first(self):
        self.assertEqual(evaluate("2 + 3 * 4"), 14)

    def test_precedence_add_last(self):
        self.assertEqual(evaluate("2 * 3 + 4"), 10)

    def test_precedence_combined(self):
        self.assertEqual(evaluate("3 + 4 * 2 / (1 - 5) % 2"), 3)

    # Parentheses tests

    def test_parentheses_basic(self):
        self.assertEqual(evaluate("2 * (3 + 4)"), 14)

    def test_parentheses_nested(self):
        self.assertEqual(evaluate("2 * (3 + (4 - 1))"), 12)

    def test_parentheses_unclosed(self):
        with self.assertRaises(ExpressionError) as context:
            evaluate("(2 + 3")
        self.assertEqual(str(context.exception), "Mismatched parentheses")

    def test_parentheses_unopened(self):
        with self.assertRaises(ExpressionError) as context:
            evaluate("2 + 3)")
        self.assertEqual(str(context.exception), "Mismatched parentheses")

    def test_parentheses_extra(self):
        self.assertEqual(evaluate("((((1 + 2))))"), 3)

    def test_parentheses_multiple_nested(self):
        self.assertEqual(evaluate("(((1 + (2 + (3 + 4)))))"), 10)

    # Division tests

    def test_division_fraction(self):
        self.assertEqual(evaluate("1 / 2"), 0.5)

    def test_division_by_zero(self):
        with self.assertRaises(ExpressionError) as context:
            evaluate("1 / 0")
        self.assertEqual(str(context.exception), "Division by zero")

    def test_division_zero_numerator(self):
        self.assertEqual(evaluate("0 / 1"), 0)

    # Modulo tests

    def test_modulo_basic(self):
        self.assertEqual(evaluate("5 % 2"), 1)

    def test_modulo_negative(self):
        with self.assertRaises(ExpressionError) as context:
            evaluate("-5 % 3")
        self.assertEqual(str(context.exception), "Missing operand")

    def test_modulo_zero_divisor(self):
        with self.assertRaises(ExpressionError) as context:
            evaluate("5 % 0")
        self.assertEqual(str(context.exception), "Modulo by zero")

    def test_modulo_float(self):
        self.assertEqual(evaluate("10 % 3.0"), 1)

    # Precision tests

    def test_precision_01_plus_02(self):
        self.assertAlmostEqual(evaluate("0.1 + 0.2"), 0.3, places=9)

    def test_chained_operations(self):
        self.assertEqual(evaluate("1 + 2 + 3 + 4 * 5 - 6 / 2"), 1 + 2 + 3 + 20 - 3)

    # Syntax tests

    def test_syntax_double_plus(self):
        with self.assertRaises(ExpressionError) as context:
            evaluate("1 + + 2")
        self.assertEqual(str(context.exception), "Missing operand")

    def test_syntax_concatenated_numbers(self):
        with self.assertRaises(ExpressionError) as context:
            evaluate("2 2")
        self.assertEqual(str(context.exception), "Missing operator before number")

    def test_syntax_implicit_multiplication(self):
        with self.assertRaises(ExpressionError) as context:
            evaluate("(1)(2)")
        self.assertEqual(str(context.exception), "Missing operator before '('")

    def test_invalid_number_double_dot(self):
        with self.assertRaises(ExpressionError) as context:
            evaluate("3..4 + 2")
        self.assertEqual(str(context.exception), "Invalid number format")

    def test_invalid_bytes(self):
        with self.assertRaises(ExpressionError) as context:
            evaluate("\xFF\xFF")
        self.assertEqual(str(context.exception), "Invalid character in expression")

    # Spacing tests

    def test_spacing_around_operators(self):
        self.assertEqual(evaluate(" (  3+4 ) "), 7)

    def test_spacing_nested_parentheses(self):
        self.assertEqual(evaluate("3+( 4 * (2+1))"), 15)

    def test_spacing_extra_parentheses(self):
        self.assertEqual(evaluate("((3))"), 3)

    # Whitespace in number test

    def test_whitespace_in_number(self):
        with self.assertRaises(ExpressionError) as context:
            evaluate("12 34")
        self.assertEqual(str(context.exception), "Missing operator before number")

    # Operator position tests

    def test_operator_position_start(self):
        with self.assertRaises(ExpressionError) as context:
            evaluate("*2+3")
        self.assertEqual(str(context.exception), "Missing operand")

    def test_operator_position_end(self):
        with self.assertRaises(ExpressionError) as context:
            evaluate("2+3-")
        self.assertEqual(str(context.exception), "Missing operand")

    def test_operator_before_parens(self):
        with self.assertRaises(ExpressionError) as context:
            evaluate("*(2+3)")
        self.assertEqual(str(context.exception), "Missing operand")

    # Dot tests

    def test_dot_alone(self):
        with self.assertRaises(ExpressionError) as context:
            evaluate(".")
        self.assertEqual(str(context.exception), "Invalid number format")

    def test_dot_end_of_number(self):
       self.assertEqual(evaluate("3."), 3.0)  

    def test_dot_start_of_number(self):
        try:
            evaluate(".3")
        except Exception:
            self.fail("evaluate('.3') raised Exception unexpectedly!")

    # Large expression test

    def test_large_expression(self):
        expr = "1" + "+1" * 1000
        self.assertEqual(evaluate(expr), 1001)

if __name__ == "__main__":
    unittest.main()
