from datetime import datetime
from typing import List, Optional
from abc import ABC, abstractmethod

# ==========================================
# 1. ASSETS & STRUCTURE
# ==========================================


class PlayTable:
    def __init__(self, table_id: str, capacity: int):
        self.__table_id = table_id
        self.__capacity = capacity
        self.__status = "Available"  # Available, Occupied, Reserved
        self.__is_matching_enabled = False
        self.__customers = []
        self.__board_games = []
        self.__current_order = None

    def set_matching(self, status: bool):
        self.__is_matching_enabled = status

    def assign_order(self, order_obj):
        self.__current_order = order_obj
        self.__status = "Occupied"

    def get_table_id(self):
        return self.__table_id

    def reset_table(self):
        self.__status = "Available"
        self.__customers = []
        self.__board_games = []
        self.__current_order = None


class Lobby(ABC):
    def __init__(self, lobby_id: str, floor: int):
        self.__lobby_id = lobby_id
        self.__floor = floor
        self.__play_tables: List['PlayTable'] = []

    def add_table(self, table: 'PlayTable'):
        self.__play_tables.append(table)

    @abstractmethod
    def get_service_fee(self) -> float:
        pass

    def get_tables(self):
        return self.__play_tables


class NormalLobby(Lobby):
    def __init__(self, lobby_id: str, floor: int):
        super().__init__(lobby_id, floor)
        self.__zone_name = "Common Zone"

    def get_service_fee(self) -> float:
        return 0.0


class VIPLobby(Lobby):
    def __init__(self, lobby_id: str, floor: int, room_service_fee: float):
        super().__init__(lobby_id, floor)
        self.__room_service_fee = room_service_fee
        self.__has_private_ac = True

    def get_service_fee(self) -> float:
        return self.__room_service_fee

# ==========================================
# 2. ORDERING SYSTEM
# ==========================================


class OrderItem:
    def __init__(self, menu_item, quantity: int):
        self.__menu_item = menu_item
        self.__quantity = quantity
        self.__price_at_order = menu_item.get_price()
        self.__timestamp = datetime.now()

    def get_item_total(self):
        return self.__price_at_order * self.__quantity


class Order:
    def __init__(self, order_id: str, customer, tables: List[PlayTable]):
        self.__order_id = order_id
        self.__customer = customer
        self.__tables = tables
        self.__items: List[OrderItem] = []
        self.__status = "Open"
        self.__discount_rate = 0.0

    def add_item(self, menu_item, quantity: int):

        if self.__status == "Open":
            item = OrderItem(menu_item, quantity)
            self.__items.append(item)
            return True
        return False

    def set_discount(self, rate: float):
        self.__discount_rate = rate

    def calculate_total(self):
        subtotal = sum(item.get_item_total() for item in self.__items)
        discount = subtotal * self.__discount_rate
        return subtotal - discount

# ==========================================
# 3. PAYMENT SYSTEM
# ==========================================


class Payment(ABC):
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

    @abstractmethod
    def validate_payment(self) -> bool:
        pass


class Cash(Payment):
    def __init__(self, payment_id, order, amount_received: float):
        super().__init__(payment_id, order, "Cash")
        self.__amount_received = amount_received
        self.__change = amount_received - self.get_total_amount()

    def validate_payment(self) -> bool:
        pass


class Card(Payment):
    def __init__(self, payment_id, order, card_no: str):
        super().__init__(payment_id, order, "Card")
        self.__card_no = card_no

    def validate_payment(self) -> bool:
        pass


class OnlinePayment(Payment):
    def __init__(self, payment_id, order, transaction_ref: str):
        super().__init__(payment_id, order, "Online")
        self.__transaction_ref = transaction_ref

    def validate_payment(self) -> bool:
        pass


# ==========================================
# 4. RESERVATION SYSTEM (Time Range Support)
# ==========================================

class Reservation:
    def __init__(self, res_id: str, customer, table, date_str: str, start_time_str: str, end_time_str: str, guest_count: int):
        self.__reservation_id = res_id
        self.__customer = customer
        self.__table = table
        self.__date = date_str        # Format: YYYY-MM-DD
        self.__start_time = start_time_str  # Format: HH:MM
        self.__end_time = end_time_str      # Format: HH:MM
        self.__guest_count = guest_count
        self.__status = "Pending"     # Pending, Confirmed, Cancelled, Completed, No-Show, In-Play
        self.__created_at = datetime.now()

    def get_id(self):
        return self.__reservation_id

    def get_table(self):
        return self.__table

    def get_date(self):
        return self.__date

    def get_start_time(self):
        return self.__start_time

    def get_end_time(self):
        return self.__end_time
    
    def get_start_datetime_obj(self):
        return datetime.strptime(f"{self.__date} {self.__start_time}", "%Y-%m-%d %H:%M")

    def get_end_datetime_obj(self):
        return datetime.strptime(f"{self.__date} {self.__end_time}", "%Y-%m-%d %H:%M")

    def get_status(self):
        return self.__status

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

    def check_in(self):
        if self.__status == "Confirmed":
            self.__status = "Completed"
            return True
        return False


class ReservationManager:
    def __init__(self):
        self.__reservations: List[Reservation] = []

    def check_availability(self, table, date_str: str, start_str: str, end_str: str) -> bool:
        
        fmt = "%Y-%m-%d %H:%M"
        new_start = datetime.strptime(f"{date_str} {start_str}", fmt)
        new_end = datetime.strptime(f"{date_str} {end_str}", fmt)

        for res in self.__reservations:
            if res.get_table() == table and res.get_status() != "Cancelled":
                
                
                if res.get_date() != date_str:
                    continue

                
                existing_start = res.get_start_datetime_obj()
                existing_end = res.get_end_datetime_obj()

                
                if new_start < existing_end and new_end > existing_start:
                    return False  
                    
        return True 

    def make_reservation(self, customer, table, date_str: str, start_str: str, end_str: str, guest_count: int) -> Optional[Reservation]:
        
        if start_str >= end_str:
            print("Error: Start time must be before end time.")
            return None

        
        if not self.check_availability(table, date_str, start_str, end_str):
            print(f"Error: Table {table.get_table_id()} is already booked during {start_str}-{end_str}.")
            return None

        
        new_id = f"RES-{len(self.__reservations) + 1:04d}"
        new_reservation = Reservation(new_id, customer, table, date_str, start_str, end_str, guest_count)
        
        self.__reservations.append(new_reservation)
        print(f"Success: Reservation {new_id} created for {date_str} ({start_str} - {end_str}).")
        return new_reservation

    def cancel_reservation(self, reservation_id: str):
        for res in self.__reservations:
            if res.get_id() == reservation_id:
                if res.cancel_booking():
                    print(f"Reservation {reservation_id} has been cancelled.")
                    return True
                else:
                    print(f"Cannot cancel reservation {reservation_id} (Status: {res.get_status()}).")
                    return False
        print("Reservation ID not found.")
        return False

    def get_daily_reservations(self, date_str: str):
        
        daily_list = []
        for res in self.__reservations:
            if res.get_date() == date_str:
                daily_list.append(res)
        return daily_list