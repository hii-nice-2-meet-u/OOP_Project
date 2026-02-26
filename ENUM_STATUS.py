from enum import Enum


class MemberTier(Enum):
    NONE_TIER = "None"
    BRONZE = "Bronze"
    SILVER = "Silver"
    GOLD = "Gold"
    PLATINUM = "Platinum"


class ReservationStatus(Enum):
    PENDING = "Pending"
    CANCELLED = "Cancelled"
    COMPLETED = "Completed"
    NO_SHOW = "No-Show"


class TableStatus(Enum):
    AVAILABLE = "Available"
    RESERVED = "Reserved"
    OCCUPIED = "Occupied"
    MAINTENANCE = "Maintenance"


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
