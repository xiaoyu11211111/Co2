# Code review checklist

Used by the reviewer (Developer 2) and the tester (Developer 3) for every Pull
Request in this project. The exercise only requires one constructive comment,
but these are the things worth looking at, in the order that finds bugs fastest.

## 1. Correctness

- [ ] The 10% discount is applied to the goods subtotal, not to shipping.
- [ ] Non-students pay exactly the original price.
- [ ] The free-shipping threshold is measured on the **undiscounted** subtotal,
      so using the discount never costs a customer their free shipping.
- [ ] Money is rounded half up to cents, and no float noise (`17.990000000000002`)
      reaches the order total.
- [ ] Boundary values are covered: exactly £50.00, £49.99, an empty cart, and a
      quantity greater than one.

## 2. Coding standards

- [ ] Names say what the thing is (`apply_student_discount`, `is_student`).
- [ ] Every public function has a docstring that explains *why*, not just *what*.
- [ ] No magic numbers: the rate lives in `STUDENT_DISCOUNT_RATE`.
- [ ] Public functions stay free of I/O so they can be tested in isolation.

## 3. Tests

- [ ] Every behaviour added by the PR has at least one test.
- [ ] Tests fail if the feature is reverted (a test that always passes is worthless).
- [ ] Test names describe the behaviour, not the implementation.
- [ ] The whole suite passes locally: `python -m unittest discover -s tests -t . -v`.

## 4. Scope and review hygiene

- [ ] The PR does one thing; unrelated refactors are split out.
- [ ] The commit message explains the change (`Apply student discount`).
- [ ] The description states the expected numbers, not just "implements discount".
- [ ] The author has responded to every review comment.

## Giving feedback

Be specific and talk about the code, not the person:

- Good: "`3.25 * 0.9` is `2.9249999…` in binary, so `round()` gives `2.92`. Could
  we compute with `Decimal` and round half up?"
- Weak: "the rounding is wrong" — it does not say where or why.
- Always say what would make the change acceptable, and mark the comment as
  *blocking* or *nice to have*.
