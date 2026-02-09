class SystemLog:
    pass


class FinancialLog:
    pass


class AuditLog:
    def __init__(self):
        self.__log_id = None
        self.__timestamp = None
        self.__action = None
        self.__performed_by = None


class Transaction:
    def __init__(self):
        self.__transaction_id = None
        self.__timestamp = None
        self.__customer = None
        self.__items = []
        self.__total_amount = 0.0


class BoardGame:
    def __init__(self, _name: str, _item_id: str):
        self.__user_name = None
        self.__user_password = None
        self.__name = _name
        self.__item_id = _item_id
        self.__status = None
        self.__description = None
        self.__difficulty = None
        self.__category = None


class OrderSystem:
    def __init__(self):
        self.__orders = []


class Order:
    def __init__(self):
        self.__order_id = None
        self.__timestamp = None
        self.__table = None
        self.__customer = None
        self.__menu = None
