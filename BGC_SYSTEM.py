from datetime import *
import time

from BGC_MENU import *
from BGC_PAYMENT import *
from BGC_PERSON import *
from BGC_PLAY_SESSION import *
from BGC_RESERVATION import *
from ENUM_STATUS import *

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

    def create_person(self, person):
        if isinstance(person, Person):
            self.__person.append(person)
        else:
            raise TypeError("Type Error : must be an instance of Person")

    def create_owner(self, name):
        new_owner = Owner(name)
        self.create_person(new_owner)
        return new_owner

    def create_manager(self, name):
        new_manager = Manager(name)
        self.create_person(new_manager)
        return new_manager

    def create_staff(self, name):
        new_staff = Staff(name)
        self.create_person(new_staff)
        return new_staff

    def create_customer_member(self, name):
        new_customer = Member(name)
        self.create_person(new_customer)
        return new_customer

    def create_customer_walk_in(self):
        new_walk_in = WalkInCustomer()
        self.create_person(new_walk_in)
        return new_walk_in

    def add_owner_to_branch(self, branch_id, owner_id):
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

    def get_owner(self):
        return self.get_person_by_type(Owner)

    def get_manager(self):
        return self.get_person_by_type(Manager)

    def get_staff(self):
        return self.get_person_by_type(Staff)

    def get_customer(self):
        return self.get_person_by_type(Customer)

    def get_customer_member(self):
        return self.get_person_by_type(Member)

    def get_customer_walk_in(self):
        return self.get_person_by_type(Walk_InCustomer)

    def find_person_by_id(self, user_id):
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

    def find_cafe_branch_by_id(self, branch_id):
        for cafe_branch in self.__cafe_branches:
            if cafe_branch.branch_id == branch_id:
                return cafe_branch
        return None

    def find_cafe_branch_by_table_id(self, table_id):
        for cafe_branch in self.__cafe_branches:
            if cafe_branch.find_table_by_id(table_id):
                return cafe_branch
        return None

    def find_cafe_branch_by_board_game_id(self, board_game_id):
        for cafe_branch in self.__cafe_branches:
            if cafe_branch.find_board_game_by_id(board_game_id):
                return cafe_branch
        return None

    def find_cafe_branch_by_menu_item_id(self, menu_item_id):
        for cafe_branch in self.__cafe_branches:
            if cafe_branch.find_menu_item_by_id(menu_item_id):
                return cafe_branch
        return None

    def find_cafe_branch_by_play_session_id(self, play_session_id):
        for cafe_branch in self.__cafe_branches:
            if cafe_branch.find_play_session_by_id(play_session_id):
                return cafe_branch
        return None

    def remove_cafe_branch_by_id(self, cafe_branch_id):
        cafe_branch = self.find_cafe_branch_by_id(cafe_branch_id)
        if cafe_branch:
            self.__cafe_branches.remove(cafe_branch)
        else:
            raise ValueError("Invalid ID : Cafe Branch not found")

    def update_cafe_branch_by_id(self, branch_id, name, location):
        cafe_branch = self.find_cafe_branch_by_id(branch_id)
        if cafe_branch:
            cafe_branch.name = name
            cafe_branch.location = location
        else:
            raise ValueError("Invalid ID : Cafe Branch not found")

    # / ════════════════════════════════════════════════════════════════
    # \ RESERVATION

    def make_reservation(self, customer_id, branch_id, pax, date, start_time, end_time, table_id="auto"):
        customer = self.find_person_by_id(customer_id)
        if not customer:
            raise ValueError("Customer not found.")

        tier = customer.member_tier if isinstance(customer, Member) else MemberTier.NONE_TIER

        self.__validate_active_quota(customer_id, tier)
        self.__validate_advance_booking(date, tier)
        self.__validate_duration(start_time, end_time, tier)

        branch = self.find_cafe_branch_by_id(branch_id)
        if not branch:
            raise ValueError("Cafe branch not found.")
            
        target_table = None

        if table_id == "auto":
            available_tables = []
            for table in branch.tables:
                if table.capacity >= pax and self.__is_table_free(table.table_id, date, start_time, end_time):
                    available_tables.append(table)
            
            if not available_tables:
                raise ValueError("No available tables for the requested capacity and time.")
            
            target_table = min(available_tables, key=lambda t: t.capacity)
            
        else:
            target_table = branch.find_table_by_id(table_id)
            if not target_table:
                raise ValueError("The specified table is not found.")
            if target_table.capacity < pax:
                raise ValueError("The specified table does not have enough capacity.")
            if not self.__is_table_free(target_table.table_id, date, start_time, end_time):
                raise ValueError("The specified table is already booked for this time slot.")

        self.__validate_minimum_lead_time(target_table, date, start_time)

        target_table.status = TableStatus.RESERVED
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
        for reservation in self.__reservations:
            if reservation.reservation_id == reservation_id:
                return reservation
        return None

    def remove_reservation_by_id(self, reservation_id):
        reservation = self.find_reservation_by_id(reservation_id)
        if reservation:
            self.__reservations.remove(reservation)
        else:
            raise ValueError("Reservation not found")

    def cancel_reservation(self, reservation_id):
        reservation = self.find_reservation_by_id(reservation_id)

        if reservation is None:
            raise ValueError("Reservation not found")

        reservation.status = ReservationStatus.CANCELLED

        branch = self.find_cafe_branch_by_id(reservation.branch_id)
        table = branch.find_table_by_id(reservation.table_id)

        if table.status == TableStatus.RESERVED:
            table.status = TableStatus.AVAILABLE

    def update_reservation_status_by_id(self, reservation_id, status):
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
    # \ PRIVATE HELPER METHODS (RESERVATION)

    def __is_table_free(self, table_id, date_str, start_time, end_time):
        new_start = datetime.strptime(start_time, "%H:%M")
        new_end = datetime.strptime(end_time, "%H:%M")
        
        for r in self.__reservations:
            status_str = str(getattr(r, 'status', ''))
            
            if r.date == date_str and r.table_id == table_id and "PENDING" in status_str:
                exist_start = datetime.strptime(r.start_time, "%H:%M")
                exist_end = datetime.strptime(r.end_time, "%H:%M")
                
                if new_start < exist_end and new_end > exist_start:
                    return False 
        return True

    def __validate_active_quota(self, customer_id, tier):
        active_resv = []
        for r in self.__reservations:
            status_str = str(getattr(r, 'status', ''))
            
            if r.customer_id == customer_id and "PENDING" in status_str:
                active_resv.append(r)
                
        max_quota = 1
        if tier == MemberTier.PLATINUM:
            max_quota = 3
        elif tier == MemberTier.GOLD:
            max_quota = 2
        
        if len(active_resv) >= max_quota:
            raise ValueError(f"Active booking quota exceeded. Maximum allowed for your tier is {max_quota}.")
        
    def __validate_advance_booking(self, date_str, tier):
        resv_date = datetime.strptime(date_str, "%Y-%m-%d").date()
        today = datetime.now().date()
        days_advance = (resv_date - today).days

        if days_advance < 0:
            raise ValueError("Cannot make a reservation in the past.")

        max_adv_days = 5
        if tier == MemberTier.PLATINUM:
            max_adv_days = 30
        elif tier == MemberTier.GOLD:
            max_adv_days = 21
        elif tier == MemberTier.SILVER:
            max_adv_days = 14
        elif tier == MemberTier.BRONZE:
            max_adv_days = 7

        if days_advance > max_adv_days:
            raise ValueError(f"Maximum advance booking exceeded. Your tier allows up to {max_adv_days} days.")

    def __validate_duration(self, start_time, end_time, tier):
        start_dt = datetime.strptime(start_time, "%H:%M")
        end_dt = datetime.strptime(end_time, "%H:%M")
        duration_hrs = (end_dt - start_dt).total_seconds() / 3600

        max_dur_hrs = 2
        if tier == MemberTier.PLATINUM:
            max_dur_hrs = 999
        elif tier == MemberTier.GOLD:
            max_dur_hrs = 7
        elif tier == MemberTier.SILVER:
            max_dur_hrs = 3.5

        if duration_hrs > max_dur_hrs:
            raise ValueError(f"Maximum duration exceeded. Your tier allows up to {max_dur_hrs} hours per session.")

    def __validate_minimum_lead_time(self, table, date_str, start_time):
        resv_datetime = datetime.strptime(f"{date_str} {start_time}", "%Y-%m-%d %H:%M")
        lead_time = resv_datetime - datetime.now()
        
        is_vip_table = type(table).__name__ == "PlayTableVIP"
        min_lead_hours = 3 if is_vip_table else 1

        if lead_time < timedelta(hours=min_lead_hours):
            table_type_str = "VIP" if is_vip_table else "Standard"
            raise ValueError(f"Minimum lead time not met. {table_type_str} tables require at least {min_lead_hours} hour(s) advance booking.")

    # / ════════════════════════════════════════════════════════════════
    # \ TABLE

    def create_table_to_branch(self, branch_id, capacity):
        cafe_branch = self.find_cafe_branch_by_id(branch_id)
        if cafe_branch:
            return cafe_branch.add_table(capacity)
        else:
            raise ValueError("Cafe Branch not found")

    def get_branch_tables(self, branch_id):
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
                    reservation.branch_id,
                    reservation.table_id,
                    TableStatus.RESERVED,
                )
            elif time_diff < datetime.timedelta(hours=0):
                self.update_table_status(
                    reservation.branch_id,
                    reservation.table_id,
                    TableStatus.AVAILABLE,
                )

    def search_available_table(self, branch_id, required_capacity=0):
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
        if not isinstance(status, TableStatus):
            raise TypeError("Status must be TableStatus")

        cafe_branch = self.find_cafe_branch_by_table_id(table_id)
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
        cafe_branch = self.find_cafe_branch_by_id(branch_id)
        if cafe_branch:
            return cafe_branch.add_board_game(
                name, genre, price, min_players, max_players, description
            )
        else:
            raise ValueError("Cafe Branch not found")

    def get_branch_board_games(self, branch_id):
        cafe_branch = self.find_cafe_branch_by_id(branch_id)
        if cafe_branch:
            return cafe_branch.board_games
        else:
            raise ValueError("Cafe Branch not found")

    def find_board_game_by_id(self, board_game_id):
        cafe_branch = self.find_cafe_branch_by_board_game_id(board_game_id)
        if cafe_branch:
            board_game = cafe_branch.find_board_game_by_id(board_game_id)
            if board_game:
                return board_game
        raise ValueError("Board Game not found")

    def search_board_game_by_min_players(self, branch_id, min_players):
        cafe_branch = self.find_cafe_branch_by_id(branch_id)
        if cafe_branch:
            return cafe_branch.search_board_game_by_min_players(min_players)
        else:
            raise ValueError("Cafe Branch not found")

    def update_board_game_status(self, board_game_id, status):
        if not isinstance(status, BoardGameStatus):
            raise TypeError("Status must be BoardGameStatus")

        board_game = self.find_board_game_by_id(board_game_id)
        if board_game:
            board_game.status = status
        else:
            raise ValueError("Board Game not found")

    def remove_board_game_by_id(self, board_game_id):
        board_game = self.find_board_game_by_id(board_game_id)
        if board_game:
            cafe_branch = self.find_cafe_branch_by_board_game_id(board_game_id)
            cafe_branch.remove_board_game_by_id(board_game_id)
        else:
            raise ValueError("Board Game not found")

    # / ════════════════════════════════════════════════════════════════
    # \ MENU

    def create_menu_to_branch(self, branch_id):
        cafe_branch = self.find_cafe_branch_by_id(branch_id)
        if cafe_branch:
            new_menu = MenuList()
            cafe_branch.create_menu(new_menu)
            return new_menu
        else:
            raise ValueError("Cafe Branch not found")

    def create_menu_item_food_to_branch(self, branch_id, name, price, description=""):
        cafe_branch = self.find_cafe_branch_by_id(branch_id)
        if cafe_branch:
            return cafe_branch.create_menu_item_food(name, price, description)

    def create_menu_item_drink_to_branch(self, branch_id, name, price, description=""):
        cafe_branch = self.find_cafe_branch_by_id(branch_id)
        if cafe_branch:
            return cafe_branch.create_menu_item_drink(name, price, description)

    def get_branch_menu(self, branch_id):
        cafe_branch = self.find_cafe_branch_by_id(branch_id)
        if cafe_branch:
            return cafe_branch.get_menu()
        else:
            raise ValueError("Cafe Branch not found")

    def get_branch_menu_item(self, branch_id):
        cafe_branch = self.find_cafe_branch_by_id(branch_id)
        if cafe_branch:
            return cafe_branch.get_menu_item()
        else:
            raise ValueError("Cafe Branch not found")

    def get_branch_menu_item_food(self, branch_id):
        cafe_branch = self.find_cafe_branch_by_id(branch_id)
        if cafe_branch:
            return cafe_branch.get_menu_item_food()
        else:
            raise ValueError("Cafe Branch not found")

    def get_branch_menu_item_drink(self, branch_id):
        cafe_branch = self.find_cafe_branch_by_id(branch_id)
        if cafe_branch:
            return cafe_branch.get_menu_item_drink()
        else:
            raise ValueError("Cafe Branch not found")

    def find_menu_item_by_id(self, menu_item_id):
        cafe_branch = self.find_cafe_branch_by_menu_item_id(menu_item_id)
        if cafe_branch:
            return cafe_branch.find_menu_item_by_id(menu_item_id)
        else:
            raise ValueError("Menu Item not found")

    def remove_menu_item_by_id(self, menu_item_id):
        cafe_branch = self.find_cafe_branch_by_menu_item_id(menu_item_id)
        if cafe_branch:
            cafe_branch.remove_menu_item_by_id(menu_item_id)
        else:
            raise ValueError("Menu Item not found")

    def update_menu_item_by_id(self, menu_item_id, name, price, description=""):
        cafe_branch = self.find_cafe_branch_by_menu_item_id(menu_item_id)
        if cafe_branch:
            cafe_branch.update_menu_item_by_id(menu_item_id, name, price, description)
        else:
            raise ValueError("Menu Item not found")

    # / ════════════════════════════════════════════════════════════════
    # \ GAME SESSION - CHECK-IN
    def get_active_session_by_table(self, table_id):
        for session in self.__game_sessions:
            if session.table_id == table_id and session.end_time is None:
                return session
        return None
    def check_in_reserved(self, reservation_id, customer_id):
        reservation = self.find_reservation_by_id(reservation_id)
        if reservation is None:
            raise ValueError("Reservation not found")
        customer = self.find_person_by_id(customer_id)
        if customer is None:
            raise ValueError("Customer not found")
        now = datetime.now()

        # ! fix time arrive
        if now < reservation.reservation_time:
            raise ValueError("Too early to check-in")
        if reservation.status != ReservationStatus.PENDING:
            raise ValueError("Can check in reservation that already completed")
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

            session = PlaySession(reservation.table_id, datetime.now())
            branch.add_play_session(session)
            session.add_players_id(reservation.customer_id)
            return session

    def check_in_walk_in(self, branch_id, player_amount, table_id="auto"):
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
            table = branch.find_table_by_id(table_id)
            if table is None:
                raise ValueError("Table not found")

            if table.status != TableStatus.AVAILABLE:
                raise ValueError("Table is not available")

            if table.capacity < player_amount:
                raise ValueError("Table capacity not enough")

        table.status = TableStatus.OCCUPIED

        session = PlaySession(table.table_id, datetime.now())
        session.add_players_id(self.create_customer_walk_in().user_id)
        branch.add_play_session(session)

        return session

    def check_in_member(self, branch_id, player_amount, member_id, table_id="auto"):
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
            table = branch.find_table_by_id(table_id)
            if table is None:
                raise ValueError("Table not found")

            if table.status != TableStatus.AVAILABLE:
                raise ValueError("Table is not available")

            if table.capacity < player_amount:
                raise ValueError("Table capacity not enough")

        table.status = TableStatus.OCCUPIED

        session = PlaySession(table.table_id, datetime.now())
        session.add_players_id(member_id)
        branch.add_play_session(session)
        return session

    # / ════════════════════════════════════════════════════════════════
    # \ GAME SESSION - JOIN

    def join_session(self, play_session_id, customer_id):
        cafe_branch = self.find_cafe_branch_by_play_session_id(play_session_id)
        if cafe_branch is None:
            raise ValueError("Cafe Branch not found")

        play_session = cafe_branch.find_play_session_by_id(play_session_id)

        if play_session:
            play_session.add_players_id(customer_id)
        else:
            raise ValueError("Play Session not found")

    def join_session_walk_in(self, play_session_id):
        cafe_branch = self.find_cafe_branch_by_play_session_id(play_session_id)
        if cafe_branch is None:
            raise ValueError("Cafe Branch not found")

        play_session = cafe_branch.find_play_session_by_id(play_session_id)
        if play_session:
            play_session.add_players_id(self.create_customer_walk_in().user_id)
        else:
            raise ValueError("Play Session not found")

    def join_session_member(self, play_session_id, member_id):
        cafe_branch = self.find_cafe_branch_by_play_session_id(play_session_id)
        if cafe_branch is None:
            raise ValueError("Cafe Branch not found")

        play_session = cafe_branch.find_play_session_by_id(play_session_id)

        if play_session:
            play_session.add_players_id(member_id)
        else:
            raise ValueError("Play Session not found")

    def join_session_walk_in_by_table_id(self, table_id):
        cafe_branch = self.find_cafe_branch_by_table_id(table_id)
        if cafe_branch is None:
            raise ValueError("Cafe Branch not found")

        play_session = cafe_branch.find_play_session_by_table_id(table_id)
        if play_session:
            play_session.add_players_id(self.create_customer_walk_in().user_id)
        else:
            raise ValueError("Play Session not found")

    def join_session_member_by_table_id(self, table_id, member_id):
        cafe_branch = self.find_cafe_branch_by_table_id(table_id)
        if cafe_branch is None:
            raise ValueError("Cafe Branch not found")

        play_session = cafe_branch.find_play_session_by_table_id(table_id)
        if play_session:
            play_session.add_players_id(member_id)
        else:
            raise ValueError("Play Session not found")

    # / ════════════════════════════════════════════════════════════════
    # \ GAME SESSION - BORROW BOARD GAME

    def borrow_board_game(self, table_id, board_game_id):
        cafe_branch = self.find_cafe_branch_by_table_id(table_id)
        if cafe_branch is None:
            raise ValueError("Cafe Branch not found")

        play_session = cafe_branch.find_play_session_by_table_id(table_id)
        if play_session is None:
            raise ValueError("Play Session not found")

        if len(play_session.current_board_games_id) + 1 > 2:
            # ! raise ValueError("limit 2 board games per session")
            return None

        board_game = cafe_branch.find_board_game_by_id(board_game_id)
        if board_game is None:
            raise ValueError("Board Game not found")

        if board_game.status != BoardGameStatus.AVAILABLE:
            # ! raise ValueError("Board Game is not available")
            return None

            if board_game.status == BoardGameStatus.IN_USE:
                # ! raise ValueError("Board Game already borrowed")
                return None

        play_session.add_board_games_id(board_game_id)
        board_game.status = BoardGameStatus.IN_USE
        return board_game

    def return_board_game(self, table_id, board_game_id):
        cafe_branch = self.find_cafe_branch_by_table_id(table_id)
        if cafe_branch is None:
            raise ValueError("Cafe Branch not found")

        play_session = cafe_branch.find_play_session_by_table_id(table_id)
        if play_session is None:
            raise ValueError("Play Session not found")

        board__game = cafe_branch.find_board_game_by_id(board__game_id)
        if board__game is None:
            raise ValueError("Board Game not found")

        board__game.status = BoardGameStatus.AVAILABLE
        play_session.remove_board_games_id(board__game_id)

        return board__game

    def fix_board_game(self, board__game_id):
        cafe_branch = self.find_cafe_branch_by_board_game_id(board__game_id)
        if cafe_branch is None:
            raise ValueError("Cafe Branch not found")

        board_game = cafe_branch.find_board_game_by_id(board_game_id)
        if board_game is None:
            raise ValueError("Board Game not found")

        board__game.status = BoardGameStatus.MAINTENANCE
        for session in cafe_branch.get_play_sessions():
            if board__game_id in session.current_board_games_id:
                raise ValueError("Board Game in use")

        return board__game

    # / ════════════════════════════════════════════════════════════════
    # \ GAME SESSION - ORDER

    def take_order(self, table_id, menu_item_id):
        cafe_branch = self.find_cafe_branch_by_table_id(table_id)
        if cafe_branch is None:
            raise ValueError("Cafe Branch not found")

        play_session = cafe_branch.find_play_session_by_table_id(table_id)
        if play_session:
            menu_item = cafe_branch.find_menu_item_by_id(menu_item_id)
            if menu_item:
                play_session.take_order(menu_item)
            else:
                raise ValueError("Menu Item not found")
        else:
            raise ValueError("Play Session not found")

    def get_pending_orders(self, branch_id):
        cafe_branch = self.find_cafe_branch_by_id(branch_id)
        if cafe_branch:
            return cafe_branch.get_pending_orders()
        else:
            raise ValueError("Cafe Branch not found")

    def update_order(self, play_session_id, order_id, session_status):
        cafe_branch = self.find_cafe_branch_by_play_session_id(play_session_id)
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
    # / ════════════════════════════════════════════════════════════════
    def check_out_by_table_id(self, table_id):

        cafe_branch = self.find_cafe_branch_by_table_id(table_id)
        if cafe_branch is None:
            raise ValueError("Cafe Branch not found")

        play_session = cafe_branch.find_play_session_by_table_id(table_id)
        if play_session is None:
            raise ValueError("Play Session not found")

        table = cafe_branch.find_table_by_id(table_id)

        total = 0

        for board_game_id in play_session.current_board_games_id:
            board_game = cafe_branch.find_board_game_by_id(board_game_id)
            board_game.status = BoardGameStatus.AVAILABLE

        for order in play_session.current_order:
            if order.status != OrderStatus.CANCELLED:
                total += order.menu_item.price
        
        cafe_branch.end_play_session(play_session.session_id)
        if table:
            table.status = TableStatus.AVAILABLE
        total += table.price_per_hour * play_session.duration()
        return total
    def check_out_by_session_id(self, play_session_id):
        cafe_branch = self.find_cafe_branch_by_play_session_id(play_session_id)
        if cafe_branch is None:
            raise ValueError("Cafe Branch not found")

        play_session = cafe_branch.find_play_session_by_id(play_session_id)
        if play_session is None:
            raise ValueError("Play Session not found")

        table = cafe_branch.find_table_by_id(play_session.table_id)

        total = 0

        for board_game_id in play_session.current_board_games_id:
            board_game = cafe_branch.find_board_game_by_id(board_game_id)
            if board_game:
                total += board_game.price
                board_game.status = BoardGameStatus.AVAILABLE

        for order in play_session.current_order:
            if order.status != OrderStatus.CANCELLED:
                total += order.menu_item.price

        cafe_branch.end_play_session(play_session.session_id)
        if table:
            table.status = TableStatus.AVAILABLE
        total += table.price_per_hour * play_session.duration()
        return total
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

    def create_menu_item_drink(self, name, price, description=""):
        if self.__menu_list is not None:
            new_menu_item = Drink(name, price, description)
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

    def find_play_session_by_id(self, play_session_id):
        for play_session in self.__play_sessions:
            if play_session.session_id == play_session_id:
                return play_session
        return None

    def find_play_session_by_table_id(self, table_id):
        for play_session in self.__play_sessions:
            if play_session.table_id == table_id:
                return play_session
        return None

    def remove_play_session_by_id(self, play_session_id):
        play_session = self.find_play_session_by_id(play_session_id)
        if play_session:
            self.__play_sessions.remove(play_session)
        else:
            raise ValueError("Invalid ID : Play Session not found")

    def end_play_session(self, play_session_id):
        play_session = self.find_play_session_by_id(play_session_id)
        if play_session:
            play_session.end_time = datetime.now()
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
