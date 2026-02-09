import BGC_menu


class Registration:
    def __init__(self):
        self.__registration_id = None
        self.__timestamp = None
        self.__customer = None
        self.__status = None


class Payment:
    def __init__(self, amount):
        self.__amount = amount
        self.__status = "Pending"

    def process_payment(self):
        raise NotImplementedError


class Cash(Payment):
    def process_payment(self):
        self._Payment__status = "Success"
        return True


class Card(Payment):
    def process_payment(self):
        self._Payment__status = "Success"
        return True


class OnlinePayment(Payment):
    def process_payment(self):
        self._Payment__status = "Success"
        return True

from datetime import datetime, timedelta


class Reservation:
    def __init__(self, reservation_id, customer, table, start_time, end_time, pax):
        self.__reservation_id = reservation_id
        self.__customer = customer
        self.__table = table
        self.__start_time = start_time
        self.__end_time = end_time
        self.__pax = pax
        self.__deposit_amount = 0.0
        self.__status = "Pending"

    def pay_deposit(self, amount):
        self.__deposit_amount = amount
        self.__status = "Confirmed"

    def check_in(self):
        self.__status = "Checked-In"
        self.__table.set_status("Occupied")

    def cancel(self):
        self.__status = "Cancelled"

    def mark_no_show(self):
        self.__status = "No-show"

    # getters
    def get_status(self):
        return self.__status

    def get_table(self):
        return self.__table

class ReservationManager:
    def __init__(self):
        self.__reservations = []

    def create_reservation(self, reservation):
        self.__reservations.append(reservation)
        return reservation

    def check_availability(self, table):
        for r in self.__reservations:
            if r.get_table() == table and r.get_status() in ["Confirmed", "Checked-In"]:
                return False
        return True

    def cancel_reservation(self, reservation):
        reservation.cancel()

    def process_no_show(self, reservation):
        reservation.mark_no_show()


class Transaction:
    def __init__(self):
        self.__transaction_id = None
        self.__timestamp = None
        self.__customer = None
        self.__items = []
        self.__total_amount = 0.0


class AuditLog:
    def __init__(self, log_id, event_code, ref_id, actor):
        self.__log_id = log_id
        self.__event_code = event_code
        self.__ref_id = ref_id
        self.__actor = actor
        self.__timestamp = datetime.now()


class OrderSystem:
    def __init__(self):
        self.__orders = []

    def create_order(self, customer, table):
        order_id = f"ORD-{len(self.__orders)+1}"
        order = Order(order_id, customer, table)
        self.__orders.append(order)
        return order

class Order:
    def __init__(self, order_id, customer, table):
        self.__order_id = order_id
        self.__customer = customer
        self.__table = table
        self.__items = []
        self.__total_amount = 0.0

    def add_item(self, item: MenuItem, qty: int):
        for _ in range(qty):
            self.__items.append(item)
            self.__total_amount += item.get_price()

    def calculate_total(self):
        return self.__total_amount

    def get_total(self):
        return self.__total_amount


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
    def __init__(self, table_id, capacity):
        self.__table_id = table_id
        self.__capacity = capacity
        self.__status = "Available"
        self.__board_games = []

    def set_status(self, status):
        self.__status = status

    def assign_board_game(self, game):
        self.__board_games.append(game)
        game.set_status("In-Play")

    def clear_table(self):
        self.__board_games.clear()
        self.__status = "Available"


class BoardGame:
    def __init__(self, name, item_id):
        self.__name = name
        self.__item_id = item_id
        self.__status = "Available"

    def set_status(self, status):
        self.__status = status

    def get_status(self):
        return self.__status

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
