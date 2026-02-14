"""
Board Game Cafe - Person Module
Handles all person-related classes: Staff, Manager, Customer, Member, TempCustomer
"""

from abc import ABC, abstractmethod
from datetime import datetime
from enum import Enum
from typing import Optional, List, Dict
import hashlib
import secrets


# ==========================================
# CONSTANTS
# ==========================================

class TierEnum(Enum):
    SILVER = "Silver"
    GOLD = "Gold"
    PLATINUM = "Platinum"


# Silver tier constants
SILVER_DISCOUNT_RATE = 0.05
SILVER_POINTS_MULTIPLIER = 1.0
SILVER_MAX_BOOKINGS = 2
SILVER_MAX_DURATION_HOURS = 2
SILVER_MAX_ADVANCE_DAYS = 7

# Gold tier constants
GOLD_DISCOUNT_RATE = 0.10
GOLD_POINTS_MULTIPLIER = 1.5
GOLD_MAX_BOOKINGS = 4
GOLD_MAX_DURATION_HOURS = 3
GOLD_MAX_ADVANCE_DAYS = 14

# Platinum tier constants
PLATINUM_DISCOUNT_RATE = 0.15
PLATINUM_POINTS_MULTIPLIER = 2.0
PLATINUM_MAX_BOOKINGS = 6
PLATINUM_MAX_DURATION_HOURS = 4
PLATINUM_MAX_ADVANCE_DAYS = 30

# Penalty thresholds
PENALTY_THRESHOLD_FOR_SUSPENSION = 10.0
NO_SHOW_PENALTY_POINTS = 2.0

# ==========================================
# BASE PERSON HIERARCHY
# ==========================================

class Person(ABC):
    def __init__(self, person_id: str, name: str, contact: str):
        if not person_id or not name:
            raise ValueError("Person ID and name cannot be empty")
        
        self._person_id = person_id
        self._name = name
        self._contact = contact
        self._created_at = datetime.now()
        self._username = None
        self._password_hash = None

    def set_credentials(self, username: str, password: str) -> None:
        if not username or not password:
            raise ValueError("Username and password cannot be empty")
        
        self._username = username
        salt = secrets.token_hex(16)
        self._password_hash = hashlib.sha256((salt + password).encode('utf-8')).hexdigest() + ':' + salt

    @property
    def username(self) -> Optional[str]:
        return self._username

    def verify_password(self, password: str) -> bool:
        if not self._password_hash:
            return False
        
        hash_part, salt = self._password_hash.split(':')
        return hash_part == hashlib.sha256((salt + password).encode('utf-8')).hexdigest()

    def record_login(self) -> None:
        pass

    @property
    def person_id(self) -> str:
        return self._person_id

    @property
    def name(self) -> str:
        return self._name

    @property
    def contact(self) -> str:
        return self._contact

    @property
    def created_at(self) -> datetime:
        return self._created_at

    def update_contact(self, new_contact: str) -> None:
        if not new_contact:
            raise ValueError("Contact information cannot be empty")
        self._contact = new_contact

    def update_name(self, new_name: str) -> None:
        if not new_name:
            raise ValueError("Name cannot be empty")
        self._name = new_name


# ==========================================
# STAFF HIERARCHY
# ==========================================

class Staff(Person):
    def __init__(self, person_id: str, name: str, contact: str, 
                 username: str, password: str, salary: float):
        if salary < 0:
            raise ValueError("Salary cannot be negative")
        
        super().__init__(person_id, name, contact)
        self.set_credentials(username, password)
        
        self._salary = salary
        self._staff_id = person_id
        self._is_active = True

    @property
    def salary(self) -> float:
        return self._salary

    @property
    def staff_id(self) -> str:
        return self._staff_id

    @property
    def is_active(self) -> bool:
        return self._is_active

    def update_salary(self, new_salary: float) -> None:
        if new_salary < 0:
            raise ValueError("Salary cannot be negative")
        self._salary = new_salary

    def deactivate(self) -> None:
        self._is_active = False

    def reactivate(self) -> None:
        self._is_active = True

    def take_order(self, cafe_system, branch, order) -> bool:
        if not self._is_active:
            raise PermissionError("Inactive staff cannot take orders")
        
        try:
            cafe_system.place_order(branch, order)
            return True
        except Exception as e:
            raise RuntimeError(f"Failed to take order: {e}")

    def serve_item(self, order, item_id: str) -> bool:
        if not self._is_active:
            raise PermissionError("Inactive staff cannot serve items")
        
        try:
            order.mark_served(item_id)
            return True
        except Exception as e:
            raise RuntimeError(f"Failed to serve item: {e}")

    def assign_table(self, table, customer) -> bool:
        if not self._is_active:
            raise PermissionError("Inactive staff cannot assign tables")
        
        try:
            if not table.is_available:
                raise ValueError("Table is not available")
            table.assign_customer(customer)
            return True
        except AttributeError:
            raise RuntimeError("Invalid table or customer object")

    def handle_check_in(self, reservation) -> bool:
        if not self._is_active:
            raise PermissionError("Inactive staff cannot handle check-ins")
        
        try:
            reservation.check_in()
            return True
        except Exception as e:
            raise RuntimeError(f"Check-in failed: {e}")


