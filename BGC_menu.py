from typing import List, Optional

class MenuItem:
    """
    Represents a generic item on the menu (Food or Drink).
    Uses strict private attributes.
    """
    def __init__(self, item_id: str, name: str, price: float, description: str = ""):
        self.__item_id = item_id
        self.__name = name
        self.__price = price
        self.__description = description

    # --- Getters ---
    def get_item_id(self) -> str:
        return self.__item_id

    def get_name(self) -> str:
        return self.__name

    def get_price(self) -> float:
        return self.__price

    def get_description(self) -> str:
        return self.__description

    # --- Setters ---
    def set_price(self, new_price: float):
        if new_price > 0:
            self.__price = new_price

class Food(MenuItem):
    """Subclass for Food items."""
    def __init__(self, item_id: str, name: str, price: float, description: str, calories: int, allergens: List[str]):
        super().__init__(item_id, name, price, description)
        self.__calories = calories
        self.__allergens = allergens

    def get_details(self) -> str:
        return f"[Food] {self.get_name()} ({self.__calories} kcal) - Allergens: {', '.join(self.__allergens)}"

class Drink(MenuItem):
    """Subclass for Drink items."""
    def __init__(self, item_id: str, name: str, price: float, description: str, size: str, is_alcoholic: bool):
        super().__init__(item_id, name, price, description)
        self.__size = size
        self.__is_alcoholic = is_alcoholic

    def get_details(self) -> str:
        algo_tag = "(Alcoholic)" if self.__is_alcoholic else ""
        return f"[Drink] {self.get_name()} [{self.__size}] {algo_tag}"

class MenuList:
    """Manages the collection of all menu items."""
    def __init__(self):
        self.__items: List[MenuItem] = []

    def add_item(self, item: MenuItem):
        self.__items.append(item)

    def remove_item(self, item_id: str):
        # Create a new list excluding the item with the given ID
        self.__items = [item for item in self.__items if item.get_item_id() != item_id]

    def get_item_by_id(self, item_id: str) -> Optional[MenuItem]:
        for item in self.__items:
            if item.get_item_id() == item_id:
                return item
        return None

    def get_all_items(self) -> List[MenuItem]:
        return self.__items