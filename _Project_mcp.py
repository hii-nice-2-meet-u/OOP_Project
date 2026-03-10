from mcp.server.fastmcp import FastMCP
from datetime import datetime
from BGC_PERSON import *
from BGC_PLAY_SESSION import Table
from ENUM_STATUS import BoardGameStatus
import sys
import os
import re
import math

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
    table_id: str = "auto",
    payment_method: str = "online",
    card_number: str = None,
    expiry_date: str = None,
    cvv: str = None,
    email: str = None
) -> str:
    """Book a table in advance with a mandatory 30 THB deposit (Non-cash only).
    IMPORTANT: Only registered Members (MEMBER-XXXXX) can make reservations.
    Walk-in customers CANNOT book in advance — they should register as Members first.
    customer_name: full name of the registered Member (not walk-in).
    date_str format: YYYY-MM-DD, time format: HH:MM
    table_id: specific TABLE-XXXXX to book, or 'auto' to let system pick the best fit.
    payment_method: 'online' or 'credit_card' (Cash is not allowed for reservations).
    For 'credit_card': provide card_number, expiry_date, cvv.
    For 'online': provide email."""

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
            
        kwargs = {}
        if payment_method == "credit_card":
            kwargs = {"card_number": card_number, "expiry_date": expiry_date, "cvv": cvv}
        elif payment_method == "online":
            kwargs = {"email": email}

        res = system.make_reservation(
            member.user_id, branch.branch_id, players, date_str, start_t, end_t, 
            table_id=table_id, method_type=payment_method, **kwargs
        )
        return f"Booking successful! ID: {res.reservation_id} (Deposit ฿30 paid via {payment_method}) at table {res.table_id}"
    except Exception as e:
        return f"Error occurred: {str(e)}"

