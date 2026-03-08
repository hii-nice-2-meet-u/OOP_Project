from mcp.server.fastmcp import FastMCP
from datetime import datetime
from BGC_PERSON import *
import sys
import os

# --- STEP 1: Manage PATH correctly ---
# Force Python to see all BGC_... files in the current folder
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

# --- STEP 2: Create MCP Instance ---
mcp = FastMCP("BoardGameCafe")

# --- STEP 3: Load system (Catch Import Error) ---
try:
    from demo__instance import system
    print("Downloading Demo_instance....", file=sys.stderr)

except Exception as e:
    # Print Error to stderr only (Do not print to stdout)
    print(f"Server Setup Error: {e}", file=sys.stderr)
    sys.exit(1)


# --- STEP 4: Create Tools for Claude ---

@mcp.tool()
def make_reservation(
    customer_name: str,
    branch_name: str,
    players: int,
    date_str: str,
    start_t: str,
    end_t: str,
    table_id: str,
) -> str:
    """Book a table (date_str format: YYYY-MM-DD, time format: HH:MM)
    Example call: make_reservation("MEMBER_A", "Ladkrabang", 4, "2024-07-01", "18:00", "20:00")
    Use branch name for booking instead of ID for testing convenience"""
    try:
        member = system.find_person_by_name(customer_name)
        if not member:
            return "Customer name not found in the system"
        branch = system.find_cafe_branch_by_name(branch_name)
        if not branch:
            return "Branch not found"
        res = system.make_reservation(
            member.user_id, branch.branch_id, players, date_str, start_t, end_t, table_id
        )
        return f"Booking successful! ID: {res.reservation_id} at table {res.table_id}"
    except Exception as e:
        return f"Error occurred: {str(e)}"


@mcp.tool()
def get_all_cafe_branches() -> str:
    """View all cafe branches with their table counts"""
    branches = system.get_cafe_branches()
    result = []
    for b in branches:
        result.append(
            f"Branch : {b.name:<25} ( ID : {b.branch_id} ) - Tables : {b.total_tables}"
        )
    return "\n".join(result) if result else "No branch data available"


@mcp.tool()
def get_person_by_type(person_type: str) -> str:
    """Get all persons of a specific type ('Owner', 'Manager', 'Staff', 'Customer_member', 'customer_walk_in')
    pass with CamelCase owner -> Owner (Case Sensitive)
    Supported types: 'Owner', 'Manager', 'Staff', 'Member', 'WalkInCustomer'"""
    try:
        person_module = sys.modules.get('BGC_PERSON')
        target_class = getattr(person_module, person_type)
        persons = system.get_person_by_type(target_class)

        def format_person(p):
            if person_type == 'Member':
                tier_name = p.get_member_tier().value if hasattr(p, 'get_member_tier') else 'None'
                return f"ID: {p.user_id}, Name: {p.name}, Tier: {tier_name}, Total Spent: {p.get_total_spent() if hasattr(p, 'get_total_spent') else 0}"
            return f"ID: {p.user_id}, Name: {p.name}"

        return (
            "\n".join([format_person(p) for p in persons])
            if persons
            else "No data found"
        )
    except Exception as e:
        return f"Error: {e}"


@mcp.tool()
def get_branch_tables(branch_id: str) -> str:
    """Get all tables in a specific branch"""
    try:
        tables = system.get_branch_tables(branch_id)
        return (
            "\n".join(
                [
                    f"Table ID: {t.table_id}, Cap: {t.capacity}, Status: {t.status}"
                    for t in tables
                ]
            )
            if tables
            else "No table data available"
        )
    except Exception as e:
        return f"Error: {e}"


@mcp.tool()
def search_available_table(branch_id: str, required_capacity: int = 0) -> str:
    """Search for available tables. required_capacity=0 means any capacity."""
    try:
        tables = system.search_available_table(branch_id, required_capacity)
        return (
            "\n".join(
                [f"Table ID: {t.table_id}, Cap: {t.capacity}" for t in tables])
            if tables
            else "No available tables"
        )
    except Exception as e:
        return f"Error: {e}"


