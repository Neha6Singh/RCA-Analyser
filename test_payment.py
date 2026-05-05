# test_payment.py — unit tests for payment_service module

import pytest
from payment_service import User, Wallet, process_payment, get_payment_summary


class TestProcessPayment:
    def test_successful_payment(self):
        """A user with a funded wallet can make a payment."""
        wallet = Wallet(balance=100.00)
        user = User(user_id="U001", name="Alice", wallet=wallet)
        result = process_payment(user, amount=49.99)
        assert result["success"] is True
        assert "49.99" in result["message"]
        assert wallet.balance == pytest.approx(50.01)

    def test_insufficient_funds(self):
        """Payment fails with insufficient funds."""
        wallet = Wallet(balance=10.00)
        user = User(user_id="U002", name="Bob", wallet=wallet)
        with pytest.raises(ValueError, match="Insufficient funds"):
            process_payment(user, amount=50.00)

    def test_invalid_amount(self):
        """Payment with zero or negative amount is rejected."""
        wallet = Wallet(balance=100.00)
        user = User(user_id="U003", name="Carol", wallet=wallet)
        result = process_payment(user, amount=0)
        assert result["success"] is False

    def test_guest_user_no_wallet(self):
        """
        Guest user with no wallet set up should get a clear error response,
        not an AttributeError crash.

        This test FAILS on the buggy version because process_payment()
        calls user.wallet.charge() without checking if wallet is None.
        """
        guest = User(user_id="GUEST-001", name="Guest User", wallet=None)
        # Should return a failure dict, not raise AttributeError
        result = process_payment(guest, amount=25.00)
        assert result["success"] is False
        assert "wallet" in result["message"].lower()


class TestGetPaymentSummary:
    def test_user_with_wallet(self):
        wallet = Wallet(balance=200.00)
        user = User(user_id="U004", name="Dave", wallet=wallet)
        summary = get_payment_summary(user)
        assert summary["has_wallet"] is True
        assert summary["wallet_balance"] == 200.00

    def test_user_without_wallet(self):
        user = User(user_id="U005", name="Eve", wallet=None)
        summary = get_payment_summary(user)
        assert summary["has_wallet"] is False
        assert summary["wallet_balance"] is None
