from abc import ABC, abstractmethod
from datetime import datetime
from enum import Enum
from typing import Optional

# ==========================================
# 1. ENUMERATIONS
# ==========================================

class TierEnum(Enum):
    SILVER = "Silver"
    GOLD = "Gold"
    PLATINUM = "Platinum"


# ==========================================
# 2. BASE PERSON HIERARCHY
# ==========================================

class Person(ABC):
    
    def __init__(self, person_id: str, name: str, contact: str):
        self.__person_id = person_id
        self.__name = name
        self.__contact = contact

    @property
    def person_id(self) -> str:
        return self.__person_id

    @property
    def name(self) -> str:
        return self.__name

    @property
    def contact(self) -> str:
        return self.__contact

    def update_contact(self, new_contact: str):
        """Update contact information."""
        self.__contact = new_contact


# ==========================================
# 3. STAFF HIERARCHY (Internal Actors)
# ==========================================

class Staff(Person):
    
    def __init__(self, person_id: str, name: str, contact: str, salary: float):
        super().__init__(person_id, name, contact)
        self.__salary = salary
        self.__staff_id = person_id

    @property
    def salary(self) -> float:
        return self.__salary

    @property
    def staff_id(self) -> str:
        return self.__staff_id

    def take_order(self, order) -> bool:
        try:
            # Implementation would validate and process the order
            return True
        except Exception as e:
            print(f"Error taking order: {e}")
            return False

    def serve_item(self, order) -> bool:
        try:
            return True
        except Exception as e:
            print(f"Error serving item: {e}")
            return False

    def assign_table(self, table, customer) -> bool:
        try:
            return True
        except Exception as e:
            print(f"Error assigning table: {e}")
            return False

    def check_booking_status(self, reservation) -> str:
        return "confirmed"

    def assign_walk_in_customer(self, customer) -> bool:
        """Assign a walk-in customer to a table."""
        try:
            return True
        except Exception as e:
            print(f"Error assigning walk-in: {e}")
            return False

    def register_walk_in_customer(self, customer) -> bool:
        try:
            return True
        except Exception as e:
            print(f"Error registering customer: {e}")
            return False

    def handle_check_in(self, reservation) -> bool:
        try:
            return True
        except Exception as e:
            print(f"Error during check-in: {e}")
            return False


class Manager(Person):
    
    def __init__(self, person_id: str, name: str, contact: str, salary: float):
        super().__init__(person_id, name, contact)
        self.__salary = salary

    def approve_void_bill(self, transaction) -> bool:
        try:
            return True
        except Exception as e:
            print(f"Error approving void: {e}")
            return False

    def add_staff(self, staff: Staff) -> bool:
        try:
            return True
        except Exception as e:
            print(f"Error adding staff: {e}")
            return False

    def remove_staff(self, staff_id: str) -> bool:
        try:
            return True
        except Exception as e:
            print(f"Error removing staff: {e}")
            return False

    def override_inventory_stock(self, item, new_quantity: int) -> bool:
        """Override inventory levels for menu items."""
        try:
            print(f"Manager {self.name} set {item} inventory to {new_quantity}")
            return True
        except Exception as e:
            print(f"Error overriding inventory: {e}")
            return False

    def view_daily_sales(self) -> dict:
        """View daily sales report."""
        # Implementation would query sales system
        return {
            "date": datetime.now().date(),
            "total_sales": 0.0,
            "transaction_count": 0
        }


# ==========================================
# 4. CUSTOMER & MEMBER HIERARCHY
# ==========================================

class Customer(Person):
    """A standard walk-in customer without membership benefits."""
    
    def __init__(self, person_id: str, name: str, contact: str, birthdate: Optional[datetime] = None):
        super().__init__(person_id, name, contact)
        self.__total_spend = 0.0
        self.__birthdate = birthdate
        self.__visit_history = []

    def increment_spend(self, amount: float):
        """Add to customer's total spending."""
        if amount > 0:
            self.__total_spend += amount
            self.__visit_history.append({
                "date": datetime.now(),
                "amount": amount
            })

    @property
    def total_spend(self) -> float:
        """Get customer's total spending."""
        return self.__total_spend

    @property
    def birthdate(self) -> Optional[datetime]:
        """Get customer's birthdate."""
        return self.__birthdate

    @property
    def visit_history(self) -> list:
        """Get customer's visit history."""
        return self.__visit_history.copy()


class Member(Customer):
    """Base class for all registered members with loyalty benefits."""
    
    def __init__(self, person_id: str, name: str, contact: str, member_id: str, 
                 birthdate: Optional[datetime] = None):
        super().__init__(person_id, name, contact, birthdate)
        self.__member_id = member_id
        self.__points = 0
        self.__join_date = datetime.now()
        self.__is_active = True

    @property
    def member_id(self) -> str:
        return self.__member_id

    @property
    def points(self) -> int:
        return self.__points

    @property
    def join_date(self) -> datetime:
        return self.__join_date

    @property
    def is_active(self) -> bool:
        return self.__is_active

    def add_points(self, amount: int):
        if amount > 0:
            self.__points += amount

    def redeem_points(self, amount: int) -> bool:
        if 0 < amount <= self.__points:
            self.__points -= amount
            return True
        return False

    def deactivate(self):
        self.__is_active = False

    def reactivate(self):
        self.__is_active = True


