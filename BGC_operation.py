"""
Board Game Cafe - Operations Module
Handles physical assets, tables, games, reservations, and payments.
"""

from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from typing import List, Optional, Dict
from enum import Enum


# ==========================================
# CONSTANTS
# ==========================================

DEFAULT_TABLE_PRICE_PER_HOUR_THB = 50.0
VIP_ROOM_BASE_FEE_THB = 200.0
RESERVATION_GRACE_PERIOD_MINUTES = 15
CURRENCY_SYMBOL = "฿"


class GameStatus(Enum):
    """Status of board game availability."""
    AVAILABLE = "Available"
    IN_USE = "In Use"
    MAINTENANCE = "Maintenance"
    RETIRED = "Retired"


class TableStatus(Enum):
    """Status of play table."""
    AVAILABLE = "Available"
    OCCUPIED = "Occupied"
    RESERVED = "Reserved"
    MAINTENANCE = "Maintenance"


class ReservationStatus(Enum):
    """Status of reservation."""
    PENDING = "Pending"
    CONFIRMED = "Confirmed"
    CHECKED_IN = "Checked In"
    COMPLETED = "Completed"
    CANCELLED = "Cancelled"
    NO_SHOW = "No Show"


class PaymentStatus(Enum):
    """Status of payment."""
    PENDING = "Pending"
    PROCESSING = "Processing"
    COMPLETED = "Completed"
    FAILED = "Failed"
    REFUNDED = "Refunded"


# ==========================================
# BOARD GAME ASSETS
# ==========================================

class BoardGame:
    """
    Represents a physical board game asset in the shop.
    Tracks condition, availability, and usage.
    """

    def __init__(self, game_id: str, name: str, genre: str, price: float,
                 min_players: int = 2, max_players: int = 4, 
                 play_time_minutes: int = 60):
        if not game_id or not name:
            raise ValueError("Game ID and name cannot be empty")
        if price < 0:
            raise ValueError("Price cannot be negative")
        if min_players < 1 or max_players < min_players:
            raise ValueError("Invalid player count range")
        
        self._game_id = game_id
        self._name = name
        self._genre = genre
        self._price = price
        self._min_players = min_players
        self._max_players = max_players
        self._play_time_minutes = play_time_minutes
        self._status = GameStatus.AVAILABLE
        self._condition_notes = ""
        self._times_played = 0
        self._current_table = None

    @property
    def game_id(self) -> str:
        """Unique game identifier."""
        return self._game_id

    @property
    def name(self) -> str:
        """Game name."""
        return self._name

    @property
    def genre(self) -> str:
        """Game genre/category."""
        return self._genre

    @property
    def price(self) -> float:
        """Rental/usage price."""
        return self._price

    @property
    def min_players(self) -> int:
        """Minimum number of players."""
        return self._min_players

    @property
    def max_players(self) -> int:
        """Maximum number of players."""
        return self._max_players

    @property
    def play_time_minutes(self) -> int:
        """Average play time in minutes."""
        return self._play_time_minutes

    @property
    def status(self) -> GameStatus:
        """Current availability status."""
        return self._status

    @property
    def is_available(self) -> bool:
        """Check if game is available for use."""
        return self._status == GameStatus.AVAILABLE

    @property
    def times_played(self) -> int:
        """Total number of times game has been played."""
        return self._times_played

    def set_status(self, status: GameStatus) -> None:
        """Update game status."""
        self._status = status

    def update_condition(self, notes: str) -> None:
        """Update condition notes for the game."""
        self._condition_notes = notes
        if "damaged" in notes.lower() or "broken" in notes.lower():
            self._status = GameStatus.MAINTENANCE

    def mark_in_use(self, table) -> None:
        """Mark game as in use at a specific table."""
        if not self.is_available:
            raise ValueError(f"Game {self._name} is not available")
        
        self._status = GameStatus.IN_USE
        self._current_table = table
        self._times_played += 1

    def mark_available(self) -> None:
        """Mark game as available again."""
        self._status = GameStatus.AVAILABLE
        self._current_table = None

    def get_formatted_price(self) -> str:
        """Get formatted price with currency."""
        return f"{CURRENCY_SYMBOL}{self._price:.2f}"


