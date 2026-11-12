"""Unit tests for the shopping cart."""

import unittest

from cart import Cart, CartItem


class CartItemTest(unittest.TestCase):
    def test_line_total_multiplies_price_by_quantity(self):
        item = CartItem("Coffee beans", 12.50, 3)
        self.assertEqual(item.line_total, 37.50)

    def test_line_total_is_rounded_to_cents(self):
        item = CartItem("Sticker", 0.33, 3)
        self.assertEqual(item.line_total, 0.99)

    def test_quantity_must_be_positive(self):
        with self.assertRaises(ValueError):
            CartItem("Sticker", 1.00, 0)


class CartTest(unittest.TestCase):
    def test_empty_cart_has_zero_subtotal(self):
        self.assertEqual(Cart().subtotal(), 0.0)

    def test_subtotal_sums_line_totals(self):
        cart = Cart([CartItem("Mug", 8.00, 2), CartItem("Tea", 3.25)])
        self.assertEqual(cart.subtotal(), 19.25)

    def test_add_appends_item(self):
        cart = Cart().add(CartItem("Mug", 8.00))
        self.assertEqual(len(cart), 1)
        self.assertEqual(cart.subtotal(), 8.00)


if __name__ == "__main__":
    unittest.main()
