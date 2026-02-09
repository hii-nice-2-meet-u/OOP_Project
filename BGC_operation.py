
class Payment:
    def __init__(self):
        self.__payment_id = None
        self.__timestamp = None
        self.__customer = None
        self.__total_amount = 0.0
        self.__payment_method = None
        self.__status = None


class Cash(Payment):
    def __init__(self):
        super().__init__()


class Card(Payment):
    def __init__(self):
        super().__init__()


class OnlinePayment(Payment):
    def __init__(self):
        super().__init__()


class Lobby:
    def __init__(self):
        self.__lobby_id = None
        self.__play_tables = []


class PlayTable:
    def __init__(self):
        self.__table_id = None
        self.__status = None
        self.__customers = []
        self.__board_game = []
