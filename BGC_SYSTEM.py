import datetime
import time

from BGC_MENU import *
from BGC_PAYMENT import *
from BGC_PERSON import *
from BGC_PLAY_SESSION import *
from BGC_RESERVATION import *
from ENUM_STATUS import *

# | ================================================================================================================================
# | #EFFF11


class CafeSystem:
    def __init__(self):
        self.__person = []
        self.__cafe_branches = []
        self.__reservations = []

    # / ================================================================
    # - Getters
    # / ================================================================

    @property
    def person(self):
        return self.__person.copy()

    @property
    def cafe_branches(self):
        return self.__cafe_branches.copy()

    @property
    def reservations(self):
        return self.__reservations.copy()

    # / ================================================================
    # - Setters
    # / ================================================================

    # / ================================================================
    # - Methods
    # / ================================================================
    # \ ADD PERSON

    def add_person(self, person):
        if isinstance(person, Person):
            self.__person.append(person)
        else:
            raise TypeError("Type Error : must be an instance of Person")

    def add_owner(self, name):
        new_owner = Owner(name)
        self.add_person(new_owner)
        return new_owner

    def add_manager(self, name):
        new_manager = Manager(name)
        self.add_person(new_manager)
        return new_manager

    def add_staff(self, name):
        new_staff = Staff(name)
        self.add_person(new_staff)
        return new_staff

    def add_customer_member(self, name):
        new_customer = Member(name)
        self.add_person(new_customer)
        return new_customer

    def add_customer_walk_in(self):
        new_walk_in = WalkInCustomer()
        self.add_person(new_walk_in)
        return new_walk_in

    # / ================================================================
    # \ CAFE BRANCH

    def add_cafe_branch(self, cafe_branch_name, cafe_branch_location=""):
        new_cafe_branch = CafeBranch(cafe_branch_name, cafe_branch_location)
        self.__cafe_branches.append(new_cafe_branch)
        return new_cafe_branch

    def remove_cafe_branch_by_id(self, cafe_branch_id):
        cafe_branch = self.find_cafe_branch_by_id(cafe_branch_id)
        if cafe_branch:
            self.__cafe_branches.remove(cafe_branch)
        else:
            raise ValueError("Invalid ID : Cafe Branch not found")

    # / ================================================================
    # \ RESERVATION

    def add_reservation(self, reservation):
        if isinstance(reservation, Reservation):
            self.__reservations.append(reservation)
        else:
            raise TypeError("Type Error : must be an instance of Reservation")

    def remove_reservation_by_id(self, reservation_id):
        reservation = self.find_reservation_by_id(reservation_id)
        if reservation:
            self.__reservations.remove(reservation)
        else:
            raise ValueError("Invalid ID : Reservation not found")

    # / ================================================================
    # \ FIND METHODS

    def find_person_by_id(self, user_id):
        for person in self.__person:
            if person.user_id == user_id:
                return person
        return None

    def find_cafe_branch_by_id(self, branch_id):
        for cafe_branch in self.__cafe_branches:
            if cafe_branch.branch_id == branch_id:
                return cafe_branch
        return None

    def find_reservation_by_id(self, reservation_id):
        for reservation in self.__reservations:
            if reservation.reservation_id == reservation_id:
                return reservation
        return None

    # / ================================================================
    # \ TABLE

    def add_table_to_branch(self, branch_id, capacity):
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
        now = datetime.datetime.now()

        for reservation in self.__reservations:
            reservation_time = reservation.reservation_time
            time_diff = reservation_time - now

            if datetime.timedelta(hours=0) <= time_diff <= datetime.timedelta(hours=1):
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
            if table.status is not TableStatus.AVAILABLE:
                continue
            if table.capacity >= required_capacity:
                available_tables.append(table)

        return available_tables

    def update_table_status(self, branch_id, table_id, status):
        if not isinstance(status, TableStatus):
            raise TypeError("Status must be TableStatus")

        cafe_branch = self.find_cafe_branch_by_id(branch_id)
        if cafe_branch is None:
            raise ValueError("Cafe Branch not found")

        table = cafe_branch.get_table_by_id(table_id)
        if table is None:
            raise ValueError("Table not found")

        table.status = status

    # / ================================================================
    # \ GAME SESSION

    def check_in_reserved(self, reservation_id, customer):
        reservation = self.find_reservation_by_id(reservation_id)
        if reservation is None:
            raise ValueError("Reservation not found")

        now = datetime.datetime.now()

        # ! fix time arrive
        if now < reservation.reservation_time:
            raise ValueError("Too early to check-in")

        branch = self.find_cafe_branch_by_id(reservation.branch_id)
        if branch is None:
            raise ValueError("Branch not found")

        table = branch.get_table_by_id(reservation.table_id)
        if table is None:
            raise ValueError("Table not found")

        table.status = TableStatus.OCCUPIED

        if customer.temp_id == reservation.customer_id:
            session = PlaySession(reservation.table_id, datetime.datetime.now())

            branch.add_play_session(session)
            session.add_players_id(reservation.customer_id)
            return session
        else:
            raise ValueError("Wrong personal ID")

    def check_in_walkin(self, branch_id, player_amount, table_id="auto"):
        self.update_reserved_tables()

        branch = self.find_cafe_branch_by_id(branch_id)
        if branch is None:
            raise ValueError("Cafe Branch not found")

        if table_id == "auto":
            tables = self.search_available_table(branch_id, player_amount)
            if tables is None:
                raise ValueError("No available table")
            table = min(tables, key=lambda t: t.capacity)

            # print(f"Table {table.table_id} is available")
        else:
            table = branch.get_table_by_id(table_id)
            if table is None:
                raise ValueError("Table not found")

            if table.status != TableStatus.AVAILABLE:
                raise ValueError("Table is not available")

            if table.capacity < player_amount:
                raise ValueError("Table capacity not enough")

        table.status = TableStatus.OCCUPIED

        session = PlaySession(table.table_id, datetime.datetime.now())
        branch.add_play_session(session)
        return session

    def check_in_member(self, branch_id, player_amount, member_id, table_id="auto"):
        pass

    # / ================================================================
    # \ BOARD GAME

    def add_board_game_to_branch(
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

    # / ================================================================
    # \ MENU

    def add_menu_to_branch(self, branch_id):
        cafe_branch = self.find_cafe_branch_by_id(branch_id)
        if cafe_branch:
            new_menu = MenuList()
            cafe_branch.add_menu(new_menu)
            return new_menu
        else:
            raise ValueError("Cafe Branch not found")

    def add_menu_item_food_to_branch(self, branch_id, name, price, description=""):
        cafe_branch = self.find_cafe_branch_by_id(branch_id)
        if cafe_branch:
            return cafe_branch.add_menu_item_food(name, price, description)

    def add_menu_item_drink_to_branch(self, branch_id, name, price, description=""):
        cafe_branch = self.find_cafe_branch_by_id(branch_id)
        if cafe_branch:
            return cafe_branch.add_menu_item_drink(name, price, description)

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

    # / ================================================================


# | ================================================================================================================================
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

    # / ================================================================
    # - Getters
    # / ================================================================

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

    # / ================================================================

    @property
    def total_tables(self):
        return len(self.__tables)

    @property
    def total_board_games(self):
        return len(self.__board_games)

    @property
    def total_menu_items(self):
        return len(self.__menu_list.menu_items())

    # / ================================================================
    # - Setters
    # / ================================================================

    @name.setter
    def name(self, name):
        self.__name = name

    @location.setter
    def location(self, location):
        self.__location = location

    # / ================================================================
    # - Methods
    # / ================================================================
    # \ TABLE

    def add_table(self, capacity):
        new_table = Table(capacity)
        self.__tables.append(new_table)
        return new_table

    def get_tables(self):
        return self.__tables.copy()

    def get_table_by_id(self, table_id):
        for table in self.__tables:
            if table.table_id == table_id:
                return table
        return None

    # / ================================================================
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

    def get_board_game_by_id(self, board_game_id):
        for board_game in self.__board_games:
            if board_game.board_game_id == board_game_id:
                return board_game
        return None

    # / ================================================================
    # \ MENU

    def add_menu(self, menu):
        if isinstance(menu, MenuList):
            self.__menu_list = menu
        else:
            raise TypeError("Type Error : must be an instance of Menu")

    def add_menu_item_food(self, name, price, description=""):
        if self.__menu_list is not None:
            new_menu_item = Food(name, price, description)
            self.__menu_list.add_menu_item(new_menu_item)
            return new_menu_item
        else:
            raise ValueError("Menu not found")

    def add_menu_item_drink(self, name, price, description=""):
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
            return [
                item for item in self.__menu_list.menu_items if isinstance(item, Food)
            ]
        else:
            raise ValueError("Menu not found")

    def get_menu_item_drink(self):
        if self.__menu_list is not None:
            return [
                item for item in self.__menu_list.menu_items if isinstance(item, Drink)
            ]
        else:
            raise ValueError("Menu not found")

    def get_menu_item_by_id(self, menu_item_id):
        if self.__menu_list is not None:
            return self.__menu_list.get_menu_item_by_id(menu_item_id)
        else:
            raise ValueError("Menu not found")

    def remove_menu_item_by_id(self, menu_item_id):
        if self.__menu_list is not None:
            self.__menu_list.remove_menu_item(menu_item_id)
        else:
            raise ValueError("Menu not found")

    def update_menu_item_by_id(self, menu_item_id, name, price, description=""):
        if self.__menu_list is not None:
            menu_item = self.__menu_list.get_menu_item_by_id(menu_item_id)
            if menu_item is not None:
                menu_item.name = name
                menu_item.price = price
                menu_item.description = description
            else:
                raise ValueError("Menu Item not found")
        else:
            raise ValueError("Menu not found")

    # / ================================================================
    # \ STAFF

    def add_staff(self, staff):
        if isinstance(staff, Staff):
            self.__staff_id.append(staff.user_id)
        else:
            raise TypeError("Type Error : must be an instance of Staff")

    def add_staff_by_id(self, staff_id):
        person = self.find_person_by_id(staff_id)
        if person is not None and isinstance(person, Staff):
            self.__staff_id.append(staff_id)
        else:
            raise TypeError("Invalid ID : ID does not exist")

    def get_staff(self):
        return self.__staff_id.copy()

    def remove_staff_by_id(self, staff_id):
        if staff_id in self.__staff_id:
            self.__staff_id.remove(staff_id)
        else:
            raise ValueError("Invalid ID : ID does not exist")

    # / ================================================================
    # \ MANAGER

    def add_manager(self, manager):
        if isinstance(manager, Manager):
            self.__manager_id = manager.user_id
        else:
            raise TypeError("Type Error : must be an instance of Manager")

    def add_manager_by_id(self, manager_id):
        person = self.find_person_by_id(manager_id)
        if person is not None and isinstance(person, Manager):
            self.__manager_id = manager_id
        else:
            raise TypeError("Invalid ID : ID does not exist")

    def get_manager(self):
        return self.__manager_id

    def remove_manager(self):
        self.__manager_id = None

    # / ================================================================
    # \ OWNER

    def add_owner(self, owner):
        if isinstance(owner, Owner):
            self.__owner_id = owner.user_id
        else:
            raise TypeError("Type Error : must be an instance of Owner")

    def add_owner_by_id(self, owner_id):
        person = self.find_person_by_id(owner_id)
        if person is not None and isinstance(person, Owner):
            self.__owner_id = owner_id
        else:
            raise TypeError("Invalid ID : ID does not exist")

    def get_owner(self):
        return self.__owner_id

    def remove_owner(self):
        self.__owner_id = None

    # / ================================================================
    # \ PLAY SESSION

    def add_play_session(self, play_session):
        if isinstance(play_session, PlaySession):
            self.__play_sessions.append(play_session)
        else:
            raise TypeError("Type Error : must be an instance of PlaySession")

    def get_play_session_by_id(self, play_session_id):
        for play_session in self.__play_sessions:
            if play_session.session_id == play_session_id:
                return play_session
        return None

    def remove_play_session_by_id(self, play_session_id):
        play_session = self.get_play_session_by_id(play_session_id)
        if play_session:
            self.__play_sessions.remove(play_session)
        else:
            raise ValueError("Invalid ID : Play Session not found")

    # / ================================================================


# | ================================================================================================================================
