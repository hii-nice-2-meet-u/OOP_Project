"""
Board Game Cafe - Customer MCP Server
FastMCP server for customer operations including:
- Browsing branches, menus, and board games
- Making and managing reservations
- Member profile management
"""

from mcp.server.fastmcp import FastMCP
from datetime import datetime, timedelta
from typing import Optional, List, Dict, Any

from ENUM_STATUS import MemberTier, ReservationStatus
from system_instance import cafe_system

# ════════════════════════════════════════════════════════════════
# Initialize FastMCP Server
# ════════════════════════════════════════════════════════════════

mcp = FastMCP("Board Game Cafe - Customer")

# ════════════════════════════════════════════════════════════════
# Browse Functions
# ════════════════════════════════════════════════════════════════

@mcp.tool()
def list_branches() -> Dict[str, Any]:
    """
    Get list of all cafe branches with basic information.
    
    Returns:
        Dictionary containing list of branches with their details
    """
    try:
        branches = cafe_system.cafe_branches
        
        return {
            "success": True,
            "total_branches": len(branches),
            "branches": [
                {
                    "branch_id": branch.branch_id,
                    "name": branch.name,
                    "location": branch.location,
                    "total_tables": len(branch.get_tables()),
                    "available_tables": len([t for t in branch.get_tables() if t.status.value == "Available"])
                } for branch in branches
            ]
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


@mcp.tool()
def get_branch_details(branch_id: str) -> Dict[str, Any]:
    """
    Get detailed information about a specific branch.
    
    Args:
        branch_id: The ID of the branch (e.g., "BRCH-00000")
    
    Returns:
        Dictionary containing branch details including tables, games, and menu
    """
    try:
        branch = cafe_system.find_cafe_branch_by_id(branch_id)
        if not branch:
            return {"success": False, "error": "Branch not found"}
        
        return {
            "success": True,
            "branch": {
                "branch_id": branch.branch_id,
                "name": branch.name,
                "location": branch.location,
                "tables": [
                    {
                        "table_id": table.table_id,
                        "capacity": table.capacity,
                        "status": table.status.value,
                        "price_per_hour": table.price_per_hour
                    } for table in branch.get_tables()
                ],
                "total_board_games": len(branch.get_board_games()),
                "available_board_games": len([g for g in branch.get_board_games() if g.status.value == "Available"]),
                "menu_items_count": len(branch.get_menu_item())
            }
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


@mcp.tool()
def check_table_availability(
    branch_id: str,
    date: str,
    start_time: str,
    end_time: str,
    total_players: int
) -> Dict[str, Any]:
    """
    Check if tables are available for a specific date and time.
    
    Args:
        branch_id: The ID of the branch (e.g., "BRCH-00000")
        date: Date in YYYY-MM-DD format (e.g., "2026-03-15")
        start_time: Start time in HH:MM format (e.g., "14:00")
        end_time: End time in HH:MM format (e.g., "16:00")
        total_players: Number of players
    
    Returns:
        Dictionary containing availability status and available tables
    """
    try:
        branch = cafe_system.find_cafe_branch_by_id(branch_id)
        if not branch:
            return {"success": False, "error": "Branch not found"}
        
        # Get tables with sufficient capacity
        available_tables = branch.find_available_tables(total_players)
        
        # Filter out tables with conflicting reservations
        available_for_slot = []
        for table in available_tables:
            has_conflict = False
            for resv in cafe_system.reservations:
                if (resv.table_id == table.table_id and 
                    resv.date == date and
                    resv.status == ReservationStatus.PENDING):
                    # Check time overlap
                    if not (end_time <= resv.start_time or start_time >= resv.end_time):
                        has_conflict = True
                        break
            
            if not has_conflict:
                available_for_slot.append(table)
        
        return {
            "success": True,
            "available": len(available_for_slot) > 0,
            "date": date,
            "start_time": start_time,
            "end_time": end_time,
            "total_players": total_players,
            "available_tables": [
                {
                    "table_id": table.table_id,
                    "capacity": table.capacity,
                    "price_per_hour": table.price_per_hour
                } for table in available_for_slot
            ]
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


@mcp.tool()
def view_menu(branch_id: str) -> Dict[str, Any]:
    """
    View the menu for a specific branch.
    
    Args:
        branch_id: The ID of the branch (e.g., "BRCH-00000")
    
    Returns:
        Dictionary containing food and drink menu items
    """
    try:
        branch = cafe_system.find_cafe_branch_by_id(branch_id)
        if not branch:
            return {"success": False, "error": "Branch not found"}
        
        menu_items = branch.get_menu_item()
        
        return {
            "success": True,
            "branch_id": branch_id,
            "branch_name": branch.name,
            "menu": {
                "food": [
                    {
                        "item_id": item.item_id,
                        "name": item.name,
                        "price": f"฿{item.price:.2f}",
                        "description": item.description,
                        "available": item.is_available if item.is_available is not None else True
                    } for item in menu_items if item.get_category() == "Food"
                ],
                "drinks": [
                    {
                        "item_id": item.item_id,
                        "name": item.name,
                        "price": f"฿{item.price:.2f}",
                        "description": item.description,
                        "available": item.is_available if item.is_available is not None else True
                    } for item in menu_items if item.get_category() == "Drink"
                ]
            }
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


@mcp.tool()
def browse_board_games(
    branch_id: str,
    genre: Optional[str] = None,
    min_players: Optional[int] = None,
    max_players: Optional[int] = None,
    available_only: bool = True
) -> Dict[str, Any]:
    """
    Browse board games available at a branch.
    
    Args:
        branch_id: The ID of the branch (e.g., "BRCH-00000")
        genre: Filter by genre (optional)
        min_players: Filter by minimum players (optional)
        max_players: Filter by maximum players (optional)
        available_only: Show only available games (default: True)
    
    Returns:
        Dictionary containing list of board games
    """
    try:
        branch = cafe_system.find_cafe_branch_by_id(branch_id)
        if not branch:
            return {"success": False, "error": "Branch not found"}
        
        games = branch.get_board_games()
        
        # Apply filters
        if available_only:
            games = [g for g in games if g.status.value == "Available"]
        if genre:
            games = [g for g in games if genre.lower() in g.genre.lower()]
        if min_players:
            games = [g for g in games if g.min_players <= min_players]
        if max_players:
            games = [g for g in games if g.max_players >= max_players]
        
        return {
            "success": True,
            "total_games": len(games),
            "games": [
                {
                    "game_id": game.game_id,
                    "name": game.name,
                    "genre": game.genre,
                    "rental_price": f"฿{game.price:.2f}",
                    "players": f"{game.min_players}-{game.max_players}",
                    "description": game.description,
                    "status": game.status.value
                } for game in games
            ]
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


@mcp.tool()
def get_board_game_details(branch_id: str, game_id: str) -> Dict[str, Any]:
    """
    Get detailed information about a specific board game.
    
    Args:
        branch_id: The ID of the branch (e.g., "BRCH-00000")
        game_id: The ID of the board game (e.g., "BG-00000")
    
    Returns:
        Dictionary containing board game details
    """
    try:
        branch = cafe_system.find_cafe_branch_by_id(branch_id)
        if not branch:
            return {"success": False, "error": "Branch not found"}
        
        game = branch.find_board_game_by_id(game_id)
        if not game:
            return {"success": False, "error": "Board game not found"}
        
        return {
            "success": True,
            "game": {
                "game_id": game.game_id,
                "name": game.name,
                "genre": game.genre,
                "rental_price": f"฿{game.price:.2f}",
                "min_players": game.min_players,
                "max_players": game.max_players,
                "description": game.description,
                "status": game.status.value,
                "available": game.status.value == "Available"
            }
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


# ════════════════════════════════════════════════════════════════
# Reservation Functions
# ════════════════════════════════════════════════════════════════

@mcp.tool()
def make_reservation(
    customer_id: str,
    branch_id: str,
    total_players: int,
    date: str,
    start_time: str,
    end_time: str,
    table_id: str = "auto"
) -> Dict[str, Any]:
    """
    Create a new table reservation.
    
    Args:
        customer_id: The customer's member ID (e.g., "MEMBER-00000")
        branch_id: The branch ID (e.g., "BRCH-00000")
        total_players: Number of players
        date: Reservation date in YYYY-MM-DD format (e.g., "2026-03-15")
        start_time: Start time in HH:MM format (e.g., "14:00")
        end_time: End time in HH:MM format (e.g., "16:00")
        table_id: Specific table ID or "auto" for automatic assignment
    
    Returns:
        Dictionary containing reservation details
    """
    try:
        reservation = cafe_system.make_reservation(
            customer_id=customer_id,
            branch_id=branch_id,
            total_players=total_players,
            date=date,
            start_time=start_time,
            end_time=end_time,
            table_id=table_id
        )
        
        return {
            "success": True,
            "message": "Reservation created successfully",
            "reservation": {
                "reservation_id": reservation.reservation_id,
                "customer_id": reservation.customer_id,
                "branch_id": reservation.branch_id,
                "table_id": reservation.table_id,
                "date": reservation.date,
                "start_time": reservation.start_time,
                "end_time": reservation.end_time,
                "status": reservation.status.value,
                "created_at": str(reservation.current_reservation_date)
            }
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


@mcp.tool()
def view_my_reservations(
    customer_id: str,
    status: Optional[str] = None,
    upcoming_only: bool = False
) -> Dict[str, Any]:
    """
    View all reservations for a specific customer.
    
    Args:
        customer_id: The customer's member ID (e.g., "MEMBER-00000")
        status: Filter by status (optional): "Pending", "Completed", "Cancelled", "No-Show"
        upcoming_only: Show only upcoming reservations (default: False)
    
    Returns:
        Dictionary containing list of reservations
    """
    try:
        reservations = [r for r in cafe_system.reservations if r.customer_id == customer_id]
        
        # Apply filters
        if status:
            reservations = [r for r in reservations if r.status.value == status]
        
        if upcoming_only:
            today = datetime.now().date()
            reservations = [r for r in reservations 
                          if datetime.strptime(r.date, "%Y-%m-%d").date() >= today
                          and r.status == ReservationStatus.PENDING]
        
        return {
            "success": True,
            "total_reservations": len(reservations),
            "reservations": [
                {
                    "reservation_id": resv.reservation_id,
                    "branch_id": resv.branch_id,
                    "table_id": resv.table_id,
                    "date": resv.date,
                    "start_time": resv.start_time,
                    "end_time": resv.end_time,
                    "status": resv.status.value,
                    "created_at": str(resv.current_reservation_date)
                } for resv in reservations
            ]
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


@mcp.tool()
def get_reservation_details(reservation_id: str) -> Dict[str, Any]:
    """
    Get detailed information about a specific reservation.
    
    Args:
        reservation_id: The reservation ID (e.g., "RESV-00000")
    
    Returns:
        Dictionary containing reservation details
    """
    try:
        reservation = None
        for resv in cafe_system.reservations:
            if resv.reservation_id == reservation_id:
                reservation = resv
                break
        
        if not reservation:
            return {"success": False, "error": "Reservation not found"}
        
        # Get branch details
        branch = cafe_system.find_cafe_branch_by_id(reservation.branch_id)
        branch_name = branch.name if branch else "Unknown"
        
        # Get table details
        table = None
        if branch:
            table = branch.find_table_by_id(reservation.table_id)
        
        return {
            "success": True,
            "reservation": {
                "reservation_id": reservation.reservation_id,
                "customer_id": reservation.customer_id,
                "branch_id": reservation.branch_id,
                "branch_name": branch_name,
                "table_id": reservation.table_id,
                "table_capacity": table.capacity if table else None,
                "date": reservation.date,
                "start_time": reservation.start_time,
                "end_time": reservation.end_time,
                "status": reservation.status.value,
                "created_at": str(reservation.current_reservation_date),
                "deposit": reservation.deposit
            }
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


@mcp.tool()
def cancel_reservation(reservation_id: str) -> Dict[str, Any]:
    """
    Cancel a reservation.
    
    Args:
        reservation_id: The reservation ID to cancel (e.g., "RESV-00000")
    
    Returns:
        Dictionary containing cancellation status
    """
    try:
        cafe_system.cancel_reservation(reservation_id)
        
        return {
            "success": True,
            "message": "Reservation cancelled successfully",
            "reservation_id": reservation_id
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


# ════════════════════════════════════════════════════════════════
# Member Profile Functions
# ════════════════════════════════════════════════════════════════

@mcp.tool()
def register_as_member(name: str) -> Dict[str, Any]:
    """
    Register a new member account.
    
    Args:
        name: The member's name
    
    Returns:
        Dictionary containing new member details
    """
    try:
        member = cafe_system.create_customer_member(name)
        
        return {
            "success": True,
            "message": "Member registered successfully",
            "member": {
                "member_id": member.user_id,
                "name": member.name,
                "member_tier": member.member_tier.value,
                "total_spent": member.total_spent,
                "discount_percentage": int(member.get_discount() * 100)
            }
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


@mcp.tool()
def get_my_profile(member_id: str) -> Dict[str, Any]:
    """
    Get member profile information including tier benefits and progress.
    
    Args:
        member_id: The member ID (e.g., "MEMBER-00000")
    
    Returns:
        Dictionary containing member profile and benefits
    """
    try:
        member = cafe_system.find_person_by_id(member_id)
        if not member:
            return {"success": False, "error": "Member not found"}
        
        # Get member tier benefits
        tier_benefits = {
            "NONE_TIER": {"discount": 0, "max_duration": 1.5, "advance_days": 3, "quota": 0},
            "Bronze": {"discount": 5, "max_duration": 2, "advance_days": 5, "quota": 1},
            "Silver": {"discount": 10, "max_duration": 3.5, "advance_days": 14, "quota": 2},
            "Gold": {"discount": 20, "max_duration": 7, "advance_days": 21, "quota": 3},
            "Platinum": {"discount": 25, "max_duration": 12, "advance_days": 30, "quota": 4}
        }
        
        tier_name = member.member_tier.value
        benefits = tier_benefits.get(tier_name, tier_benefits["NONE_TIER"])
        
        # Count active reservations
        active_reservations = len([
            r for r in cafe_system.reservations 
            if r.customer_id == member_id and r.status == ReservationStatus.PENDING
        ])
        
        # Calculate next tier
        next_tier_info = _get_next_tier_info(member.total_spent, tier_name)
        
        return {
            "success": True,
            "profile": {
                "member_id": member.user_id,
                "name": member.name,
                "member_tier": tier_name,
                "total_spent": f"฿{member.total_spent:.2f}",
                "discount_percentage": f"{benefits['discount']}%",
                "birth_date": member.birth_date if hasattr(member, 'birth_date') else None
            },
            "benefits": {
                "max_reservation_duration_hours": benefits["max_duration"],
                "advance_booking_days": benefits["advance_days"],
                "active_reservation_quota": benefits["quota"],
                "current_active_reservations": active_reservations,
                "remaining_quota": max(0, benefits["quota"] - active_reservations)
            },
            "tier_progress": next_tier_info
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


@mcp.tool()
def update_my_profile(
    member_id: str,
    name: Optional[str] = None,
    birth_date: Optional[str] = None
) -> Dict[str, Any]:
    """
    Update member profile information.
    
    Args:
        member_id: The member ID (e.g., "MEMBER-00000")
        name: New name (optional)
        birth_date: Birth date in YYYY-MM-DD format (optional)
    
    Returns:
        Dictionary containing updated profile
    """
    try:
        member = cafe_system.find_person_by_id(member_id)
        if not member:
            return {"success": False, "error": "Member not found"}
        
        if name:
            member.name = name
        
        if birth_date:
            member.birth_date = birth_date
        
        return {
            "success": True,
            "message": "Profile updated successfully",
            "profile": {
                "member_id": member.user_id,
                "name": member.name,
                "birth_date": member.birth_date if hasattr(member, 'birth_date') else None
            }
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


@mcp.tool()
def view_tier_benefits(tier: str = "all") -> Dict[str, Any]:
    """
    View benefits for member tiers.
    
    Args:
        tier: Specific tier name or "all" to see all tiers
             Options: "None", "Bronze", "Silver", "Gold", "Platinum", "all"
    
    Returns:
        Dictionary containing tier benefits information
    """
    try:
        tier_benefits = {
            "None": {
                "discount": "0%",
                "max_duration_hours": 1.5,
                "advance_booking_days": 3,
                "reservation_quota": 0,
                "required_spending": "฿0"
            },
            "Bronze": {
                "discount": "5%",
                "max_duration_hours": 2,
                "advance_booking_days": 5,
                "reservation_quota": 1,
                "required_spending": "฿250+"
            },
            "Silver": {
                "discount": "10%",
                "max_duration_hours": 3.5,
                "advance_booking_days": 14,
                "reservation_quota": 2,
                "required_spending": "฿500+"
            },
            "Gold": {
                "discount": "20%",
                "max_duration_hours": 7,
                "advance_booking_days": 21,
                "reservation_quota": 3,
                "required_spending": "฿1,000+"
            },
            "Platinum": {
                "discount": "25%",
                "max_duration_hours": 12,
                "advance_booking_days": 30,
                "reservation_quota": 4,
                "required_spending": "฿2,000+"
            }
        }
        
        if tier.lower() == "all":
            return {
                "success": True,
                "all_tiers": tier_benefits
            }
        elif tier in tier_benefits:
            return {
                "success": True,
                "tier": tier,
                "benefits": tier_benefits[tier]
            }
        else:
            return {
                "success": False,
                "error": "Invalid tier. Options: None, Bronze, Silver, Gold, Platinum, all"
            }
    except Exception as e:
        return {"success": False, "error": str(e)}


# ════════════════════════════════════════════════════════════════
# Helper Functions
# ════════════════════════════════════════════════════════════════

def _get_next_tier_info(current_spent: float, current_tier: str) -> Dict[str, Any]:
    """Get information about next tier progress."""
    tier_thresholds = {
        "NONE_TIER": ("Bronze", 250),
        "Bronze": ("Silver", 500),
        "Silver": ("Gold", 1000),
        "Gold": ("Platinum", 2000),
        "Platinum": (None, None)
    }
    
    next_tier, threshold = tier_thresholds.get(current_tier, (None, None))
    
    if next_tier is None:
        return {
            "current_tier": current_tier,
            "is_max_tier": True,
            "message": "You are at the highest tier! 🎉"
        }
    
    remaining = threshold - current_spent
    progress_percentage = min(100, (current_spent / threshold) * 100)
    
    return {
        "current_tier": current_tier,
        "next_tier": next_tier,
        "current_spent": f"฿{current_spent:.2f}",
        "required_for_next": f"฿{threshold:.2f}",
        "remaining": f"฿{remaining:.2f}",
        "progress_percentage": f"{progress_percentage:.1f}%"
    }


# ════════════════════════════════════════════════════════════════
# Run the MCP Server
# ════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    mcp.run()