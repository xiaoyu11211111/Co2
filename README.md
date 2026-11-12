# Online Shopping Application

A tiny teaching project for the *Collaborative Software Development* exercise
(Jiangxi Normal University, Exercise 2).

It contains just enough of a shop to practise the Git workflow: a shopping
cart, the checkout pricing rules, and unit tests.

## Layout

| Path | Purpose |
| --- | --- |
| `cart.py` | `CartItem` and `Cart`: what the customer picked, and the goods subtotal. |
| `checkout.py` | Shipping rules, `Customer`, `calculate_total()` and the `checkout()` entry point. |
| `tests/` | `unittest` suite for both modules. |

## Requirements

Python 3.8 or newer.  No third-party packages are needed.

## Running the tests

```bash
python -m unittest discover -s tests -t . -v
```

## Pricing rules

* Goods subtotal = sum of `unit_price * quantity` for every line.
* Shipping is free for orders of £50.00 or more, otherwise a flat £4.99.
* Students get 10% off the goods subtotal (`apply_student_discount()`). The
  free-shipping threshold is still measured on the undiscounted subtotal, so
  using the discount never costs a student their free shipping.
* Money is rounded half up to cents, and the discount is computed with
  `Decimal` so no floating point noise reaches the order total.
* `checkout()` returns a small order summary dictionary instead of touching a
  database, so the rules can be tested in isolation.

## Contributing

Do not commit directly to `main`.  Create a short-lived feature branch, add
tests for the behaviour you change, and open a Pull Request for review.

## Branching and review workflow

Every branch is a short-lived topic branch that becomes exactly one Pull
Request.  `main` is only ever advanced by merging an approved PR.

| Branch | Purpose | Review state |
| --- | --- | --- |
| `main` | Baseline: cart and checkout, no student discount. | protected |
| `add-discount` | Feature: 10% student discount at checkout. | ready for review |
| `add-tests` | Extra edge-case tests requested during review. | open |
| `add-docs` | Documentation: PR template and review checklist. | open |

The rules the team agreed on:

1. Never commit to `main` directly; open a PR instead.
2. One topic per branch, one branch per PR.
3. A PR needs at least one constructive review comment and an approval before
   it is merged.
4. Merge only when the full test suite passes locally (and in CI, once there is
   one).

Supporting documents:

* `docs/pull-request-template.md` - fill this in for every PR.
* `docs/review-checklist.md` - what the reviewer and tester check before
  approving.