@mcp.tool()
def get_branch_board_games(branch_id: str) -> str:
    """Get all board games in a specific branch"""
    try:
        games = system.get_branch_board_games(branch_id)
        return (
            "\n".join(
                [
                    f"Game ID: {g.game_id}, Name: {g.name}, Status: {g.status}"
                    for g in games
                ]
            )
            if games
            else "No board games available"
        )
    except Exception as e:
        return f"Error: {e}"


@mcp.tool()
def search_board_game_by_min_players(branch_id: str, min_players: int) -> str:
    """Search for board games by minimum players required"""
    try:
        games = system.search_board_game_by_min_players(branch_id, min_players)
        return (
            "\n".join(
                [f"Game ID: {g.game_id}, Name: {g.name}" for g in games])
            if games
            else "No games found"
        )
    except Exception as e:
        return f"Error: {e}"


@mcp.tool()
def search_board_game_by_max_players(branch_id: str, max_players: int) -> str:
    """Search for board games by maximum players required"""
    try:
        games = system.search_board_game_by_max_players(branch_id, max_players)
        return (
            "\n".join(
                [f"Game ID: {g.game_id}, Name: {g.name}" for g in games])
            if games
            else "No games found"
        )
    except Exception as e:
        return f"Error: {e}"


@mcp.tool()
def get_branch_menu(branch_id: str) -> str:
    """Get all menu items in a branch"""
    try:
        items = system.get_branch_menu_item(branch_id)
        return (
            "\n".join(
                [
                    f"Menu ID: {m.item_id}, Name: {m.name}, Price: {m.price}"
                    for m in items
                ]
            )
            if items
            else "No menus available"
        )
    except Exception as e:
        return f"Error: {e}"


@mcp.tool()
def get_pending_orders(branch_id: str) -> str:
    """Get pending food/drink orders for a branch"""
    try:
        orders = system.get_pending_orders(branch_id)
        branch = system.find_cafe_branch_by_id(branch_id)

        return (
            "\n".join(
                [
                    f"Order ID: {o.order_id}, Status: {o.status}"
                    for o in orders
                ]
            )
            if orders
            else "No pending orders"
        )
    except Exception as e:
        return f"Error: {e}"


@mcp.tool()
def create_customer_member(name: str) -> str:
    """Create a new customer member"""
    try:
        member = system.create_customer_member(name)
        return f"Created member ID: {member.user_id}, Name: {member.name}"
    except Exception as e:
        return f"Error: {e}"


@mcp.tool()
def cancel_reservation(reservation_id: str, current_time) -> str:
    """Cancel a reservation by ID, current time = time of reservation """
    try:
        res = system.cancel_reservation(reservation_id, current_time)
        return "Cancellation successful" if res else "Cancellation failed or no data found"
    except Exception as e:
        return f"Error: {e}"


@mcp.tool()
def check_in(
    branch_id: str,
    player_amount: int,
    customer_id: str = "walk_in",
    table_id: str = "auto",
) -> str:
    """Check in a walk-in or walk-in member"""
    try:
        session = system.check_in(
            branch_id, player_amount, customer_id, table_id)
        return f"Check in successful! Session ID: {session.session_id}, Table: {session.table_id}"
    except Exception as e:
        return f"Error: {e}"


@mcp.tool()
def check_in_reserved(reservation_id: str, customer_id: str, current_time: datetime) -> str:
    """Check in a reserved session"""
    try:
        session = system.check_in_reserved(
            reservation_id, customer_id, current_time)
        return f"Check in reserved successful! Session ID: {session.session_id}"
    except Exception as e:
        return f"Error: {e}"


@mcp.tool()
def join_session(play_session_id: str, customer_id: str = "walk_in") -> str:
    """Join an existing play session"""
    try:
        system.join_session(play_session_id, customer_id)
        return "Successfully joined"
    except Exception as e:
        return f"Error: {e}"


@mcp.tool()
def borrow_board_game(play_session_id: str, board_game_id: str) -> str:
    """Borrow a board game for a session"""
    try:
        res = system.borrow_board_game(play_session_id, board_game_id)
        return "Successfully borrowed" if res else "Failed to borrow"
    except Exception as e:
        return f"Error: {e}"