class TieredMember(Member, ABC):
    """
    เอ๋อละไอเหี้ย
    """
    
    def __init__(self, person_id: str, name: str, contact: str, member_id: str, 
                 tier: TierEnum, birthdate: Optional[datetime] = None):
        super().__init__(person_id, name, contact, member_id, birthdate)
        self.__tier = tier
        self.__penalty_points = 0.0
        self._set_tier_benefits()

    @property
    def tier(self) -> TierEnum:
        return self.__tier

    @property
    def penalty_points(self) -> float:
        return self.__penalty_points

    def add_penalty(self, points: float):
        """Add penalty points for no-shows or violations."""
        self.__penalty_points += points

    def clear_penalties(self):
        """Clear all penalty points."""
        self.__penalty_points = 0.0

    @abstractmethod
    def _set_tier_benefits(self):
        """Set tier-specific benefits (called during initialization)."""
        pass

    @abstractmethod
    def get_discount_rate(self) -> float:
        """Calculate discount percentage based on tier."""
        pass

    @abstractmethod
    def calculate_points_earned(self, amount: float) -> int:
        """Calculate loyalty points earned based on spending and tier."""
        pass

    @abstractmethod
    def get_max_active_bookings(self) -> int:
        """Get maximum number of active bookings allowed."""
        pass

    @abstractmethod
    def get_max_booking_duration(self) -> int:
        """Get maximum booking duration in hours."""
        pass

    @abstractmethod
    def get_max_advance_booking_days(self) -> int:
        """Get maximum days in advance a booking can be made."""
        pass


class SilverMember(TieredMember):
    """Silver tier member with basic benefits."""
    
    def __init__(self, person_id: str, name: str, contact: str, member_id: str,
                 birthdate: Optional[datetime] = None):
        super().__init__(person_id, name, contact, member_id, TierEnum.SILVER, birthdate)

    def _set_tier_benefits(self):
        self.__max_active_bookings = 2
        self.__max_booking_duration = 2  # hours
        self.__max_advance_booking_days = 7  # days

    def get_discount_rate(self) -> float:
        return 0.05  # 5% discount

    def calculate_points_earned(self, amount: float) -> int:
        return int(amount * 1.0)  # 1 point per dollar

    def get_max_active_bookings(self) -> int:
        return self.__max_active_bookings

    def get_max_booking_duration(self) -> int:
        return self.__max_booking_duration

    def get_max_advance_booking_days(self) -> int:
        return self.__max_advance_booking_days


class GoldMember(TieredMember):
    """Gold tier member with enhanced benefits."""
    
    def __init__(self, person_id: str, name: str, contact: str, member_id: str,
                 birthdate: Optional[datetime] = None):
        super().__init__(person_id, name, contact, member_id, TierEnum.GOLD, birthdate)

    def _set_tier_benefits(self):
        self.__max_active_bookings = 4
        self.__max_booking_duration = 3  # hours
        self.__max_advance_booking_days = 14  # days

    def get_discount_rate(self) -> float:
        return 0.10  # 10% discount

    def calculate_points_earned(self, amount: float) -> int:
        return int(amount * 1.5)  # 1.5 points per dollar

    def get_max_active_bookings(self) -> int:
        return self.__max_active_bookings

    def get_max_booking_duration(self) -> int:
        return self.__max_booking_duration

    def get_max_advance_booking_days(self) -> int:
        return self.__max_advance_booking_days


class PlatinumMember(TieredMember):
    """Platinum tier member with premium benefits."""
    
    def __init__(self, person_id: str, name: str, contact: str, member_id: str,
                 birthdate: Optional[datetime] = None):
        super().__init__(person_id, name, contact, member_id, TierEnum.PLATINUM, birthdate)

    def _set_tier_benefits(self):
        self.__max_active_bookings = 6
        self.__max_booking_duration = 4  # hours
        self.__max_advance_booking_days = 30  # days

    def get_discount_rate(self) -> float:
        return 0.15  # 15% discount

    def calculate_points_earned(self, amount: float) -> int:
        return int(amount * 2.0)  # 2 points per dollar

    def get_max_active_bookings(self) -> int:
        return self.__max_active_bookings

    def get_max_booking_duration(self) -> int:
        return self.__max_booking_duration

    def get_max_advance_booking_days(self) -> int:
        return self.__max_advance_booking_days


class TempCustomer(Customer):
    """Temporary customer for one-time visits without registration."""
    
    def __init__(self, name: str):
        visit_date = datetime.now()
        temporary_id = f"TEMP-{int(visit_date.timestamp())}"
        super().__init__(person_id=temporary_id, name=name, contact="N/A")
        self.__visit_date = visit_date
        self.__temporary_id = temporary_id
        self.__queue_token = None

    @property
    def temporary_id(self) -> str:
        return self.__temporary_id

    @property
    def queue_token(self) -> Optional[str]:
        return self.__queue_token

    def set_queue_token(self, token: str):
        """Assign a queue token for waiting customers."""
        self.__queue_token = token

    @property
    def visit_date(self) -> datetime:
        return self.__visit_date
