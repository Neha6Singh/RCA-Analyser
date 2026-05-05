# payment_service.py — handles payment processing for checkout flow
# BUG: process_payment does not check if user.wallet is None before calling .charge()
# This causes AttributeError when a guest user (no wallet set up) attempts checkout.

class Wallet:
    def __init__(self, balance: float):
        self.balance = balance

    def charge(self, amount: float) -> bool:
        if self.balance < amount:
            raise ValueError(f"Insufficient funds: balance={self.balance}, amount={amount}")
        self.balance -= amount
        return True


class User:
    def __init__(self, user_id: str, name: str, wallet: Wallet = None):
        self.user_id = user_id
        self.name = name
        self.wallet = wallet  # Can be None for guest users


def process_payment(user: User, amount: float) -> dict:
    """
    Processes a payment for the given user.
    Returns a dict with 'success' and 'message' keys.
    """
    if amount <= 0:
        return {"success": False, "message": "Amount must be positive"}

    # FIX: Guard against guest users who have no wallet configured
    if user.wallet is None:
        return {"success": False, "message": "No wallet configured for this user"}

    result = user.wallet.charge(amount)

    if result:
        return {"success": True, "message": f"Payment of £{amount:.2f} processed successfully"}
    return {"success": False, "message": "Payment failed"}


def get_payment_summary(user: User) -> dict:
    """Returns a summary of the user's payment account."""
    return {
        "user_id": user.user_id,
        "name": user.name,
        "wallet_balance": user.wallet.balance if user.wallet else None,
        "has_wallet": user.wallet is not None,
    }
