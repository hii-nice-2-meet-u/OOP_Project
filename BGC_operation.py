from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Optional

# ==========================================
# 1. ASSETS & STRUCTURE
# ==========================================

class BoardGame:
    """Represents a physical board game asset in the shop."""
    def __init__(self, game_id: str, name: str, category: str, difficulty: int):
        self.__game_id = game_id
        self.__name = name
        self.__category = category
        self.__difficulty = difficulty # 1-5
        self.__status = "Available" # Available, In_Use, Maintenance

    def set_status(self, status: str):
        self.__status = status
    
    def get_name(self):
        return self.__name

class PlayTable:
    """Represents a table where customers sit and play."""
    def __init__(self, table_id: str, capacity: int):
        self.__table_id = table_id
        self.__capacity = capacity
        self.__status = "Available"  # Available, Occupied, Reserved
        self.__is_matching_enabled = False # For matching service
        self.__customers = []
        self.__board_games: List[BoardGame] = [] # Games currently at the table
        self.__current_order = None

    def assign_game(self, game: BoardGame):
        self.__board_games.append(game)
        game.set_status("In_Use")

    def return_game(self, game: BoardGame):
        if game in self.__board_games:
            self.__board_games.remove(game)
            game.set_status("Available")

    def assign_order(self, order_obj):
        self.__current_order = order_obj
        self.__status = "Occupied"

    def get_table_id(self):
        return self.__table_id

    def reset_table(self):
        """Clears the table after payment."""
        self.__status = "Available"
        self.__customers = []
        for game in self.__board_games:
            game.set_status("Available")
        self.__board_games = []
        self.__current_order = None

class Lobby(ABC):
    """Abstract Base Class for different lobby zones."""
    def __init__(self, lobby_id: str, floor: int):
        self.__lobby_id = lobby_id
        self.__floor = floor
        self.__play_tables: List[PlayTable] = []

    def add_table(self, table: PlayTable):
        self.__play_tables.append(table)

    def get_all_tables(self):
        return self.__play_tables

    @abstractmethod
    def get_service_fee_rate(self) -> float:
        pass

class NormalLobby(Lobby):
    def get_service_fee_rate(self) -> float:
        return 1.0 # Standard rate

class VIPLobby(Lobby):
    def __init__(self, lobby_id: str, floor: int, room_service_fee: float):
        super().__init__(lobby_id, floor)
        self.__room_service_fee = room_service_fee

    def get_service_fee_rate(self) -> float:
        return 1.5 # 50% extra charge

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

    def get_item_total(self):
        return self.__price_at_order * self.__quantity

class Order:
    """
    Represents an order. 
    Supports multiple tables (e.g., group booking) and incremental ordering.
    """
    def __init__(self, order_id: str, customer, tables: List[PlayTable]):
        self.__order_id = order_id
        self.__customer = customer
        self.__tables = tables
        self.__items: List[OrderItem] = []
        self.__status = "Open" # Open = Can add items, Closed = Paid
        self.__discount_rate = 0.0

    def add_item(self, menu_item, quantity: int) -> bool:
        """Allows adding items incrementally if status is Open."""
        if self.__status == "Open":
            item = OrderItem(menu_item, quantity)
            self.__items.append(item)
            return True
        return False

    def set_discount(self, rate: float):
        self.__discount_rate = rate

    def close_order(self):
        self.__status = "Closed"

    def calculate_total(self):
        subtotal = sum(item.get_item_total() for item in self.__items)
        discount = subtotal * self.__discount_rate
        return subtotal - discount

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
        self.__table = table
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

class ReservationManager:
    def __init__(self):
        self.__reservations: List[Reservation] = []

    def check_availability(self, table, date_str: str, start_str: str, end_str: str) -> bool:
        """
        Checks if the table is available during the requested time slot.
        Logic: Overlap occurs if (NewStart < OldEnd) and (NewEnd > OldStart)
        """
        fmt = "%Y-%m-%d %H:%M"
        new_start = datetime.strptime(f"{date_str} {start_str}", fmt)
        new_end = datetime.strptime(f"{date_str} {end_str}", fmt)

        for res in self.__reservations:
            # 1. Check Table match and status
            if res.get_table() == table and res.get_status() != "Cancelled":
                
                # 2. Check Date match
                if res.get_date() != date_str:
                    continue

                # 3. Check Time Overlap
                existing_start = res.get_start_datetime_obj()
                existing_end = res.get_end_datetime_obj()

                if new_start < existing_end and new_end > existing_start:
                    return False  # Overlap detected
        return True # Available

    def make_reservation(self, customer, table, date_str: str, start_str: str, end_str: str, guest_count: int) -> Optional[Reservation]:
        # Validation: Start time must be before End time
        if start_str >= end_str:
            print("Error: Invalid time range.")
            return None

        # Validation: Availability
        if not self.check_availability(table, date_str, start_str, end_str):
            print(f"Error: Table {table.get_table_id()} is booked for this time.")
            return None

        # Create Reservation
        new_id = f"RES-{len(self.__reservations) + 1:04d}"
        new_res = Reservation(new_id, customer, table, date_str, start_str, end_str, guest_count)
        self.__reservations.append(new_res)
        print(f"Success: Reservation {new_id} created.")
        return new_res

    def cancel_reservation(self, res_id: str):
        for res in self.__reservations:
            if res.get_id() == res_id:
                res.cancel_booking()
                return True
        return False