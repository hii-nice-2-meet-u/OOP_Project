from abc import ABC, abstractmethod
from datetime import datetime

# ==========================================
# 1. ASSETS & STRUCTURE
# ==========================================


class BoardGame:
    """Represents a physical board game asset in the shop."""

    def __init__(self, game_id: str, name: str, category: str):
        self.__game_id = game_id
        self.__category = category
        self.__name = name
        self.__status = "Available"  # Available, In_Use, Maintenance, Not_Available

    def set_status(self, status: str):
        self.__status = status

    def get_name(self):
        return self.__name


class PlayTable:
    """Represents a table where customers sit and play."""

    def __init__(self):
        pass


# ==========================================
# 2. ORDERING SYSTEM
# ==========================================


class ItemOrder:
    """A snapshot of a menu item ordered with a specific quantity."""

    def __init__(self):
        pass

# ==========================================
# 3. PAYMENT SYSTEM
# ==========================================


class PaymentMethod(ABC):
    """Abstract Base Class for Payments."""
    def __init__(self):
        pass


class Cash(PaymentMethod):
    def __init__(self, payment_id, order, amount_received: float):
        super().__init__(payment_id, order, "Cash")
        


class Card(PaymentMethod):
    def __init__(self, payment_id, order, card_no: str, bank_name: str):
        super().__init__(payment_id, order, "Card")



class OnlinePayment(PaymentMethod):
    def __init__(self, payment_id, order, transaction_ref: str):
        super().__init__(payment_id, order, "Online")

# ==========================================
# 4. RESERVATION SYSTEM
# ==========================================


class Reservation:
    def __init__(self):
        pass