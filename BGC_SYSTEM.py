from datetime import *
import time
import random

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

    # / ════════════════════════════════════════════════════════════════
    # - Methods
    # / ════════════════════════════════════════════════════════════════
    # \ PERSON METHOD

    def add_person(self, person):
        if not isinstance(person, Person):
            raise TypeError("Type Error : must be an instance of Person")
        self.__person.append(person)

    def create_owner(self, name):
        try:
            new_owner = Owner(name)
            self.add_person(new_owner)
            return new_owner
        except (TypeError, ValueError) as e:
            raise ValueError(f"Failed to create owner: {e}")

    def create_manager(self, name):
        try:
            new_manager = Manager(name)
            self.add_person(new_manager)
            return new_manager
        except (TypeError, ValueError) as e:
            raise ValueError(f"Failed to create manager: {e}")

    def create_staff(self, name):
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

    def add_owner_to_branch(self, branch_id, owner_id):
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
        except TypeError as e:
            raise ValueError(f"Cannot add owner: {e}")

    def add_manager_to_branch(self, branch_id, manager_id):
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
        except TypeError as e:
            raise ValueError(f"Cannot add manager: {e}")

    def add_staff_to_branch(self, branch_id, staff_id):
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

    def remove_person_by_id(self, user_id):
        validate_id(user_id, ["OWNER", "MANAGER", "STAFF", "MEMBER", "WALK"])

        person = self.find_person_by_id(user_id)
        if person is None:
            raise ValueError("Invalid ID : Person not found")

        self.__person.remove(person)

    def update_person_by_id(self, user_id, name):
        validate_id(user_id, ["OWNER", "MANAGER", "STAFF", "MEMBER", "WALK"])

        person = self.find_person_by_id(user_id)
        if person is None:
            raise ValueError("Invalid ID : Person not found")

        try:
            person.name = name
        except ValueError as e:
            raise ValueError(f"Cannot update person : {e}")

    def add_spent(self, customer_id, amount, authorizer_id):
        """
        Add total spent to a customer's account.
        Only Owners or Managers can authorize this action.
        """
        validate_id(customer_id, ["MEMBER", "WALK"])

        if not isinstance(amount, (int, float)) or amount <= 0:
            raise ValueError("Amount must be a positive number")

        # Check authorization
        authorizer = self.find_person_by_id(authorizer_id)
        if not authorizer:
            raise ValueError("Authorizer not found")
            
        if not (isinstance(authorizer, Owner) or isinstance(authorizer, Manager)):
            raise ValueError("Unauthorized: Only Owners and Managers can add spent amount directly.")

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

    def create_cafe_branch(self, cafe_branch_name, cafe_branch_location=""):
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
                if cafe_branch.find_play_session_by_id(_id):
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

    def find_cafe_branch_by_name(self, name):
        if not isinstance(name, str):
            return None

        name = name.lower()
        for cafe_branch in self.__cafe_branches:
            if cafe_branch.name.lower() == name:
                return cafe_branch
        return None

    def remove_cafe_branch_by_id(self, cafe_branch_id):
        validate_id(cafe_branch_id, ["BRCH"])

        cafe_branch = self.find_cafe_branch_by_id(cafe_branch_id)
        if cafe_branch is None:
            raise ValueError("Invalid ID : Cafe Branch not found")

        self.__cafe_branches.remove(cafe_branch)

    def update_cafe_branch_by_id(self, branch_id, name, location):
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
    ):
        validate_id(customer_id, ["MEMBER", "WALK"])
        validate_id(branch_id, ["BRCH"])

        if not isinstance(total_player, int) or total_player <= 0:
            raise ValueError("total_player must be a positive integer")

        customer = self.find_person_by_id(customer_id)
        if customer is None:
            raise ValueError("Customer not found.")

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

        # 🟢 ด่านที่ 4: สร้างการจอง
        try:
            new_reservation = Reservation(
                customer_id,
                branch_id,
                target_table.table_id,
                date,
                start_time,
                end_time,
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

        now = current_time if current_time is not None else datetime.now()

        try:
            reservation_time = datetime.strptime(
                f"{reservation.date} {reservation.start_time}", "%Y-%m-%d %H:%M"
            )
        except ValueError as e:
            raise ValueError(f"Invalid reservation date/time format: {e}")

        if now > reservation_time:
            raise ValueError(
                "Cannot cancel. The reservation time has already passed.")

        reservation.status = ReservationStatus.CANCELLED

        try:
            branch = self.find_cafe_branch_by_id(reservation.branch_id)
            if branch is not None:
                table = branch.find_table_by_id(reservation.table_id)
                if table is not None and table.status == TableStatus.RESERVED:
                    table.status = TableStatus.AVAILABLE
        except Exception:
            pass  # ไม่ block การยกเลิกหากหาโต๊ะไม่เจอ

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

        today = datetime.now().date()
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
            ValueError("Invalid time format. Expected HH:MM.")

        duration_hrs = (end_dt - start_dt).total_seconds() / 3600
        if duration_hrs <= 0:
            duration_hrs += 24

        if duration_hrs <= 0 or duration_hrs > 24:
            raise ValueError(
                "End time must be after start time or within 24 hours.")

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
            ValueError(
                "I nvalid date/time format. Expected YYYY-MM-DD and HH:MM.")

        lead_time = reservation_time - datetime.now()
        one_hour = timedelta(hours=1)

        if lead_time < one_hour:
            raise ValueError(
                "Minimum lead time not met. Tables require at least 1 hour(s) advance booking."
            )

    # / ════════════════════════════════════════════════════════════════
    # \ TABLE

    def create_table_to_branch(self, branch_id, capacity):
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
        now = datetime.now()
        for reservation in self.__reservations:
            try:
                reservation_time = reservation.reservation_time
                time_diff = reservation_time - now
                if timedelta(hours=0) <= time_diff <= timedelta(hours=1):
                    self.update_table_status(
                        reservation.table_id, TableStatus.RESERVED)
                elif time_diff < timedelta(hours=0):
                    self.update_table_status(
                        reservation.table_id, TableStatus.AVAILABLE
                    )
            except (ValueError, TypeError):
                continue  # ข้ามการจองที่มีข้อมูลผิดพลาด

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

        cafe_branch = self.find_cafe_branch_by_id(table_id)
        if cafe_branch is None:
            raise ValueError("Cafe Branch not found")

        table = cafe_branch.find_table_by_id(table_id)
        if table is None:
            raise ValueError("Table not found")

        table.status = status

    # / ════════════════════════════════════════════════════════════════
    # \ BOARD GAME

    def create_board_game_to_branch(
        self, branch_id, name, genre, price, min_players, max_players, description=""
    ):
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

        cafe_branch = self.find_cafe_branch_by_id(board_game_id)
        if cafe_branch is None:
            raise ValueError("Board Game not found")

        board_game = cafe_branch.find_board_game_by_id(board_game_id)
        if board_game is None:
            raise ValueError("Board Game not found")

        return board_game

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

        return cafe_branch.search_board_game_by_min_players(max_players)

    def update_board_game_status(self, board_game_id, status):
        validate_id(board_game_id, ["BG"])

        if not isinstance(status, BoardGameStatus):
            raise TypeError("Status must be BoardGameStatus")

        board_game = self.find_board_game_by_id(board_game_id)
        board_game.status = status

    def remove_board_game_by_id(self, board_game_id):
        validate_id(board_game_id, ["BG"])

        cafe_branch = self.find_cafe_branch_by_id(board_game_id)
        if cafe_branch is None:
            raise ValueError("Board Game not found")
        cafe_branch.remove_board_game_by_id(board_game_id)

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

    def create_menu_item_food_to_branch(self, branch_id, name, price, description=""):
        validate_id(branch_id, ["BRCH"])

        cafe_branch = self.find_cafe_branch_by_id(branch_id)
        if cafe_branch is None:
            raise ValueError("Cafe Branch not found")

        try:
            return cafe_branch.create_menu_item_food(name, price, description)
        except (TypeError, ValueError) as e:
            raise ValueError(f"Failed to create food item: {e}")

    def create_menu_item_drink_to_branch(
        self, branch_id, name, price, cup_size="S", description=""
    ):
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

        cafe_branch = self.find_cafe_branch_by_id(menu_item_id)
        if cafe_branch is None:
            raise ValueError("Menu Item not found")
        return cafe_branch.find_menu_item_by_id(menu_item_id)

    def remove_menu_item_by_id(self, menu_item_id):
        validate_id(menu_item_id, ["FOOD", "DRINK"])

        cafe_branch = self.find_cafe_branch_by_id(menu_item_id)
        if cafe_branch is None:
            raise ValueError("Menu Item not found")
        cafe_branch.remove_menu_item_by_id(menu_item_id)

    def update_menu_item_by_id(self, menu_item_id, name, price, description=""):
        validate_id(menu_item_id, ["FOOD", "DRINK"])

        if not isinstance(name, str) or not name.strip():
            raise ValueError("Name must be a non-empty string")
        if not isinstance(price, (int, float)) or price < 0:
            raise ValueError("Price must be a non-negative number")
        if not isinstance(description, str):
            raise ValueError("Description must be a string")

        cafe_branch = self.find_cafe_branch_by_id(menu_item_id)
        if cafe_branch is None:
            raise ValueError("Menu Item not found")

        try:
            cafe_branch.update_menu_item_by_id(
                menu_item_id, name, price, description)
        except (TypeError, ValueError) as e:
            raise ValueError(f"Failed to update menu item: {e}")

    # / ════════════════════════════════════════════════════════════════
    # \ GAME SESSION - CHECK-IN

    def check_in_reserved(
        self, reservation_id, customer_id, current_time=datetime.now()
    ):
        validate_id(reservation_id, ["RESV"])
        validate_id(customer_id, ["MEMBER", "WALK"])

        if not isinstance(current_time, datetime):
            raise ValueError("current_time must be a datetime object")

        reservation = self.find_reservation_by_id(reservation_id)
        if reservation is None:
            raise ValueError("Reservation not found")

        customer = self.find_person_by_id(customer_id)
        if customer is None:
            raise ValueError("Customer not found")

        now = current_time if current_time else datetime.now()
        if now < reservation.reservation_time:
            raise ValueError("Too early to check-in")

        late_limit = reservation.reservation_time + timedelta(minutes=15)
        if now > late_limit:
            reservation.status = ReservationStatus.NO_SHOW
            raise ValueError(
                "Check-in failed: You are more than 15 minutes late. Marked as No-Show."
            )

        if reservation.status != ReservationStatus.PENDING:
            raise ValueError(
                "Can't check in reservation that already completed")

        branch = self.find_cafe_branch_by_id(reservation.branch_id)
        if branch is None:
            raise ValueError("Branch not found")

        table = branch.find_table_by_id(reservation.table_id)
        if table is None:
            raise ValueError("Table not found")

        if customer.user_id != reservation.customer_id:
            raise ValueError("Wrong personal ID")

        try:
            reservation.status = ReservationStatus.COMPLETED
            table.status = TableStatus.OCCUPIED
            session = PlaySession(reservation.table_id, now)
            branch.add_play_session(session)
            session.add_players_id(reservation.customer_id)
            
            # Fill the remaining player slots with anonymous walk-in IDs
            for _ in range(reservation.players - 1):
                session.add_players_id(self.create_customer_walk_in().user_id)
                
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
        validate_id(branch_id, ["BRCH"])

        if not isinstance(customer_id, str):
            raise ValueError("Invalid ID : Customer ID must be a string")
        if customer_id != "walk_in":
            validate_id(customer_id, ["MEMBER"])

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
            if table.status != TableStatus.AVAILABLE:
                raise ValueError("Table is not available")
            if table.capacity < player_amount:
                raise ValueError("Table capacity not enough")

        try:
            table.status = TableStatus.OCCUPIED
            actual_start = start_time if start_time is not None else datetime.now()
            session = PlaySession(table.table_id, actual_start)

            if customer_id == "walk_in":
                customer_id = self.create_customer_walk_in().user_id
            session.add_players_id(customer_id)
            
            # Fill the remaining player slots with anonymous walk-in IDs
            for _ in range(player_amount - 1):
                session.add_players_id(self.create_customer_walk_in().user_id)

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

        cafe_branch = self.find_cafe_branch_by_id(any_id)
        if cafe_branch is None:
            raise ValueError("Cafe Branch not found")

        play_session = cafe_branch.find_play_session_by_id(any_id)
        if play_session is None:
            raise ValueError("Play Session not found")

        try:
            # Check table capacity before joining
            table = cafe_branch.find_table_by_id(play_session.table_id)
            if table is None:
                raise ValueError("Table for this session not found")
                
            if play_session.get_total_players() >= table.capacity:
                raise ValueError(f"Table capacity is full ({table.capacity}/{table.capacity})")

            if customer_id == "walk_in":
                play_session.add_players_id(
                    self.create_customer_walk_in().user_id)
            else:
                play_session.add_players_id(customer_id)
            return True
        except (TypeError, ValueError) as e:
            raise ValueError(f"Failed to join session: {e}")

    # / ════════════════════════════════════════════════════════════════
    # \ GAME SESSION - BORROW BOARD GAME

    def borrow_board_game(self, any_id, board_game_id):
        validate_id(any_id, ["TABLE", "PS"])
        validate_id(board_game_id, ["BG"])

        cafe_branch = self.find_cafe_branch_by_id(any_id)
        if cafe_branch is None:
            raise ValueError("Cafe Branch not found")

        play_session = cafe_branch.find_play_session_by_id(any_id)
        if play_session is None:
            raise ValueError("Play Session not found")

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

    def return_board_game(self, any_id, board_game_id):
        validate_id(any_id, ["TABLE", "PS"])
        validate_id(board_game_id, ["BG"])

        cafe_branch = self.find_cafe_branch_by_id(any_id)
        if cafe_branch is None:
            raise ValueError("Cafe Branch not found")

        play_session = cafe_branch.find_play_session_by_id(any_id)
        if play_session is None:
            raise ValueError("Play Session not found")

        board_game = cafe_branch.find_board_game_by_id(board_game_id)
        if board_game is None:
            raise ValueError("Board Game not found")

        try:
            if self.check_board_game_damage():
                board_game.status = BoardGameStatus.MAINTENANCE
                play_session.add_game_penalty(board_game_id)
            else:
                board_game.status = BoardGameStatus.AVAILABLE
            play_session.remove_board_games_id(board_game_id)
            return board_game
        except (TypeError, ValueError) as e:
            raise ValueError(f"Failed to return board game: {e}")

    # 10% chance of damage : simulate chance of damage in real life situation
    def check_board_game_damage(self):
        return random.random() < 0.1

    def maintenance_board_game(self, board_game_id):
        validate_id(board_game_id, ["BG"])

        cafe_branch = self.find_cafe_branch_by_id(board_game_id)
        if cafe_branch is None:
            raise ValueError("Cafe Branch not found")

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

    def take_order(self, any_id, menu_item_id):
        validate_id(any_id, ["TABLE", "PS"])
        validate_id(menu_item_id, ["FOOD", "DRINK"])

        cafe_branch = self.find_cafe_branch_by_id(any_id)
        if cafe_branch is None:
            raise ValueError("Play Session already closed or Cafe Branch not found")

        play_session = cafe_branch.find_play_session_by_id(any_id)
        if play_session is None:
            raise ValueError("Play Session not found")

        menu_item = cafe_branch.find_menu_item_by_id(menu_item_id)
        if menu_item is None:
            raise ValueError("Menu Item not found")

        try:
            return play_session.take_order(menu_item)
        except (TypeError, ValueError) as e:
            raise ValueError(f"Failed to take order: {e}")

    def get_pending_orders(self, branch_id):
        validate_id(branch_id, ["BRCH"])

        cafe_branch = self.find_cafe_branch_by_id(branch_id)
        if cafe_branch is None:
            raise ValueError("Cafe Branch not found")
        return cafe_branch.get_pending_orders()

    def update_order(self, play_session_id, order_id, session_status):
        validate_id(play_session_id, ["PS"])
        validate_id(order_id, ["ORDER"])

        cafe_branch = self.find_cafe_branch_by_id(play_session_id)
        if cafe_branch is None:
            raise ValueError("Cafe Branch not found")

        play_session = cafe_branch.find_play_session_by_id(play_session_id)
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
        validate_id(play_session_id, ["PS"])
        validate_id(order_id, ["ORDER"])

        cafe_branch = self.find_cafe_branch_by_id(play_session_id)
        if cafe_branch is None:
            raise ValueError("Cafe Branch not found")

        play_session = cafe_branch.find_play_session_by_id(play_session_id)
        if play_session is None:
            raise ValueError("Play Session not found")

        for order in play_session.current_order:
            if order.order_id == order_id:
                if order.status == OrderStatus.SERVED:
                    raise ValueError("Cannot cancel an order that has already been served")
                self.update_order(play_session_id, order_id, OrderStatus.CANCELLED)
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

        if end_time is None:
            end_time = datetime.now()

        cafe_branch = self.find_cafe_branch_by_id(any_id)
        if cafe_branch is None:
            raise ValueError("Cafe Branch not found")

        play_session = cafe_branch.find_play_session_by_id(any_id)
        if play_session is None:
            raise ValueError("Play Session not found")

        if play_session.payment is not None:
            raise ValueError("This session already checked out")

        total = 0
        try:
            for board_game_id in play_session.current_board_games_id:
                board_game = cafe_branch.find_board_game_by_id(board_game_id)
                if board_game:
                    board_game.status = BoardGameStatus.AVAILABLE

            for order in play_session.current_order:
                if order.status == OrderStatus.SERVED:
                    total += order.menu_items.price

            self.update_table_status(
                play_session.table_id, TableStatus.AVAILABLE)

            actual_end_time = end_time if end_time is not None else datetime.now()
            cafe_branch.end_play_session(
                play_session.session_id, actual_end_time)

            discount = 0
            for player_id in play_session.current_players_id:
                try:
                    player = self.find_person_by_id(player_id)
                    if isinstance(player, Member):
                        discount = max(discount, player.get_discount())
                except ValueError:
                    continue  # ข้าม player ที่หาไม่เจอ

            total += (
                Table.price_per_hour
                * play_session.duration()
                * play_session.get_total_players()
            )

            penalty_fee = 0
            for game_id in play_session.game_penalty:
                try:
                    _board_game = cafe_branch.find_board_game_by_id(game_id)
                    if _board_game:
                        penalty_fee += _board_game.price
                except ValueError:
                    continue  # ข้ามเกมที่หาไม่เจอ

            total = (total * (1 - discount)) + penalty_fee

        except (TypeError, ValueError) as e:
            raise ValueError(f"Error calculating checkout total: {e}")

        # !!! เพิ่มเงินไปที่ Member total spend ด้วยนับเเบบชม. x เวลา ( เเบบง่าย ไม่นับส่วนลด )

        payment = self.create_payment(total, method_type, **kwargs)
        play_session.payment = payment

        return payment, total

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
                new_payment.process_payment = True
                return new_payment
        except Exception as e:
            raise ValueError(f"Payment validation failed: {e}")


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
        self.__menu_list = None
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
        return [
            board_game
            for board_game in self.__board_games
            if board_game.min_players >= min_players
        ]

    def search_board_game_by_max_players(self, max_players):
        return [
            board_game
            for board_game in self.__board_games
            if board_game.max_players <= max_players
        ]

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

    def get_pending_orders(self):
        pending_orders = []
        for play_session in self.__play_sessions:
            for order in play_session.current_order:
                if order.status == OrderStatus.PENDING:
                    pending_orders.append(order)
        return pending_orders

    # / ════════════════════════════════════════════════════════════════
    # \ PLAY SESSION

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
            end_time = datetime.now()

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
