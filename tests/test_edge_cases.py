"""Edge-case tests added in the second review round.

The first Pull Request brought the student discount together with the happy
path tests.  Developer 2 then asked for the awkward cases to be covered too:
the free-shipping boundary, quantity multiplication and input validation.

These tests only use the public API of :mod:`checkout`, so they would keep
passing if the discount were reimplemented with plain floats.
"""

import unittest

from cart import Cart, CartItem
from checkout import STUDENT_DISCOUNT_RATE, Customer, calculate_total


class DiscountConstantTest(unittest.TestCase):
    def test_discount_rate_is_ten_percent(self):
        self.assertEqual(STUDENT_DISCOUNT_RATE, 0.10)


class FreeShippingBoundaryTest(unittest.TestCase):
    def test_student_at_threshold_still_ships_free(self):
        # GBP 50 goods: 10% off = GBP 45.  The threshold is measured on the
        # undiscounted subtotal, so shipping stays free.
        cart = Cart([CartItem("Desk lamp", 50.00)])
        self.assertEqual(calculate_total(cart, Customer("Ada", True)), 45.00)

    def test_student_just_below_threshold_pays_shipping(self):
        # GBP 49.99 goods: 10% off = GBP 44.99, plus GBP 4.99 shipping.
        cart = Cart([CartItem("Desk lamp", 49.99)])
        self.assertEqual(calculate_total(cart, Customer("Ada", True)), 49.98)


class QuantityTest(unittest.TestCase):
    def test_quantity_is_multiplied_before_the_discount(self):
        # 3 x GBP 20.00 = GBP 60 goods, free shipping, 10% off -> GBP 54.
        cart = Cart([CartItem("Notebook", 20.00, 3)])
        self.assertEqual(calculate_total(cart, Customer("Ada", True)), 54.00)


class InputValidationTest(unittest.TestCase):
    def test_is_student_accepts_truthy_values(self):
        self.assertIs(Customer("Ada", 1).is_student, True)

    def test_customer_type_is_validated(self):
        cart = Cart([CartItem("Tea", 3.25)])
        with self.assertRaises(TypeError):
            calculate_total(cart, "Ada")

    def test_repr_shows_the_student_flag(self):
        self.assertIn("is_student=True", repr(Customer("Ada", True)))


if __name__ == "__main__":
    unittest.main()
