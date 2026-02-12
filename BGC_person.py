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
        self.__salary = salary

class Manager(Staff):
    """Inherits Staff. Can manage inventory and approve refunds."""
    def __init__(self, person_id: str, name: str, contact: str, salary: float, department: str):
        super().__init__(person_id, name, contact, salary)


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

class TempCustomer(Customer):
    """Temporary customer with limited access."""
    def __init__(self, person_id: str, name: str, contact: str):
        super().__init__(person_id, name, contact)


       