# ==========================================
# PLAY TABLES
# ==========================================

class PlayTable(ABC):
    """
    Abstract base class for tables where customers sit and play.
    Handles table assignment, game tracking, and pricing.
    """

    def __init__(self, table_id: str, capacity: int, name: str,
                 price_per_hour: float = DEFAULT_TABLE_PRICE_PER_HOUR_THB):
        if not table_id or not name:
            raise ValueError("Table ID and name cannot be empty")
        if capacity < 1:
            raise ValueError("Capacity must be at least 1")
        if price_per_hour < 0:
            raise ValueError("Price per hour cannot be negative")
        
        self._table_id = table_id
        self._capacity = capacity
        self._table_name = name
        self._price_per_hour = price_per_hour
        self._status = TableStatus.AVAILABLE
        self._current_customers = []
        self._board_games: List[BoardGame] = []
        self._active_order = None
        self._occupied_since = None

    @property
    def table_id(self) -> str:
        """Unique table identifier."""
        return self._table_id

    @property
    def capacity(self) -> int:
        """Maximum number of people the table can accommodate."""
        return self._capacity

    @property
    def table_name(self) -> str:
        """Display name of the table."""
        return self._table_name

    @property
    def price_per_hour(self) -> float:
        """Hourly rate for the table."""
        return self._price_per_hour

    @property
    def status(self) -> TableStatus:
        """Current table status."""
        return self._status

    @property
    def is_available(self) -> bool:
        """Check if table is available."""
        return self._status == TableStatus.AVAILABLE

    @property
    def current_customers(self) -> List:
        """List of current customers at the table."""
        return self._current_customers.copy()

    @property
    def board_games(self) -> List[BoardGame]:
        """List of games currently at the table."""
        return self._board_games.copy()

    @property
    def active_order(self):
        """Current active order for the table."""
        return self._active_order

    @property
    def occupied_since(self) -> Optional[datetime]:
        """When the table was occupied."""
        return self._occupied_since

    def assign_customer(self, customer) -> None:
        """Assign a customer to the table."""
        if not self.is_available:
            raise ValueError(f"Table {self._table_name} is not available")
        
        if len(self._current_customers) >= self._capacity:
            raise ValueError(f"Table {self._table_name} is at capacity")
        
        self._current_customers.append(customer)
        self._status = TableStatus.OCCUPIED
        if self._occupied_since is None:
            self._occupied_since = datetime.now()

    def assign_order(self, order) -> None:
        """Assign an order to this table."""
        if self._status != TableStatus.OCCUPIED:
            raise ValueError("Table must be occupied to assign an order")
        
        self._active_order = order

    def add_board_game(self, board_game: BoardGame) -> None:
        """Add a board game to this table."""
        if board_game in self._board_games:
            raise ValueError(f"Game {board_game.name} is already at this table")
        
        board_game.mark_in_use(self)
        self._board_games.append(board_game)

    def remove_board_game(self, board_game: BoardGame) -> None:
        """Remove a board game from this table."""
        if board_game not in self._board_games:
            raise ValueError(f"Game {board_game.name} is not at this table")
        
        board_game.mark_available()
        self._board_games.remove(board_game)

    def calculate_table_charge(self, hours: float) -> float:
        """Calculate table rental charge for given hours."""
        if hours < 0:
            raise ValueError("Hours cannot be negative")
        return self._price_per_hour * hours

    def get_hours_occupied(self) -> float:
        """Calculate how many hours the table has been occupied."""
        if self._occupied_since is None:
            return 0.0
        
        duration = datetime.now() - self._occupied_since
        return duration.total_seconds() / 3600

    def clear_table(self) -> None:
        """Clear the table and make it available."""
        # Return all games to available status
        for game in self._board_games:
            game.mark_available()
        
        self._status = TableStatus.AVAILABLE
        self._current_customers = []
        self._board_games = []
        self._active_order = None
        self._occupied_since = None

    def set_maintenance(self) -> None:
        """Mark table as under maintenance."""
        if self._status == TableStatus.OCCUPIED:
            raise ValueError("Cannot set occupied table to maintenance")
        self._status = TableStatus.MAINTENANCE

    def get_table_summary(self) -> Dict:
        """Get summary information about the table."""
        return {
            'table_id': self._table_id,
            'name': self._table_name,
            'capacity': self._capacity,
            'status': self._status.value,
            'customer_count': len(self._current_customers),
            'game_count': len(self._board_games),
            'has_active_order': self._active_order is not None,
            'hours_occupied': self.get_hours_occupied(),
            'current_charge': self.calculate_table_charge(self.get_hours_occupied())
        }


