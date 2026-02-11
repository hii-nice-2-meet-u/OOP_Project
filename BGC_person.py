from abc import ABC, abstractmethod
from datetime import datetime

# ==========================================
# 1. BASE PERSON HIERARCHY
# ==========================================

class Person(ABC):
    """Abstract Base Class for all individuals in the system."""
    def __init__(self, user_id: str, name: str, contact: str):
        self.__user_id = user_id
        self.__name = name
        self.__contact = contact


# ==========================================
# 2. STAFF HIERARCHY (Internal Actors)
# ==========================================

class Staff(Person):
    """Base class for employees. Can process orders and handle customers."""
    def __init__(self, user_id: str, name: str, contact: str, salary: float):
        super().__init__(user_id, name, contact)
        self.__salary = salary
        self.__staff_id = user_id

    def get_salary(self):
        return self.__salary

    def take_order(self, order):
        """Process an order taken from a customer."""
        pass
    def serve_item(self, order):
        """Serve food/drink to the customer."""
        pass
    def assign_table(self, table):
        """Assign a play table to a customer."""
        pass
    def check_booking_status(self, reservation):
        """Check the status of a reservation."""
        pass
    def assign_walk_in_customer(self, customer):
        """Assign a walk-in customer to a table."""
        pass
    def register_walk_in_customer(self, customer):
        """Register a walk-in customer as a member."""
        pass
    def handle_check_in(self, reservation):
        """Handle customer check-in for a reservation."""
        pass

class Manager(Staff):
    """Inherits Staff. Can manage inventory and approve refunds."""
    def __init__(self, person_id: str, name: str, contact: str, salary: float, department: str):
        super().__init__(person_id, name, contact, salary)
    def approve_void_bill(self, transaction):
        """Approve voiding a bill."""
        pass
    def add_staff(self, staff):
        """Add a new staff member to the system."""
        pass
    def remove_staff(self, staff_id: str):
        """Remove a staff member from the system."""
        pass
    def override_inventory_stock(self, item):
        """Override inventory levels for menu items."""
        pass
    def view_daily_sales(self):
        """View system audit logs."""
        pass


# ==========================================
# 3. CUSTOMER & MEMBER HIERARCHY
# ==========================================

class Customer(Person):
    """A standard walk-in customer without membership benefits."""
    def __init__(self, person_id: str, name: str, contact: str):
        super().__init__(person_id, name, contact)
        self.__totalspend = 0
        self.__birthdate = None

    def increment_spend(self, amount: float):
        self.__totalspend += amount
    @property
    def get_total_spend(self) -> float:
        return self.__totalspend
    @property
    def get_birthdate(self):
        return self.__birthdate
class Member(Customer):
    """Base class for all registered members."""
    def __init__(self, person_id: str, name: str, contact: str, member_id: str):
        super().__init__(person_id, name, contact)
        self.__member_id = member_id
        self.__points = 0
        self.__join_date = datetime.now()

    def get_member_id(self) -> str:
        return self.__member_id

    def add_points(self, amount: int):
        self.__points += amount

class Member(Member, ABC):
    """
    Abstract Class derived from Member.
    Specific tiers must implement discount and point calculation logic.
    """
    def __init__(self, person_id: str, name: str, contact: str, member_id: str):
        super().__init__(person_id, name, contact, member_id)
        self.__member_tier = None
        self.__penalty_points = 0.0
        self.__max_active_booking_quota = 0
        self.__max_booking_duration = 0
        self.__max_advance_booking_days = 0
        self.__discount_rate = 0.0

    def get_discount_rate(self) -> float:
        pass
    def set_discount_rate(self, rate: float):
        self.__discount_rate = rate
    def get_tier_name(self) -> str:
        pass 
    def get_max_active_booking_quota(self) -> int:
        return self.__max_active_booking_quota
    def get_max_booking_duration(self) -> int:
        return self.__max_booking_duration
    def get_max_advance_booking_days(self) -> int:
        return self.__max_advance_booking_days

class TempCustomer(Customer):
    """Temporary customer for one-time visits without registration."""
    def __init__(self, name: str):
        super().__init__(person_id="TEMP", name=name, contact="N/A")
        self.__visit_date = datetime.now()
        self.__temporary_id = f"TEMP-{int(self.__visit_date.timestamp())}"
        self.__queue_token = None
    def get_temporary_id(self) -> str:
        return self.__temporary_id
    def get_queue_token(self) -> str:
        return self.__queue_token
    def set_queue_token(self, token: str):
        self.__queue_token = token
