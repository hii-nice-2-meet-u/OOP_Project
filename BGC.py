from abc import ABC, abstractmethod
from ENUM_STATUS import TableStatus

import datetime
from BGC_MENU import *
from BGC_PAYMENT import *
from BGC_PERSON import *
from BGC_RESERVATION import *

# | ================================================================================================================================


class BoardGame:
    __counter = 0

    def __init__(
        self,
        name,
        genre,
        price,
        status,
        min_players,
        max_players,
        description="",
    ):
        self.__board_game_id = "BG-" + str(BoardGame.__counter).zfill(5)
        BoardGame.__counter += 1
        self.__name = name
        self.__genre = genre
        self.__price = price
        self.__status = status
        self.__min_players = min_players
        self.__max_players = max_players
        self.__description = description

    # / ================================================================
    # - Getters
    # / ================================================================

    @property
    def game_id(self):
        return self.__board_game_id

    @property
    def name(self):
        return self.__name

    @property
    def genre(self):
        return self.__genre

    @property
    def price(self):
        return self.__price

    @property
    def status(self):
        return self.__status

    @property
    def min_players(self):
        return self.__min_players

    @property
    def max_players(self):
        return self.__max_players

    @property
    def description(self):
        return self.__description

    # / ================================================================
    # - Setters
    # / ================================================================

    @name.setter
    def name(self, name):
        self.__name = name

    @genre.setter
    def genre(self, genre):
        self.__genre = genre

    @price.setter
    def price(self, price):
        self.__price = price

    @status.setter
    def status(self, status):
        self.__status = status

    @min_players.setter
    def min_players(self, min_players):
        self.__min_players = min_players

    @max_players.setter
    def max_players(self, max_players):
        self.__max_players = max_players

    @description.setter
    def description(self, description):
        self.__description = description

    # / ================================================================
    # - Methods
    # / ================================================================

    # / ================================================================


# | ================================================================================================================================


class PlaySession:
    __counter = 0

    def __init__(self, session_id, table_id, start_time):
        self.__session_id = "PS-" + str(PlaySession.__counter).zfill(5)
        self.__table_id = table_id
        self.__start_time = start_time
        self.__end_time = None
        self.__current_players_id = []
        self.__current_board_games_id = []
        self.__current_order = []
        self.__payment = None

    # / ================================================================
    # - Getters
    # / ================================================================

    @property
    def session_id(self):
        return self.__session_id

    @property
    def table_id(self):
        return self.__table_id

    @property
    def start_time(self):
        return self.__start_time

    @property
    def end_time(self):
        return self.__end_time

    @property
    def current_players_id(self):
        return self.__current_players_id.copy()

    @property
    def current_board_games_id(self):
        return self.__current_board_games_id.copy()

    @property
    def current_order(self):
        return self.__current_order.copy()

    @property
    def payment(self):
        return self.__payment

    # / ================================================================
    # - Setters
    # / ================================================================

    @table_id.setter
    def table_id(self, table_id):
        self.__table_id = table_id

    @start_time.setter
    def start_time(self, start_time):
        self.__start_time = start_time

    @end_time.setter
    def end_time(self, end_time):
        self.__end_time = end_time

    @current_players_id.setter
    def current_players_id(self, players_id):
        self.__current_players_id = players_id

    @current_board_games_id.setter
    def current_board_games_id(self, board_games_id):
        self.__current_board_games_id = board_games_id

    @current_order.setter
    def current_order(self, order):
        self.__current_order = order

    @payment.setter
    def payment(self, payment):
        self.__payment = payment

    # / ================================================================
    # - Methods
    # / ================================================================

    # / ================================================================


# | ================================================================================================================================


class Table:
    __counter = 0

    def __init__(self, capacity):
        self.__table_id = "TABLE-" + str(Table.__counter).zfill(5)
        Table.__counter += 1
        self.__capacity = capacity
        self.__status = TableStatus.AVAILABLE

    # / ================================================================
    # - Getters
    # / ================================================================

    @property
    def table_id(self):
        return self.__table_id

    @property
    def capacity(self):
        return self.__capacity

    @property
    def status(self):
        return self.__status

    # / ================================================================
    # - Setters
    # / ================================================================

    @capacity.setter
    def capacity(self, capacity):
        self.__capacity = capacity

    @status.setter
    def status(self, status):
        self.__status = status

    # / ================================================================
    # - Methods
    # / ================================================================

    # / ================================================================


# | ================================================================================================================================


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

    def add_cafe_branch(self, cafe_branch_name, cafe_branch_location=""):
        new_cafe_branch = CafeBranch(cafe_branch_name, cafe_branch_location)
        self.__cafe_branches.append(new_cafe_branch)
        return new_cafe_branch

    def add_person(self, person):
        if isinstance(person, Person):
            self.__person.append(person)
        else:
            raise TypeError("Type Error : must be an instance of Person")

    def add_reservation(self, reservation):
        if isinstance(reservation, Reservation):
            self.__reservations.append(reservation)
        else:
            raise TypeError("Type Error : must be an instance of Reservation")

    # / ================================================================

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

    # / ================================================================

    def add_table_to_branch(self, branch_id, capacity):
        cafe_branch = self.find_cafe_branch_by_id(branch_id)
        if cafe_branch:
            return cafe_branch.add_table(capacity)
        else:
            raise ValueError("Cafe Branch not found")

    def add_board_game_to_branch(
        self,
        branch_id,
        name,
        genre,
        price,
        status,
        min_players,
        max_players,
        description="",
    ):
        cafe_branch = self.find_cafe_branch_by_id(branch_id)
        if cafe_branch:
            return cafe_branch.add_board_game(
                name, genre, price, status, min_players, max_players, description
            )
        else:
            raise ValueError("Cafe Branch not found")

    def add_menu_item_to_branch(self, branch_id, name, price, description=""):


    # / ================================================================

    def get_branch_tables(self, branch_id):
        cafe_branch = self.find_cafe_branch_by_id(branch_id)
        if cafe_branch:
            return cafe_branch.tables
        else:
            raise ValueError("Cafe Branch not found")

    def get_branch_board_games(self, branch_id):
        cafe_branch = self.find_cafe_branch_by_id(branch_id)
        if cafe_branch:
            return cafe_branch.board_games
        else:
            raise ValueError("Cafe Branch not found")

    # / ================================================================


# | ================================================================================================================================


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
        self.__play_sessions = []
        self.__staff_id = []
        self.__manager_id = None
        self.__owner_id = None

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
    def tables(self):
        return self.__tables.copy()

    @property
    def board_games(self):
        return self.__board_games.copy()

    @property
    def menu_list(self):
        return self.__menu_list

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

    def add_table(self, capacity):
        new_table = Table(capacity)
        self.__tables.append(new_table)
        return new_table

    def add_board_game(
        self, name, genre, price, status, min_players, max_players, description=""
    ):
        new_board_game = BoardGame(
            name, genre, price, status, min_players, max_players, description
        )
        self.__board_games.append(new_board_game)
        return new_board_game

    def add_menu(self, menu):
        if isinstance(menu, Menu):
            self.__menu_list = menu
        else:
            raise TypeError("Type Error : must be an instance of Menu")

    def add_menu_item(self, name, price, description=""):
        if self.__menu_list is not None:
            new_menu_item = MenuItem(name, price, description)
            self.__menu_list.add_menu_item(new_menu_item)
            return new_menu_item
        else:
            raise ValueError("Menu not found")

    # / ================================================================


# | ================================================================================================================================