class PlayTableStandard(PlayTable):
    """Standard play table with basic amenities."""
    
    def __init__(self, table_id: str, capacity: int, name: str,
                 price_per_hour: float = DEFAULT_TABLE_PRICE_PER_HOUR_THB):
        super().__init__(table_id, capacity, name, price_per_hour)


class PlayTableVIP(PlayTable):
    """
    VIP play table with premium amenities and private room.
    Includes additional room service fee.
    """
    
    def __init__(self, table_id: str, capacity: int, name: str,
                 room_service_fee: float = VIP_ROOM_BASE_FEE_THB,
                 price_per_hour: float = DEFAULT_TABLE_PRICE_PER_HOUR_THB):
        super().__init__(table_id, capacity, name, price_per_hour)
        self._room_service_fee = room_service_fee
        self._has_private_server = True

    @property
    def room_service_fee(self) -> float:
        """One-time room service fee for VIP room."""
        return self._room_service_fee

    @property
    def has_private_server(self) -> bool:
        """Whether VIP room has dedicated server."""
        return self._has_private_server

    def calculate_table_charge(self, hours: float) -> float:
        """Calculate total charge including room service fee."""
        base_charge = super().calculate_table_charge(hours)
        return base_charge + self._room_service_fee


# ==========================================
# RESERVATION SYSTEM
# ==========================================

