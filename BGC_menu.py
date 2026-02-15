"""
Board Game Cafe - Menu Management Module
Handles menu items, inventory, and ordering system.
"""

from typing import List, Optional, Dict
from datetime import datetime
from abc import ABC, abstractmethod


# ==========================================
# CONSTANTS
# ==========================================

MINIMUM_STOCK_ALERT_THRESHOLD = 5
DEFAULT_TAX_RATE = 0.07
CURRENCY_SYMBOL = "฿"


# ==========================================
# MENU ITEMS
# ==========================================

class MenuItem(ABC):
    def __init__(self, item_id: str, name: str, price: float, description: str = ""):
        if not item_id or not name:
            raise ValueError("Item ID and name cannot be empty")
        if price < 0:
            raise ValueError("Price cannot be negative")

        self._item_id = item_id
        self._name = name
        self._price = price
        self._description = description
        self._stock_level = 0
        self._is_available = True
        self._created_at = datetime.now()
        self._last_updated = datetime.now()

    @property
    def item_id(self) -> str:
        return self._item_id

    @property
    def name(self) -> str:
        return self._name

    @property
    def price(self) -> float:
        return self._price

    @property
    def description(self) -> str:
        return self._description

    @property
    def stock_level(self) -> int:
        return self._stock_level

    @property
    def is_available(self) -> bool:
        return self._is_available and self._stock_level > 0

    @property
    def created_at(self) -> datetime:
        return self._created_at

    @property
    def last_updated(self) -> datetime:
        return self._last_updated

    def set_price(self, new_price: float, approved_by: Optional[str] = None) -> None:
        if new_price < 0:
            raise ValueError("Price cannot be negative")

        self._price = new_price
        self._last_updated = datetime.now()

    def set_description(self, new_description: str) -> None:
        self._description = new_description
        self._last_updated = datetime.now()

    def set_stock_level(self, quantity: int, approved_by: Optional[str] = None) -> None:
        if quantity < 0:
            raise ValueError("Stock level cannot be negative")

        self._stock_level = quantity
        self._last_updated = datetime.now()

    def add_stock(self, quantity: int) -> None:
        if quantity <= 0:
            raise ValueError("Quantity to add must be positive")

        self._stock_level += quantity
        self._last_updated = datetime.now()

    def reduce_stock(self, quantity: int) -> None:
        if quantity <= 0:
            raise ValueError("Quantity to reduce must be positive")

        if quantity > self._stock_level:
            raise ValueError(
                f"Insufficient stock. Available: {self._stock_level}")

        self._stock_level -= quantity
        self._last_updated = datetime.now()

    def mark_unavailable(self) -> None:
        self._is_available = False
        self._last_updated = datetime.now()

    def mark_available(self) -> None:
        self._is_available = True
        self._last_updated = datetime.now()

    def is_low_stock(self) -> bool:
        return self._stock_level <= MINIMUM_STOCK_ALERT_THRESHOLD

    def get_formatted_price(self) -> str:
        return f"{CURRENCY_SYMBOL}{self._price:.2f}"

    @abstractmethod
    def get_category(self) -> str:
        pass


class Food(MenuItem):
    def __init__(self, item_id: str, name: str, price: float, description: str,
                 cuisine_type: str = "General", is_spicy: bool = False,
                 allergens: Optional[List[str]] = None):
        super().__init__(item_id, name, price, description)
        self._cuisine_type = cuisine_type
        self._is_spicy = is_spicy
        self._allergens = allergens or []

    @property
    def cuisine_type(self) -> str:
        return self._cuisine_type

    @property
    def is_spicy(self) -> bool:
        return self._is_spicy

    @property
    def allergens(self) -> List[str]:
        return self._allergens.copy()

    def get_category(self) -> str:
        return "Food"

    def add_allergen(self, allergen: str) -> None:
        if allergen not in self._allergens:
            self._allergens.append(allergen)
            self._last_updated = datetime.now()

    def remove_allergen(self, allergen: str) -> None:
        if allergen in self._allergens:
            self._allergens.remove(allergen)
            self._last_updated = datetime.now()


class Drink(MenuItem):
    def __init__(self, item_id: str, name: str, price: float, description: str,
                 size: str, is_alcoholic: bool = False,
                 temperature_options: Optional[List[str]] = None):
        super().__init__(item_id, name, price, description)
        self._size = size
        self._is_alcoholic = is_alcoholic
        self._temperature_options = temperature_options or [
            "Cold", "Room Temperature"]

    @property
    def size(self) -> str:
        return self._size

    @property
    def is_alcoholic(self) -> bool:
        return self._is_alcoholic

    @property
    def temperature_options(self) -> List[str]:
        return self._temperature_options.copy()

    def get_category(self) -> str:
        return "Drink"

    def add_temperature_option(self, option: str) -> None:
        if option not in self._temperature_options:
            self._temperature_options.append(option)
            self._last_updated = datetime.now()


class Snack(MenuItem):
    def __init__(self, item_id: str, name: str, price: float, description: str,
                 is_shareable: bool = True, serving_size: str = "Individual"):
        super().__init__(item_id, name, price, description)
        self._is_shareable = is_shareable
        self._serving_size = serving_size

    @property
    def is_shareable(self) -> bool:
        return self._is_shareable

    @property
    def serving_size(self) -> str:
        return self._serving_size

    def get_category(self) -> str:
        return "Snack"


# ==========================================
# MENU MANAGEMENT
# ==========================================

