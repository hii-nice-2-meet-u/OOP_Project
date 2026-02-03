import BGC_menu


class Registration:
    def __init__(self):
        self.__registration_id = None
        self.__timestamp = None
        self.__customer = None
        self.__status = None


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


class Reservation:
    def __init__(self):
        self.__reservation_id = None
        self.__customer = None
        self.__table = None
        self.__date = None
        self.__time = None
        self.__status = None


class ReservationManager:
    def __init__(self):
        self.__reservations = []


class Transaction:
    def __init__(self):
        self.__transaction_id = None
        self.__timestamp = None
        self.__customer = None
        self.__items = []
        self.__total_amount = 0.0


class AuditLog:
    def __init__(self):
        self.__log_id = None
        self.__timestamp = None
        self.__action = None
        self.__performed_by = None


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


class BoardGameCafeSystem:
    def __init__(self):
        self.__board_game_cafes = []
        self.__Persons = []


class BoardGameCafe:
    def __init__(self):
        self.__cafe_name = None
        self.__cafe_id = None
        self.__cafe_status = None
        self.__location = None
        self.__lobbies = []
        self.__board_games = []
        self.__menu_list = MenuList()
        self.__order_system = OrderSystem()
        self.__reservation_manager = ReservationManager()
        self.__managers = []
        self.__staffs = []
        self.__transactions = []
        self.__audit_logs = []


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


class Person:
    def __init__(self, _name: str, _id: str):
        self.__name = _name
        self.__user_id = _id

    def get_name(self):
        return self.__name

    def set_name(self, _name):
        if not isinstance(_name, str):
            raise ValueError("\t• ⚠️ \t- Name must be a string")
        self.__name = _name

    def get_user_id(self):
        return self.__user_id

    def set_user_id(self, _id):
        if not isinstance(_id, str):
            raise ValueError("\t• ⚠️ \t- User ID must be a string")
        self.__user_id = _id


class Owner(Person):
    def __init__(self, _name: str, _id: str):
        super().__init__(_name, _id)


class Manager(Person):
    def __init__(self, _name: str, _id: str):
        super().__init__(_name, _id)


class Staff(Person):
    def __init__(self, _name: str, _id: str):
        super().__init__(_name, _id)


class Reception(Staff):
    def __init__(self, _name: str, _id: str):
        super().__init__(_name, _id)


class Customer(Person):
    def __init__(self, _name: str, _id: str):
        super().__init__(_name, _id)
        self.__coupon = []
        self.__birth_date = ""
        self.__point = 0


class Member(Customer):
    def __init__(self, _name: str, _id: str):
        super().__init__(_name, _id)


class MemberSilver(Member):
    def __init__(self, _name: str, _id: str):
        super().__init__(_name, _id)


class MemberGold(Member):
    def __init__(self, _name: str, _id: str):
        super().__init__(_name, _id)


class MemberPlatinum(Member):
    def __init__(self, _name: str, _id: str):
        super().__init__(_name, _id)


class NonMember(Customer):
    def __init__(self, _name: str, _id: str):
        super().__init__(_name, _id)


class MenuList:
    def __init__(self):
        self.__items = []

    def item_add(self, _menu_item):
        self.__items.append(_menu_item)

    def item_remove(self, _menu_item):
        self.__items.remove(_menu_item)

    def get_item_by_id(self, _item_id):
        for item in self.__items:
            if item.get_item_id() == _item_id:
                return item
        return None

    def get_item_by_name(self, _name):
        for item in self.__items:
            if item.get_name() == _name:
                return item
        return None

    def get_all_items(self):
        return self.__items

    def get_all_food(self):
        item_list = []
        for item in self.__items:
            if item.__class__ is Food:
                item_list.append(item)
        return item_list

    def get_all_drink(self):
        item_list = []
        for item in self.__items:
            if item.__class__ is Drink:
                item_list.append(item)
        return item_list


class MenuItem:
    def __init__(self, _name: str, _item_id: str, _price: float):
        self.__name = _name
        self.__item_id = _item_id
        self.__price = _price

    def get_name(self):
        return self.__name

    def set_name(self, _name):
        if not isinstance(value, str):
            raise ValueError("\t• ⚠️ \t- Name must be a string")
        self._name = value

    def get_item_id(self):
        return self.__item_id

    def set_item_id(self, _item_id):
        if not isinstance(value, str):
            raise ValueError("\t• ⚠️ \t- Item ID must be a string")
        self._item_id = value

    def get_price(self):
        return self.__price

    def set_price(self, _price):
        if not isinstance(value, float):
            raise ValueError("\t• ⚠️ \t- Price must be a float")
        self._price = value


class Food(MenuItem):
    def __init__(self, _name: str, _item_id: str, _price: float):
        super().__init__(_name, _item_id, _price)


class Drink(MenuItem):
    def __init__(self, _name: str, _item_id: str, _price: float):
        super().__init__(_name, _item_id, _price)