class Reservation:
    """
    Represents a table reservation with validation and lifecycle management.
    """
    
    def __init__(self, reservation_id: str, customer, table: PlayTable,
                 date_str: str, start_time_str: str, end_time_str: str, 
                 guest_count: int):
        if not reservation_id:
            raise ValueError("Reservation ID cannot be empty")
        if guest_count < 1:
            raise ValueError("Guest count must be at least 1")
        if guest_count > table.capacity:
            raise ValueError(f"Guest count exceeds table capacity of {table.capacity}")
        
        # Validate and parse date/time
        try:
            self._start_datetime = datetime.strptime(
                f"{date_str} {start_time_str}", "%Y-%m-%d %H:%M"
            )
            self._end_datetime = datetime.strptime(
                f"{date_str} {end_time_str}", "%Y-%m-%d %H:%M"
            )
        except ValueError as e:
            raise ValueError(f"Invalid date/time format: {e}")
        
        if self._end_datetime <= self._start_datetime:
            raise ValueError("End time must be after start time")
        
        self._reservation_id = reservation_id
        self._customer = customer
        self._table = table
        self._guest_count = guest_count
        self._status = ReservationStatus.PENDING
        self._created_at = datetime.now()
        self._confirmed_at = None
        self._checked_in_at = None
        self._special_requests = ""
        self._cancellation_reason = ""

    @property
    def reservation_id(self) -> str:
        """Unique reservation identifier."""
        return self._reservation_id

    @property
    def customer(self):
        """Customer who made the reservation."""
        return self._customer

    @property
    def table(self) -> PlayTable:
        """Reserved table."""
        return self._table

    @property
    def guest_count(self) -> int:
        """Number of guests."""
        return self._guest_count

    @property
    def start_datetime(self) -> datetime:
        """Reservation start date and time."""
        return self._start_datetime

    @property
    def end_datetime(self) -> datetime:
        """Reservation end date and time."""
        return self._end_datetime

    @property
    def status(self) -> ReservationStatus:
        """Current reservation status."""
        return self._status

    @property
    def created_at(self) -> datetime:
        """When reservation was created."""
        return self._created_at

    @property
    def duration_hours(self) -> float:
        """Duration of reservation in hours."""
        duration = self._end_datetime - self._start_datetime
        return duration.total_seconds() / 3600

    def get_date(self) -> str:
        """Get reservation date as string."""
        return self._start_datetime.strftime("%Y-%m-%d")

    def get_start_time(self) -> str:
        """Get start time as string."""
        return self._start_datetime.strftime("%H:%M")

    def get_end_time(self) -> str:
        """Get end time as string."""
        return self._end_datetime.strftime("%H:%M")

    def confirm_booking(self) -> bool:
        """Confirm the reservation."""
        if self._status != ReservationStatus.PENDING:
            raise ValueError(f"Cannot confirm reservation with status: {self._status.value}")
        
        self._status = ReservationStatus.CONFIRMED
        self._confirmed_at = datetime.now()
        return True

    def cancel_booking(self, reason: str = "") -> bool:
        """Cancel the reservation with reason."""
        if self._status in [ReservationStatus.COMPLETED, ReservationStatus.NO_SHOW]:
            raise ValueError(f"Cannot cancel reservation with status: {self._status.value}")
        
        self._status = ReservationStatus.CANCELLED
        self._cancellation_reason = reason
        return True

    def check_in(self) -> bool:
        """Check in the customer for their reservation."""
        if self._status != ReservationStatus.CONFIRMED:
            raise ValueError("Only confirmed reservations can be checked in")
        
        current_time = datetime.now()
        
        # Check if within grace period
        grace_end = self._start_datetime + timedelta(minutes=RESERVATION_GRACE_PERIOD_MINUTES)
        if current_time > grace_end:
            self._status = ReservationStatus.NO_SHOW
            raise ValueError("Check-in time has passed grace period")
        
        self._status = ReservationStatus.CHECKED_IN
        self._checked_in_at = current_time
        self._table.assign_customer(self._customer)
        return True

    def complete(self) -> bool:
        """Mark reservation as completed."""
        if self._status != ReservationStatus.CHECKED_IN:
            raise ValueError("Only checked-in reservations can be completed")
        
        self._status = ReservationStatus.COMPLETED
        return True

    def mark_no_show(self) -> bool:
        """Mark reservation as no-show."""
        if self._status != ReservationStatus.CONFIRMED:
            raise ValueError("Only confirmed reservations can be marked as no-show")
        
        self._status = ReservationStatus.NO_SHOW
        return True

    def set_special_requests(self, requests: str) -> None:
        """Add special requests to the reservation."""
        self._special_requests = requests

    def is_upcoming(self) -> bool:
        """Check if reservation is in the future."""
        return datetime.now() < self._start_datetime

    def is_active(self) -> bool:
        """Check if reservation is currently active."""
        now = datetime.now()
        return self._start_datetime <= now <= self._end_datetime

    def get_reservation_summary(self) -> Dict:
        """Get detailed reservation summary."""
        return {
            'reservation_id': self._reservation_id,
            'customer': self._customer.name if self._customer else "Unknown",
            'table': self._table.table_name,
            'date': self.get_date(),
            'start_time': self.get_start_time(),
            'end_time': self.get_end_time(),
            'duration_hours': self.duration_hours,
            'guest_count': self._guest_count,
            'status': self._status.value,
            'created_at': self._created_at.isoformat(),
            'confirmed_at': self._confirmed_at.isoformat() if self._confirmed_at else None,
            'checked_in_at': self._checked_in_at.isoformat() if self._checked_in_at else None,
            'special_requests': self._special_requests
        }


