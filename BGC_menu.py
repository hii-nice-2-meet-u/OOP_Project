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
        if not isinstance(_name, str):
            raise ValueError("\t• ⚠️ \t- Name must be a string")
        self._name = _name

    def get_item_id(self):
        return self.__item_id

    def set_item_id(self, _item_id):
        if not isinstance(_item_id, str):
            raise ValueError("\t• ⚠️ \t- Item ID must be a string")
        self.__item_id = _item_id

    def get_price(self):
        return self.__price

    def set_price(self, _price):
        if not isinstance(_price, float):
            raise ValueError("\t• ⚠️ \t- Price must be a float")
        self.__price = _price


class Food(MenuItem):
    def __init__(self, _name: str, _item_id: str, _price: float):
        super().__init__(_name, _item_id, _price)


class Drink(MenuItem):
    def __init__(self, _name: str, _item_id: str, _price: float):
        super().__init__(_name, _item_id, _price)