class Manager(Person):
    def __init__(self, person_id: str, name: str, contact: str,
                 username: str, password: str, salary: float):
        if salary < 0:
            raise ValueError("Salary cannot be negative")
        
        super().__init__(person_id, name, contact)
        self.set_credentials(username, password)
        
        self._salary = salary
        self._is_active = True
        self._managed_staff: List[str] = []

    @property
    def salary(self) -> float:
        return self._salary

    @property
    def is_active(self) -> bool:
        return self._is_active

    @property
    def managed_staff(self) -> List[str]:
        return self._managed_staff.copy()

    def approve_void_bill(self, payment, reason: str) -> bool:
        if not self._is_active:
            raise PermissionError("Inactive manager cannot approve voids")
        
        if not reason or len(reason) < 10:
            raise ValueError("Void reason must be at least 10 characters")
        
        try:
            payment.refund(reason)
            return True
        except Exception as e:
            raise RuntimeError(f"Void approval failed: {e}")

    def add_staff(self, cafe_system, branch, staff: Staff) -> bool:
        if not self._is_active:
            raise PermissionError("Inactive manager cannot add staff")
        
        try:
            branch.staff.append(staff)
            self._managed_staff.append(staff.staff_id)
            return True
        except Exception as e:
            raise RuntimeError(f"Failed to add staff: {e}")

    def remove_staff(self, branch, staff_id: str, reason: str) -> bool:
        if not self._is_active:
            raise PermissionError("Inactive manager cannot remove staff")
        
        if not reason or len(reason) < 10:
            raise ValueError("Removal reason must be at least 10 characters")
        
        try:
            for staff in branch.staff:
                if staff.staff_id == staff_id:
                    staff.deactivate()
                    if staff_id in self._managed_staff:
                        self._managed_staff.remove(staff_id)
                    return True
            return False
        except Exception as e:
            raise RuntimeError(f"Failed to remove staff: {e}")

    def override_inventory_stock(self, menu_item, new_quantity: int, reason: str) -> bool:
        if not self._is_active:
            raise PermissionError("Inactive manager cannot override inventory")
        
        if new_quantity < 0:
            raise ValueError("Inventory quantity cannot be negative")
        
        if not reason or len(reason) < 10:
            raise ValueError("Override reason must be at least 10 characters")
        
        try:
            menu_item.set_stock_level(new_quantity, approved_by=self._person_id)
            return True
        except AttributeError:
            raise RuntimeError("Invalid menu item object")

    def view_daily_sales(self, cafe_system, branch, date: Optional[datetime] = None) -> Dict:
        if not self._is_active:
            raise PermissionError("Inactive manager cannot view reports")
        
        return cafe_system.get_branch_report(branch)


# ==========================================
# CUSTOMER & MEMBER HIERARCHY
# ==========================================

class Customer(Person):
    def __init__(self, person_id: str, name: str, contact: str, 
                 birthdate: Optional[datetime] = None):
        super().__init__(person_id, name, contact)
        self._total_spend = 0.0
        self._birthdate = birthdate
        self._visit_history: List[Dict] = []

    @property
    def total_spend(self) -> float:
        return self._total_spend

    @property
    def birthdate(self) -> Optional[datetime]:
        return self._birthdate

    @property
    def visit_history(self) -> List[Dict]:
        return self._visit_history.copy()

    @property
    def visit_count(self) -> int:
        return len(self._visit_history)

    def increment_spend(self, amount: float) -> None:
        if amount <= 0:
            raise ValueError("Spend amount must be positive")
        
        self._total_spend += amount
        self._visit_history.append({
            "date": datetime.now(),
            "amount": amount
        })

    def is_birthday_today(self) -> bool:
        if not self._birthdate:
            return False
        
        today = datetime.now()
        return (today.month == self._birthdate.month and 
                today.day == self._birthdate.day)