# ==========================================
# PAYMENT SYSTEM
# ==========================================
class Payment(ABC):
    def __init__(self, payment_id: str, order, method: str):
        if not payment_id:
            raise ValueError("Payment ID cannot be empty")
        if order is None:
            raise ValueError("Order cannot be None")
        if not method:
            raise ValueError("Payment method cannot be empty")
        
        self.__payment_id = payment_id
        self.__total_amount = order.calculate_total()
        self.__payment_method = method
        self.__order = order
    def calculate_total(self) -> float:
        return self.__total_amount
    def process_payment(self) -> bool:
        self.__order.set_payment_status("Paid")
        return True
class PaymentMethod(ABC):
    def __init__(self, payment_id: str, order, method: str):
        self.__timestamp = datetime.now()
        self.__order = order
        self.__status = PaymentStatus.PENDING
        self.__completed_at = None
        self.__transaction_reference = ""

    @property
    def timestamp(self) -> datetime:
        return self.__timestamp


    @property
    def payment_method(self) -> str:
        return self.__payment_method

    @property
    def status(self) -> PaymentStatus:
        return self.__status

    @property
    def order(self):
        return self.__order

    def complete_payment(self) -> bool:
        if self._status != PaymentStatus.PENDING:
            raise ValueError(f"Cannot complete payment with status: {self._status.value}")
        
        try:
            self.__status = PaymentStatus.PROCESSING
            self.__process_transaction()
            
            self.__status = PaymentStatus.COMPLETED
            self.__completed_at = datetime.now()
            self.__order.close_order()
            if self.__order.table:
                self.__order.table.clear_table()
            if self.__order.customer:
                self.__order.customer.increment_spend(self.__total_amount)
            
            return True
        except Exception as e:
            self.__status = PaymentStatus.FAILED
            raise RuntimeError(f"Payment processing failed: {e}")

    @abstractmethod
    def __process_transaction(self) -> None:
        pass

    def refund(self, reason: str) -> bool:
        if self.__status != PaymentStatus.COMPLETED:
            raise ValueError("Only completed payments can be refunded")
        
        if not reason or len(reason) < 10:
            raise ValueError("Refund reason must be at least 10 characters")
        
        self.__status = PaymentStatus.REFUNDED
        return True



class Cash(PaymentMethod):
    def __init__(self, payment_id: str, order, amount_received: float):
        if amount_received < order.calculate_total():
            raise ValueError("Insufficient cash received")
        
        super().__init__(payment_id, order, "Cash")
        self._amount_received = amount_received
        self._change = amount_received - self.total_amount

    @property
    def amount_received(self) -> float:
        return self._amount_received

    @property
    def change(self) -> float:
        return self._change

    def _process_transaction(self) -> None:
        self._transaction_reference = f"CASH-{self._payment_id}"


class Card(Payment):
    def __init__(self, payment_id: str, order, last_four_digits: str, bank_name: str):
        if len(last_four_digits) != 4 or not last_four_digits.isdigit():
            raise ValueError("Last four digits must be exactly 4 digits")
        
        super().__init__(payment_id, order, "Card")
        self._last_four_digits = last_four_digits  # Only store last 4 digits
        self._bank_name = bank_name

    @property
    def last_four_digits(self) -> str:
        return self._last_four_digits

    @property
    def bank_name(self) -> str:
        return self._bank_name

    def _process_transaction(self) -> None:
        # In real implementation, this would integrate with payment gateway
        self._transaction_reference = f"CARD-{self._payment_id}-{self._last_four_digits}"


class OnlinePayment(PaymentMethod):
    
    def __init__(self, payment_id: str, order, transaction_ref: str, platform: str):
        if not transaction_ref:
            raise ValueError("Transaction reference cannot be empty")
        
        super().__init__(payment_id, order, "Online")
        self._transaction_reference = transaction_ref
        self._platform = platform

    @property
    def platform(self) -> str:
        return self._platform

    def _process_transaction(self) -> None:
        """API"""
        pass