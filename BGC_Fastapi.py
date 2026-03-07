"""
Board Game Cafe - Staff API
FastAPI endpoints for staff operations including:
- Session management (check-in, check-out)
- Order management
- Board game management
- Table management
"""

from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum

from BGC_PAYMENT import CreditCard, Cash, OnlinePayment
from ENUM_STATUS import OrderStatus, TableStatus, BoardGameStatus
from system_instance import cafe_system

# ════════════════════════════════════════════════════════════════
# Initialize FastAPI App
# ════════════════════════════════════════════════════════════════

app = FastAPI(
    title="Board Game Cafe - Staff API",
    description="API for staff to manage cafe operations",
    version="1.0.0"
)

# ════════════════════════════════════════════════════════════════
# Pydantic Models
# ════════════════════════════════════════════════════════════════

class CheckInWalkInRequest(BaseModel):
    branch_id: str = Field(..., json_schema_extra={"example": "BRCH-00000"})
    total_players: int = Field(..., ge=1, json_schema_extra={"example": 4})
    table_id: Optional[str] = Field(None, json_schema_extra={"example": "TABLE-00000"})

class CheckInReservedRequest(BaseModel):
    reservation_id: str = Field(..., json_schema_extra={"example": "RESV-00000"})
    customer_id: str = Field(..., json_schema_extra={"example": "MEMBER-00000"})

class JoinSessionRequest(BaseModel):
    session_id: str = Field(..., json_schema_extra={"example": "PS-00000"})
    customer_id: Optional[str] = Field(None, json_schema_extra={"example": "MEMBER-00001"})

class BorrowBoardGameRequest(BaseModel):
    table_id: str = Field(..., json_schema_extra={"example": "TABLE-00000"})
    board_game_id: str = Field(..., json_schema_extra={"example": "BG-00000"})

class ReturnBoardGameRequest(BaseModel):
    table_id: str = Field(..., json_schema_extra={"example": "TABLE-00000"})
    board_game_id: str = Field(..., json_schema_extra={"example": "BG-00000"})
    is_damaged: bool = Field(False, json_schema_extra={"example": False})

class TakeOrderRequest(BaseModel):
    table_id: str = Field(..., json_schema_extra={"example": "TABLE-00000"})
    menu_item_id: str = Field(..., json_schema_extra={"example": "FOOD-00000"})

class UpdateOrderStatusRequest(BaseModel):
    session_id: str = Field(..., json_schema_extra={"example": "PS-00000"})
    order_id: str = Field(..., json_schema_extra={"example": "ORDER-00000"})

class PaymentMethodEnum(str, Enum):
    cash = "cash"
    card = "card"
    online = "online"

class CheckOutRequest(BaseModel):
    table_id: str = Field(..., json_schema_extra={"example": "TABLE-00000"})
    method_type: PaymentMethodEnum = Field(..., json_schema_extra={"example": "cash"})
    paid_amount: Optional[float] = Field(None, json_schema_extra={"example": 500.0})
    card_number: Optional[str] = Field(None, json_schema_extra={"example": "4111111111111111"})
    expiry_date: Optional[str] = Field(None, json_schema_extra={"example": "12/28"})
    cvv: Optional[str] = Field(None, json_schema_extra={"example": "123"})
    email: Optional[str] = Field(None, json_schema_extra={"example": "customer@example.com"})

class CreateTableRequest(BaseModel):
    branch_id: str = Field(..., json_schema_extra={"example": "BRCH-00000"})
    capacity: int = Field(..., ge=1, json_schema_extra={"example": 4})

class CreateBoardGameRequest(BaseModel):
    branch_id: str = Field(..., json_schema_extra={"example": "BRCH-00000"})
    name: str = Field(..., json_schema_extra={"example": "Uno"})
    genre: str = Field(..., json_schema_extra={"example": "Card Game"})
    price: float = Field(..., ge=0, json_schema_extra={"example": 100.0})
    min_players: int = Field(..., ge=1, json_schema_extra={"example": 2})
    max_players: int = Field(..., ge=1, json_schema_extra={"example": 10})
    description: str = Field("", json_schema_extra={"example": "A classic card game"})

class CreateMenuItemRequest(BaseModel):
    branch_id: str = Field(..., json_schema_extra={"example": "BRCH-00000"})
    name: str = Field(..., json_schema_extra={"example": "Pizza"})
    price: float = Field(..., ge=0, json_schema_extra={"example": 200.0})
    description: str = Field("", json_schema_extra={"example": "Delicious pizza"})
    item_type: str = Field(..., json_schema_extra={"example": "food"})  # "food" or "drink"
    cup_size: Optional[str] = Field("S", json_schema_extra={"example": "M"})  # For drinks only

