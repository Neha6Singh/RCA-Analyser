# rca-test-project

A minimal Python payment service used to verify the [RCA Bug Tracker](https://github.com) GitHub integration.

## The Bug

`payment_service.py` crashes with `AttributeError` when a guest user (no wallet) attempts checkout.

**Affected function:** `process_payment()` in `payment_service.py`  
**Root cause:** Missing null check on `user.wallet` before calling `.charge()`  
**Failing test:** `test_guest_user_no_wallet` in `test_payment.py`

## Run Tests Locally

```bash
pip install pytest
pytest test_payment.py -v
```

The `test_guest_user_no_wallet` test will **fail** on the `main` branch (the bug is present).  
The `fix/null-check-wallet` branch contains the fix — that test passes there.
