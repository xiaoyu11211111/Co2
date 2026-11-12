"""Unit tests for the checkout pricing rules."""

import unittest

from cart import Cart, CartItem
from checkout import (
    Customer,
    apply_student_discount,
    calculate_total,
    checkout,
    shipping_cost,
)


class ShippingCostTest(unittest.TestCase):
    def test_free_shipping_at_threshold(self):
        self.assertEqual(shipping_cost(50.00), 0.0)

    def test_free_shipping_above_threshold(self):
        self.assertEqual(shipping_cost(120.00), 0.0)

    def test_fee_charged_below_threshold(self):
        self.assertEqual(shipping_cost(49.99), 4.99)


class CalculateTotalTest(unittest.TestCase):
    def test_small_order_includes_shipping(self):
        cart = Cart([CartItem("Tea", 3.25)])
        self.assertEqual(calculate_total(cart, Customer("Ada")), 8.24)

    def test_large_order_ships_free(self):
        cart = Cart([CartItem("Coffee beans", 12.50, 8)])
        self.assertEqual(calculate_total(cart, Customer("Ada")), 100.00)

    def test_cart_type_is_validated(self):
        with self.assertRaises(TypeError):
            calculate_total([], Customer("Ada"))


class StudentDiscountTest(unittest.TestCase):
    """Feature under review: 10% discount for eligible students."""

    def test_student_pays_ninety_percent(self):
        self.assertEqual(apply_student_discount(100.00, True), 90.00)

    def test_non_student_pays_full_price(self):
        self.assertEqual(apply_student_discount(100.00, False), 100.00)

    def test_discount_is_rounded_to_cents(self):
        self.assertEqual(apply_student_discount(19.99, True), 17.99)

    def test_student_order_total_matches_exercise_example(self):
        # 8 x GBP 12.50 = GBP 100 goods, free shipping, 10% off -> GBP 90.
        cart = Cart([CartItem("Coffee beans", 12.50, 8)])
        self.assertEqual(calculate_total(cart, Customer("Ada", is_student=True)), 90.00)

    def test_non_student_order_total_is_unchanged(self):
        cart = Cart([CartItem("Coffee beans", 12.50, 8)])
        self.assertEqual(calculate_total(cart, Customer("Ada")), 100.00)

    def test_student_small_order_still_pays_shipping(self):
        # GBP 20 goods -> 10% off = GBP 18, plus GBP 4.99 shipping.
        cart = Cart([CartItem("Mug", 20.00)])
        self.assertEqual(calculate_total(cart, Customer("Ada", True)), 22.99)

    def test_student_discount_applies_to_goods_only(self):
        cart = Cart([CartItem("Tea", 3.25)])
        self.assertEqual(calculate_total(cart, Customer("Ada", True)), 7.92)


class CheckoutTest(unittest.TestCase):
    def test_order_summary(self):
        cart = Cart([CartItem("Mug", 8.00, 2), CartItem("Tea", 3.25)])
        order = checkout(cart, Customer("Ada"))
        self.assertEqual(order["customer"], "Ada")
        self.assertEqual(order["items"], 2)
        self.assertEqual(order["total"], 24.24)

    def test_order_summary_for_student(self):
        cart = Cart([CartItem("Mug", 8.00, 2), CartItem("Tea", 3.25)])
        order = checkout(cart, Customer("Ada", is_student=True))
        self.assertEqual(order["total"], 22.32)


if __name__ == "__main__":
    unittest.main()