@mcp.tool()
def return_board_game(play_session_id: str, board_game_id: str, is_damaged: bool = False) -> str:
    """Return a board game from a session
    Set is_damaged to true to flag the board game as broken (MAINTENANCE)
    """
    try:
        system.return_board_game(
            play_session_id, board_game_id, is_damaged=is_damaged)
        return "Successfully returned"
    except Exception as e:
        return f"Error: {e}"


@mcp.tool()
def take_order(play_session_id: str, menu_item_id: str) -> str:
    """Take an order for a session
    e.g. take_order("PS-00000", "FOOD-00000")
    """
    try:
        order = system.take_order(play_session_id, menu_item_id)
        return f"Order successful Order ID: {order.order_id}" if order else "Order failed"
    except Exception as e:
        return f"Error: {str(e)}"


@mcp.tool()
def update_order_serve(play_session_id: str, order_id: str) -> str:
    """Update order status to served"""
    try:
        system.update_order_serve(play_session_id, order_id)
        return "Order status updated to served"
    except Exception as e:
        return f"Error: {e}"


@mcp.tool()
def update_order_cancel(play_session_id: str, order_id: str) -> str:
    """Cancel an order"""
    try:
        system.update_order_cancel(play_session_id, order_id)
        return "Order cancelled"
    except Exception as e:
        return f"Error: {e}"
@mcp.tool()
def bill_history(play_session_id: str) -> str:
    """View past receipt of a checked-out session (Use PS- only)
    e.g. bill_history("PS-00000")
    """
    try:
        items = system.bill_history(play_session_id)
        lines = []
        for label, price in items:
            prefix = ">>> " if label == "TOTAL" else "    "
            sign = "-" if price < 0 else " "
            lines.append(f"{prefix}{label:<45} {sign}฿{abs(price):.2f}")
        return "\n".join(lines)
    except Exception as e:
        return f"Error: {e}"


@mcp.tool()
def bill_history_by_person(person_id: str) -> str:
    """View all receipt history for a specific person
    e.g. bill_history_by_person("MEMBER-00000")
    """
    try:
        all_bills = system.bill_history_by_person(person_id)
        if not all_bills:
            return "No service history found"
        lines = []
        for label, price in items:
            if price is None:
                lines.append(f"{'─'*64}")
                lines.append(f"  {label}")
            elif label == "TOTAL":
                lines.append(f"  >>> {label:<43}  ฿{price:.2f}")
            else:
                sign = "-" if price < 0 else " "
                lines.append(f"      {label:<43} {sign}฿{abs(price):.2f}")
        lines.append(f"{'─'*64}")
        return "\n".join(lines)
    except Exception as e:
        return f"Error: {e}"

@mcp.tool()
def check_out(play_session_id: str, method_type: str = "cash", paid_amount: float = None) -> str:
    """Check out a session and generate receipt
    method_type can be 'cash', 'card', or 'online'.
    If using cash and paying less/more than total, pass paid_amount.
    """
    try:
        kwargs = {}
        if paid_amount is not None:
            kwargs["paid_amount"] = paid_amount

        receipt, total = system.check_out(
            play_session_id, method_type=method_type, **kwargs)
        return f"Check out successful. Total: {total}, Receipt ID: {receipt.payment_id}"
    except Exception as e:
        return f"Error: {e}"


# / =====================================================================
# #00FF00
# / Method for Config Board Game Cafe

@mcp.tool()
def add_table_to_branch(auth_id: str, branch_id: str, capacity: int) -> str:
    """
    Add a table to a branch (Requires Owner ID or Manager ID to authorize)
    e.g. add_table_to_branch("OWNER-PESO67", "BRCH-00000", 4)
    """
    try:
        # 1. Authorization Check
        if not (auth_id.startswith("OWNER") or auth_id.startswith("MANAGER")):
            return "Authorization Failed: Only Owner or Manager can add a table"
        
        person = system.find_person_by_id(auth_id)
        if isinstance(person, Manager):
            if system.find_cafe_branch_by_id(branch_id).manager_id != person.user_id:
                return f"You are not Manager of {system.find_cafe_branch_by_id(branch_id).name}"
        if person is None:
            return f"Authorization Failed: User ID {auth_id} not found in the system"

        # 2. Execute Action
        table = system.create_table_to_branch(branch_id, capacity)
        return f"Table created successfully Table ID: {table.table_id} (Capacity: {capacity} seats) in branch {branch_id}"
    except Exception as e:
        return f"Error: {e}"
    
