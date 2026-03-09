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
    from _Project_instance import system
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
    import re

    # ✅ ด่านที่ 0: validate format ก่อน DB lookup ทุกอย่าง
    if not re.match(r'^\d{4}-\d{2}-\d{2}$', str(date_str)):
        return f"Invalid date format: '{date_str}'. Expected YYYY-MM-DD (e.g. 2024-07-01)"
    for t_val, t_name in [(start_t, "start_time"), (end_t, "end_time")]:
        if not re.match(r'^\d{2}:\d{2}$', str(t_val)):
            return f"Invalid time format for {t_name}: '{t_val}'. Expected HH:MM (e.g. 18:00)"
    if not isinstance(players, int) or players <= 0:
        return "players must be a positive integer"

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


# Alias map: รองรับทั้ง class name จริง และ alias ที่ Claude มักส่งมา
_PERSON_TYPE_ALIASES = {
    "Owner":           "Owner",
    "Manager":         "Manager",
    "Staff":           "Staff",
    "Member":          "Member",
    "WalkInCustomer":  "WalkInCustomer",
    "Customer_member": "Member",
    "customer_member": "Member",
    "customer_walk_in":"WalkInCustomer",
    "WalkIn":          "WalkInCustomer",
    "walk_in":         "WalkInCustomer",
    "customer":        "Member",
    "Customer":        "Member",
}

