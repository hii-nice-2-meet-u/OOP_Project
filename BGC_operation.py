from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Optional

# ==========================================
# 1. ASSETS & STRUCTURE
# ==========================================


class BoardGame:
    """Represents a physical board game asset in the shop."""

    def __init__(self, game_id: str, name: str, genre: str, price: float):
        self.__game_id = game_id
        self.__name = name
        self.__genre = genre
        self.__price = price
        self.__status = "Available"  # Available, In_Use, Maintenance

    def update_condition(self, status: str):
        self.__status = status 

    def get_name(self):
        return self.__name

    def get_price(self):
        return self.__price


class PlayTable:
    """Represents a table where customers sit and play."""

    def __init__(self, table_id: str, capacity: int, name: str):
        self.__table_id = table_id
        self.__capacity = capacity
        self.__status = "Available"  # Available, Occupied, Reserved
        self.__price_per_hour = 50.0
        self.__table_name = name
        self.__active_order = []

    def assign_order(self, order_obj):
        self.__active_order = order_obj
        self.__status = "Occupied"
    def calculate_price(self, hours: float):
        return self.__price_per_hour * hours
    def get_menu_ordered(self):
        return self.__active_order
    def get_table_id(self):
        return self.__table_id
    def clear_table(self):
        self.__status = "Available"
        self.__customers = []
        for game in self.__board_games:
            game.set_status("Available")
        self.__board_games = []
        self.__current_order = None

class PlayTableStandard(PlayTable):
    def __init__(self, table_id: str, capacity: int, name: str):
        super().__init__(table_id, capacity, name)
        self.__board_games: List[BoardGame] = []
        self.__active_order = []
    def add_board_game(self, board_game: BoardGame):
        self.__board_games.append(board_game)
    def remove_board_game(self, board_game: BoardGame):
        self.__board_games.remove(board_game)
class PlayTableVIP(PlayTable):
    def __init__(self, table_id: str, capacity: int, name: str, room_service_fee: float):
        super().__init__(table_id, capacity, name)
        self.__room_service_fee = room_service_fee
        self.__board_games: List[BoardGame] = []
        self.__active_order = []
    def add_board_game(self, board_game: BoardGame):
        self.__board_games.append(board_game)
    def remove_board_game(self, board_game: BoardGame):
        self.__board_games.remove(board_game)



# ==========================================
# 2. ORDERING SYSTEM
# ==========================================


class OrderItem:
    """A snapshot of a menu item ordered with a specific quantity."""

    def __init__(self, menu_item, quantity: int):
        self.__menu_item = menu_item
        self.__quantity = quantity
        # Snapshot price to prevent issues if menu price changes later
        self.__price_at_order = menu_item.get_price()
        self.__timestamp = datetime.now()
        self.__playtable = None  # To be linked when added to an order
    def get_item_total(self):
        return self.__price_at_order * self.__quantity
    def calculate_item_total(self):
        return self.__price_at_order * self.__quantity
    def check_all_served(self):
        return True  # Placeholder for actual implementation



# ==========================================
# 3. PAYMENT SYSTEM
# ==========================================


class Payment(ABC):
    """Abstract Base Class for Payments."""

    def __init__(self, payment_id: str, order: Order, method: str):
        self.__payment_id = payment_id
        self.__timestamp = datetime.now()
        self.__order = order
        self.__total_amount = order.calculate_total()
        self.__payment_method = method
        self.__status = "Pending"

    def get_total_amount(self):
        return self.__total_amount

    def complete_payment(self):
        self.__status = "Completed"
        self.__order.close_order()
        # Automatically clear all associated tables
        # In real implementation, we might access tables via getter
        pass


class Cash(Payment):
    def __init__(self, payment_id, order, amount_received: float):
        super().__init__(payment_id, order, "Cash")
        self.__amount_received = amount_received
        self.__change = amount_received - self.get_total_amount()


class Card(Payment):
    def __init__(self, payment_id, order, card_no: str, bank_name: str):
        super().__init__(payment_id, order, "Card")
        self.__card_no = card_no
        self.__bank_name = bank_name


class OnlinePayment(Payment):
    def __init__(self, payment_id, order, transaction_ref: str):
        super().__init__(payment_id, order, "Online")
        self.__transaction_ref = transaction_ref

# ==========================================
# 4. RESERVATION SYSTEM
# ==========================================


class Reservation:
    def __init__(self, res_id: str, customer, table, date_str: str, start_time_str: str, end_time_str: str, guest_count: int):
        self.__reservation_id = res_id
        self.__customer = customer
        self.__date = date_str          # Format: YYYY-MM-DD
        self.__start_time = start_time_str  # Format: HH:MM
        self.__end_time = end_time_str      # Format: HH:MM
        self.__guest_count = guest_count
        self.__status = "Pending"       # Pending, Confirmed, Cancelled, Completed
        self.__created_at = datetime.now()

    # --- Getters for Validation ---
    def get_id(self): return self.__reservation_id
    def get_table(self): return self.__table
    def get_date(self): return self.__date
    def get_status(self): return self.__status

    def get_start_datetime_obj(self):
        return datetime.strptime(f"{self.__date} {self.__start_time}", "%Y-%m-%d %H:%M")

    def get_end_datetime_obj(self):
        return datetime.strptime(f"{self.__date} {self.__end_time}", "%Y-%m-%d %H:%M")

    # --- Actions ---
    def confirm_booking(self):
        if self.__status == "Pending":
            self.__status = "Confirmed"
            return True
        return False

    def cancel_booking(self):
        if self.__status != "Completed":
            self.__status = "Cancelled"
            return True
        return False