class Member(Customer):
    def __init__(self, person_id: str, name: str, contact: str, member_id: str,
                 username: str, password: str, birthdate: Optional[datetime] = None):
        super().__init__(person_id, name, contact, birthdate)
        self.set_credentials(username, password)
        
        self._member_id = member_id
        self._points = 0
        self._join_date = datetime.now()
        self._is_active = True
        self._tier = None
    def determine_tier(self) -> None:
        if self.total_spend >= 20000:
            self._tier = TierEnum.PLATINUM
        elif self.total_spend >= 7500:
            self._tier = TierEnum.GOLD
        elif self.total_spend >= 2000:
            self._tier = TierEnum.SILVER
        else:
            self._tier = None
    def get_tier(self) -> Optional[TierEnum]:
        self.determine_tier()
        return self._tier
    def get_discount_rate(self) -> float:
        tier = self.get_tier()
        if tier == TierEnum.PLATINUM:
            return PLATINUM_DISCOUNT_RATE
        elif tier == TierEnum.GOLD:
            return GOLD_DISCOUNT_RATE
        elif tier == TierEnum.SILVER:
            return SILVER_DISCOUNT_RATE
        else:
            return 0.0
    def get_points_multiplier(self) -> float:
        tier = self.get_tier()
        if tier == TierEnum.PLATINUM:
            return PLATINUM_POINTS_MULTIPLIER
        elif tier == TierEnum.GOLD:
            return GOLD_POINTS_MULTIPLIER
        elif tier == TierEnum.SILVER:
            return SILVER_POINTS_MULTIPLIER
        else:
            return 1.0
    def get_booking_limits(self) -> Dict:
        tier = self.get_tier()
        if tier == TierEnum.PLATINUM:
            return {
                "max_bookings": PLATINUM_MAX_BOOKINGS,
                "max_duration_hours": PLATINUM_MAX_DURATION_HOURS,
                "max_advance_days": PLATINUM_MAX_ADVANCE_DAYS
            }
        elif tier == TierEnum.GOLD:
            return {
                "max_bookings": GOLD_MAX_BOOKINGS,
                "max_duration_hours": GOLD_MAX_DURATION_HOURS,
                "max_advance_days": GOLD_MAX_ADVANCE_DAYS
            }
        elif tier == TierEnum.SILVER:
            return {
                "max_bookings": SILVER_MAX_BOOKINGS,
                "max_duration_hours": SILVER_MAX_DURATION_HOURS,
                "max_advance_days": SILVER_MAX_ADVANCE_DAYS
            }
        else:
            return {
                "max_bookings": 0,
                "max_duration_hours": 0,
                "max_advance_days": 0
            }
    def can_book(self, requested_date: datetime, duration_hours: int) -> bool:
        limits = self.get_booking_limits()
        if limits["max_bookings"] == 0:
            return False
        
        if duration_hours > limits["max_duration_hours"]:
            return False
        
        if (requested_date - datetime.now()).days > limits["max_advance_days"]:
            return False
        
        return True
    @property
    def member_id(self) -> str:
        return self._member_id

    @property
    def points(self) -> int:
        return self._points

    @property
    def join_date(self) -> datetime:
        return self._join_date

    @property
    def is_active(self) -> bool:
        return self._is_active

    def add_points(self, amount: int) -> None:
        if amount <= 0:
            raise ValueError("Points amount must be positive")
        self._points += amount

    def redeem_points(self, amount: int) -> bool:
        if amount <= 0:
            raise ValueError("Redemption amount must be positive")
        
        if amount > self._points:
            raise ValueError(f"Insufficient points. Balance: {self._points}")
        
        self._points -= amount
        return True

    def deactivate(self) -> None:
        self._is_active = False

    def reactivate(self) -> None:
        self._is_active = True


class TempCustomer(Customer):
    def __init__(self, name: str):
        if not name:
            raise ValueError("Name cannot be empty")
        
        visit_date = datetime.now()
        temporary_id = f"TEMP-{int(visit_date.timestamp())}"
        super().__init__(person_id=temporary_id, name=name, contact="N/A")
        
        self._visit_date = visit_date
        self._temporary_id = temporary_id
        self._queue_token: Optional[str] = None

    @property
    def temporary_id(self) -> str:
        return self._temporary_id

    @property
    def queue_token(self) -> Optional[str]:
        return self._queue_token

    @property
    def visit_date(self) -> datetime:
        return self._visit_date

    def set_queue_token(self, token: str) -> None:
        if not token:
            raise ValueError("Queue token cannot be empty")
        self._queue_token = token

    def update_contact(self, new_contact: str) -> None:
        raise NotImplementedError("Temporary customers cannot update contact information")