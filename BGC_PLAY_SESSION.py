import datetime
import math

from BGC_MENU import *
from BGC_PAYMENT import *

from ENUM_STATUS import TableStatus, BoardGameStatus

# | ════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
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

    # / ════════════════════════════════════════════════════════════════
    # - Getters
    # / ════════════════════════════════════════════════════════════════

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

    # / ════════════════════════════════════════════════════════════════
    # - Setters
    # / ════════════════════════════════════════════════════════════════

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

    # / ════════════════════════════════════════════════════════════════
    # - Methods
    # / ════════════════════════════════════════════════════════════════

    # / ════════════════════════════════════════════════════════════════


# | ════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
# | #EFFF11


class Table:
    __counter = 0
    price_per_hour = 15

    def __init__(self, capacity):
        self.__table_id = "TABLE-" + str(Table.__counter).zfill(5)
        Table.__counter += 1
        self.__capacity = capacity
        self.__status = TableStatus.AVAILABLE

    # / ════════════════════════════════════════════════════════════════
    # - Getters
    # / ════════════════════════════════════════════════════════════════

    @property
    def table_id(self):
        return self.__table_id

    @property
    def capacity(self):
        return self.__capacity

    @property
    def status(self):
        return self.__status

    # / ════════════════════════════════════════════════════════════════
    # - Setters
    # / ════════════════════════════════════════════════════════════════

    @capacity.setter
    def capacity(self, capacity):
        self.__capacity = capacity

    @status.setter
    def status(self, status):
        self.__status = status

    # / ════════════════════════════════════════════════════════════════
    # - Methods
    # / ════════════════════════════════════════════════════════════════

    # / ════════════════════════════════════════════════════════════════


# | ════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
# | #EFFF11


class PlaySession:
    __counter = 0

    def __init__(self, table_id, start_time, reserved_duration=0, reserved_end_time=None):
        self.__session_id = "PS-" + str(PlaySession.__counter).zfill(5)
        PlaySession.__counter += 1
        self.__table_id = table_id
        self.__start_time = start_time
        self.__end_time = None
        self.__current_players_id = []
        self.__current_board_games_id = []
        self.__current_order = []
        self.__reservation_id = None
        self.__payment = None
        self.__game_penalty = []
        self.__reserved_duration = reserved_duration
        self.__reserved_end_time = reserved_end_time

    # / ════════════════════════════════════════════════════════════════
    # - Getters
    # / ════════════════════════════════════════════════════════════════

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
    def reservation_id(self):
        return self.__reservation_id

    @property
    def payment(self):
        return self.__payment

    @property
    def game_penalty(self):
        return self.__game_penalty.copy()

    @property
    def reserved_duration(self):
        return self.__reserved_duration

    @property
    def reserved_end_time(self):
        return self.__reserved_end_time

    @property
    def is_time_up(self):
        if self.__reserved_end_time is None:
            return False
        return datetime.datetime.now() >= self.__reserved_end_time

    # / ════════════════════════════════════════════════════════════════
    # - Setters
    # / ════════════════════════════════════════════════════════════════

    @end_time.setter
    def end_time(self, end_time):
        self.__end_time = end_time

    @payment.setter
    def payment(self, payment):
        if not isinstance(payment, Payment):
            raise ValueError("Invalid payment")
        self.__payment = payment

    @reservation_id.setter
    def reservation_id(self, value):
        self.__reservation_id = value

    # / ════════════════════════════════════════════════════════════════
    # - Methods
    # / ════════════════════════════════════════════════════════════════

    def add_players_id(self, player_id):
        self.__current_players_id.append(player_id)

    def add_board_games_id(self, board_game_id):
        self.__current_board_games_id.append(board_game_id)

    def add_game_penalty(self, game_id):
        self.__game_penalty.append(game_id)

    def get_total_players(self):
        return len(self.__current_players_id)

    def take_order(self, menu_item):
        if not isinstance(menu_item, MenuItem):
            raise ValueError("Type Error : Invalid order")
        new_order = Order(menu_item)
        self.__current_order.append(new_order)
        return new_order
        

    def remove_board_games_id(self, board_game_id):
        self.__current_board_games_id.remove(board_game_id)

    def remove_players_id(self, player_id):
        self.__current_players_id.remove(player_id)

    def duration(self, end_time=None):
        start = self.__start_time
        # Use provided end_time, or stored end_time, or now
        if end_time is None:
            end = self.__end_time if self.__end_time is not None else datetime.datetime.now()
        else:
            end = end_time

        if start is None:
            return 0
        
        diff_seconds = (end - start).total_seconds()
        calculated_duration = math.ceil(diff_seconds / 3600.0)
        
        # Ensure minimum 1 hour and at least reserved_duration if the session has started
        return max(1, calculated_duration, self.__reserved_duration)
        
 
    # / ════════════════════════════════════════════════════════════════


# | ════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════