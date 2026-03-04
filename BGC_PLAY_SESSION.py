import datetime

from BGC_MENU import *
from BGC_PAYMENT import *

from ENUM_STATUS import TableStatus, BoardGameStatus

# | ================================================================================================================================
# | #EFFF11


class BoardGame:
    __counter = 0

    def __init__(
        self,
        name,
        genre,
        price,
        min_players,
        max_players,
        description="",
    ):
        self.__board_game_id = "BG-" + str(BoardGame.__counter).zfill(5)
        BoardGame.__counter += 1
        self.__name = name
        self.__genre = genre
        self.__price = price
        self.__status = BoardGameStatus.AVAILABLE
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
# | #EFFF11


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
# | #EFFF11


class PlaySession:
    __counter = 0

    def __init__(self, session_id, table_id, start_time):
        self.__session_id = "PS-" + str(PlaySession.__counter).zfill(5)
        PlaySession.__counter += 1
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