# ════════════════════════════════════════════════════════════════
# Session Management Endpoints
# ════════════════════════════════════════════════════════════════

@app.post("/api/staff/sessions/check-in/walk-in", tags=["Session Management"])
async def check_in_walk_in(request: CheckInWalkInRequest):
    """
    Check in a walk-in customer to start a new play session.
    """
    try:
        play_session = cafe_system.check_in_walk_in(
            branch_id=request.branch_id,
            total_players=request.total_players,
            table_id=request.table_id
        )
        return {
            "success": True,
            "message": "Walk-in check-in successful",
            "data": {
                "session_id": play_session.session_id,
                "table_id": play_session.table_id,
                "start_time": str(play_session.start_time)
            }
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/staff/sessions/check-in/reserved", tags=["Session Management"])
async def check_in_reserved(request: CheckInReservedRequest):
    """
    Check in a customer with a reservation.
    """
    try:
        play_session = cafe_system.check_in_reserved(
            reservation_id=request.reservation_id,
            customer_id=request.customer_id
        )
        return {
            "success": True,
            "message": "Reserved check-in successful",
            "data": {
                "session_id": play_session.session_id,
                "table_id": play_session.table_id,
                "start_time": str(play_session.start_time),
                "reservation_id": request.reservation_id
            }
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/staff/sessions/join", tags=["Session Management"])
async def join_session(request: JoinSessionRequest):
    """
    Add a customer to an existing play session.
    """
    try:
        cafe_system.join_session(
            session_id=request.session_id,
            customer_id=request.customer_id
        )
        return {
            "success": True,
            "message": "Customer joined session successfully"
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/staff/sessions/active", tags=["Session Management"])
async def get_active_sessions(branch_id: Optional[str] = None):
    """
    Get all active play sessions, optionally filtered by branch.
    """
    try:
        branch = cafe_system.find_cafe_branch_by_id(branch_id) if branch_id else None
        if branch_id and not branch:
            raise ValueError("Branch not found")
        
        sessions = branch.get_play_sessions() if branch else cafe_system.get_play_sessions()
        
        return {
            "success": True,
            "data": [
                {
                    "session_id": ps.session_id,
                    "table_id": ps.table_id,
                    "start_time": str(ps.start_time),
                    "players": ps.current_players_id,
                    "board_games": ps.current_board_games_id,
                    "orders": [
                        {
                            "order_id": order.order_id,
                            "item": order.menu_items.name,
                            "status": order.status.value
                        } for order in ps.current_order
                    ]
                } for ps in sessions
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) 

@app.get("/api/staff/sessions/{session_id}", tags=["Session Management"])
async def get_session_details(session_id: str):
    """
    Get detailed information about a specific play session.
    """
    try:
        branch = cafe_system.find_cafe_branch_by_id(session_id)
        if not branch:
            raise ValueError("Session not found")
        
        play_session = branch.find_play_session_by_id(session_id)
        if not play_session:
            raise ValueError("Session not found")
        
        return {
            "success": True,
            "data": {
                "session_id": play_session.session_id,
                "table_id": play_session.table_id,
                "start_time": str(play_session.start_time),
                "end_time": str(play_session.end_time) if play_session.end_time else None,
                "players": play_session.current_players_id,
                "board_games": play_session.current_board_games_id,
                "penalties": play_session.game_penalty,
                "orders": [
                    {
                        "order_id": order.order_id,
                        "item_id": order.menu_items.item_id,
                        "item_name": order.menu_items.name,
                        "price": order.menu_items.price,
                        "status": order.status.value
                    } for order in play_session.current_order
                ],
                "payment": {
                    "payment_id": play_session.payment.payment_id,
                    "amount": play_session.payment.amount,
                    "method": play_session.payment.payment_method.__class__.__name__,
                    "processed": play_session.payment.process_payment
                } if play_session.payment else None
            }
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# ════════════════════════════════════════════════════════════════
# Board Game Management
# ════════════════════════════════════════════════════════════════

@app.post("/api/staff/board-games/borrow", tags=["Board Game Management"])
async def borrow_board_game(request: BorrowBoardGameRequest):
    """
    Lend a board game to a table.
    """
    try:
        cafe_system.borrow_board_game(
            table_id=request.table_id,
            board_game_id=request.board_game_id
        )
        return {
            "success": True,
            "message": "Board game borrowed successfully"
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/staff/board-games/return", tags=["Board Game Management"])
async def return_board_game(request: ReturnBoardGameRequest):
    """
    Return a board game from a table.
    """
    try:
        cafe_system.return_board_game(
            table_id=request.table_id,
            board_game_id=request.board_game_id,
            is_damaged=request.is_damaged
        )
        return {
            "success": True,
            "message": "Board game returned successfully",
            "penalty_applied": request.is_damaged
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/staff/board-games", tags=["Board Game Management"])
async def get_board_games(
    branch_id: str,
    status: Optional[str] = None,
    min_players: Optional[int] = None
):
    """
    Get list of board games, optionally filtered by status and minimum players.
    """
    try:
        branch = cafe_system.find_cafe_branch_by_id(branch_id)
        if not branch:
            raise ValueError("Branch not found")
        
        games = branch.get_board_games()
        
        # Apply filters
        if status:
            games = [g for g in games if g.status.value == status]
        if min_players:
            games = [g for g in games if g.min_players <= min_players]
        
        return {
            "success": True,
            "data": [
                {
                    "game_id": game.game_id,
                    "name": game.name,
                    "genre": game.genre,
                    "price": game.price,
                    "status": game.status.value,
                    "min_players": game.min_players,
                    "max_players": game.max_players,
                    "description": game.description
                } for game in games
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/staff/board-games", tags=["Board Game Management"])
async def create_board_game(request: CreateBoardGameRequest):
    """
    Create a new board game in the system.
    """
    try:
        game = cafe_system.create_board_game_to_branch(
            branch_id=request.branch_id,
            name=request.name,
            genre=request.genre,
            price=request.price,
            min_players=request.min_players,
            max_players=request.max_players,
            description=request.description
        )
        return {
            "success": True,
            "message": "Board game created successfully",
            "data": {
                "game_id": game.game_id,
                "name": game.name
            }
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# ════════════════════════════════════════════════════════════════
# Order Management
# ════════════════════════════════════════════════════════════════

@app.post("/api/staff/orders/take", tags=["Order Management"])
async def take_order(request: TakeOrderRequest):
    """
    Take an order for a table.
    """
    try:
        cafe_system.take_order(
            table_id=request.table_id,
            menu_item_id=request.menu_item_id
        )
        return {
            "success": True,
            "message": "Order taken successfully"
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.patch("/api/staff/orders/preparing", tags=["Order Management"])
async def update_order_preparing(request: UpdateOrderStatusRequest):
    """
    Update order status to PREPARING.
    """
    try:
        cafe_system.update_order_preparing(
            session_id=request.session_id,
            order_id=request.order_id
        )
        return {
            "success": True,
            "message": "Order status updated to PREPARING"
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.patch("/api/staff/orders/serve", tags=["Order Management"])
async def update_order_serve(request: UpdateOrderStatusRequest):
    """
    Update order status to SERVED.
    """
    try:
        cafe_system.update_order_serve(
            session_id=request.session_id,
            order_id=request.order_id
        )
        return {
            "success": True,
            "message": "Order status updated to SERVED"
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/staff/orders/pending", tags=["Order Management"])
async def get_pending_orders(branch_id: Optional[str] = None):
    """
    Get all pending orders, optionally filtered by branch.
    """
    try:
        if branch_id:
            branch = cafe_system.find_cafe_branch_by_id(branch_id)
            if not branch:
                raise ValueError("Branch not found")
            pending_orders = branch.get_pending_orders()
        else:
            # Get pending orders from all branches
            pending_orders = []
            for branch in cafe_system.cafe_branches:
                pending_orders.extend(branch.get_pending_orders())
        
        return {
            "success": True,
            "data": [
                {
                    "order_id": order.order_id,
                    "item_name": order.menu_items.name,
                    "price": order.menu_items.price,
                    "status": order.status.value
                } for order in pending_orders
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# ════════════════════════════════════════════════════════════════
# Payment & Checkout
# ════════════════════════════════════════════════════════════════

@app.post("/api/staff/checkout", tags=["Payment"])
async def checkout(request: CheckOutRequest):
    """
    Process checkout for a table.
    """
    try:
        payment = cafe_system.check_out(
            table_id=request.table_id,
            method_type=request.method_type.value,
            paid_amount=request.paid_amount,
            card_number=request.card_number,
            expiry_date=request.expiry_date,
            cvv=request.cvv,
            email=request.email
        )
        
        result = {
            "success": True,
            "message": "Checkout successful",
            "data": {
                "payment_id": payment.payment_id,
                "amount": payment.amount,
                "method": payment.payment_method.__class__.__name__,
                "time": str(payment.payment_time)
            }
        }
        
        # Add change if cash payment
        if request.method_type == PaymentMethodEnum.cash and hasattr(payment.payment_method, 'change'):
            result["data"]["change"] = payment.payment_method.change
        
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# ════════════════════════════════════════════════════════════════
# Table Management
# ════════════════════════════════════════════════════════════════

@app.get("/api/staff/tables", tags=["Table Management"])
async def get_tables(
    branch_id: str,
    status: Optional[str] = None,
    min_capacity: Optional[int] = None
):
    """
    Get all tables in a branch, optionally filtered by status and capacity.
    """
    try:
        branch = cafe_system.find_cafe_branch_by_id(branch_id)
        if not branch:
            raise ValueError("Branch not found")
        
        tables = branch.get_tables()
        
        # Apply filters
        if status:
            tables = [t for t in tables if t.status.value == status]
        if min_capacity:
            tables = [t for t in tables if t.capacity >= min_capacity]
        
        return {
            "success": True,
            "data": [
                {
                    "table_id": table.table_id,
                    "capacity": table.capacity,
                    "status": table.status.value
                } for table in tables
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/staff/tables", tags=["Table Management"])
async def create_table(request: CreateTableRequest):
    """
    Create a new table in a branch.
    """
    try:
        table = cafe_system.create_table_to_branch(
            branch_id=request.branch_id,
            capacity=request.capacity
        )
        return {
            "success": True,
            "message": "Table created successfully",
            "data": {
                "table_id": table.table_id,
                "capacity": table.capacity,
                "status": table.status.value
            }
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# ════════════════════════════════════════════════════════════════
# Menu Management
# ════════════════════════════════════════════════════════════════

@app.get("/api/staff/menu", tags=["Menu Management"])
async def get_menu(branch_id: str):
    """
    Get the menu for a specific branch.
    """
    try:
        branch = cafe_system.find_cafe_branch_by_id(branch_id)
        if not branch:
            raise ValueError("Branch not found")
        
        menu_items = branch.get_menu_item()
        
        return {
            "success": True,
            "data": {
                "food": [
                    {
                        "item_id": item.item_id,
                        "name": item.name,
                        "price": item.price,
                        "description": item.description,
                        "available": item.is_available
                    } for item in menu_items if item.get_category() == "Food"
                ],
                "drinks": [
                    {
                        "item_id": item.item_id,
                        "name": item.name,
                        "price": item.price,
                        "description": item.description,
                        "available": item.is_available
                    } for item in menu_items if item.get_category() == "Drink"
                ]
            }
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/staff/menu", tags=["Menu Management"])
async def create_menu_item(request: CreateMenuItemRequest):
    """
    Create a new menu item.
    """
    try:
        if request.item_type.lower() == "food":
            item = cafe_system.create_menu_item_food_to_branch(
                branch_id=request.branch_id,
                name=request.name,
                price=request.price,
                description=request.description
            )
        elif request.item_type.lower() == "drink":
            item = cafe_system.create_menu_item_drink_to_branch(
                branch_id=request.branch_id,
                name=request.name,
                price=request.price,
                description=request.description
            )
        else:
            raise ValueError("item_type must be 'food' or 'drink'")
        
        return {
            "success": True,
            "message": "Menu item created successfully",
            "data": {
                "item_id": item.item_id,
                "name": item.name,
                "price": item.price
            }
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# ════════════════════════════════════════════════════════════════
# Reservation Management
# ════════════════════════════════════════════════════════════════

@app.get("/api/staff/reservations", tags=["Reservation Management"])
async def get_reservations(
    branch_id: Optional[str] = None,
    status: Optional[str] = None,
    date: Optional[str] = None
):
    """
    Get all reservations, optionally filtered.
    """
    try:
        reservations = cafe_system.reservations
        
        # Apply filters
        if branch_id:
            reservations = [r for r in reservations if r.branch_id == branch_id]
        if status:
            reservations = [r for r in reservations if r.status.value == status]
        if date:
            reservations = [r for r in reservations if r.date == date]
        
        return {
            "success": True,
            "data": [
                {
                    "reservation_id": resv.reservation_id,
                    "customer_id": resv.customer_id,
                    "branch_id": resv.branch_id,
                    "table_id": resv.table_id,
                    "date": resv.date,
                    "start_time": resv.start_time,
                    "end_time": resv.end_time,
                    "status": resv.status.value
                } for resv in reservations
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# ════════════════════════════════════════════════════════════════
# Health Check
# ════════════════════════════════════════════════════════════════

@app.get("/", tags=["System"])
async def root():
    """
    Health check endpoint.
    """
    return {
        "message": "Board Game Cafe - Staff API",
        "status": "running",
        "version": "1.0.0"
    }

@app.get("/api/health", tags=["System"])
async def health_check():
    """
    Detailed health check.
    """
    return {
        "status": "healthy",
        "timestamp": str(datetime.now()),
        "branches": len(cafe_system.cafe_branches),
        "active_sessions": sum(len(b.get_play_sessions()) for b in cafe_system.cafe_branches)
    }

# ════════════════════════════════════════════════════════════════
# Run the application
# ════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)