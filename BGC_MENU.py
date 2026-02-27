from abc import ABC, abstractmethod
from ENUM_STATUS import OrderStatus

# | ================================================================================================================================


class MenuItem(ABC):
    def __init__(self, item_id, name, price, is_available=None, description=""):
        self.__item_id = item_id
        self.__name = name
        self.__price = price
        self.__is_available = is_available
        self.__description = description

    # / ================================================================
    # - Getters
    # / ================================================================

    @property
    def item_id(self):
        return self.__item_id

    @property
    def name(self):
        return self.__name

    @property
    def price(self):
        return self.__price

    @property
    def is_available(self):
        return self.__is_available

    @property
    def description(self):
        return self.__description

    # / ================================================================
    # - Setters
    # / ================================================================

    @name.setter
    def name(self, name):
        self.__name = name

    @price.setter
    def price(self, price):
        self.__price = price

    @is_available.setter
    def availability(self, is_available):
        self.__is_available = is_available

    @description.setter
    def description(self, description):
        self.__description = description

    # / ================================================================
    # - Methods
    # / ================================================================

    # / ================================================================


# | ================================================================================================================================


class Food(MenuItem):
    __counter = 0

    def __init__(self, name, price, description="", is_available=None):
        temp_id = "FOOD-" + str(Food.__counter).zfill(5)
        Food.__counter += 1
        super().__init__(temp_id, name, price, is_available, description)

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


# | ================================================================================================================================


class Drink(MenuItem):
    __counter = 0

    def __init__(self, name, price, description="", is_available=None, cup_size="S"):
        temp_id = "DRNK-" + str(Drink.__counter).zfill(5)
        Drink.__counter += 1
        super().__init__(temp_id, name, price, is_available, description)
        self.__cup_size = cup_size

    # / ================================================================
    # - Getters
    # / ================================================================

    @property
    def cup_size(self):
        return self.__cup_size

    # / ================================================================
    # - Setters
    # / ================================================================

    @cup_size.setter
    def cup_size(self, cup_size):
        self.__cup_size = cup_size

    # / ================================================================
    # - Methods
    # / ================================================================

    # / ================================================================


# | ================================================================================================================================


class MenuList:
    def __init__(self):
        self.__menu_items = []

    # / ================================================================
    # - Getters
    # / ================================================================

    @property
    def menu_items(self):
        return self.__menu_items

    # / ================================================================
    # - Setters
    # / ================================================================

    # / ================================================================
    # - Methods
    # / ================================================================

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

    def get_menu_item_list(self):
        return self.__menu_items.copy()

    # / ================================================================


# | ================================================================================================================================


class Order:
    __counter = 0

    def __init__(self, menu_items):
        self.__order_id = "ODR-" + str(Order.__counter).zfill(5)
        Order.__counter += 1
        self.__menu_items = menu_items
        self.__status = OrderStatus.PENDING

    # / ================================================================
    # - Getters
    # / ================================================================

    @property
    def order_id(self):
        return self.__order_id

    @property
    def menu_items(self):
        return self.__menu_items

    @property
    def status(self):
        return self.__status

    @property
    def get_price(self):
        return self.__menu_items.price

    # / ================================================================
    # - Setters
    # / ================================================================

    @menu_items.setter
    def menu_items(self, menu_items):
        self.__menu_items = menu_items

    @status.setter
    def status(self, status):
        self.__status = status

    # / ================================================================
    # - Methods
    # / ================================================================

    # / ================================================================


# | ================================================================================================================================
