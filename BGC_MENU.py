import ENUM_STATUS


class MenuItem(ABC):
    def __init__(self, item_id, name, price, is_available=None, description=""):
        self.__item_id = item_id
        self.__name = name
        self.__price = price
        self.__is_available = is_available
        self.__description = description

    @property
    def item_id(self):
        return self.__item_id

    @item_id.setter
    def item_id(self, item_id):
        self.__item_id = item_id

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name):
        self.__name = name

    @property
    def price(self):
        return self.__price

    @price.setter
    def price(self, price):
        self.__price = price

    @property
    def is_available(self):
        return self.__is_available

    @is_available.setter
    def availability(self, is_available):
        self.__is_available = is_available

    @property
    def description(self):
        return self.__description

    @description.setter
    def description(self, description):
        self.__description = description


class Food(MenuItem):
    def __init__(self, item_id, name, price, description="", is_available=None):
        super().__init__(item_id, name, price, is_available, description)


class Drink(MenuItem):
    def __init__(
        self, item_id, name, price, description="", is_available=None, cup_size="S"
    ):
        super().__init__(item_id, name, price, is_available, description)
        self.__cup_size = cup_size

    @property
    def cup_size(self):
        return self.__cup_size

    @cup_size.setter
    def cup_size(self, cup_size):
        self.__cup_size = cup_size


class MenuList:
    def __init__(self):
        self.__menu_items = []

    def add_menu_item(self, menu_item):
        self.__menu_items.append(menu_item)

    def remove_menu_item(self, item_id):
        self.__menu_items = [
            item for item in self.__menu_items if item.item_id != item_id
        ]

    def get_menu_item(self, item_id):
        for item in self.__menu_items:
            if item.item_id == item_id:
                return item
        return None

    def list_menu_items(self):
        return self.__menu_items.copy()


class Order:
    __counter = 0

    def __init__(self, menu_items):
        self.__order_id = "ODR-" + str(Order.__counter).zfill(5)
        Order.__counter += 1
        self.__menu_items = menu_items
        self.__status = "Pending"

    @property
    def order_id(self):
        return self.__order_id

    @order_id.setter
    def order_id(self, order_id):
        self.__order_id = order_id

    @property
    def menu_items(self):
        return self.__menu_items
    @property
    def status(self):
        return self.__status
    @status.setter
    def status(self, status):
        self.__status = status
    @property
    def status(self):
        return self.__status

    @status.setter
    def status(self, status):
        self.__status = status
