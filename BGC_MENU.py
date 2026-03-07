from abc import ABC, abstractmethod

from ENUM_STATUS import OrderStatus

# | ════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
# | #EFFF11


class MenuItem(ABC):
    def __init__(self, item_id, name, price, is_available=None, description=""):
        self.__item_id = item_id
        self.__name = name
        self.__price = price
        self.__is_available = is_available
        self.__description = description

    # / ════════════════════════════════════════════════════════════════
    # - Getters
    # / ════════════════════════════════════════════════════════════════

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

    # / ════════════════════════════════════════════════════════════════
    # - Setters
    # / ════════════════════════════════════════════════════════════════

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

    # / ════════════════════════════════════════════════════════════════
    # - Methods
    # / ════════════════════════════════════════════════════════════════

    # / ════════════════════════════════════════════════════════════════


# | ════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
# | #EFFF11


class Food(MenuItem):
    __counter = 0

    def __init__(self, name, price, description="", is_available=None):
        temp_id = "FOOD-" + str(Food.__counter).zfill(5)
        Food.__counter += 1
        super().__init__(temp_id, name, price, is_available, description)

    # / ════════════════════════════════════════════════════════════════
    # - Getters
    # / ════════════════════════════════════════════════════════════════

    # / ════════════════════════════════════════════════════════════════
    # - Setters
    # / ════════════════════════════════════════════════════════════════

    # / ════════════════════════════════════════════════════════════════
    # - Methods
    # / ════════════════════════════════════════════════════════════════

    # / ════════════════════════════════════════════════════════════════


# | ════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
# | #EFFF11


class Drink(MenuItem):
    __counter = 0

    def __init__(self, name, price, description="", is_available=None, cup_size="S"):
        temp_id = "DRINK-" + str(Drink.__counter).zfill(5)
        Drink.__counter += 1
        super().__init__(temp_id, name, price, is_available, description)
        self.__cup_size = cup_size

    # / ════════════════════════════════════════════════════════════════
    # - Getters
    # / ════════════════════════════════════════════════════════════════

    @property
    def cup_size(self):
        return self.__cup_size

    # / ════════════════════════════════════════════════════════════════
    # - Setters
    # / ════════════════════════════════════════════════════════════════

    @cup_size.setter
    def cup_size(self, cup_size):
        self.__cup_size = cup_size

    # / ════════════════════════════════════════════════════════════════
    # - Methods
    # / ════════════════════════════════════════════════════════════════

    # / ================================================================


# | ================================================================================================================================
# | #EFFF11


class MenuList:
    def __init__(self):
        self.__menu_items = []

    # / ================================================================
    # - Getters
    # / ================================================================

    @property
    def menu_items(self):
        return self.__menu_items.copy()

    # / ================================================================
    # - Setters
    # / ================================================================

    # / ================================================================
    # - Methods
    # / ================================================================

    def add_menu_item(self, menu_item):
        if not isinstance(menu_item, MenuItem):
            raise ValueError("Invalid menu item")
        self.__menu_items.append(menu_item)

    def get_menu_item(self, item_id):
        for item in self.__menu_items:
            if item.item_id == item_id:
                return item
        return None

    def get_menu_item_food(self):
        return [item for item in self.__menu_items if isinstance(item, Food)]

    def get_menu_item_drink(self):
        return [item for item in self.__menu_items if isinstance(item, Drink)]

    def get_menu_item_list(self):
        return self.__menu_items.copy()

    def find_menu_item_by_id(self, item_id):
        for item in self.__menu_items:
            if item.item_id == item_id:
                return item
        return None

    def remove_menu_item(self, item_id):
        self.__menu_items = [
            item for item in self.__menu_items if item.item_id != item_id
        ]

    # / ================================================================


# | ================================================================================================================================
# | #EFFF11


class Order:
    __counter = 0

    def __init__(self, menu_items):
        self.__order_id = "ORDER-" + str(Order.__counter).zfill(5)
        Order.__counter += 1
        self.__menu_items = menu_items
        self.__status = OrderStatus.PENDING

    # / ════════════════════════════════════════════════════════════════
    # - Getters
    # / ════════════════════════════════════════════════════════════════

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

    # / ════════════════════════════════════════════════════════════════
    # - Setters
    # / ════════════════════════════════════════════════════════════════

    @status.setter
    def status(self, status):
        self.__status = status

    # / ════════════════════════════════════════════════════════════════
    # - Methods
    # / ════════════════════════════════════════════════════════════════

    def set_order_status(self, status):
        self.__status = status

    def set_order_preparing(self):
        self.__status = OrderStatus.CANCELLED

    def set_order_serve(self):
        self.__status = OrderStatus.SERVED

    def set_order_cancel(self):
        self.__status = OrderStatus.CANCELLED

    # / ════════════════════════════════════════════════════════════════


# | ════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
