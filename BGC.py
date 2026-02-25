from abc import ABC, abstractmethod
from ENUM_STATUS import TableStatus


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

    # / ================================================================
    # - Setters
    # / ================================================================

    # / ================================================================
    # - Methods
    # / ================================================================

    # / ================================================================


class Table:
    __counter = 0

    def __init__(self, table_id, capacity):
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


class CafeSystem:
    def __init__(self):
        self.__person = []
        self.__cafe_branches = []
        self.__reservations = []

    # / ================================================================
    # - Getters
    # / ================================================================

    # / ================================================================
    # - Setters
    # / ================================================================

    # / ================================================================
    # - Methods
    # / ================================================================

    # / ================================================================


class CafeBranch:
    __counter = 0

    def __init__(self, branch_id, name, location=""):
        self.__branch_id = "BRCH-" + str(CafeBranch.__counter).zfill(5)
        CafeBranch.__counter += 1
        self.__name = name
        self.__location = location
        self.__tables = []
        self.__board_games = []
        self.__menu_list = None

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

    @tables.setter
    def tables(self, tables):
        self.__tables = tables

    @board_games.setter
    def board_games(self, board_games):
        self.__board_games = board_games

    @menu_list.setter
    def menu_list(self, menu_list):
        self.__menu_list = menu_list

    # / ================================================================
    # - Methods
    # / ================================================================

    # / ================================================================
