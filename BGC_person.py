from abc import ABC, abstractmethod
from datetime import datetime

# ==========================================
# 1. BASE PERSON HIERARCHY
# ==========================================

class Person(ABC):
    """Abstract Base Class for all individuals in the system."""
    def __init__(self, person_id: str, name: str, contact: str):
        self.__person_id = person_id
        self.__name = name
        self.__contact = contact


# ==========================================
# 2. STAFF HIERARCHY (Internal Actors)
# ==========================================

class Staff(Person):
    """Base class for employees. Can process orders and handle customers."""
    def __init__(self, person_id: str, name: str, contact: str, salary: float):
        super().__init__(person_id, name, contact)


class Manager(Staff):
    """Inherits Staff. Can manage inventory and approve refunds."""
    def __init__(self, person_id: str, name: str, contact: str, salary: float, department: str):
        super().__init__(person_id, name, contact, salary)


class Owner(Manager):
    """Inherits Manager. Has full access to financial reports and system settings."""
    def __init__(self, person_id: str, name: str, contact: str, salary: float):
        super().__init__(person_id, name, contact, salary, "All Departments")

# ==========================================
# 3. CUSTOMER & MEMBER HIERARCHY
# ==========================================

class Customer(Person):
    """A standard walk-in customer without membership benefits."""
    def __init__(self, person_id: str, name: str, contact: str):
        super().__init__(person_id, name, contact)
        self.__visit_count = 0

    def increment_visit(self):
        self.__visit_count += 1

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

    @abstractmethod
    def get_discount_rate(self) -> float:
        """Returns the discount percentage for this tier."""
        pass

    @abstractmethod
    def get_tier_name(self) -> str:
        pass

class SilverMember(Member):
    def get_discount_rate(self) -> float:
        return 0.05  # 5% Discount

    def get_tier_name(self) -> str:
        return "Silver"

class GoldMember(Member):
    def get_discount_rate(self) -> float:
        return 0.10  # 10% Discount

    def get_tier_name(self) -> str:
        return "Gold"

class PlatinumMember(Member):
    def get_discount_rate(self) -> float:
        return 0.15  # 15% Discount

    def get_tier_name(self) -> str:
        return "Platinum"

# ==========================================
# 4. REGISTRATION LOGIC
# ==========================================

class Registration:
    """Class to handle the transition from Customer to Member."""
    def __init__(self, reg_id: str, customer: Customer, staff: Staff, tier_type: str):
        self.__reg_id = reg_id
        self.__customer = customer
        self.__processed_by = staff
        self.__tier_type = tier_type # "Silver", "Gold", "Platinum"
        self.__reg_date = datetime.now()

       