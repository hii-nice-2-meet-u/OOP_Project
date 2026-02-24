import ENUM_STATUS


class BoardGame:
    def __init__(
        self,
        game_id,
        name,
        genre,
        price,
        status,
        min_players,
        max_players,
        description="",
    ):
        self.__game_id = game_id
        self.__name = name
        self.__genre = genre
        self.__price = price
        self.__status = status
        self.__min_players = min_players
        self.__max_players = max_players
        self.__description = description

    @property
    def game_id(self):
        return self.__game_id

    @game_id.setter
    def game_id(self, game_id):
        self.__game_id = game_id

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name):
        self.__name = name

    @property
    def genre(self):
        return self.__genre

    @genre.setter
    def genre(self, genre):
        self.__genre = genre

    @property
    def price(self):
        return self.__price

    @price.setter
    def price(self, price):
        self.__price = price

    @property
    def status(self):
        return self.__status

    @status.setter
    def status(self, status):
        self.__status = status

    @property
    def min_players(self):
        return self.__min_players

    @min_players.setter
    def min_players(self, min_players):
        self.__min_players = min_players

    @property
    def max_players(self):
        return self.__max_players

    @max_players.setter
    def max_players(self, max_players):
        self.__max_players = max_players

    @property
    def description(self):
        return self.__description

    @description.setter
    def description(self, description):
        self.__description = description


class PlayTable(ABC):
    price_per_hour = 0

    def __init__(self, table_id, capacity):
        self.__table_id = table_id
        self.__capacity = capacity
        self.__status = AVAILABLE
        self.__current_game = []
        self.__current_players = []
        self.__current_order = []

    @property
    def table_id(self):
        return self.__table_id

    @table_id.setter
    def table_id(self, table_id):
        self.__table_id = table_id

    @property
    def capacity(self):
        return self.__capacity

    @capacity.setter
    def capacity(self, capacity):
        self.__capacity = capacity

    @property
    def status(self):
        return self.__status

    @status.setter
    def status(self, status):
        self.__status = status

    @property
    def current_game(self):
        return self.__current_game

    @current_game.setter
    def current_game(self, current_game):
        self.__current_game = current_game

    @property
    def current_players(self):
        return self.__current_players

    @current_players.setter
    def current_players(self, current_players):
        self.__current_players = current_players

    @property
    def current_order(self):
        return self.__current_order

    @current_order.setter
    def current_order(self, current_order):
        self.__current_order = current_order

    # ! ! ! ! ! ! ! !
    def calculate_total_price(self, hours):
        pass

    # ! ! ! ! ! ! ! !

    def get_table_by_id(self, table_id):
        for table in self.__play_tables:
            if table.table_id == table_id:
                return table
        return None


class PlayTableStandard(PlayTable):
    price_per_hour = 50.00

    def __init__(self, table_id, capacity):
        super().__init__(table_id, capacity)


class PlayTableVIP(PlayTable):
    price_per_hour = 75.00

    def __init__(self, table_id, capacity):
        super().__init__(table_id, capacity)


class CafeSystem:
    def __init__(self):
        self.__person = []
        self.__cafe_branches = []
        self.__reservations = []


class CafeBranch:
    __counter = 0

    def __init__(self, branch_id, name, location=""):
        self.__branch_id = CafeBranch.__counter
        CafeBranch.__counter += 1
        self.__name = name
        self.__location = location
        self.__play_tables = []
        self.__board_games = []
        self.__menu_list = None

    @property
    def branch_id(self):
        return self.__branch_id

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name):
        self.__name = name
