from datetime import *
import time

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
    # - Setters
    # / ════════════════════════════════════════════════════════════════

    # / ════════════════════════════════════════════════════════════════
    # - Methods
    # / ════════════════════════════════════════════════════════════════
    # \ PERSON METHOD

    def add_person(self, person):
        if isinstance(person, Person):
            self.__person.append(person)
        else:
            raise TypeError("Type Error : must be an instance of Person")

    def create_owner(self, name):
        new_owner = Owner(name)
        self.add_person(new_owner)
        return new_owner

    def create_manager(self, name):
        new_manager = Manager(name)
        self.add_person(new_manager)
        return new_manager

    def create_staff(self, name):
        new_staff = Staff(name)
        self.add_person(new_staff)
        return new_staff

    def create_customer_member(self, name):
        new_customer = Member(name)
        self.add_person(new_customer)
        return new_customer

    def create_customer_walk_in(self):
        new_walk_in = WalkInCustomer()
        self.add_person(new_walk_in)
        return new_walk_in

    def add_owner_to_branch(self, branch_id, owner_id):
        validate_id(branch_id, ["BRCH"])
        validate_id(owner_id, ["OWNER"])

        cafe_branch = self.find_cafe_branch_by_id(branch_id)
        if cafe_branch:
            owner = self.find_person_by_id(owner_id)
            if owner:
                cafe_branch.add_owner(owner)
            else:
                raise ValueError("Owner not found")
        else:
            raise ValueError("Cafe Branch not found")

    def add_manager_to_branch(self, branch_id, manager_id):
        validate_id(branch_id, ["BRCH"])
        validate_id(manager_id, ["MANAGER"])

        cafe_branch = self.find_cafe_branch_by_id(branch_id)
        if cafe_branch:
            manager = self.find_person_by_id(manager_id)
            if manager:
                cafe_branch.add_manager(manager)
            else:
                raise ValueError("Manager not found")
        else:
            raise ValueError("Cafe Branch not found")

    def add_staff_to_branch(self, branch_id, staff_id):
        validate_id(branch_id, ["BRCH"])
        validate_id(staff_id, ["STAFF"])

        cafe_branch = self.find_cafe_branch_by_id(branch_id)
        if cafe_branch:
            staff = self.find_person_by_id(staff_id)
            if staff:
                cafe_branch.add_staff(staff)
            else:
                raise ValueError("Staff not found")
        else:
            raise ValueError("Cafe Branch not found")

    def get_person(self):
        return self.__person.copy()

    def get_person_by_type(self, person_type):
        return [person for person in self.__person if isinstance(person, person_type)]

    def find_person_by_id(self, user_id):
        validate_id(user_id, ["OWNER", "MANAGER", "STAFF", "MEMBER", "WALK"])

        for person in self.__person:
            if person.user_id == user_id:
                return person
        return None

    def remove_person_by_id(self, user_id):
        person = self.find_person_by_id(user_id)
        if person:
            self.__person.remove(person)
        else:
            raise ValueError("Invalid ID : Person not found")

    def update_person_by_id(self, user_id, name):
        person = self.find_person_by_id(user_id)
        if person:
            person.name = name
        else:
            raise ValueError("Invalid ID : Person not found")

    # / ════════════════════════════════════════════════════════════════
    # \ CAFE BRANCH

    def create_cafe_branch(self, cafe_branch_name, cafe_branch_location=""):
        new_cafe_branch = CafeBranch(cafe_branch_name, cafe_branch_location)
        self.__cafe_branches.append(new_cafe_branch)
        return new_cafe_branch

    def get_cafe_branches(self):
        return self.cafe_branches

    def find_cafe_branch_by_id(self, _id):
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

    def remove_cafe_branch_by_id(self, cafe_branch_id):
        validate_id(cafe_branch_id, ["BRCH"])

        cafe_branch = self.find_cafe_branch_by_id(cafe_branch_id)
        if cafe_branch:
            self.__cafe_branches.remove(cafe_branch)
        else:
            raise ValueError("Invalid ID : Cafe Branch not found")

    def update_cafe_branch_by_id(self, branch_id, name, location):
        validate_id(branch_id, ["BRCH"])

        cafe_branch = self.find_cafe_branch_by_id(branch_id)
        if cafe_branch:
            cafe_branch.name = name
            cafe_branch.location = location
        else:
            raise ValueError("Invalid ID : Cafe Branch not found")

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

        customer = self.find_person_by_id(customer_id)
        if customer is None:
            raise ValueError("Customer not found.")

        # ดึงระดับสมาชิกแบบเต็มบล็อก (หลีกเลี่ยงการเขียนแบบย่อ)
        if hasattr(customer, "member_tier"):
            tier = customer.member_tier
        else:
            tier = MemberTier.NONE_TIER

        # 🟢 ด่านที่ 1: ตรวจสอบกฎธุรกิจทั้งหมด
        self.__validate_active_quota(customer_id, tier)
        self.__validate_advance_booking(date, tier)
        self.__validate_duration(start_time, end_time, tier)
        self.__validate_minimum_lead_time(date, start_time)

        branch = self.find_cafe_branch_by_id(branch_id)
        if branch is None:
            raise ValueError("Cafe branch not found.")

        # 🟢 ด่านที่ 2: ค้นหาและตรวจสอบโต๊ะ
        target_table = None

        if table_id == "auto":
            available_tables = []

            for table in branch.tables:
                if table.capacity >= total_player:
                    if (
                        self.__is_table_free(table.table_id, date, start_time, end_time)
                        == True
                    ):
                        available_tables.append(table)

            # เช็คว่ามีโต๊ะว่างหรือไม่
            if not available_tables:
                raise ValueError(
                    "No available tables for the requested capacity and time."
                )

            # ค้นหาโต๊ะที่มีความจุน้อยที่สุด (พอดีกับจำนวนคน ) ด้วย Loop ธรรมดาแทนการใช้ lambda
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
                raise ValueError("The specified table does not have enough capacity.")
            if (
                self.__is_table_free(target_table.table_id, date, start_time, end_time)
                == False
            ):
                raise ValueError(
                    "The specified table is already booked for this time slot."
                )

        # 🟢 ด่านที่ 3: สร้างการจอง
        new_resv = Reservation(
            customer_id, branch_id, target_table.table_id, date, start_time, end_time
        )

        new_resv.status = ReservationStatus.PENDING
        self.add_reservation(new_resv)

        return new_resv

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
        if reservation:
            self.__reservations.remove(reservation)
        else:
            raise ValueError("Reservation not found")

    def cancel_reservation(self, reservation_id, current_time=None):
        validate_id(reservation_id, ["RESV"])

        reservation = self.find_reservation_by_id(reservation_id)

        # 1. เช็คว่ามีใบจองนี้ในระบบหรือไม่
        if reservation is None:
            raise ValueError("Reservation not found.")

        # 2. เช็คว่าใบจองนี้ถูกยกเลิกไปแล้วหรือยัง (ป้องกันการยกเลิกซ้ำ)
        if reservation.status == ReservationStatus.CANCELLED:
            raise ValueError("Cannot cancel. Reservation is already cancelled.")

        # 3. เช็คสถานะ: ต้องเป็น PENDING เท่านั้นถึงจะยกเลิกได้ (ถ้า COMPLETED ไปแล้วห้ามยกเลิก)
        if reservation.status != ReservationStatus.PENDING:
            raise ValueError("Cannot cancel. Reservation is not in PENDING status.")

        # 4. จัดการเวลา (รองรับการจำลองเวลาตอน Test)
        if current_time is not None:
            now = current_time
        else:
            now = datetime.now()

        # นำวันที่และเวลาจองมาประกอบร่างกันเพื่อใช้เปรียบเทียบ
        resv_datetime = datetime.strptime(f"{reservation.date} {reservation.start_time}", "%Y-%m-%d %H:%M")

        # 5. เช็คเวลา: ห้ามยกเลิกหากเวลาปัจจุบัน "เลย" เวลาจองไปแล้ว
        if now > resv_datetime:
            raise ValueError("Cannot cancel. The reservation time has already passed.")

        # / ════════════════════════════════════════════════════════════════
        # หากผ่านด่านเงื่อนไขทั้งหมดด้านบนมาได้ ให้ดำเนินการยกเลิก
        # / ════════════════════════════════════════════════════════════════
        
        # เปลี่ยนสถานะใบจองเป็น CANCELLED
        reservation.status = ReservationStatus.CANCELLED

        # ค้นหาสาขาและโต๊ะเพื่อคืนสถานะโต๊ะให้ว่าง
        branch = self.find_cafe_branch_by_id(reservation.branch_id)
        if branch is None:
            pass
        else:
            table = branch.find_table_by_id(reservation.table_id)
            if table is None:
                pass
            else:
                # เคลียร์สถานะโต๊ะให้ว่าง (AVAILABLE) หากโต๊ะนั้นถูกล็อกสถานะ RESERVED ไว้ล่วงหน้าแล้ว
                if table.status == TableStatus.RESERVED:
                    table.status = TableStatus.AVAILABLE

    def update_reservation_status_by_id(self, reservation_id, status):
        validate_id(reservation_id, ["RESV"])

        if not isinstance(status, ReservationStatus):
            raise TypeError("Status must be ReservationStatus")

        reservation = self.find_reservation_by_id(reservation_id)
        if reservation:
            reservation.status = status
        else:
            raise ValueError("Invalid ID : Reservation not found")

    def set_reservation_cancel_by_id(self, reservation_id):
        self.update_reservation_status_by_id(
            reservation_id,
            ReservationStatus.CANCELLED,
        )

    def set_reservation_no_show_by_id(self, reservation_id):
        self.update_reservation_status_by_id(
            reservation_id,
            ReservationStatus.NO_SHOW,
        )

    def set_reservation_complete_by_id(self, reservation_id):
        self.update_reservation_status_by_id(
            reservation_id,
            ReservationStatus.COMPLETED,
        )

    # / ════════════════════════════════════════════════════════════════
    # \ PRIVATE HELPER METHODS (BUSINESS RULES VALIDATION)
    # / ════════════════════════════════════════════════════════════════

    def __is_table_free(self, table_id, date_str, start_time, end_time):
        new_start = datetime.strptime(start_time, "%H:%M")
        new_end = datetime.strptime(end_time, "%H:%M")

        for reservation in self.__reservations:
            if reservation.date == date_str and reservation.table_id == table_id:
                if reservation.status == ReservationStatus.PENDING:
                    exist_start = datetime.strptime(reservation.start_time, "%H:%M")
                    exist_end = datetime.strptime(reservation.end_time, "%H:%M")

                    # เช็คเวลาทับซ้อน
                    if new_start < exist_end and new_end > exist_start:
                        return False

        return True

    def __validate_active_quota(self, customer_id, tier):
        active_count = 0

        # นับจำนวนคิวที่ยังค้างอยู่
        for reservation in self.__reservations:
            if reservation.customer_id == customer_id:
                if reservation.status == ReservationStatus.PENDING:
                    active_count = active_count + 1

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

        # ตรวจสอบโควตา
        if active_count >= max_quota:
            raise ValueError(
                f"Active booking quota exceeded. Maximum allowed for your tier is {max_quota}."
            )

    def __validate_advance_booking(self, date_str, tier):
        resv_date = datetime.strptime(date_str, "%Y-%m-%d").date()
        today = datetime.now().date()

        # คำนวณวันล่วงหน้า
        days_advance = (resv_date - today).days

        if days_advance < 0:
            raise ValueError("Cannot make a reservation in the past.")

        # กำหนดวันล่วงหน้าตามระดับสมาชิก
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
        start_dt = datetime.strptime(start_time, "%H:%M")
        end_dt = datetime.strptime(end_time, "%H:%M")

        # คำนวณระยะเวลา (ชั่วโมง)
        duration_hrs = (end_dt - start_dt).total_seconds() / 3600

        # กรณีข้ามคืน (เช่น 23:00 ถึง 02:00)
        if duration_hrs <= 0:
            duration_hrs = duration_hrs + 24

        if duration_hrs <= 0 or duration_hrs > 24:
            raise ValueError("End time must be after start time or within 24 hours.")

        # กำหนดชั่วโมงสูงสุดตามระดับสมาชิก
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
            if tier == MemberTier.PLATINUM:
                limit_str = "Unlimited"
            else:
                limit_str = f"{max_dur_hrs} hours"

            raise ValueError(
                f"Maximum duration exceeded. Your tier allows up to {limit_str} per session."
            )

    def __validate_minimum_lead_time(self, date_str, start_time):
        resv_datetime = datetime.strptime(f"{date_str} {start_time}", "%Y-%m-%d %H:%M")

        # คำนวณเวลาที่เหลือก่อนถึงคิว (ลบด้วยเวลาปัจจุบัน)
        lead_time = resv_datetime - datetime.now()

        # กำหนดเวลา 1 ชั่วโมง ให้เป็นตัวแปรแบบตรงไปตรงมา
        one_hour = timedelta(hours=1)

        if lead_time < one_hour:
            raise ValueError(
                "Minimum lead time not met. Tables require at least 1 hour(s) advance booking."
            )

    # / ════════════════════════════════════════════════════════════════
    # \ TABLE

    def create_table_to_branch(self, branch_id, capacity):
        validate_id(branch_id, ["BRCH"])

        cafe_branch = self.find_cafe_branch_by_id(branch_id)
        if cafe_branch:
            return cafe_branch.add_table(capacity)
        else:
            raise ValueError("Cafe Branch not found")

    def get_branch_tables(self, branch_id):
        validate_id(branch_id, ["BRCH"])

        cafe_branch = self.find_cafe_branch_by_id(branch_id)
        if cafe_branch:
            return cafe_branch.tables
        else:
            raise ValueError("Cafe Branch not found")

    def update_reserved_tables(self):
        now = datetime.now()

        for reservation in self.__reservations:
            reservation_time = reservation.reservation_time
            time_diff = reservation_time - now

            if timedelta(hours=0) <= time_diff <= timedelta(hours=1):
                self.update_table_status(
                    reservation.table_id,
                    TableStatus.RESERVED,
                )
            elif time_diff < timedelta(hours=0):
                self.update_table_status(
                    reservation.table_id,
                    TableStatus.AVAILABLE,
                )

    def search_available_table(self, branch_id, required_capacity=0):
        validate_id(branch_id, ["BRCH"])

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
        self,
        branch_id,
        name,
        genre,
        price,
        min_players,
        max_players,
        description="",
    ):
        validate_id(branch_id, ["BRCH"])

        cafe_branch = self.find_cafe_branch_by_id(branch_id)
        if cafe_branch:
            return cafe_branch.add_board_game(
                name, genre, price, min_players, max_players, description
            )
        else:
            raise ValueError("Cafe Branch not found")

    def get_branch_board_games(self, branch_id):
        validate_id(branch_id, ["BRCH"])

        cafe_branch = self.find_cafe_branch_by_id(branch_id)
        if cafe_branch:
            return cafe_branch.board_games
        else:
            raise ValueError("Cafe Branch not found")

    def find_board_game_by_id(self, board_game_id):
        validate_id(board_game_id, ["BG"])

        cafe_branch = self.find_cafe_branch_by_id(board_game_id)
        if cafe_branch:
            board_game = cafe_branch.find_board_game_by_id(board_game_id)
            if board_game:
                return board_game
        raise ValueError("Board Game not found")

    def search_board_game_by_min_players(self, branch_id, min_players):
        validate_id(branch_id, ["BRCH"])

        cafe_branch = self.find_cafe_branch_by_id(branch_id)
        if cafe_branch:
            return cafe_branch.search_board_game_by_min_players(min_players)
        else:
            raise ValueError("Cafe Branch not found")

    def update_board_game_status(self, board_game_id, status):
        validate_id(board_game_id, ["BG"])

        if not isinstance(status, BoardGameStatus):
            raise TypeError("Status must be BoardGameStatus")

        board_game = self.find_board_game_by_id(board_game_id)
        if board_game:
            board_game.status = status
        else:
            raise ValueError("Board Game not found")

    def remove_board_game_by_id(self, board_game_id):
        validate_id(board_game_id, ["BG"])

        board_game = self.find_board_game_by_id(board_game_id)
        if board_game:
            cafe_branch = self.find_cafe_branch_by_id(board_game_id)
            cafe_branch.remove_board_game_by_id(board_game_id)
        else:
            raise ValueError("Board Game not found")

    # / ════════════════════════════════════════════════════════════════
    # \ MENU

    def create_menu_to_branch(self, branch_id):
        validate_id(branch_id, ["BRCH"])

        cafe_branch = self.find_cafe_branch_by_id(branch_id)
        if cafe_branch:
            new_menu = MenuList()
            cafe_branch.create_menu(new_menu)
            return new_menu
        else:
            raise ValueError("Cafe Branch not found")

    def create_menu_item_food_to_branch(self, branch_id, name, price, description=""):
        validate_id(branch_id, ["BRCH"])

        cafe_branch = self.find_cafe_branch_by_id(branch_id)
        if cafe_branch:
            return cafe_branch.create_menu_item_food(name, price, description)

    def create_menu_item_drink_to_branch(
        self, branch_id, name, price, cup_size="S", description=""
    ):
        validate_id(branch_id, ["BRCH"])

        cafe_branch = self.find_cafe_branch_by_id(branch_id)
        if cafe_branch:
            return cafe_branch.create_menu_item_drink(
                name, price, cup_size, description
            )

    def get_branch_menu(self, branch_id):
        validate_id(branch_id, ["BRCH"])

        cafe_branch = self.find_cafe_branch_by_id(branch_id)
        if cafe_branch:
            return cafe_branch.get_menu()
        else:
            raise ValueError("Cafe Branch not found")

    def get_branch_menu_item(self, branch_id):
        validate_id(branch_id, ["BRCH"])

        cafe_branch = self.find_cafe_branch_by_id(branch_id)
        if cafe_branch:
            return cafe_branch.get_menu_item()
        else:
            raise ValueError("Cafe Branch not found")

    def get_branch_menu_item_food(self, branch_id):
        validate_id(branch_id, ["BRCH"])

        cafe_branch = self.find_cafe_branch_by_id(branch_id)
        if cafe_branch:
            return cafe_branch.get_menu_item_food()
        else:
            raise ValueError("Cafe Branch not found")

    def get_branch_menu_item_drink(self, branch_id):
        validate_id(branch_id, ["BRCH"])

        cafe_branch = self.find_cafe_branch_by_id(branch_id)
        if cafe_branch:
            return cafe_branch.get_menu_item_drink()
        else:
            raise ValueError("Cafe Branch not found")

    def find_menu_item_by_id(self, menu_item_id):
        validate_id(menu_item_id, ["FOOD", "DRINK"])

        cafe_branch = self.find_cafe_branch_by_id(menu_item_id)
        if cafe_branch:
            return cafe_branch.find_menu_item_by_id(menu_item_id)
        else:
            raise ValueError("Menu Item not found")

    def remove_menu_item_by_id(self, menu_item_id):
        validate_id(menu_item_id, ["FOOD", "DRINK"])

        cafe_branch = self.find_cafe_branch_by_id(menu_item_id)
        if cafe_branch:
            cafe_branch.remove_menu_item_by_id(menu_item_id)
        else:
            raise ValueError("Menu Item not found")

    def update_menu_item_by_id(self, menu_item_id, name, price, description=""):
        validate_id(menu_item_id, ["FOOD", "DRINK"])

        cafe_branch = self.find_cafe_branch_by_id(menu_item_id)
        if cafe_branch:
            cafe_branch.update_menu_item_by_id(menu_item_id, name, price, description)
        else:
            raise ValueError("Menu Item not found")

    # / ════════════════════════════════════════════════════════════════
    # \ GAME SESSION - CHECK-IN

    def check_in_reserved(
        self, reservation_id, customer_id, current_time=datetime.now()
    ):
        validate_id(reservation_id, ["RESV"])
        validate_id(customer_id, ["MEMBER", "WALK"])

        reservation = self.find_reservation_by_id(reservation_id)
        if reservation is None:
            raise ValueError("Reservation not found")
        customer = self.find_person_by_id(customer_id)
        if customer is None:
            raise ValueError("Customer not found")
        if current_time: #เอาไว้ test
            now = current_time
        else:
            now = datetime.now()

        if now < reservation.reservation_time:
            raise ValueError("Too early to check-in")
        late_limit = reservation.reservation_time + timedelta(minutes=15)
        if current_time > late_limit:
            reservation.status = ReservationStatus.NO_SHOW
            raise ValueError(
                "Check-in failed: You are more than 15 minutes late. Marked as No-Show."
            )
        if reservation.status != ReservationStatus.PENDING:
            raise ValueError("Can't check in reservation that already completed")
        branch = self.find_cafe_branch_by_id(reservation.branch_id)
        if branch is None:
            raise ValueError("Branch not found")

        table = branch.find_table_by_id(reservation.table_id)
        if table is None:
            raise ValueError("Table not found")

        if customer.user_id != reservation.customer_id:
            raise ValueError("Wrong personal ID")
        else:
            reservation.status = ReservationStatus.COMPLETED
            table.status = TableStatus.OCCUPIED

            session = PlaySession(reservation.table_id, now)
            branch.add_play_session(session)
            session.add_players_id(reservation.customer_id)
            return session

    def check_in_walk_in(self, branch_id, player_amount, table_id="auto", start_time=None):
        validate_id(branch_id, ["BRCH"])
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

        table.status = TableStatus.OCCUPIED

        actual_start = start_time if start_time is not None else datetime.now() #เอาไว้ test
        session = PlaySession(table.table_id, actual_start)
        session.add_players_id(self.create_customer_walk_in().user_id)
        branch.add_play_session(session)

        return session

    def check_in_member(self, branch_id, player_amount, member_id, table_id="auto", start_time=None):
        validate_id(branch_id, ["BRCH"])
        validate_id(member_id, ["MEMBER"])

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

        table.status = TableStatus.OCCUPIED

        actual_start = start_time if start_time is not None else datetime.now() #เอาไว้ test
        session = PlaySession(table.table_id, actual_start)
        session.add_players_id(member_id)
        branch.add_play_session(session)
        return session

    # / ════════════════════════════════════════════════════════════════
    # \ GAME SESSION - JOIN

    def join_session(self, any_id, customer_id="walk_in"):
        validate_id(any_id, ["TABLE", "PS"])
        if customer_id != "walk_in":
            validate_id(customer_id, ["MEMBER", "WALK"])

        cafe_branch = self.find_cafe_branch_by_id(any_id)
        play_session = cafe_branch.find_play_session_by_id(any_id)

        if cafe_branch is None:
            raise ValueError("Cafe Branch not found")

        if play_session:
            if customer_id == "walk_in":
                play_session.add_players_id(self.create_customer_walk_in().user_id)
            else:
                play_session.add_players_id(customer_id)
        else:
            raise ValueError("Play Session not found")

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
            return None

        board_game = cafe_branch.find_board_game_by_id(board_game_id)
        if board_game is None:
            raise ValueError("Board Game not found")

        if board_game.status != BoardGameStatus.AVAILABLE:
            return None

        play_session.add_board_games_id(board_game_id)
        board_game.status = BoardGameStatus.IN_USE
        return board_game

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

        board_game.status = BoardGameStatus.AVAILABLE
        play_session.remove_board_games_id(board_game_id)

        return board_game

    def maintenance_board_game(self, board_game_id):
        validate_id(board_game_id, ["BG"])

        cafe_branch = self.find_cafe_branch_by_id(board_game_id)
        if cafe_branch is None:
            raise ValueError("Cafe Branch not found")

        board_game = cafe_branch.find_board_game_by_id(board_game_id)
        if board_game is None:
            raise ValueError("Board Game not found")

        board_game.status = BoardGameStatus.MAINTENANCE
        for session in cafe_branch.get_play_sessions():
            if board_game_id in session.current_board_games_id:
                raise ValueError("Board Game in use")

        return board_game
    # / ════════════════════════════════════════════════════════════════
    # \ GAME SESSION - ORDER

    def take_order(self, any_id, menu_item_id):
        validate_id(any_id, ["TABLE", "PS"])
        validate_id(menu_item_id, ["FOOD", "DRINK"])

        cafe_branch = self.find_cafe_branch_by_id(any_id)
        if cafe_branch is None:
            raise ValueError("Cafe Branch not found")

        play_session = cafe_branch.find_play_session_by_id(any_id)
        if play_session:
            menu_item = cafe_branch.find_menu_item_by_id(menu_item_id)
            if menu_item:
                play_session.take_order(menu_item)
            else:
                raise ValueError("Menu Item not found")
        else:
            raise ValueError("Play Session not found")

    def get_pending_orders(self, branch_id):
        validate_id(branch_id, ["BRCH"])

        cafe_branch = self.find_cafe_branch_by_id(branch_id)
        if cafe_branch:
            return cafe_branch.get_pending_orders()
        else:
            raise ValueError("Cafe Branch not found")

    def update_order(self, play_session_id, order_id, session_status):
        validate_id(play_session_id, ["PS"])
        validate_id(order_id, ["ORDER"])

        cafe_branch = self.find_cafe_branch_by_id(play_session_id)
        if cafe_branch is None:
            raise ValueError("Cafe Branch not found")

        play_session = cafe_branch.find_play_session_by_id(play_session_id)
        if play_session:
            for order in play_session.current_order:
                if order.order_id == order_id:
                    order.set_order_status(session_status)
                    return
            raise ValueError("Order not found")
        else:
            raise ValueError("Play Session not found")

    def update_order_preparing(self, play_session_id, order_id):
        self.update_order(play_session_id, order_id, OrderStatus.PREPARING)

    def update_order_serve(self, play_session_id, order_id):
        self.update_order(play_session_id, order_id, OrderStatus.SERVED)

    def update_order_cancel(self, play_session_id, order_id):
        self.update_order(play_session_id, order_id, OrderStatus.CANCELLED)

    # / ════════════════════════════════════════════════════════════════
    # \ GAME SESSION - CHECK-OUT

    def check_out(self, any_id, method_type="cash", end_time=None, **kwargs):

        validate_id(any_id, ["TABLE", "PS"])

        cafe_branch = self.find_cafe_branch_by_id(any_id)
        if cafe_branch is None:
            raise ValueError("Cafe Branch not found")

        play_session = cafe_branch.find_play_session_by_id(any_id)

        if play_session is None:
            raise ValueError("Play Session not found")

        if play_session.payment is not None:
            raise ValueError("This session already checked out")

        total = 0

        for board_game_id in play_session.current_board_games_id:
            board_game = cafe_branch.find_board_game_by_id(board_game_id)
            board_game.status = BoardGameStatus.AVAILABLE

        for order in play_session.current_order:
            if order.status == OrderStatus.SERVED:
                total += order.menu_items.price

        self.update_table_status(play_session.table_id, TableStatus.AVAILABLE)

        actual_end_time = end_time if end_time is not None else datetime.now()
        cafe_branch.end_play_session(play_session.session_id, actual_end_time)

        total += (
            Table.price_per_hour
            * play_session.duration()
            * play_session.get_total_players()
        )

        payment = self.create_payment(total, method_type, **kwargs)

        play_session.payment = payment

        return payment
    # / ════════════════════════════════════════════════════════════════
    # \ PAYMENT

    # kwargs คือรับ parameter หลังจากมันมาทำเป็น dict เช่น
    # create_payment(6969, online, account_email="SKIBIDI")
    # kwrag = [account:SKIBIDI]
    def create_payment(self, total, method_type="cash", **kwargs):

        if method_type == "cash":
            paid_amount = kwargs.get("paid_amount", total)  # ← default จ่ายเต็ม

            if paid_amount < total:
                raise ValueError("Paid amount is not enough")

            change = paid_amount - total
            payment_method = Cash(paid_amount)
            payment_method.change = change

        elif method_type == "card":
            payment_method = CreditCard(kwargs["card_number"], kwargs["expiry_date"], kwargs["cvv"])

        elif method_type == "online":
            payment_method = OnlinePayment(kwargs["email"])

        else:
            raise ValueError("Invalid payment method")

        if payment_method.validate_method():
            new_payment = Payment(total, payment_method)
            new_payment.process_payment = True
            return new_payment


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

    # / ════════════════════════════════════════════════════════════════

    @property
    def total_tables(self):
        return len(self.__tables)

    @property
    def total_board_games(self):
        return len(self.__board_games)

    @property
    def total_menu_items(self):
        return len(self.__menu_list.menu_items())

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
            if board_game.min_players <= min_players
        ]

    def remove_board_game_by_id(self, board_game_id):
        self.__board_games = [
            board_game
            for board_game in self.__board_games
            if board_game.board_game_id != board_game_id
        ]

    # / ════════════════════════════════════════════════════════════════
    # \ MENU

    def create_menu(self, menu):
        if isinstance(menu, MenuList):
            self.__menu_list = menu
        else:
            raise TypeError("Type Error : must be an instance of Menu")

    def create_menu_item_food(self, name, price, description=""):
        if self.__menu_list is not None:
            new_menu_item = Food(name, price, description)
            self.__menu_list.add_menu_item(new_menu_item)
            return new_menu_item
        else:
            raise ValueError("Menu not found")

    def create_menu_item_drink(self, name, price, cup_size="S", description=""):
        if self.__menu_list is not None:
            new_menu_item = Drink(name, price, description, cup_size=cup_size)
            self.__menu_list.add_menu_item(new_menu_item)
            return new_menu_item
        else:
            raise ValueError("Menu not found")

    def get_menu(self):
        if self.__menu_list is not None:
            return self.__menu_list
        else:
            raise ValueError("Menu not found")

    def get_menu_item(self):
        if self.__menu_list is not None:
            return self.__menu_list.menu_items
        else:
            raise ValueError("Menu not found")

    def get_menu_item_food(self):
        if self.__menu_list is not None:
            return self.__menu_list.get_menu_item_food()
        else:
            raise ValueError("Menu not found")

    def get_menu_item_drink(self):
        if self.__menu_list is not None:
            return self.__menu_list.get_menu_item_drink()
        else:
            raise ValueError("Menu not found")

    def find_menu_item_by_id(self, menu_item_id):
        if self.__menu_list is not None:
            return self.__menu_list.find_menu_item_by_id(menu_item_id)
        else:
            raise ValueError("Menu not found")

    def remove_menu_item_by_id(self, menu_item_id):
        if self.__menu_list is not None:
            self.__menu_list.remove_menu_item(menu_item_id)
        else:
            raise ValueError("Menu not found")

    def update_menu_item_by_id(self, menu_item_id, name, price, description=""):
        if self.__menu_list is not None:
            menu_item = self.__menu_list.find_menu_item_by_id(menu_item_id)
            if menu_item is not None:
                menu_item.name = name
                menu_item.price = price
                menu_item.description = description
            else:
                raise ValueError("Menu Item not found")
        else:
            raise ValueError("Menu not found")

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
        if isinstance(play_session, PlaySession):
            self.__play_sessions.append(play_session)
        else:
            raise TypeError("Type Error : must be an instance of PlaySession")

    def get_play_sessions(self):
        return self.__play_sessions.copy()

    def find_play_session_by_id(self, any_id):
        if any_id.startswith("PS-"):
            for play_session in self.__play_sessions:
                if play_session.session_id == any_id:
                    return play_session
        elif any_id.startswith("TABLE-"):
            for play_session in self.__play_sessions:
                if play_session.table_id == any_id:
                    return play_session
        else:
            raise ValueError("Invalid ID")
        return None

    def remove_play_session_by_id(self, play_session_id):
        play_session = self.find_play_session_by_id(play_session_id)
        if play_session:
            self.__play_sessions.remove(play_session)
        else:
            raise ValueError("Invalid ID : Play Session not found")

    def end_play_session(self, play_session_id, end_time=None):
        if end_time is None:
            end_time = datetime.now()
        play_session = self.find_play_session_by_id(play_session_id)
        if play_session:
            play_session.end_time = end_time
            self.__play_sessions_history.append(play_session)
            self.__play_sessions.remove(play_session)
        else:
            raise ValueError("Invalid ID : Play Session not found")

    # / ════════════════════════════════════════════════════════════════
    # \ STAFF

    def add_staff(self, staff):
        if isinstance(staff, Staff):
            self.__staff_id.append(staff.user_id)
        else:
            raise TypeError("Type Error : must be an instance of Staff")

    def get_staff(self):
        return self.__staff_id.copy()

    def remove_staff_by_id(self, staff_id):
        if staff_id in self.__staff_id:
            self.__staff_id.remove(staff_id)
        else:
            raise ValueError("Invalid ID : ID does not exist")

    # / ════════════════════════════════════════════════════════════════
    # \ MANAGER

    def add_manager(self, manager):
        if isinstance(manager, Manager):
            self.__manager_id = manager.user_id
        else:
            raise TypeError("Type Error : must be an instance of Manager")

    def get_manager(self):
        return self.__manager_id

    def remove_manager(self):
        self.__manager_id = None

    # / ════════════════════════════════════════════════════════════════
    # \ OWNER

    def add_owner(self, owner):
        if isinstance(owner, Owner):
            self.__owner_id = owner.user_id
        else:
            raise TypeError("Type Error : must be an instance of Owner")

    def get_owner(self):
        return self.__owner_id

    def remove_owner(self):
        self.__owner_id = None

    # / ════════════════════════════════════════════════════════════════


# | ════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════