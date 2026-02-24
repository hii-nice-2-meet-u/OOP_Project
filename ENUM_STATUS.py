from enum import Enum


class MemberTier(Enum):
    BRONZE = "Bronze"
    SILVER = "Silver"
    GOLD = "Gold"
    NONE = "None"


class ReservationStatus(Enum):
    PENDING = "Pending"
    CANCELLED = "Cancelled"
    COMPLETED = "Completed"
    NO_SHOW = "No-Show"


class TableStatus(Enum):
    AVAILABLE = "Available"
    RESERVED = "Reserved"
    OCCUPIED = "Occupied"


class OrderStatus(Enum):
    PENDING = "Pending"
    PREPARING = "Preparing"
    SERVED = "Served"
    CANCELLED = "Cancelled"


class BoardGameStatus(Enum):
    AVAILABLE = "Available"
    IN_USE = "In-Use"
    MAINTENANCE = "Maintenance"
    UNAVAILABLE = "Unavailable"
