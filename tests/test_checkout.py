"""Unit tests for the checkout pricing rules."""

import unittest

from cart import Cart, CartItem
from checkout import Customer, calculate_total, checkout, shipping_cost


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


class CheckoutTest(unittest.TestCase):
    def test_order_summary(self):
        cart = Cart([CartItem("Mug", 8.00, 2), CartItem("Tea", 3.25)])
        order = checkout(cart, Customer("Ada"))
        self.assertEqual(order["customer"], "Ada")
        self.assertEqual(order["items"], 2)
        self.assertEqual(order["total"], 24.24)


if __name__ == "__main__":
    unittest.main()
