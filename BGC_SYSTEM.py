from datetime import *
import time
import random
import math

from BGC_MENU import *
from BGC_PAYMENT import *
from BGC_PERSON import *
from BGC_PLAY_SESSION import *
from BGC_RESERVATION import *
from ENUM_STATUS import *

# | ════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
# | #FFFF67


def get_validate_id(_id, list_type_id):
    for type_id in list_type_id:
        if _id.startswith(type_id):
            return True
    return False


def validate_id(_id, list_type_id):
    if not isinstance(_id, str) or not _id.strip():
        raise ValueError("Invalid ID : ID must be a non-empty string")
    if not get_validate_id(_id, list_type_id):
        raise ValueError(f"Invalid ID : ID must be start with {list_type_id}")


# | ════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
# | #EFFF11


class CafeSystem:
    def __init__(self):
        self.__person = []
        self.__cafe_branches = []
        self.__reservations = []
        self.__simulated_time = None

    # / ════════════════════════════════════════════════════════════════
    # - Getters
    # / ════════════════════════════════════════════════════════════════

    @property
    def person(self):
        return self.__person.copy()

    @property
    def cafe_branches(self):
        return self.__cafe_branches.copy()

    @property
    def reservations(self):
        return self.__reservations.copy()

    def get_time(self):
        if self.__simulated_time is not None:
            return self.__simulated_time
        return datetime.now()

    def set_simulated_time(self, time_str):
        if time_str is None:
            self.__simulated_time = None
            return "System time reset to real-time."
            
        formats = (
            "%Y-%m-%dT%H:%M:%S", 
            "%Y-%m-%dT%H:%M", 
            "%Y-%m-%d %H:%M:%S", 
            "%Y-%m-%d %H:%M"
        )
        for fmt in formats:
            try:
                self.__simulated_time = datetime.strptime(time_str, fmt)
                return f"System time set to {self.__simulated_time}"
            except ValueError:
                continue
        raise ValueError(f"Invalid time format: {time_str}")

    # / ════════════════════════════════════════════════════════════════
    # - Methods
    # / ════════════════════════════════════════════════════════════════
    # \ PERSON METHOD

    def add_person(self, person):
        if not isinstance(person, Person):
            raise TypeError("Type Error : must be an instance of Person")
        self.__person.append(person)

    def create_owner(self, name, requester_id=None):
        self.__authorize(requester_id, [Owner])
        try:
            new_owner = Owner(name)
            self.add_person(new_owner)
            return new_owner
        except (TypeError, ValueError) as e:
            raise ValueError(f"Failed to create owner: {e}")

    def create_manager(self, name, requester_id=None):
        self.__authorize(requester_id, [Owner])
        try:
            new_manager = Manager(name)
            self.add_person(new_manager)
            return new_manager
        except (TypeError, ValueError) as e:
            raise ValueError(f"Failed to create manager: {e}")

    def create_staff(self, name, requester_id=None):
        self.__authorize(requester_id, [Owner, Manager])
        try:
            new_staff = Staff(name)
            self.add_person(new_staff)
            return new_staff
        except (TypeError, ValueError) as e:
            raise ValueError(f"Failed to create staff: {e}")

    def create_customer_member(self, name):
        try:
            new_customer = Member(name)
            self.add_person(new_customer)
            return new_customer
        except (TypeError, ValueError) as e:
            raise ValueError(f"Failed to create member: {e}")

    def create_customer_walk_in(self):
        try:
            new_walk_in = WalkInCustomer()
            self.add_person(new_walk_in)
            return new_walk_in
        except (TypeError, ValueError) as e:
            raise ValueError(f"Failed to create walk-in customer: {e}")

    def add_owner_to_branch(self, branch_id, owner_id, requester_id=None):
        self.__authorize(requester_id, [Owner])
        validate_id(branch_id, ["BRCH"])
        validate_id(owner_id, ["OWNER"])

        cafe_branch = self.find_cafe_branch_by_id(branch_id)
        if cafe_branch is None:
            raise ValueError("Cafe Branch not found")
        owner = self.find_person_by_id(owner_id)
        if owner is None:
            raise ValueError("Owner not found")

        try:
            cafe_branch.add_owner(owner)
            owner.add_owned_branch(branch_id)
        except TypeError as e:
            raise ValueError(f"Cannot add owner: {e}")

    def add_manager_to_branch(self, branch_id, manager_id, requester_id=None):
        self.__authorize(requester_id, [Owner])
        validate_id(branch_id, ["BRCH"])
        validate_id(manager_id, ["MANAGER"])

        cafe_branch = self.find_cafe_branch_by_id(branch_id)
        if cafe_branch is None:
            raise ValueError("Cafe Branch not found")

        manager = self.find_person_by_id(manager_id)
        if manager is None:
            raise ValueError("Manager not found")

        try:
            cafe_branch.add_manager(manager)
            manager.managed_branches = branch_id
        except TypeError as e:
            raise ValueError(f"Cannot add manager: {e}")

    def add_staff_to_branch(self, branch_id, staff_id, requester_id=None):
        self.__authorize(requester_id, [Owner, Manager])
        validate_id(branch_id, ["BRCH"])
        validate_id(staff_id, ["STAFF"])

        cafe_branch = self.find_cafe_branch_by_id(branch_id)
        if cafe_branch is None:
            raise ValueError("Cafe Branch not found")

        staff = self.find_person_by_id(staff_id)
        if staff is None:
            raise ValueError("Staff not found")

        try:
            cafe_branch.add_staff(staff)
            staff.assigned_branch = branch_id
        except TypeError as e:
            raise ValueError(f"Cannot add staff: {e}")

    def get_person(self):
        return self.__person.copy()

    def get_person_by_type(self, person_type):
        return [person for person in self.__person if isinstance(person, person_type)]

    def find_person_by_id(self, user_id):
        for person in self.__person:
            if person.user_id == user_id:
                return person
        return None

    def find_person_by_name(self, name):
        name = name.lower()
        for person in self.__person:
            if person.name.lower() == name:
                return person
        return None

    def remove_person_by_id(self, user_id, requester_id=None):
        self.__authorize(requester_id, [Owner, Manager])
        validate_id(user_id, ["OWNER", "MANAGER", "STAFF", "MEMBER", "WALK"])

        person = self.find_person_by_id(user_id)
        if person is None:
            raise ValueError("Invalid ID : Person not found")

        self.__person.remove(person)

    def update_person_by_id(self, user_id, name, requester_id=None):
        self.__authorize(requester_id, [Owner, Manager])
        validate_id(user_id, ["OWNER", "MANAGER", "STAFF", "MEMBER", "WALK"])

        person = self.find_person_by_id(user_id)
        if person is None:
            raise ValueError("Invalid ID : Person not found")

        try:
            person.name = name
        except ValueError as e:
            raise ValueError(f"Cannot update person : {e}")

    def add_spent(self, customer_id, amount):
        validate_id(customer_id, ["MEMBER", "WALK"])

        if not isinstance(amount, (int, float)) or amount < 0:
            raise ValueError("Amount must be a positive number")

        customer = self.find_person_by_id(customer_id)
        if not customer:
            raise ValueError("Customer not found")

        if not isinstance(customer, Member):
            raise ValueError("Only Members can accumulate total spent")

        try:

            customer.total_spent = amount

            return customer
        except Exception as e:
            raise ValueError(f"Failed to add spent amount: {e}")

    # / ════════════════════════════════════════════════════════════════
    # \ CAFE BRANCH

    def create_cafe_branch(self, cafe_branch_name, cafe_branch_location="", requester_id=None):
        self.__authorize(requester_id, [Owner])
        try:
            if not isinstance(cafe_branch_name, str) or not cafe_branch_name.strip():
                raise ValueError("Branch name must be a non-empty string")

            new_cafe_branch = CafeBranch(
                cafe_branch_name, cafe_branch_location)
            self.__cafe_branches.append(new_cafe_branch)
            return new_cafe_branch

        except (TypeError, ValueError) as e:
            raise ValueError(f"Failed to create cafe branch : {e}")

    def get_cafe_branches(self):
        return self.cafe_branches

    def find_cafe_branch_by_id(self, _id):
        if not isinstance(_id, str):
            return None

        if _id.startswith("BRCH-"):
            for cafe_branch in self.__cafe_branches:
                if cafe_branch.branch_id == _id:
                    return cafe_branch
        elif _id.startswith("PS-"):
            for cafe_branch in self.__cafe_branches:
                if cafe_branch.find_play_session_by_id(_id):          # active
                    return cafe_branch
                if cafe_branch.find_play_session_history_by_id(_id):  # history
                    return cafe_branch
        elif _id.startswith("TABLE-"):
            for cafe_branch in self.__cafe_branches:
                if cafe_branch.find_table_by_id(_id):
                    return cafe_branch
        elif _id.startswith("BG-"):
            for cafe_branch in self.__cafe_branches:
                if cafe_branch.find_board_game_by_id(_id):
                    return cafe_branch
        elif _id.startswith("FOOD-") or _id.startswith("DRINK-"):
            for cafe_branch in self.__cafe_branches:
                if cafe_branch.find_menu_item_by_id(_id):
                    return cafe_branch
        return None

    def find_play_session_by_id(self, any_id):
        for branch in self.__cafe_branches:
            session = branch.find_play_session_by_id(any_id)
            if session:
                return session
        return None

    def find_play_session_history_by_id(self, any_id):
        for branch in self.__cafe_branches:
            session = branch.find_play_session_history_by_id(any_id)
            if session:
                return session
        return None

    def find_cafe_branch_by_name(self, name):
        if not isinstance(name, str):
            return None

        name = name.lower()
        for cafe_branch in self.__cafe_branches:
            if cafe_branch.name.lower() == name:
                return cafe_branch
        return None

    def remove_cafe_branch_by_id(self, cafe_branch_id, requester_id=None):
        self.__authorize(requester_id, [Owner])
        validate_id(cafe_branch_id, ["BRCH"])

        cafe_branch = self.find_cafe_branch_by_id(cafe_branch_id)
        if cafe_branch is None:
            raise ValueError("Invalid ID : Cafe Branch not found")

        self.__cafe_branches.remove(cafe_branch)

    def update_cafe_branch_by_id(self, branch_id, name, location, requester_id=None):
        self.__authorize(requester_id, [Owner])
        validate_id(branch_id, ["BRCH"])

        cafe_branch = self.find_cafe_branch_by_id(branch_id)
        if cafe_branch is None:
            raise ValueError("Invalid ID : Cafe Branch not found")

        try:
            cafe_branch.name = name
            cafe_branch.location = location
        except (TypeError, ValueError) as e:
            raise ValueError(f"Cannot update branch: {e}")

    # / ════════════════════════════════════════════════════════════════
    # \ RESERVATION

    def make_reservation(
        self,
        customer_id,
        branch_id,
        total_player,
        date,
        start_time,
        end_time,
        table_id="auto",
        method_type="online",
        **kwargs
    ):
        #import re ใช้เรียง format เวลา 
        import re
        if not re.match(r'^\d{4}-\d{2}-\d{2}$', str(date)):
            raise ValueError(
                f"Invalid date format: '{date}'. Expected YYYY-MM-DD (e.g. 2024-07-01)")
        for t_val, t_name in [(start_time, "start_time"), (end_time, "end_time")]:
            if not re.match(r'^\d{2}:\d{2}$', str(t_val)):
                raise ValueError(
                    f"Invalid time format for {t_name}: '{t_val}'. Expected HH:MM (e.g. 18:00)")
        try:
            datetime.strptime(date, "%Y-%m-%d")
            datetime.strptime(start_time, "%H:%M")
            datetime.strptime(end_time, "%H:%M")
        except ValueError as e:
            raise ValueError(f"Invalid date/time value: {e}")

        validate_id(customer_id, ["MEMBER", "WALK"])
        validate_id(branch_id, ["BRCH"])

        if not isinstance(total_player, int) or total_player <= 0:
            raise ValueError("total_player must be a positive integer")

        customer = self.find_person_by_id(customer_id)
        if customer is None:
            raise ValueError("Customer not found.")

        # 🔴 Policy: Walk-in customers cannot make reservations.
        # They must register as a member first.
        if isinstance(customer, WalkInCustomer):
            raise ValueError(
                "Walk-in customers are not allowed to make reservations. "
                "Please register as a Member first to enjoy advance booking privileges."
            )

        tier = customer.get_member_tier()

        # 🟢 ด่านที่ 1: ตรวจสอบกฎเวลาและระยะเวลา
        try:
            self.__validate_minimum_lead_time(date, start_time)
            self.__validate_advance_booking(date, tier)
            self.__validate_duration(start_time, end_time, tier)
        except ValueError as e:
            raise ValueError(f"Failed to make reservation: {e}")

        branch = self.find_cafe_branch_by_id(branch_id)
        if branch is None:
            raise ValueError("Cafe branch not found.")

        # 🟢 ด่านที่ 2: ค้นหาและตรวจสอบโต๊ะ
        target_table = None

        if table_id == "auto":
            available_tables = []
            for table in branch.tables:
                if table.capacity >= total_player:
                    if self.__is_table_free(table.table_id, date, start_time, end_time):
                        available_tables.append(table)

            if not available_tables:
                raise ValueError(
                    "No available tables for the requested capacity and time."
                )

            target_table = available_tables[0]
            for t in available_tables:
                if t.capacity < target_table.capacity:
                    target_table = t
        else:
            validate_id(table_id, ["TABLE"])

            target_table = branch.find_table_by_id(table_id)
            if target_table is None:
                raise ValueError("The specified table is not found.")
            if target_table.capacity < total_player:
                raise ValueError(
                    "The specified table does not have enough capacity.")
            if not self.__is_table_free(
                target_table.table_id, date, start_time, end_time
            ):
                raise ValueError(
                    "The specified table is already booked for this time slot."
                )

        # 🟢 ด่านที่ 3: ตรวจสอบโควตาการจองของสมาชิก
        self.__validate_active_quota(customer_id, tier)

        # 🟢 ด่านที่ 3.5: จัดการเงินมัดจำ (Deposit) 30 บาท (ห้ามใช้เงินสด)
        if method_type.lower() == "cash":
            raise ValueError("Reservation deposit cannot be paid in cash. Please use Online or Credit Card.")
        
        deposit_amount = 30.0
        try:
            # สร้าง Payment Record สำหรับมัดจำ
            self.create_payment(deposit_amount, method_type=method_type, **kwargs)
        except Exception as e:
            raise ValueError(f"Deposit payment failed: {e}")

        # 🟢 ด่านที่ 4: สร้างการจอง
        try:
            new_reservation = Reservation(
                customer_id,
                branch_id,
                target_table.table_id,
                date,
                start_time,
                end_time,
                total_player=total_player,
                current_time=self.get_time(),
                deposit=deposit_amount
            )
            new_reservation.status = ReservationStatus.PENDING
            self.add_reservation(new_reservation)
            return new_reservation
        except (TypeError, ValueError) as e:
            raise ValueError(f"Failed to create reservation: {e}")

    def add_reservation(self, reservation):
        if not isinstance(reservation, Reservation):
            raise TypeError("Must be an instance of Reservation")
        self.__reservations.append(reservation)

    def get_reservations(self):
        return self.reservations

    def find_reservation_by_id(self, reservation_id):
        validate_id(reservation_id, ["RESV"])

        for reservation in self.__reservations:
            if reservation.reservation_id == reservation_id:
                return reservation
        return None

    def remove_reservation_by_id(self, reservation_id):
        validate_id(reservation_id, ["RESV"])

        reservation = self.find_reservation_by_id(reservation_id)
        if reservation is None:
            raise ValueError("Reservation not found")
        self.__reservations.remove(reservation)

    def cancel_reservation(self, reservation_id, current_time=None):
        validate_id(reservation_id, ["RESV"])

        reservation = self.find_reservation_by_id(reservation_id)
        if reservation is None:
            raise ValueError("Reservation not found.")
        if reservation.status == ReservationStatus.CANCELLED:
            raise ValueError(
                "Cannot cancel. Reservation is already cancelled.")
        if reservation.status != ReservationStatus.PENDING:
            raise ValueError(
                "Cannot cancel. Reservation is not in PENDING status.")

        if current_time is None:
            now = self.get_time()
        elif isinstance(current_time, datetime):
            now = current_time
        elif isinstance(current_time, str):
            parsed = None
            for fmt in ("%Y-%m-%dT%H:%M:%S", "%Y-%m-%dT%H:%M", "%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M"):
                try:
                    parsed = datetime.strptime(current_time, fmt)
                    break
                except ValueError:
                    continue
            if parsed is None:
                raise ValueError(
                    "Invalid current_time format. Expected 'YYYY-MM-DD HH:MM' or ISO format.")
            now = parsed
        else:
            raise TypeError(
                "current_time must be a datetime object or a string.")

        try:
            reservation_time = datetime.strptime(
                f"{reservation.date} {reservation.start_time}", "%Y-%m-%d %H:%M"
            )
        except ValueError as e:
            raise ValueError(f"Invalid reservation date/time format: {e}")

        if now > reservation_time:
            raise ValueError(
                "Cannot cancel. The reservation time has already passed.")

        # 🟢 Cancellation Policy Logic
        time_diff = (reservation_time - now).total_seconds() / 3600.0
        if time_diff < 24.0:
            # Late cancellation: forfeit 50%
            # Assuming a deposit attribute exists on Reservation object, otherwise this is conceptual.
            # For now, we update status and possibly a message.
            # penalty = reservation.deposit * 0.5 # If deposit exists
            reservation.status = ReservationStatus.CANCELLED
            # Logic to "keep" 50% would happen at the accounting level (not fully implemented here)
        else:
            # Free cancellation: refund 100%
            reservation.status = ReservationStatus.CANCELLED

        try:
            branch = self.find_cafe_branch_by_id(reservation.branch_id)
            if branch is not None:
                table = branch.find_table_by_id(reservation.table_id)
                if table is not None and table.status == TableStatus.RESERVED:
                    table.status = TableStatus.AVAILABLE
        except Exception:
            pass
        return True

    def update_reservation_status_by_id(self, reservation_id, status):
        validate_id(reservation_id, ["RESV"])

        if not isinstance(status, ReservationStatus):
            raise TypeError("Status must be ReservationStatus")

        reservation = self.find_reservation_by_id(reservation_id)
        if reservation is None:
            raise ValueError("Invalid ID : Reservation not found")
        reservation.status = status

    def set_reservation_cancel_by_id(self, reservation_id):
        self.update_reservation_status_by_id(
            reservation_id, ReservationStatus.CANCELLED
        )

    def set_reservation_no_show_by_id(self, reservation_id):
        self.update_reservation_status_by_id(
            reservation_id, ReservationStatus.NO_SHOW)

    def set_reservation_complete_by_id(self, reservation_id):
        self.update_reservation_status_by_id(
            reservation_id, ReservationStatus.COMPLETED
        )

    # / ════════════════════════════════════════════════════════════════
    # \ PRIVATE HELPER METHODS (BUSINESS RULES VALIDATION)
    # / ════════════════════════════════════════════════════════════════

    def __is_table_free(self, table_id, date_str, start_time, end_time):
        try:
            new_start = datetime.strptime(start_time, "%H:%M")
            new_end = datetime.strptime(end_time, "%H:%M")
        except ValueError as e:
            raise ValueError(f"Invalid time format (expected HH:MM): {e}")

        for reservation in self.__reservations:
            if reservation.date == date_str and reservation.table_id == table_id:
                if reservation.status == ReservationStatus.PENDING:
                    try:
                        exist_start = datetime.strptime(
                            reservation.start_time, "%H:%M")
                        exist_end = datetime.strptime(
                            reservation.end_time, "%H:%M")
                    except ValueError:
                        continue  # ข้ามการจองที่มี format ผิด
                    if new_start < exist_end and new_end > exist_start:
                        return False
        return True

    def __validate_active_quota(self, customer_id, tier):
        active_count = 0
        for reservation in self.__reservations:
            if reservation.customer_id == customer_id:
                if reservation.status == ReservationStatus.PENDING:
                    active_count += 1

        # กำหนดโควตาตามระดับสมาชิก
        max_quota = 1
        if tier == MemberTier.BRONZE:
            max_quota = 1
        elif tier == MemberTier.SILVER:
            max_quota = 2
        elif tier == MemberTier.GOLD:
            max_quota = 3
        elif tier == MemberTier.PLATINUM:
            max_quota = 4

        if active_count >= max_quota:
            raise ValueError(
                f"Active booking quota exceeded. Maximum allowed for your tier is {max_quota}."
            )

    def __validate_advance_booking(self, date_str, tier):
        try:
            reservation_date = datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError as e:
            raise ValueError("Invalid date format. Expected YYYY-MM-DD.")

        today = self.get_time().date()
        days_advance = (reservation_date - today).days

        if days_advance < 0:
            raise ValueError("Cannot make a reservation in the past.")

        max_adv_days = 5
        if tier == MemberTier.NONE_TIER:
            max_adv_days = 5
        if tier == MemberTier.BRONZE:
            max_adv_days = 5
        elif tier == MemberTier.SILVER:
            max_adv_days = 14
        elif tier == MemberTier.GOLD:
            max_adv_days = 21
        elif tier == MemberTier.PLATINUM:
            max_adv_days = 30

        if days_advance > max_adv_days:
            raise ValueError(
                f"Maximum advance booking exceeded. Your tier allows up to {max_adv_days} days."
            )

    def __validate_duration(self, start_time, end_time, tier):
        try:
            start_dt = datetime.strptime(start_time, "%H:%M")
            end_dt = datetime.strptime(end_time, "%H:%M")
        except ValueError:
            raise ValueError("Invalid time format. Expected HH:MM.")

        duration_hrs = (end_dt - start_dt).total_seconds() / 3600

        if duration_hrs <= 0:
            raise ValueError(
                "End time must be after start time.")

        max_dur_hrs = 2
        if tier == MemberTier.BRONZE:
            max_dur_hrs = 2
        elif tier == MemberTier.SILVER:
            max_dur_hrs = 3.5
        elif tier == MemberTier.GOLD:
            max_dur_hrs = 7
        elif tier == MemberTier.PLATINUM:
            max_dur_hrs = 999

        if duration_hrs > max_dur_hrs:
            limit_str = (
                "Unlimited" if tier == MemberTier.PLATINUM else f"{max_dur_hrs} hours"
            )
            raise ValueError(
                f"Maximum duration exceeded. Your tier allows up to {limit_str} per session."
            )

    def __validate_minimum_lead_time(self, date_str, start_time):
        try:
            reservation_time = datetime.strptime(
                f"{date_str} {start_time}", "%Y-%m-%d %H:%M"
            )
        except ValueError:
            raise ValueError(
                "Invalid date/time format. Expected YYYY-MM-DD and HH:MM.")

        lead_time = reservation_time - self.get_time()
        one_hour = timedelta(hours=1)

        if lead_time < one_hour:
            raise ValueError(
                "Minimum lead time not met. Tables require at least 1 hour(s) advance booking."
            )

    # / ════════════════════════════════════════════════════════════════
    # \ TABLE

    def create_table_to_branch(self, branch_id, capacity, requester_id=None):
        self.__authorize(requester_id, [Owner, Manager])
        validate_id(branch_id, ["BRCH"])

        if not isinstance(capacity, int) or capacity <= 0:
            raise ValueError("Capacity must be a positive integer")

        cafe_branch = self.find_cafe_branch_by_id(branch_id)
        if cafe_branch is None:
            raise ValueError("Cafe Branch not found")

        try:
            return cafe_branch.add_table(capacity)
        except (TypeError, ValueError) as e:
            raise ValueError(f"Failed to add table: {e}")

    def get_branch_tables(self, branch_id):
        validate_id(branch_id, ["BRCH"])

        cafe_branch = self.find_cafe_branch_by_id(branch_id)
        if cafe_branch is None:
            raise ValueError("Cafe Branch not found")

        return cafe_branch.tables

    def update_reserved_tables(self):
        now = self.get_time()
        for reservation in self.__reservations:
            if reservation.status != ReservationStatus.PENDING:
                continue
            
            try:
                reservation_time = reservation.reservation_time
                time_diff = reservation_time - now
                
                # Check table status first to prevent overwriting OCCUPIED tables
                cafe_branch = self.find_cafe_branch_by_id(reservation.branch_id)
                if not cafe_branch: continue
                table = cafe_branch.find_table_by_id(reservation.table_id)
                if not table or table.status == TableStatus.OCCUPIED:
                    continue  # Never overwrite an currently active play session
                
                # 🟢 No-Show Threshold Policy: 15 minutes
                if time_diff < timedelta(minutes=-15):
                    # More than 15 mins late -> mark as NO_SHOW and free the table
                    self.update_table_status(reservation.table_id, TableStatus.AVAILABLE)
                    reservation.status = ReservationStatus.NO_SHOW
                    # Forfeit 100% of deposit logic would go here if deposit exists
                    continue # Move to next reservation

                # Keep table RESERVED from 1 hour before, up until 15 mins after reservation time
                if timedelta(minutes=-15) <= time_diff <= timedelta(hours=1):
                    self.update_table_status(reservation.table_id, TableStatus.RESERVED)
                else:
                    # If outside the reservation window, ensure table is available if it was reserved by this reservation
                    if table.status == TableStatus.RESERVED:
                        self.update_table_status(reservation.table_id, TableStatus.AVAILABLE)

            except (ValueError, TypeError):
                continue

    def search_available_table(self, branch_id, required_capacity=0):
        validate_id(branch_id, ["BRCH"])
        if not isinstance(required_capacity, int) or required_capacity < 0:
            raise ValueError("required_capacity must be a positive integer")

        self.update_reserved_tables()

        cafe_branch = self.find_cafe_branch_by_id(branch_id)
        if cafe_branch is None:
            raise ValueError("Cafe Branch not found")

        available_tables = []
        for table in cafe_branch.tables:
            if table.status != TableStatus.AVAILABLE:
                continue
            if table.capacity >= required_capacity:
                available_tables.append(table)
        return available_tables

    def update_table_status(self, table_id, status):
        validate_id(table_id, ["TABLE"])

        if not isinstance(status, TableStatus):
            raise TypeError("Status must be TableStatus")

        # Find the branch that owns this table
        found_table = False
        for branch in self.__cafe_branches:
            table = branch.find_table_by_id(table_id)
            if table:
                table.status = status
                found_table = True
                break
        
        if not found_table:
            raise ValueError("Table not found")

    # / ════════════════════════════════════════════════════════════════
    # \ BOARD GAME

    def create_board_game_to_branch(
        self, branch_id, name, genre, price, min_players, max_players, description="", requester_id=None
    ):
        self.__authorize(requester_id, [Owner, Manager])
        validate_id(branch_id, ["BRCH"])

        if not isinstance(price, (int, float)) or price < 0:
            raise ValueError("Price must be a non-negative number")
        if not isinstance(min_players, int) or min_players <= 0:
            raise ValueError("min_players must be a positive integer")
        if not isinstance(max_players, int) or max_players < min_players:
            raise ValueError("max_players must be >= min_players")

        cafe_branch = self.find_cafe_branch_by_id(branch_id)
        if cafe_branch is None:
            raise ValueError("Cafe Branch not found")

        try:
            return cafe_branch.add_board_game(
                name, genre, price, min_players, max_players, description
            )
        except (TypeError, ValueError) as e:
            raise ValueError(f"Failed to add board game: {e}")

    def get_branch_board_games(self, branch_id):
        validate_id(branch_id, ["BRCH"])

        cafe_branch = self.find_cafe_branch_by_id(branch_id)
        if cafe_branch is None:
            raise ValueError("Cafe Branch not found")

        return cafe_branch.board_games

    def find_board_game_by_id(self, board_game_id):
        validate_id(board_game_id, ["BG"])

        # Iterate through all branches to find the board game
        for branch in self.__cafe_branches:
            board_game = branch.find_board_game_by_id(board_game_id)
            if board_game:
                return board_game
        raise ValueError("Board Game not found")

    def search_board_game_by_min_players(self, branch_id, min_players):
        validate_id(branch_id, ["BRCH"])

        cafe_branch = self.find_cafe_branch_by_id(branch_id)
        if cafe_branch is None:
            raise ValueError("Cafe Branch not found")

        return cafe_branch.search_board_game_by_min_players(min_players)

    def search_board_game_by_max_players(self, branch_id, max_players):
        validate_id(branch_id, ["BRCH"])

        cafe_branch = self.find_cafe_branch_by_id(branch_id)
        if cafe_branch is None:
            raise ValueError("Cafe Branch not found")

        return cafe_branch.search_board_game_by_max_players(max_players)

    def update_board_game_status(self, board_game_id, status):
        validate_id(board_game_id, ["BG"])

        if not isinstance(status, BoardGameStatus):
            raise TypeError("Status must be BoardGameStatus")

        board_game = self.find_board_game_by_id(board_game_id)
        board_game.status = status

    def remove_board_game_by_id(self, board_game_id, requester_id=None):
        self.__authorize(requester_id, [Owner, Manager])
        validate_id(board_game_id, ["BG"])

        # Find the branch that owns this board game
        found_branch = None
        for branch in self.__cafe_branches:
            bg = branch.find_board_game_by_id(board_game_id)
            if bg:
                found_branch = branch
                break
        
        if found_branch is None:
            raise ValueError("Board Game not found")
            
        # BUG FIX: Prevent removing games that are actively being played
        bg = found_branch.find_board_game_by_id(board_game_id)
        if bg and bg.status != BoardGameStatus.AVAILABLE:
            raise ValueError("Cannot remove a board game that is currently IN_USE or in MAINTENANCE")
            
        found_branch.remove_board_game_by_id(board_game_id)

    # / ════════════════════════════════════════════════════════════════
    # \ MENU

    def create_menu_to_branch(self, branch_id):
        validate_id(branch_id, ["BRCH"])

        cafe_branch = self.find_cafe_branch_by_id(branch_id)
        if cafe_branch is None:
            raise ValueError("Cafe Branch not found")

        try:
            new_menu = MenuList()
            cafe_branch.create_menu(new_menu)
            return new_menu
        except (TypeError, ValueError) as e:
            raise ValueError(f"Failed to create menu: {e}")

    def create_menu_item_food_to_branch(self, branch_id, name, price, description="", requester_id=None):
        self.__authorize(requester_id, [Owner, Manager])
        validate_id(branch_id, ["BRCH"])

        cafe_branch = self.find_cafe_branch_by_id(branch_id)
        if cafe_branch is None:
            raise ValueError("Cafe Branch not found")

        try:
            return cafe_branch.create_menu_item_food(name, price, description)
        except (TypeError, ValueError) as e:
            raise ValueError(f"Failed to create food item: {e}")

    def create_menu_item_drink_to_branch(
        self, branch_id, name, price, cup_size, description="", requester_id=None
    ):
        self.__authorize(requester_id, [Owner, Manager])
        validate_id(branch_id, ["BRCH"])

        cafe_branch = self.find_cafe_branch_by_id(branch_id)
        if cafe_branch is None:
            raise ValueError("Cafe Branch not found")

        try:
            return cafe_branch.create_menu_item_drink(
                name, price, cup_size, description
            )
        except (TypeError, ValueError) as e:
            raise ValueError(f"Failed to create drink item: {e}")

    def get_branch_menu(self, branch_id):
        validate_id(branch_id, ["BRCH"])

        cafe_branch = self.find_cafe_branch_by_id(branch_id)
        if cafe_branch is None:
            raise ValueError("Cafe Branch not found")
        return cafe_branch.get_menu()

    def get_branch_menu_item(self, branch_id):
        validate_id(branch_id, ["BRCH"])

        cafe_branch = self.find_cafe_branch_by_id(branch_id)
        if cafe_branch is None:
            raise ValueError("Cafe Branch not found")
        return cafe_branch.get_menu_item()

    def get_branch_menu_item_food(self, branch_id):
        validate_id(branch_id, ["BRCH"])

        cafe_branch = self.find_cafe_branch_by_id(branch_id)
        if cafe_branch is None:
            raise ValueError("Cafe Branch not found")
        return cafe_branch.get_menu_item_food()

    def get_branch_menu_item_drink(self, branch_id):
        validate_id(branch_id, ["BRCH"])

        cafe_branch = self.find_cafe_branch_by_id(branch_id)
        if cafe_branch is None:
            raise ValueError("Cafe Branch not found")
        return cafe_branch.get_menu_item_drink()

    def find_menu_item_by_id(self, menu_item_id):
        validate_id(menu_item_id, ["FOOD", "DRINK"])

        # Iterate through all branches to find the menu item
        for branch in self.__cafe_branches:
            menu_item = branch.find_menu_item_by_id(menu_item_id)
            if menu_item:
                return menu_item
        raise ValueError("Menu Item not found")

    def remove_menu_item_by_id(self, menu_item_id, requester_id=None):
        self.__authorize(requester_id, [Owner, Manager])
        validate_id(menu_item_id, ["FOOD", "DRINK"])

        # Find the branch that owns this menu item
        found_branch = None
        for branch in self.__cafe_branches:
            menu_item = branch.find_menu_item_by_id(menu_item_id)
            if menu_item:
                found_branch = branch
                break
        
        if found_branch is None:
            raise ValueError("Menu Item not found")
        found_branch.remove_menu_item_by_id(menu_item_id)

    def update_menu_item_by_id(self, menu_item_id, name, price, description="", requester_id=None):
        self.__authorize(requester_id, [Owner, Manager])
        validate_id(menu_item_id, ["FOOD", "DRINK"])

        if not isinstance(name, str) or not name.strip():
            raise ValueError("Name must be a non-empty string")
        if not isinstance(price, (int, float)) or price < 0:
            raise ValueError("Price must be a non-negative number")
        if not isinstance(description, str):
            raise ValueError("Description must be a string")

        # Find the branch that owns this menu item
        found_branch = None
        for branch in self.__cafe_branches:
            menu_item = branch.find_menu_item_by_id(menu_item_id)
            if menu_item:
                found_branch = branch
                break
        
        if found_branch is None:
            raise ValueError("Menu Item not found")

        try:
            found_branch.update_menu_item_by_id(
                menu_item_id, name, price, description)
        except (TypeError, ValueError) as e:
            raise ValueError(f"Failed to update menu item: {e}")

    # / ════════════════════════════════════════════════════════════════
    # \ GAME SESSION - CHECK-IN

    def check_in_reserved(
        self, reservation_id, customer_id, current_time=None
    ):
        validate_id(reservation_id, ["RESV"])
        validate_id(customer_id, ["MEMBER", "WALK"])

        if current_time is not None and not isinstance(current_time, datetime):
            raise ValueError("current_time must be a datetime object")

        reservation = self.find_reservation_by_id(reservation_id)
        if reservation is None:
            raise ValueError("Reservation not found")

        customer = self.find_person_by_id(customer_id)
        if customer is None:
            raise ValueError("Customer not found")

        # BUG FIX: Check status FIRST before any time-based logic
        # so cancelled/no-show reservations get a clear, relevant error message
        if reservation.status == ReservationStatus.CANCELLED:
            raise ValueError("Cannot check-in: This reservation has been cancelled.")
        if reservation.status == ReservationStatus.NO_SHOW:
            raise ValueError("Cannot check-in: This reservation was marked as No-Show.")
        if reservation.status == ReservationStatus.COMPLETED:
            raise ValueError("Cannot check-in: This reservation is already completed.")

        # BUG FIX: Default to self.get_time() INSIDE the function body, not in
        # the signature, to avoid the classic 'frozen clock' mutable default bug.
        now = current_time if current_time is not None else self.get_time()
        if now < reservation.reservation_time:
            raise ValueError("Too early to check-in")

        late_limit = reservation.reservation_time + timedelta(minutes=15)
        if now > late_limit:
            reservation.status = ReservationStatus.NO_SHOW
            raise ValueError(
                "Check-in failed: You are more than 15 minutes late. Marked as No-Show."
            )

        branch = self.find_cafe_branch_by_id(reservation.branch_id)
        if branch is None:
            raise ValueError("Branch not found")

        table = branch.find_table_by_id(reservation.table_id)
        if table is None:
            raise ValueError("Table not found")
        
        if table.status == TableStatus.OCCUPIED:
            active_session = branch.find_play_session_by_id(table.table_id)
            if active_session and active_session.check_time_up(now):
                # Get bill preview for staff
                try:
                    total_amount = self.get_active_bill(active_session.session_id, current_time=now)["total_amount"]
                except Exception as e:
                    total_amount = 0.0
                raise ValueError(
                    f"FORCE CHECKOUT REQUIRED: Table {table.table_id} is occupied by expired session {active_session.session_id}. "
                    f"Estimated Total: ฿{total_amount:.2f}. "
                    f"Please perform payment and check_out for them before proceeding."
                )
            raise ValueError("Check-in failed: The table is still occupied by another session.")

        try:
            res_start = datetime.strptime(reservation.start_time, "%H:%M")
            res_end = datetime.strptime(reservation.end_time, "%H:%M")
            res_duration = (res_end - res_start).total_seconds() / 3600.0
            if res_duration < 0: res_duration += 24 # Overflow cross midnight
            
            actual_res_end = reservation.reservation_time + timedelta(hours=res_duration)

            session = PlaySession(
                reservation.table_id, 
                now, 
                reserved_duration=math.ceil(res_duration),
                reserved_end_time=actual_res_end,
                deposit=reservation.deposit
            )
            session.add_players_id(reservation.customer_id)
            session.reservation_id = reservation.reservation_id

            branch.add_play_session(session)
            reservation.status = ReservationStatus.COMPLETED
            table.status = TableStatus.OCCUPIED

            return session
        except (TypeError, ValueError) as e:
            raise ValueError(f"Failed to create play session: {e}")

    def check_in(
        self,
        branch_id,
        player_amount,
        customer_id="walk_in",
        table_id="auto",
        start_time=None,
    ):
        if start_time is None:
            actual_start = self.get_time()
        elif isinstance(start_time, datetime):
            actual_start = start_time
        else:
            parsed = None
            for fmt in ("%Y-%m-%dT%H:%M:%S", "%Y-%m-%dT%H:%M",
                        "%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M"):
                try:
                    parsed = datetime.strptime(start_time, fmt)
                    break
                except ValueError:
                    continue
            if parsed is None:
                raise ValueError(
                    "start_time format invalid. Use 'YYYY-MM-DD HH:MM' or ISO format")
            actual_start = parsed

        validate_id(branch_id, ["BRCH"])

        if not isinstance(customer_id, str):
            raise ValueError("Invalid ID : Customer ID must be a string")
        if customer_id != "walk_in":
            validate_id(customer_id, ["MEMBER", "WALK"])

        if not isinstance(player_amount, int) or player_amount <= 0:
            raise ValueError("player_amount must be a positive integer")

        self.update_reserved_tables()

        branch = self.find_cafe_branch_by_id(branch_id)
        if branch is None:
            raise ValueError("Cafe Branch not found")

        if table_id == "auto":
            tables = self.search_available_table(branch_id, player_amount)
            if not tables:
                raise ValueError("No available table")
            table = min(tables, key=lambda t: t.capacity)
        else:
            validate_id(table_id, ["TABLE"])

            table = branch.find_table_by_id(table_id)
            if table is None:
                raise ValueError("Table not found")
            if table.status == TableStatus.OCCUPIED:
                active_session = branch.find_play_session_by_id(table.table_id)
                if active_session and active_session.check_time_up(actual_start):
                    try:
                        total_amount = self.get_active_bill(active_session.session_id, current_time=actual_start)["total_amount"]
                    except:
                        total_amount = 0.0
                    raise ValueError(
                        f"FORCE CHECKOUT REQUIRED: Table {table.table_id} is occupied by expired session {active_session.session_id}. "
                        f"Estimated Total: ฿{total_amount:.2f}. "
                        f"Please perform payment and check_out for them before proceeding."
                    )
                raise ValueError("Check-in failed: The table is still occupied by another session.")
            
            if table.status != TableStatus.AVAILABLE:
                raise ValueError(f"Table is not available (Status: {table.status})")
            if table.capacity < player_amount:
                raise ValueError("Table capacity not enough")

        try:
            session = PlaySession(table.table_id, actual_start)

            if customer_id == "walk_in":
                for _ in range(player_amount):
                    session.add_players_id(self.create_customer_walk_in().user_id)
            elif "," in customer_id:
                ids = [mid.strip() for mid in customer_id.split(",") if mid.strip()]
                seen_ids = set()
                for mid in ids:
                    validate_id(mid, ["MEMBER", "WALK"])
                    if self.find_person_by_id(mid) is None:
                        raise ValueError(f"Member ID {mid} not found")
                    if mid in seen_ids:
                        raise ValueError(f"Duplicate player ID in list: {mid}")
                    if self.__is_person_in_active_session(mid):
                        raise ValueError(f"Player {mid} is already in another active session")
                    seen_ids.add(mid)
                    session.add_players_id(mid)
            else:
                if self.find_person_by_id(customer_id) is None:
                    raise ValueError(f"Member ID {customer_id} not found")
                if self.__is_person_in_active_session(customer_id):
                    raise ValueError(f"Player {customer_id} is already in another active session")
                if customer_id in session.current_players_id:
                    raise ValueError(f"Player {customer_id} is already in this session")
                session.add_players_id(customer_id)

            table.status = TableStatus.OCCUPIED
            branch.add_play_session(session)
            return session
        except (TypeError, ValueError) as e:
            raise ValueError(f"Failed to create check-in session: {e}")

    # / ════════════════════════════════════════════════════════════════
    # \ GAME SESSION - JOIN

    def join_session(self, any_id, customer_id="walk_in"):
        validate_id(any_id, ["TABLE", "PS"])

        if not isinstance(customer_id, str):
            raise ValueError("Invalid ID : Customer ID must be a string")
        if customer_id != "walk_in":
            validate_id(customer_id, ["MEMBER", "WALK"])

        # Find the branch that owns this table/session
        cafe_branch = None
        for branch in self.__cafe_branches:
            if any_id.startswith("TABLE") and branch.find_table_by_id(any_id):
                cafe_branch = branch
                break
            elif any_id.startswith("PS") and branch.find_play_session_by_id(any_id):
                cafe_branch = branch
                break

        if cafe_branch is None:
            raise ValueError("Cafe Branch not found")

        play_session = (cafe_branch.find_play_session_by_id(any_id))
        if play_session is None:
            raise ValueError("Play Session not found")

        if customer_id != "walk_in" and self.__is_person_in_active_session(customer_id):
            raise ValueError(f"Player {customer_id} is already in an active session")

        try:
            table = cafe_branch.find_table_by_id(play_session.table_id)
            if table is None:
                raise ValueError("Table for this session not found")

            if play_session.get_total_players() >= table.capacity:
                raise ValueError(
                    f"Table capacity is full ({table.capacity}/{table.capacity})")

            if customer_id == "walk_in":
                play_session.add_players_id(
                    self.create_customer_walk_in().user_id)
            else:
                if self.find_person_by_id(customer_id) is None:
                    raise ValueError(f"Member ID {customer_id} not found")
                if customer_id in play_session.current_players_id:
                    raise ValueError(f"Player {customer_id} is already in this session")
                play_session.add_players_id(customer_id)
            return True
        except (TypeError, ValueError) as e:
            raise ValueError(f"Failed to join session: {e}")

    # / ════════════════════════════════════════════════════════════════
    # \ GAME SESSION - BORROW BOARD GAME

    def borrow_board_game(self, any_id, board_game_id, current_time=None):
        validate_id(any_id, ["TABLE", "PS"])
        validate_id(board_game_id, ["BG"])

        # Find the branch that owns this table/session
        cafe_branch = None
        for branch in self.__cafe_branches:
            if any_id.startswith("TABLE") and branch.find_table_by_id(any_id):
                cafe_branch = branch
                break
            elif any_id.startswith("PS") and branch.find_play_session_by_id(any_id):
                cafe_branch = branch
                break

        if cafe_branch is None:
            raise ValueError("Cafe Branch not found")

        play_session = (cafe_branch.find_play_session_by_id(any_id))
        if play_session is None:
            raise ValueError("Play Session not found")
        
        self.__validate_session_time(play_session, current_time)

        if len(play_session.current_board_games_id) + 1 > 2:
            raise ValueError("Maximum 2 board games per session")
            # return None

        board_game = cafe_branch.find_board_game_by_id(board_game_id)
        if board_game is None:
            raise ValueError("Board Game not found")

        if board_game.status != BoardGameStatus.AVAILABLE:
            raise ValueError("Board Game is not available")

        try:
            play_session.add_board_games_id(board_game_id)
            board_game.status = BoardGameStatus.IN_USE
            return board_game
        except (TypeError, ValueError) as e:
            raise ValueError(f"Failed to borrow board game: {e}")

    def return_board_game(self, any_id, board_game_id, is_damaged=False):
        validate_id(any_id, ["TABLE", "PS"])
        validate_id(board_game_id, ["BG"])

        # Find the branch that owns this table/session
        cafe_branch = None
        for branch in self.__cafe_branches:
            if any_id.startswith("TABLE") and branch.find_table_by_id(any_id):
                cafe_branch = branch
                break
            elif any_id.startswith("PS") and branch.find_play_session_by_id(any_id):
                cafe_branch = branch
                break

        if cafe_branch is None:
            raise ValueError("Cafe Branch not found")

        play_session = (cafe_branch.find_play_session_by_id(any_id))
        if play_session is None:
            raise ValueError("Play Session not found")

        board_game = cafe_branch.find_board_game_by_id(board_game_id)
        if board_game is None:
            raise ValueError("Board Game not found")

        if board_game_id not in play_session.current_board_games_id:
            raise ValueError("This session did not borrow this board game")

        try:
            damage_flag = is_damaged
            if damage_flag:
                board_game.status = BoardGameStatus.MAINTENANCE
                play_session.add_game_penalty(board_game_id, board_game.price)
            else:
                board_game.status = BoardGameStatus.AVAILABLE
            play_session.remove_board_games_id(board_game_id)
            return board_game
        except (TypeError, ValueError) as e:
            raise ValueError(f"Failed to return board game: {e}")

    def maintenance_board_game(self, board_game_id, requester_id=None):
        self.__authorize(requester_id, [Owner, Manager, Staff])
        validate_id(board_game_id, ["BG"])

        # Find the branch that owns this board game
        cafe_branch = None
        for branch in self.__cafe_branches:
            bg = branch.find_board_game_by_id(board_game_id)
            if bg:
                cafe_branch = branch
                break

        if cafe_branch is None:
            raise ValueError("Board Game not found")

        board_game = cafe_branch.find_board_game_by_id(board_game_id)
        if board_game is None:
            raise ValueError("Board Game not found")

        for session in cafe_branch.get_play_sessions():
            if board_game_id in session.current_board_games_id:
                raise ValueError("Board Game is currently in use")

        board_game.status = BoardGameStatus.MAINTENANCE
        return board_game

    # / ════════════════════════════════════════════════════════════════
    # \ GAME SESSION - ORDER

    def take_order(self, any_id, menu_item_id, current_time=None):
        validate_id(any_id, ["TABLE", "PS"])
        validate_id(menu_item_id, ["FOOD", "DRINK"])

        # Find the branch that owns this table/session
        cafe_branch = None
        for branch in self.__cafe_branches:
            if any_id.startswith("TABLE") and branch.find_table_by_id(any_id):
                cafe_branch = branch
                break
            elif any_id.startswith("PS") and branch.find_play_session_by_id(any_id):
                cafe_branch = branch
                break

        if cafe_branch is None:
            raise ValueError(
                "Play Session already closed or Cafe Branch not found")

        play_session = (cafe_branch.find_play_session_by_id(any_id))
        if play_session is None:
            raise ValueError("Play Session not found")
        
        self.__validate_session_time(play_session, current_time)


        menu_item = cafe_branch.find_menu_item_by_id(menu_item_id)
        if menu_item is None:
            raise ValueError("Menu Item not found")

        try:
            return play_session.take_order(menu_item)
        except (TypeError, ValueError) as e:
            raise ValueError(f"Failed to take order: {e}")

    def get_play_session_orders(self, any_id: str):

        validate_id(any_id, ["PS", "TABLE"])

        # Find the branch that owns this table/session
        cafe_branch = None
        for branch in self.__cafe_branches:
            if any_id.startswith("TABLE") and branch.find_table_by_id(any_id):
                cafe_branch = branch
                break
            elif any_id.startswith("PS") and branch.find_play_session_by_id(any_id):
                cafe_branch = branch
                break

        if cafe_branch is None:
            raise ValueError("Cafe Branch not found")
        return cafe_branch.get_play_session_orders(any_id)

    def update_order(self, play_session_id, order_id, session_status):
        validate_id(play_session_id, ["PS", "TABLE"])
        validate_id(order_id, ["ORDER"])

        # Find the branch that owns this session
        cafe_branch = None
        for branch in self.__cafe_branches:
            if branch.find_play_session_by_id(play_session_id):
                cafe_branch = branch
                break

        if cafe_branch is None:
            raise ValueError("Cafe Branch not found")

        play_session = (cafe_branch.find_play_session_by_id(play_session_id))
        if play_session is None:
            raise ValueError("Play Session not found")

        for order in play_session.current_order:
            if order.order_id == order_id:
                try:
                    order.set_order_status(session_status)
                except (TypeError, ValueError) as e:
                    raise ValueError(f"Failed to update order: {e}")
                return

        raise ValueError("Order not found")

    def update_order_preparing(self, play_session_id, order_id):
        self.update_order(play_session_id, order_id, OrderStatus.PREPARING)

    def update_order_serve(self, play_session_id, order_id):
        self.update_order(play_session_id, order_id, OrderStatus.SERVED)

    def update_order_cancel(self, play_session_id, order_id):
        validate_id(play_session_id, ["PS", "TABLE"])
        validate_id(order_id, ["ORDER"])

        # Find the branch that owns this session
        cafe_branch = None
        for branch in self.__cafe_branches:
            if (play_session_id.startswith("PS") and branch.find_play_session_by_id(play_session_id)) or \
               (play_session_id.startswith("TABLE") and branch.find_play_session_by_table_id(play_session_id)):
                cafe_branch = branch
                break

        if cafe_branch is None:
            raise ValueError("Cafe Branch not found")

        play_session = (cafe_branch.find_play_session_by_id(play_session_id))
        if play_session is None:
            raise ValueError("Play Session not found")

        for order in play_session.current_order:
            if order.order_id == order_id:
                if order.status == OrderStatus.SERVED:
                    raise ValueError(
                        "Cannot cancel an order that has already been served")
                self.update_order(play_session_id, order_id,
                                  OrderStatus.CANCELLED)
                return

        raise ValueError("Order not found")

    # / ════════════════════════════════════════════════════════════════
    # \ GAME SESSION - CHECK-OUT

    def check_out(self, any_id, method_type="cash", end_time=None, **kwargs):
        validate_id(any_id, ["TABLE", "PS"])

        if not isinstance(method_type, str):
            raise ValueError("method_type must be a string")
        if method_type not in ["cash", "card", "online"]:
            raise ValueError(
                f"Invalid payment method: '{method_type}'. Allowed: 'cash', 'card', 'online'"
            )

        actual_end_time = end_time if end_time is not None else self.get_time()

        # Find the branch - check both active sessions and tables
        cafe_branch = None
        for branch in self.__cafe_branches:
            if any_id.startswith("TABLE") and branch.find_table_by_id(any_id):
                cafe_branch = branch
                break
            elif any_id.startswith("PS") and (
                branch.find_play_session_by_id(any_id) or
                branch.find_play_session_history_by_id(any_id)
            ):
                cafe_branch = branch
                break

        if cafe_branch is None:
            raise ValueError("Cafe Branch not found")

        play_session = (cafe_branch.find_play_session_by_id(any_id))
        if play_session is None:
            # Check history to provide a better error message if it was already checked out
            history_session = self.find_play_session_history_by_id(any_id)
            if history_session is not None:
                raise ValueError("This session already checked out")
            raise ValueError("Play Session not found")

        if play_session.payment is not None:
            raise ValueError("This session already checked out")

        # BUG FIX: Prevent checkout if they haven't returned board games!
        if play_session.current_board_games_id:
            raise ValueError("Cannot checkout while there are unreturned board games. Please return them first.")

        actual_duration = play_session.duration(actual_end_time)

        try:
            items = self.__calculate_bill(play_session)
            total = 0.0
            for label, amount in items:
                if label == "TOTAL":
                    total = amount
                    break
        except Exception as e:
            raise ValueError(f"Error calculating bill: {e}")
        
        table = cafe_branch.find_table_by_id(play_session.table_id)

        # 2. Process Payment (raises if insufficient cash)
        payment = self.create_payment(total, method_type, **kwargs)
        
        play_session.end_time = actual_end_time
        payment.payment_time = actual_end_time
        play_session.payment = payment

        # 3. Update Member Stats (Side effects - should not block checkout completion)
        try:
            for cp in play_session.current_players_id:
                customer = self.find_person_by_id(cp)
                if isinstance(customer, Member):
                    # Table cost part of the spent (roughly)
                    duration_cost = Table.price_per_hour * actual_duration
                    self.add_spent(cp, duration_cost)
                elif isinstance(customer, WalkInCustomer):
                    try:
                        self.remove_person_by_id(cp)
                    except ValueError:
                        pass
        except Exception as e:
            # We log the error but don't fail the checkout because money was paid
            print(f"Checkout log: Side-effect error (spent update): {e}")

        # 4. Finalize Session (Remove from active list)
        cafe_branch.end_play_session(play_session.session_id, actual_end_time)
        
        if table is not None:
            table.status = TableStatus.AVAILABLE
        return payment, total

    def auto_force_checkout(self, session_id, staff_id, method_type="cash", current_time=None, **kwargs):
        """
        Force a checkout for an overstayed session. 
        Requires a valid staff_id and supports all payment methods.
        Smart Cleanup: Automatically returns board games and cancels pending orders.
        """
        # 1. Validate staff
        staff = self.find_person_by_id(staff_id)
        if not staff or not isinstance(staff, Staff):
            raise ValueError("Unauthorized: Only staff members can perform force checkout.")

        # 2. Smart Cleanup
        session = self.find_play_session_by_id(session_id)
        if session:
            # Auto-return board games
            for bg_id in list(session.current_board_games_id):
                try:
                    self.return_board_game(session_id, bg_id, is_damaged=False)
                except:
                    pass
            
            # Auto-cancel pending/preparing orders
            for order in list(session.current_order):
                if order.status in [OrderStatus.PENDING, OrderStatus.PREPARING]:
                    try:
                        self.update_order_cancel(session_id, order.order_id)
                    except:
                        pass

        # 3. Perform regular checkout with the specified method and extra parameters
        return self.check_out(session_id, method_type=method_type, end_time=current_time, **kwargs)

    # / ════════════════════════════════════════════════════════════════
    # \ PAYMENT

    def create_payment(self, total, method_type="cash", **kwargs):
        if not isinstance(total, (int, float)) or total < 0:
            raise ValueError("Total must be a non-negative number")
        if not isinstance(method_type, str):
            raise ValueError("method_type must be a string")

        if method_type == "cash":
            try:
                paid_amount = kwargs.get("paid_amount", total)
                paid_amount = float(paid_amount)
            except (TypeError, ValueError):
                raise ValueError("paid_amount must be a valid number")

            if paid_amount < total:
                raise ValueError("Paid amount is not enough")

            change = paid_amount - total
            payment_method = Cash(paid_amount)
            payment_method.change = change

        elif method_type == "card":
            try:
                payment_method = CreditCard(
                    kwargs["card_number"], kwargs["expiry_date"], kwargs["cvv"]
                )
            except KeyError as e:
                raise ValueError(
                    f"Missing required field for card payment: {e}")
            except (TypeError, ValueError) as e:
                raise ValueError(f"Invalid card payment details: {e}")

        elif method_type == "online":
            try:
                payment_method = OnlinePayment(kwargs["email"])
            except KeyError:
                raise ValueError(
                    "Missing required field for online payment: email")
            except (TypeError, ValueError) as e:
                raise ValueError(f"Invalid online payment details: {e}")

        else:
            raise ValueError(
                f"Invalid payment method: '{method_type}'. Allowed: 'cash', 'card', 'online'"
            )

        try:
            if payment_method.validate_method():
                new_payment = Payment(total, payment_method)
                return new_payment
        except Exception as e:
            raise ValueError(f"Payment validation failed: {e}")

    def get_active_bill(self, session_id, current_time=None):
        play_session = self.find_play_session_by_id(session_id)
        if play_session is None:
            raise ValueError("Play Session not found")
        
        original_end = play_session.end_time
        if current_time is None:
            current_time = self.get_time()
            
        play_session.end_time = current_time
        try:
            items = self.__calculate_bill(play_session)
            total = 0.0
            for label, amount in items:
                if label == "TOTAL":
                    total = amount
            return {"items": items, "total_amount": total}
        finally:
            play_session.end_time = original_end

    def bill_history(self, session_id: str) -> list:
        validate_id(session_id, ["PS"])
        for branch in self.__cafe_branches:
            for session in branch.get_play_sessions_history():
                if session.session_id == session_id:
                    return self.__calculate_bill(session)
        raise ValueError(f"Session {session_id} not found")

    def bill_history_by_person(self, person_id: str) -> list:
        validate_id(person_id, ["MEMBER", "WALK", "OWNER", "MANAGER", "STAFF"])
        items = []
        for branch in self.__cafe_branches:
            for session in branch.get_play_sessions_history():
                if person_id in session.current_players_id:
                    items.append(
                        (f"Session {session.session_id}", None))  # header
                    items += self.__calculate_bill(session)
        return items

    def __authorize(self, requester_id, allowed_roles):
        """
        Check if the requester_id belongs to one of the allowed_roles.
        allowed_roles can be a list of classes (Owner, Manager, Staff, etc.)
        Also allowed 'system' as a special requester for bootstrap.
        """
        if requester_id == "system":
            return True
        
        # If no owner exists in the system, allow anyone to bootstrap
        owners = [p for p in self.__person if isinstance(p, Owner)]
        if not owners:
            return True

        try:
            person = self.find_person_by_id(requester_id)
            if any(isinstance(person, role) for role in allowed_roles):
                return True
            raise PermissionError(f"User {requester_id} is not authorized for this action.")
        except ValueError:
            raise PermissionError(f"User {requester_id} not found.")

    def __is_person_in_active_session(self, person_id: str) -> bool:
        if person_id.startswith("WALK-"):
            return False
        
        for branch in self.__cafe_branches:
            for session in branch.get_play_sessions():
                if person_id in session.current_players_id:
                    return True
        return False

    def __check_future_reservations(self, table_id, current_time=None):
        if current_time is None:
            current_time = self.get_time()
        

        for res in self.__reservations:
            if res.table_id == table_id and res.status == ReservationStatus.PENDING:
                time_diff = (res.reservation_time - current_time).total_seconds() / 60.0
                if -15 <= time_diff <= 30: # From 15 mins late to 30 mins in future
                    return True
        return False

    def __validate_session_time(self, play_session, current_time=None):
        if current_time is None:
            current_time = self.get_time()
        if play_session.check_time_up(current_time):
            if self.__check_future_reservations(play_session.table_id, current_time):
                raise ValueError("Time up! This table is reserved for the next guest. Please proceed to Checkout.")
            else:
                raise ValueError("Time up! Your reserved time has ended. Would you like to extend your session? (Please contact staff)")

    def __calculate_bill(self, session) -> list:
        cafe_branch = None
        for branch in self.__cafe_branches:
            if any(s.session_id == session.session_id for s in branch.get_play_sessions()):
                cafe_branch = branch
                break
            if any(s.session_id == session.session_id for s in branch.get_play_sessions_history()):
                cafe_branch = branch
                break
                
        if cafe_branch is None:
            raise ValueError(f"Cafe Branch not found for session {session.session_id}")

        items = []
        total = 0.0

        # ── ค่าโต๊ะ ──────────────────────────────
        duration = session.duration()
        total_players = session.get_total_players()
        table_cost = Table.price_per_hour * duration * total_players
        items.append(
            (f"Table fee ({duration} hr x {total_players} players @ ฿{Table.price_per_hour}/hr)", table_cost))
        total += table_cost

        # ── อาหาร/เครื่องดื่มที่เสิร์ฟแล้ว ──────
        for order in session.current_order:
            if order.status == OrderStatus.SERVED:
                items.append(
                    (f"[Order] {order.snapshot_name}", order.snapshot_price))
                total += order.snapshot_price

        # ── ส่วนลด Member ────────────────────────
        discount = 0.0
        for player_id in session.current_players_id:
            try:
                player = self.find_person_by_id(player_id)
                if isinstance(player, Member):
                    discount = max(discount, player.get_discount())
            except ValueError:
                continue

        discount_amount = total * discount
        if discount_amount > 0:
            items.append(
                (f"Discount ({int(discount * 100)}%)", -discount_amount))
            total -= discount_amount

        # ── ค่าปรับบอร์ดเกม ──────────────────────  ← ย้ายมาอยู่หลัง discount
        penalty_fee = 0.0
        for penalty in session.game_penalty:
            game_id = penalty.get("game_id")
            price_val = penalty.get("price", 0.0)
            
            # Find board game name if possible, otherwise use game_id
            board_game = cafe_branch.find_board_game_by_id(game_id)
            name_str = board_game.name if board_game else game_id
            
            items.append((f"[Penalty] Damaged: {name_str}", price_val))
            penalty_fee += price_val

        total += penalty_fee

        # ── หักเงินมัดจำ (ถ้ามี) ──────────────────
        if session.deposit > 0:
            items.append(("Reservation Deposit Deduction", -session.deposit))
            total -= session.deposit

        items.append(("TOTAL", total))
        return items