@mcp.tool()
def get_person_by_type(person_type: str) -> str:
    """Get all persons of a specific type.

    Accepted values (aliases supported):
    - "Owner"
    - "Manager"
    - "Staff"
    - "Member"         (aliases: "Customer_member", "customer_member", "customer")
    - "WalkInCustomer" (aliases: "customer_walk_in", "WalkIn", "walk_in")
    """
    try:
        resolved = _PERSON_TYPE_ALIASES.get(person_type)
        if resolved is None:
            valid = ", ".join(sorted(set(_PERSON_TYPE_ALIASES.values())))
            return f"Error: Unknown person_type '{person_type}'. Valid: {valid}"

        person_module = sys.modules.get('BGC_PERSON')
        target_class = getattr(person_module, resolved)
        persons = system.get_person_by_type(target_class)

        def format_person(p):
            if resolved == 'Member':
                tier_name = p.get_member_tier().value if hasattr(p, 'get_member_tier') else 'None'
                spent = p.get_total_spent() if hasattr(p, 'get_total_spent') else 0
                return f"ID: {p.user_id}, Name: {p.name}, Tier: {tier_name}, Total Spent: {spent}"
            return f"ID: {p.user_id}, Name: {p.name}"

        return (
            "\n".join([format_person(p) for p in persons])
            if persons
            else f"No {resolved} found"
        )
    except AttributeError:
        return f"Error: Class '{person_type}' not found in BGC_PERSON"
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
def get_play_session_orders(any_id: str) -> str:
    """Get  food/drink orders for play session im a branch
    accept only PS- and TABLE-
    e.g. get_play_session_order(TABLE-00000)
    e.g. get_play_session_order(PS-00000)
    """
    try:
        orders = system.get_play_session_orders(any_id)

        return (
            "\n".join(
                [f"Order: {o.menu_items.name} status: {o.status.value}" for o in orders])
            if orders
            else "Currently No Orders"
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
def cancel_reservation(reservation_id: str, current_time: str = None) -> str:
    try:
        parsed_time = None
        if current_time is not None:
            for fmt in ("%Y-%m-%dT%H:%M:%S", "%Y-%m-%dT%H:%M", "%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M"):
                try:
                    parsed_time = datetime.strptime(current_time, fmt)
                    break
                except ValueError:
                    continue
            if parsed_time is None:
                return "Error: current_time format invalid. Use 'YYYY-MM-DD HH:MM'"
        res = system.cancel_reservation(reservation_id, parsed_time)
        return "Cancellation successful" if res else "Cancellation failed or no data found"
    except Exception as e:
        return f"Error: {e}"


@mcp.tool()
def check_in(
    branch_id: str,
    player_amount: int,
    customer_id: str = "walk_in",
    table_id: str = "auto",
    start_time: str = None
) -> str:
    """Check in and start a new play session at a branch.

    CRITICAL - customer_id behaviour:
    - "walk_in" (default): creates player_amount anonymous WALK- customers.
      Walk-in IDs are NOT Members — their spending is NEVER tracked for tier upgrades.
    - "MEMBER-XXXXX": registers that member as the first player (1 person only).
      player_amount is still used to find a table with enough capacity.
      Use join_session() afterward to add more named members so their
      total_spent is also tracked correctly.

    RULE: If any customer is a registered Member, always pass their MEMBER-ID
    here (or via join_session). Never use walk_in for registered members,
    or their spending will be lost.

    start_time format: 'YYYY-MM-DD HH:MM' or ISO datetime. None = use now.
    """
    try:
        session = system.check_in(
            branch_id, player_amount, customer_id, table_id, start_time=start_time)
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
def check_in_members(
    branch_id: str,
    member_ids: str,
    table_id: str = "auto",
    start_time: str = None
) -> str:
    """Check in a group of registered Members together into one session.

    Use this instead of check_in() when ALL players are registered Members
    and you want EVERY player's total_spent tracked for tier upgrades.

    member_ids: comma-separated MEMBER-IDs, e.g. "MEMBER-00001,MEMBER-00002"
    The number of IDs determines player_amount automatically.

    start_time format: 'YYYY-MM-DD HH:MM' or ISO datetime. None = use now.
    """
    try:
        ids = [mid.strip() for mid in member_ids.split(",") if mid.strip()]
        if not ids:
            return "Error: No member IDs provided"

        # Check-in the first member to create the session
        session = system.check_in(
            branch_id, len(ids), ids[0], table_id, start_time=start_time
        )

        # Join all remaining members into the same session
        for mid in ids[1:]:
            system.join_session(session.session_id, mid)

        player_list = ", ".join(ids)
        return (
            f"Check in successful! Session ID: {session.session_id}, "
            f"Table: {session.table_id}, Members: {player_list}"
        )
    except Exception as e:
        return f"Error: {e}"


@mcp.tool()
def join_session(play_session_id: str, customer_id: str = "walk_in") -> str:
    """Join an existing play session.

    customer_id: MEMBER-ID of the member joining, or "walk_in" for anonymous.
    Use a real MEMBER-ID (not walk_in) to ensure this player's spending is
    tracked toward their tier at checkout.
    """
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
def flag_board_game_damaged(play_session_id: str, board_game_id: str) -> str:
    """Flag a board game as damaged (MAINTENANCE) and add it to the session's penalty list.
    Use this when a game is confirmed broken during or after a session.
    The penalty cost (game price) will be added to the session bill at checkout.
    e.g. flag_board_game_damaged("PS-00000", "BG-00000")
    """
    try:
        res = system.return_board_game(play_session_id, board_game_id, is_damaged=True)
        return (
            f"Board game '{res.name}' (ID: {res.game_id}) flagged as MAINTENANCE. "
            f"A penalty of ฿{res.price:.2f} will be charged at checkout."
        )
    except Exception as e:
        return f"Error: {e}"



@mcp.tool()
def bill_history(play_session_id: str) -> str:
    """ดูใบเสร็จย้อนหลังของ session ที่ checkout แล้ว (ใช้ PS- เท่านั้น)
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
    """ดูประวัติใบเสร็จทุก session ของ person คนนึง
    e.g. bill_history_by_person("MEMBER-00000")
    """
    try:
        items = system.bill_history_by_person(person_id)
        if not items:
            return "ไม่พบประวัติการใช้บริการ"
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
def check_out(
    play_session_id: str,
    method_type: str = "cash",
    end_time: datetime = None,
    paid_amount: float = None,
    email: str = None,
    card_number: str = None,
    expiry_date: str = None,
    cvv: str = None,
) -> str:
    try:
        kwargs = {}
        if paid_amount is not None:
            kwargs["paid_amount"] = paid_amount
        if email is not None:
            kwargs["email"] = email
        if card_number is not None:
            kwargs["card_number"] = card_number
        if expiry_date is not None:
            kwargs["expiry_date"] = expiry_date
        if cvv is not None:
            kwargs["cvv"] = cvv

        receipt, total = system.check_out(
            play_session_id, end_time=end_time, method_type=method_type, **kwargs)
        return f"Check out successful. Total: {total:.2f}, Receipt ID: {receipt.payment_id}"
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

        food = system.create_menu_item_food_to_branch(
            branch_id, name, price, description)
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

        drink = system.create_menu_item_drink_to_branch(
            branch_id, name, price, cup_size, description)
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
def authorize_add_spent(
    auth_id: str,
    customer_id: str,
    amount: float,
    authorizer_id: str = None,
) -> str:
    """Add total spent amount for a Member. Requires Owner or Manager to authorize.

    Parameters (both names accepted for the authorizer):
    - auth_id / authorizer_id : OWNER-PESO67 or MANAGER-XXXXX
    - customer_id             : MEMBER-XXXXX
    - amount                  : float, amount to add to total_spent

    Example:
        authorize_add_spent(auth_id="OWNER-PESO67", customer_id="MEMBER-00003", amount=500)
        authorize_add_spent(authorizer_id="OWNER-PESO67", customer_id="MEMBER-00003", amount=500)
    """
    try:
        # รองรับทั้ง auth_id และ authorizer_id
        effective_auth = auth_id if auth_id else authorizer_id
        if not effective_auth:
            return "Authorization Failed: Must provide auth_id or authorizer_id"

        if not (effective_auth.startswith("OWNER") or effective_auth.startswith("MANAGER")):
            return "Authorization Failed: Only Owner or Manager can authorize adding spent amount"

        person = system.find_person_by_id(effective_auth)
        if person is None:
            return f"Authorization Failed: Authorizer '{effective_auth}' not found in the system"

        customer = system.add_spent(customer_id, amount)
        return (f"Spent amount added successfully | "
                f"Customer ID: {customer.user_id} | "
                f"Current Total Spent: {customer.total_spent:.2f} | "
                f"Tier: {customer.get_member_tier().value}")
    except Exception as e:
        return f"Error: {e}"


if __name__ == "__main__":
    mcp.run()