@mcp.tool()
def get_all_cafe_branches() -> str:
    """View all cafe branches with their table counts"""
    try:
        branches = system.get_cafe_branches()
        result = [
            f"Branch : {b.name:<25} ( ID : {b.branch_id} ) - Tables : {b.total_tables}"
            for b in branches
        ]
        return "\n".join(result) if result else "No branch data available"
    except Exception as e:
        return f"Error: {e}"


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
    """Get food/drink orders for a play session.
    Accepts PS- (session ID) or TABLE- (table ID).
    e.g. get_play_session_orders("TABLE-00000")
    e.g. get_play_session_orders("PS-00000")
    """
    try:
        # ใช้ logic จาก BGC_SYSTEM โดยตรงในการหา branch และ orders
        orders = system.get_play_session_orders(any_id)
        return (
            "\n".join(
                [f"Order ID: {o.order_id} | {o.snapshot_name} | Status: {o.status.value}"
                 for o in orders])
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
def check_in_reserved(reservation_id: str, customer_id: str, current_time: str = None) -> str:
    """Check in using a reservation.
    current_time format: 'YYYY-MM-DD HH:MM' or ISO. Leave blank to use current time.
    """
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

        session = system.check_in_reserved(reservation_id, customer_id, parsed_time)
        return f"Check in reserved successful! Session ID: {session.session_id}, Table: {session.table_id}"
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
def borrow_board_game(play_session_id: str, board_game_id: str, current_time: str = None) -> str:
    """Borrow a board game for a session.
    current_time format: 'YYYY-MM-DD HH:MM' or ISO. Leave blank to use current time.
    """
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

        res = system.borrow_board_game(play_session_id, board_game_id, current_time=parsed_time)
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
def take_order(play_session_id: str, menu_item_id: str, current_time: str = None) -> str:
    """Take an order for a session
    e.g. take_order("PS-00000", "FOOD-00000")
    current_time format: 'YYYY-MM-DD HH:MM' or ISO. Leave blank to use current time.
    """
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

        order = system.take_order(play_session_id, menu_item_id, current_time=parsed_time)
        return f"Order successful Order ID: {order.order_id}" if order else "Order failed"
    except Exception as e:
        return f"Error: {str(e)}"


@mcp.tool()
def update_order_preparing(play_session_id: str, order_id: str) -> str:
    """Update order status to preparing (kitchen has started on the order)"""
    try:
        system.update_order_preparing(play_session_id, order_id)
        return "Order status updated to preparing"
    except Exception as e:
        return f"Error: {e}"


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
    end_time: str = None,
    paid_amount: float = None,
    email: str = None,
    card_number: str = None,
    expiry_date: str = None,
    cvv: str = None,
) -> str:
    """Check out a play session and process payment.

    method_type (REQUIRED, choose one):
      - "cash"   → also provide paid_amount (float)
      - "card"   → also provide card_number, expiry_date, cvv
      - "online" → also provide email

    Examples:
      check_out("PS-00000", method_type="cash",   paid_amount=500)
      check_out("PS-00000", method_type="card",   card_number="1234-5678-9012-3456", expiry_date="12/28", cvv="123")
      check_out("PS-00000", method_type="online", email="user@example.com")

    end_time: optional, format 'YYYY-MM-DD HH:MM'. Leave blank to use current time.
    """
    try:
        parsed_end = None
        if end_time is not None:
            for fmt in ("%Y-%m-%dT%H:%M:%S", "%Y-%m-%dT%H:%M", "%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M"):
                try:
                    parsed_end = datetime.strptime(end_time, fmt)
                    break
                except ValueError:
                    continue
            if parsed_end is None:
                return "Error: end_time format invalid. Use 'YYYY-MM-DD HH:MM'"

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
            play_session_id, end_time=parsed_end, method_type=method_type, **kwargs)
        return f"Check out successful. Total: ฿{total:.2f}, Receipt ID: {receipt.payment_id}"
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
        if not (auth_id.startswith("OWNER") or auth_id.startswith("MANAGER")):
            return "Authorization Failed: Only Owner or Manager can add a table"

        person = system.find_person_by_id(auth_id)
        if person is None:
            return f"Authorization Failed: User ID {auth_id} not found in the system"
        if isinstance(person, Manager):
            branch = system.find_cafe_branch_by_id(branch_id)
            if branch and branch.manager_id != person.user_id:
                return f"You are not Manager of {branch.name}"

        table = system.create_table_to_branch(branch_id, capacity, requester_id=auth_id)
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
        if person is None:
            return "Authorization Failed: User not found in the system"
        if isinstance(person, Manager):
            branch = system.find_cafe_branch_by_id(branch_id)
            if branch and branch.manager_id != person.user_id:
                return f"You are not Manager of {branch.name}"

        food = system.create_menu_item_food_to_branch(branch_id, name, price, description, requester_id=auth_id)
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
            branch = system.find_cafe_branch_by_id(branch_id)
            if branch and branch.manager_id != person.user_id:
                return f"You are not Manager of {branch.name}"

        drink = system.create_menu_item_drink_to_branch(
            branch_id, name, price, cup_size, description, requester_id=auth_id)
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
        if person is None:
            return "Authorization Failed: User not found in the system"
        if isinstance(person, Manager):
            branch = system.find_cafe_branch_by_id(branch_id)
            if branch and branch.manager_id != person.user_id:
                return f"You are not Manager of {branch.name}"

        # Create Staff and add to branch
        new_staff = system.create_staff(staff_name, requester_id=auth_id)
        system.add_staff_to_branch(branch_id, new_staff.user_id, requester_id=auth_id)

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
    - auth_id / authorizer_id : OWNER-XXXXX or MANAGER-XXXXX
    - customer_id             : MEMBER-XXXXX
    - amount                  : float, amount to add to total_spent
    """
    try:
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


@mcp.tool()
def create_cafe_branch(auth_id: str, branch_name: str, location: str = "") -> str:
    """Create a new cafe branch. OWNER only.
    e.g. create_cafe_branch("OWNER-00000", "สาขาสยาม", "สยามสแควร์")
    """
    try:
        if not auth_id.startswith("OWNER"):
            return "Authorization Failed: Only Owner can create a new branch"
        person = system.find_person_by_id(auth_id)
        if person is None:
            return f"Authorization Failed: Owner ID {auth_id} not found in the system"

        branch = system.create_cafe_branch(branch_name, location, requester_id=auth_id)
        system.add_owner_to_branch(branch.branch_id, auth_id, requester_id=auth_id)
        return f"Branch created! ID: {branch.branch_id} | Name: {branch.name} | Location: {branch.location}"
    except Exception as e:
        return f"Error: {e}"


@mcp.tool()
def create_manager(auth_id: str, manager_name: str, branch_id: str) -> str:
    """
    Create a new Manager and assign them to a branch. OWNER only.
    e.g. create_manager("OWNER-00000", "Alice", "BRCH-00000")
    """
    try:
        if not auth_id.startswith("OWNER"):
            return "Authorization Failed: Only Owner can create a Manager"
        person = system.find_person_by_id(auth_id)
        if person is None:
            return f"Authorization Failed: Owner ID {auth_id} not found in the system"

        manager = system.create_manager(manager_name, requester_id=auth_id)
        system.add_manager_to_branch(branch_id, manager.user_id, requester_id=auth_id)
        return f"Manager created! ID: {manager.user_id} | Name: {manager.name} | Assigned to: {branch_id}"
    except Exception as e:
        return f"Error: {e}"


@mcp.tool()
def add_board_game_to_branch(
    auth_id: str,
    branch_id: str,
    name: str,
    genre: str,
    price: float,
    min_players: int,
    max_players: int,
    description: str = "",
) -> str:
    """
    Add a board game to a branch (Requires Owner or Manager to authorize).
    e.g. add_board_game_to_branch("OWNER-00000", "BRCH-00000", "Catan", "Strategy", 500, 3, 6)
    """
    try:
        if not (auth_id.startswith("OWNER") or auth_id.startswith("MANAGER")):
            return "Authorization Failed: Only Owner or Manager can add a board game"

        person = system.find_person_by_id(auth_id)
        if person is None:
            return f"Authorization Failed: User ID {auth_id} not found in the system"
        if isinstance(person, Manager):
            branch = system.find_cafe_branch_by_id(branch_id)
            if branch and branch.manager_id != person.user_id:
                return f"You are not Manager of {branch.name}"

        bg = system.create_board_game_to_branch(
            branch_id, name, genre, price, min_players, max_players, description, requester_id=auth_id)
        return (
            f"Board game added! ID: {bg.game_id} | Name: {bg.name} | "
            f"Genre: {bg.genre} | Price: ฿{bg.price:.2f} | "
            f"Players: {bg.min_players}-{bg.max_players}"
        )
    except Exception as e:
        return f"Error: {e}"


@mcp.tool()
def get_active_sessions(branch_id: str) -> str:
    """
    List all active (not yet checked out) play sessions in a branch.
    e.g. get_active_sessions("BRCH-00000")
    """
    try:
        branch = system.find_cafe_branch_by_id(branch_id)
        if branch is None:
            return "Error: Branch not found"
        sessions = branch.get_play_sessions()
        if not sessions:
            return "No active sessions"
        lines = []
        now = system.get_time()  # BUG FIX: use simulated time instead of datetime.now() via is_time_up
        for s in sessions:
            players = ", ".join(s.current_players_id) or "(none)"
            time_info = ""
            if s.reserved_end_time:
                end_str = s.reserved_end_time.strftime('%H:%M')
                status_str = " [⚠️ TIME UP!]" if s.check_time_up(now) else ""
                time_info = f" | Ends: {end_str}{status_str}"
            
            lines.append(
                f"Session: {s.session_id} | Table: {s.table_id} | "
                f"Players: {s.get_total_players()} ({players}){time_info}"
            )
        return "\n".join(lines)
    except Exception as e:
        return f"Error: {e}"


@mcp.tool()
def get_overstayed_sessions(branch_id: str) -> str:
    """List all sessions that have exceeded their reserved time and need checkout.
    Useful for staff to identify tables that need to be freed for next guests.
    """
    try:
        branch = system.find_cafe_branch_by_id(branch_id)
        if branch is None:
            return "Error: Branch not found"
        sessions = branch.get_play_sessions()
        now = system.get_time()  # BUG FIX: use simulated time instead of datetime.now() via is_time_up
        overstayed = [s for s in sessions if s.check_time_up(now)]
        if not overstayed:
            return "No overstayed sessions. All tables are within their time limits."
        
        lines = [f"⚠️ Found {len(overstayed)} sessions that need FORCE CHECKOUT:"]
        for s in overstayed:
            players = ", ".join(s.current_players_id) or "(none)"
            lines.append(
                f"- Session: {s.session_id} | Table: {s.table_id} | "
                f"Reserved End: {s.reserved_end_time.strftime('%H:%M')} | "
                f"Players: {s.get_total_players()} ({players})"
            )
        return "\n".join(lines)
    except Exception as e:
        return f"Error: {e}"


@mcp.tool()
def get_reservations(branch_id: str = None) -> str:
    """
    List all reservations. Optionally filter by branch_id.
    e.g. get_reservations()  or  get_reservations("BRCH-00000")
    """
    try:
        all_reservations = system.reservations
        if branch_id:
            all_reservations = [r for r in all_reservations if r.branch_id == branch_id]
        if not all_reservations:
            return "No reservations found"
        lines = []
        for r in all_reservations:
            lines.append(
                f"ID: {r.reservation_id} | Status: {r.status.value} | "
                f"Customer: {r.customer_id} | Table: {r.table_id} | "
                f"Date: {r.date} {r.start_time}-{r.end_time}"
            )
        return "\n".join(lines)
    except Exception as e:
        return f"Error: {e}"


@mcp.tool()
def get_active_bill(play_session_id: str, current_time: str = None) -> str:
    """Preview the current bill for an ACTIVE (not yet checked out) session.
    Uses current time to estimate duration.
    e.g. get_active_bill("PS-00000")  or  get_active_bill("TABLE-00000")
    current_time format: 'YYYY-MM-DD HH:MM' or ISO. Leave blank to use current time.
    """
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

        # Find the session using BGC_SYSTEM's internal logic
        session = None
        for branch in system.get_cafe_branches():
            found = branch.find_play_session_by_id(play_session_id)
            if found:
                session = found
                break
        
        if session is None:
            return "Error: Active play session not found"
            
        if session.payment is not None:
            return "This session is already checked out. Use bill_history() instead."

        now = parsed_time if parsed_time else system.get_time()
        # Use the system's core calculation logic to ensure consistency with check_out
        active_bill = system.get_active_bill(play_session_id, current_time=now)
        
        duration = session.duration(now) # BUG FIX: added duration calculation
        
        lines = [f"=== Active Bill Preview for {session.session_id} ==="]
        time_limit_str = f" | Reserved until: {session.reserved_end_time.strftime('%H:%M')}" if hasattr(session, 'reserved_end_time') and session.reserved_end_time else ""
        lines.append(f"  Start: {session.start_time.strftime('%Y-%m-%d %H:%M')} | Now: {now.strftime('%H:%M')}{time_limit_str} | Duration: {duration:.2f} hr")
        if hasattr(session, 'check_time_up') and session.check_time_up(now):
            lines.append("  ⚠️ ALERT: TIME IS UP!")
        lines.append("")

        for label, amount in active_bill["items"]:
            if label == "TOTAL":
                continue
            lines.append(f"  {label:<50} : ฿{amount:8.2f}")

        lines.append("-" * 65)
        lines.append(f"  Estimated TOTAL {' ':<32} : ฿{active_bill['total_amount']:8.2f}")
        
        unreturned = session.current_board_games_id
        if unreturned:
            lines.append(f"\n  ⚠️  Unreturned board games: {', '.join(unreturned)}")
        return "\n".join(lines)
    except Exception as e:
        return f"Error: {e}"


@mcp.tool()
def repair_board_game(auth_id: str, board_game_id: str) -> str:
    """Mark a board game in MAINTENANCE as AVAILABLE again (repaired).
    Requires Owner or Manager.
    e.g. repair_board_game("OWNER-00000", "BG-00000")
    """
    try:
        if not (auth_id.startswith("OWNER") or auth_id.startswith("MANAGER")):
            return "Authorization Failed: Only Owner or Manager can repair board games"

        person = system.find_person_by_id(auth_id)
        if person is None:
            return f"Authorization Failed: User ID {auth_id} not found"

        system.maintenance_board_game(board_game_id, requester_id=auth_id)
        return f"Board game {board_game_id} has been repaired and is now AVAILABLE"
    except Exception as e:
        return f"Error: {e}"


@mcp.tool()
def set_system_time(time_str: str) -> str:
    """Sets the system-wide simulated time. 
    Format: 'YYYY-MM-DD HH:MM' or 'YYYY-MM-DDTHH:MM:SS'. 
    Pass an empty string to reset to real-time.
    """
    try:
        reset = not time_str or not time_str.strip()
        result = system.set_simulated_time(None if reset else time_str)
        return result
    except Exception as e:
        return f"Error: {e}"

@mcp.tool()
def get_system_time() -> str:
    """Returns the current system time (either simulated or real)."""
    try:
        now = system.get_time()
        is_simulated = system._CafeSystem__simulated_time is not None
        type_str = "(SIMULATED)" if is_simulated else "(REAL-TIME)"
        return f"{now.strftime('%Y-%m-%d %H:%M:%S')} {type_str}"
    except Exception as e:
        return f"Error: {e}"

@mcp.tool()
def resolve_checkin_conflict(
    session_id: str, 
    staff_id: str, 
    method_type: str = "cash", 
    current_time: str = None, 
    paid_amount: float = None,
    email: str = None,
    card_number: str = None,
    expiry_date: str = None,
    cvv: str = None,
    **kwargs
) -> str:
    """Resolve a check-in conflict by performing an automated force checkout.
    e.g. resolve_checkin_conflict(session_id="PS-00000", staff_id="STAFF-00001", method_type="cash", paid_amount=150.0)
    e.g. resolve_checkin_conflict(session_id="PS-00000", staff_id="STAFF-00001", method_type="card", card_number="1234...", expiry_date="12/26", cvv="123")
    
    current_time format: 'YYYY-MM-DD HH:MM' or ISO.
    """
    try:
        # BUG FIX: validate staff_id exists in the system before calling auto_force_checkout
        if not staff_id.startswith("STAFF"):
            return "Authorization Failed: Only Staff can resolve check-in conflicts"
        person = system.find_person_by_id(staff_id)
        if person is None:
            return f"Authorization Failed: Staff ID {staff_id} not found in the system"

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

        # Call the new specialized method in CafeSystem
        system.auto_force_checkout(
            session_id, staff_id, method_type=method_type, current_time=parsed_time, **kwargs
        )
        return (
            f"Successfully resolved conflict! Session {session_id} has been force-checked out by {staff_id}. "
            f"The table is now available for the new guest."
        )
    except Exception as e:
        return f"Error resolving conflict: {e}"

@mcp.tool()
def auto_force_checkout(
    session_id: str, 
    staff_id: str, 
    method_type: str = "cash", 
    current_time: str = None, 
    paid_amount: float = None,
    email: str = None,
    card_number: str = None,
    expiry_date: str = None,
    cvv: str = None,
    **kwargs
) -> str:
    """Force checkout a play session. Requires Staff authorization.
    Supports 'cash', 'card', and 'online' payment methods.
    """
    try:
        if not staff_id.startswith("STAFF"):
            return "Authorization Failed: Only Staff can perform force checkout"
        
        parsed_time = None
        if current_time is not None:
            for fmt in ("%Y-%m-%dT%H:%M:%S", "%Y-%m-%dT%H:%M", "%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M"):
                try:
                    parsed_time = datetime.strptime(current_time, fmt)
                    break
                except ValueError:
                    continue
        
        system.auto_force_checkout(
            session_id, staff_id, method_type=method_type, current_time=parsed_time,
            paid_amount=paid_amount, email=email, card_number=card_number,
            expiry_date=expiry_date, cvv=cvv, **kwargs
        )
        return f"Successfully force-checked out session {session_id} using {method_type}."
    except Exception as e:
        return f"Error during force checkout: {e}"


if __name__ == "__main__":
    mcp.run()