@mcp.tool()
def add_food_to_branch(auth_id: str, branch_id: str, name: str, price: float, description: str = "") -> str:
    """
    Add a food menu item (Requires Owner ID or Manager ID to authorize)
    """
    try:
        if not (auth_id.startswith("OWNER") or auth_id.startswith("MANAGER")):
            return "Authorization Failed: Only Owner or Manager can add a menu item"
        
        person = system.find_person_by_id(auth_id)
        if isinstance(person, Manager):
            if system.find_cafe_branch_by_id(branch_id).manager_id != person.user_id:
                return f"You are not Manager of {system.find_cafe_branch_by_id(branch_id).name}"
        if person is None:
            return "Authorization Failed: User not found in the system"

        food = system.create_menu_item_food_to_branch(branch_id, name, price, description)
        return f"Food menu added successfully Item ID: {food.item_id} | Name: {food.name} | Price: {price}"
    except Exception as e:
        return f"Error: {e}"

@mcp.tool()
def add_drink_to_branch(auth_id: str, branch_id: str, name: str, price: float, cup_size: str = "S", description: str = "") -> str:
    """
    Add a drink menu item (Requires Owner ID or Manager ID to authorize)
    """
    try:
        if not (auth_id.startswith("OWNER") or auth_id.startswith("MANAGER")):
            return "Authorization Failed: Only Owner or Manager can add a menu item"
            
        person = system.find_person_by_id(auth_id)
        if person is None:
            return "Authorization Failed: User not found in the system"
        
        if isinstance(person, Manager):
            if system.find_cafe_branch_by_id(branch_id).manager_id != person.user_id:
                return f"You are not Manager of {system.find_cafe_branch_by_id(branch_id).name}"

        drink = system.create_menu_item_drink_to_branch(branch_id, name, price, cup_size, description)
        return f"Drink added successfully Item ID: {drink.item_id} | Name: {drink.name} (Size: {cup_size}) | Price: {price}"
    except Exception as e:
        return f"Error: {e}"

@mcp.tool()
def add_staff_to_branch(auth_id: str, branch_id: str, staff_name: str) -> str:
    """
    Create and add staff to a branch (Requires Owner ID or Manager ID to authorize)
    """
    try:
        if not (auth_id.startswith("OWNER") or auth_id.startswith("MANAGER")):
            return "Authorization Failed: Only Owner or Manager can add staff"
            
        person = system.find_person_by_id(auth_id)
        if isinstance(person, Manager):
            if system.find_cafe_branch_by_id(branch_id).manager_id != person.user_id:
                return f"You are not Manager of {system.find_cafe_branch_by_id(branch_id).name}"
        if person is None:
            return "Authorization Failed: User not found in the system"

        # Create Staff and add to branch
        new_staff = system.create_staff(staff_name)
        system.add_staff_to_branch(branch_id, new_staff.user_id)
        
        return f"Staff added successfully Staff ID: {new_staff.user_id} | Name: {new_staff.name} added to branch {branch_id}"
    except Exception as e:
        return f"Error: {e}"
    
@mcp.tool()
def authorize_add_spent(auth_id: str, customer_id: str, amount: float) -> str:
    """
    Add total spent amount for a Member (Requires Owner ID or Manager ID to authorize)
    """
    try:
        if not (auth_id.startswith("OWNER") or auth_id.startswith("MANAGER")):
            return "Authorization Failed: Only Owner or Manager can authorize adding spent amount"
            
        person = system.find_person_by_id(auth_id)
        if person is None:
            return "Authorization Failed: Authorizer not found in the system"

        customer = system.add_spent(customer_id, amount)
        return (f"Spent amount added successfully Customer ID: {customer.user_id} | "
                f"Current Total Spent: {customer.total_spent} | Tier: {customer.get_member_tier().value}")
    except Exception as e:
        return f"Error: {e}"

if __name__ == "__main__":
    mcp.run()