class MenuList:
    def __init__(self, menu_name: str = "Main Menu"):
        self._menu_name = menu_name
        self._items: List[MenuItem] = []
        self._created_at = datetime.now()

    @property
    def menu_name(self) -> str:
        return self._menu_name

    @property
    def item_count(self) -> int:
        return len(self._items)

    def add_item(self, item: MenuItem) -> None:
        for existing_item in self._items:
            if existing_item.item_id == item.item_id:
                raise ValueError(f"Item with ID {item.item_id} already exists")

        self._items.append(item)

    def remove_item(self, item_id: str) -> bool:
        for item in self._items:
            if item.item_id == item_id:
                self._items.remove(item)
                return True
        return False

    def get_item_by_id(self, item_id: str) -> Optional[MenuItem]:
        for item in self._items:
            if item.item_id == item_id:
                return item
        return None

    def get_item_by_name(self, name: str) -> Optional[MenuItem]:
        for item in self._items:
            if item.name.lower() == name.lower():
                return item
        return None

    def get_all_items(self) -> List[MenuItem]:
        return self._items.copy()

    def get_available_items(self) -> List[MenuItem]:
        return [item for item in self._items if item.is_available]

    def get_items_by_category(self, category: str) -> List[MenuItem]:
        return [item for item in self._items
                if item.get_category().lower() == category.lower()]

    def get_low_stock_items(self) -> List[MenuItem]:
        return [item for item in self._items if item.is_low_stock()]

    def search_items(self, query: str) -> List[MenuItem]:
        query_lower = query.lower()
        return [item for item in self._items
                if query_lower in item.name.lower() or
                query_lower in item.description.lower()]

    def get_menu_summary(self) -> Dict:
        available = [item for item in self._items if item.is_available]

        return {
            'total_items': len(self._items),
            'available_items': len(available),
            'food_items': len([i for i in self._items if i.get_category() == "Food"]),
            'drink_items': len([i for i in self._items if i.get_category() == "Drink"]),
            'snack_items': len([i for i in self._items if i.get_category() == "Snack"]),
            'low_stock_items': len(self.get_low_stock_items()),
            'average_price': sum(i.price for i in self._items) / len(self._items) if self._items else 0
        }


# ==========================================
# ORDER SYSTEM
# ==========================================

class Order:
    def __init__(self, order_id: str, customer, table=None):
        if not order_id:
            raise ValueError("Order ID cannot be empty")

        self._order_id = order_id
        self._customer = customer
        self._table = table
        self._created_at = datetime.now()
        self._status = "Open"

        self._items: List[Dict] = []
        self._discount_amount = 0.0
        self._tax_rate = DEFAULT_TAX_RATE
        self._notes = ""

    @property
    def order_id(self) -> str:
        return self._order_id

    @property
    def customer(self):
        return self._customer

    @property
    def table(self):
        return self._table

    @property
    def status(self) -> str:
        return self._status

    @property
    def items(self) -> List[Dict]:
        return self._items.copy()

    def add_item(self, menu_item, quantity: int, instructions: str = "") -> None:
        if self._status != "Open":
            raise ValueError("Cannot add items to a closed order")

        if quantity <= 0:
            raise ValueError("Quantity must be positive")

        if not menu_item.is_available:
            raise ValueError(f"Item {menu_item.name} is not available")

        item = {
            "item_id": menu_item.item_id,
            "name": menu_item.name,
            "price": menu_item.price,
            "quantity": quantity,
            "instructions": instructions,
            "status": "Pending",
            "timestamp": datetime.now()
        }

        self._items.append(item)

    def remove_item(self, item_id: str) -> None:
        if self._status != "Open":
            raise ValueError("Cannot remove items from closed order")

        self._items = [i for i in self._items if i["item_id"] != item_id]

    def mark_preparing(self, item_id: str) -> None:
        item = self._find_item(item_id)
        if item["status"] != "Pending":
            raise ValueError("Item not pending")
        item["status"] = "Preparing"

    def mark_served(self, item_id: str) -> None:
        item = self._find_item(item_id)
        if item["status"] != "Preparing":
            raise ValueError("Item not preparing")
        item["status"] = "Served"

    def cancel_item(self, item_id: str) -> None:
        item = self._find_item(item_id)
        if item["status"] == "Served":
            raise ValueError("Cannot cancel served item")
        item["status"] = "Cancelled"

    def _find_item(self, item_id: str) -> Dict:
        for item in self._items:
            if item["item_id"] == item_id:
                return item
        raise ValueError("Item not found in order")

    def calculate_subtotal(self) -> float:
        return sum(i["price"] * i["quantity"]
                   for i in self._items
                   if i["status"] != "Cancelled")

    def calculate_tax(self) -> float:
        return (self.calculate_subtotal() - self._discount_amount) * self._tax_rate

    def calculate_total(self) -> float:
        return self.calculate_subtotal() - self._discount_amount + self.calculate_tax()

    def apply_discount(self, amount: float) -> None:
        if amount < 0:
            raise ValueError("Discount cannot be negative")
        if amount > self.calculate_subtotal():
            raise ValueError("Discount cannot exceed subtotal")
        self._discount_amount = amount

    def close_order(self) -> None:
        self._status = "Closed"

    def cancel_order(self) -> None:
        for item in self._items:
            item["status"] = "Cancelled"
        self._status = "Cancelled"

    def all_items_served(self) -> bool:
        active_items = [i for i in self._items if i["status"] != "Cancelled"]
        return all(i["status"] == "Served" for i in active_items)

    def get_order_summary(self) -> Dict:
        return {
            "order_id": self._order_id,
            "customer": self._customer.name if self._customer else "Unknown",
            "table": self._table.table_id if self._table else None,
            "item_count": len(self._items),
            "subtotal": self.calculate_subtotal(),
            "discount": self._discount_amount,
            "tax": self.calculate_tax(),
            "total": self.calculate_total(),
            "status": self._status,
            "created_at": self._created_at.isoformat(),
            "all_served": self.all_items_served()
        }