# | ════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
# | #EFFF11


class CafeBranch:
    __counter = 0

    def __init__(self, name, location=""):
        self.__branch_id = "BRCH-" + str(CafeBranch.__counter).zfill(5)
        CafeBranch.__counter += 1
        self.__name = name
        self.__location = location
        self.__tables = []
        self.__board_games = []
        self.__menu_list = MenuList()
        self.__staff_id = []
        self.__manager_id = None
        self.__owner_id = None
        self.__play_sessions = []
        self.__play_sessions_history = []

    # / ════════════════════════════════════════════════════════════════
    # - Getters
    # / ════════════════════════════════════════════════════════════════

    @property
    def branch_id(self):
        return self.__branch_id

    @property
    def name(self):
        return self.__name

    @property
    def location(self):
        return self.__location

    @property
    def menu_list(self):
        return self.__menu_list

    @property
    def tables(self):
        return self.__tables.copy()

    @property
    def board_games(self):
        return self.__board_games.copy()

    @property
    def total_tables(self):
        return len(self.__tables)

    @property
    def total_board_games(self):
        return len(self.__board_games)

    @property
    def manager_id(self):
        return self.__manager_id

    # / ════════════════════════════════════════════════════════════════
    # - Setters
    # / ════════════════════════════════════════════════════════════════

    @name.setter
    def name(self, name):
        self.__name = name

    @location.setter
    def location(self, location):
        self.__location = location

    # / ════════════════════════════════════════════════════════════════
    # - Methods
    # / ════════════════════════════════════════════════════════════════
    # \ TABLE

    def add_table(self, capacity):
        new_table = Table(capacity)
        self.__tables.append(new_table)
        return new_table

    def get_tables(self):
        return self.__tables.copy()

    def find_table_by_id(self, table_id):
        for table in self.__tables:
            if table.table_id == table_id:
                return table
        return None

    # / ════════════════════════════════════════════════════════════════
    # \ BOARD GAME

    def add_board_game(
        self, name, genre, price, min_players, max_players, description=""
    ):
        new_board_game = BoardGame(
            name, genre, price, min_players, max_players, description
        )
        self.__board_games.append(new_board_game)
        return new_board_game

    def get_board_games(self):
        return self.__board_games.copy()

    def find_board_game_by_id(self, board_game_id):
        for board_game in self.__board_games:
            if board_game.game_id == board_game_id:
                return board_game
        return None

    def search_board_game_by_min_players(self, min_players):
        return [bg for bg in self.__board_games
                if bg.min_players <= min_players <= bg.max_players]

    def search_board_game_by_max_players(self, max_players):
        return [bg for bg in self.__board_games
                if bg.min_players <= max_players <= bg.max_players]

    def remove_board_game_by_id(self, board_game_id):
        self.__board_games = [
            board_game
            for board_game in self.__board_games
            if board_game.game_id != board_game_id
        ]

    # / ════════════════════════════════════════════════════════════════
    # \ MENU

    def create_menu(self, menu):
        if not isinstance(menu, MenuList):
            raise TypeError("Type Error : must be an instance of Menu")
        self.__menu_list = menu

    def create_menu_item_food(self, name, price, description=""):
        if self.__menu_list is None:
            raise ValueError("Menu not found")

        new_menu_item = Food(name, price, description)
        self.__menu_list.add_menu_item(new_menu_item)
        return new_menu_item

    def create_menu_item_drink(self, name, price, cup_size="S", description=""):
        if self.__menu_list is None:
            raise ValueError("Menu not found")

        new_menu_item = Drink(name, price, description, cup_size=cup_size)
        self.__menu_list.add_menu_item(new_menu_item)
        return new_menu_item

    def get_menu(self):
        if self.__menu_list is None:
            raise ValueError("Menu not found")
        return self.__menu_list

    def get_menu_item(self):
        if self.__menu_list is None:
            raise ValueError("Menu not found")
        return self.__menu_list.menu_items

    def get_menu_item_food(self):
        if self.__menu_list is None:
            raise ValueError("Menu not found")
        return self.__menu_list.get_menu_item_food()

    def get_menu_item_drink(self):
        if self.__menu_list is None:
            raise ValueError("Menu not found")
        return self.__menu_list.get_menu_item_drink()

    def find_menu_item_by_id(self, menu_item_id):
        if self.__menu_list is None:
            raise ValueError("Menu not found")
        return self.__menu_list.find_menu_item_by_id(menu_item_id)

    def remove_menu_item_by_id(self, menu_item_id):
        if self.__menu_list is None:
            raise ValueError("Menu not found")
        self.__menu_list.remove_menu_item(menu_item_id)

    def update_menu_item_by_id(self, menu_item_id, name, price, description=""):
        if self.__menu_list is None:
            raise ValueError("Menu not found")

        menu_item = self.__menu_list.find_menu_item_by_id(menu_item_id)
        if menu_item is None:
            raise ValueError("Menu Item not found")

        try:
            menu_item.name = name
            menu_item.price = price
            menu_item.description = description
        except (TypeError, ValueError) as e:
            raise ValueError(f"Cannot update menu item: {e}")

    # / ════════════════════════════════════════════════════════════════
    # \ ORDER

    def get_play_session_orders(self, any_id: str):

        play_session = self.find_play_session_by_id(any_id)
        if play_session is None:
            raise ValueError("Play Session not found")
        return play_session.current_order

    # / ════════════════════════════════════════════════════════════════
    # \ PLAY SESSION
    def get_play_sessions_history(self):
        return self.__play_sessions_history.copy()

    def add_play_session(self, play_session):
        if not isinstance(play_session, PlaySession):
            raise TypeError("Type Error : must be an instance of PlaySession")
        self.__play_sessions.append(play_session)

    def get_play_sessions(self):
        return self.__play_sessions.copy()

    def find_play_session_by_id(self, any_id):
        try:
            if any_id.startswith("PS-"):
                for play_session in self.__play_sessions:
                    if play_session.session_id == any_id:
                        return play_session
            elif any_id.startswith("TABLE-"):
                for play_session in self.__play_sessions:
                    if play_session.table_id == any_id:
                        return play_session
            else:
                raise ValueError(
                    "Invalid ID : ID must be start with PS or TABLE")
            return None
        except (AttributeError, TypeError):
            raise ValueError("Invalid ID format")

    def find_play_session_history_by_id(self, any_id):
        try:
            if any_id.startswith("PS-"):
                for play_session in self.__play_sessions_history:
                    if play_session.session_id == any_id:
                        return play_session
            elif any_id.startswith("TABLE-"):
                for play_session in self.__play_sessions_history:
                    if play_session.table_id == any_id:
                        return play_session
            else:
                raise ValueError(
                    "Invalid ID : ID must be start with PS or TABLE")
            return None
        except (AttributeError, TypeError):
            raise ValueError("Invalid ID format")

    def remove_play_session_by_id(self, play_session_id):
        play_session = self.find_play_session_by_id(play_session_id)
        if play_session is None:
            raise ValueError("Invalid ID : Play Session not found")
        self.__play_sessions.remove(play_session)

    def end_play_session(self, play_session_id, end_time=None):
        if end_time is None:
             raise ValueError("end_time must be provided to end_play_session")

        play_session = self.find_play_session_by_id(play_session_id)
        if play_session is None:
            raise ValueError("Invalid ID : Play Session not found")

        try:
            play_session.end_time = end_time
            self.__play_sessions_history.append(play_session)
            self.__play_sessions.remove(play_session)
        except (TypeError, ValueError) as e:
            raise ValueError(f"Failed to end play session: {e}")

    # / ════════════════════════════════════════════════════════════════
    # \ STAFF

    def add_staff(self, staff):
        if not isinstance(staff, Staff):
            raise TypeError("Type Error : must be an instance of Staff")
        self.__staff_id.append(staff.user_id)

    def get_staff(self):
        return self.__staff_id.copy()

    def remove_staff_by_id(self, staff_id):
        if staff_id not in self.__staff_id:
            raise ValueError("Invalid ID : ID does not exist")
        self.__staff_id.remove(staff_id)

    # / ════════════════════════════════════════════════════════════════
    # \ MANAGER

    def add_manager(self, manager):
        if not isinstance(manager, Manager):
            raise TypeError("Type Error : must be an instance of Manager")
        self.__manager_id = manager.user_id

    def get_manager(self):
        return self.__manager_id

    def remove_manager(self):
        self.__manager_id = None

    # / ════════════════════════════════════════════════════════════════
    # \ OWNER

    def add_owner(self, owner):
        if not isinstance(owner, Owner):
            raise TypeError("Type Error : must be an instance of Owner")
        self.__owner_id = owner.user_id

    def get_owner(self):
        return self.__owner_id

    def remove_owner(self):
        self.__owner_id = None

    # / ════════════════════════════════════════════════════════════════


# | ════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════