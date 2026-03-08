from mcp.server.fastmcp import FastMCP
from datetime import datetime
import sys
import os

# --- STEP 1: จัดการ PATH ให้ถูกต้อง ---
# บังคับให้ Python มองเห็นไฟล์ BGC_... ทุกไฟล์ในโฟลเดอร์ปัจจุบัน
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

# --- STEP 2: สร้าง MCP Instance ---
mcp = FastMCP("BoardGameCafe")

# --- STEP 3: โหลดระบบ (ดัก Error การ Import) ---
try:
    from demo__instance import system
except Exception as e:
    # พิมพ์ Error ลง stderr เท่านั้น (ห้าม print ลง stdout)
    print(f"Server Setup Error: {e}", file=sys.stderr)
    sys.exit(1)


# --- STEP 4: สร้าง Tools ให้ Claude ---


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
    """จองโต๊ะ (date_str format: YYYY-MM-DD, time format: HH:MM)
    ตัวอย่างการเรียก: make_reservation("MEMBER_A", "Ladkrabang", 4, "2024-07-01", "18:00", "20:00")
    ใช้ชื่อสาขาในการจองแทน ID เพื่อความสะดวกในการทดสอบ"""
    try:
        member = system.find_person_by_name(customer_name)
        if not member:
            return "ไม่พบชื่อลูกค้านี้ในระบบ"
        branch = system.find_cafe_branch_by_name(branch_name)
        if not branch:
            return "สาขาไม่พบ"
        res = system.make_reservation(
            member.user_id, branch.branch_id, players, date_str, start_t, end_t, table_id
        )
        return f"จองสำเร็จ! ID: {res.reservation_id} ที่โต๊ะ {res.table_id}"
    except Exception as e:
        return f"เกิดข้อผิดพลาด: {str(e)}"


@mcp.tool()
def get_all_cafe_branches() -> str:
    """View all cafe branches with their table counts"""
    branches = system.get_cafe_branches()
    result = []
    for b in branches:
        result.append(
            f"สาขา : {b.name:<25} ( ID : {b.branch_id} ) - โต๊ะ : {b.total_tables}"
        )
    return "\n".join(result) if result else "ไม่มีข้อมูลสาขา"


@mcp.tool()
def get_person_by_type(person_type: str) -> str:
    """Get all persons of a specific type ('Owner', 'Manager', 'Staff', 'Customer_member', 'customer_walk_in')
    pass with CamelCase owner -> Owner (Case Sensitive)
    ประเภทที่รองรับ: 'Owner', 'Manager', 'Staff', 'Member', 'WalkInCustomer'"""
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
            else "ไม่พบข้อมูล"
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
            else "ไม่มีข้อมูลโต๊ะ"
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
            else "ไม่มีโต๊ะว่าง"
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
            else "ไม่มีบอร์ดเกม"
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
            else "ไม่มีเกม"
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
            else "ไม่มีเกม"
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
            else "ไม่มีเมนู"
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
            else "ไม่มีออเดอร์"
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
        return "ยกเลิกสำเร็จ" if res else "ยกเลิกไม่สำเร็จหรือไม่มีข้อมูล"
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
        session = system.check_in_reserved(reservation_id, customer_id, current_time)
        return f"Check in reserved successful! Session ID: {session.session_id}"
    except Exception as e:
        return f"Error: {e}"


@mcp.tool()
def join_session(play_session_id: str, customer_id: str = "walk_in") -> str:
    """Join an existing play session"""
    try:
        system.join_session(play_session_id, customer_id)
        return "เข้าร่วมสำเร็จ"
    except Exception as e:
        return f"Error: {e}"


@mcp.tool()
def borrow_board_game(play_session_id: str, board_game_id: str) -> str:
    """Borrow a board game for a session"""
    try:
        res = system.borrow_board_game(play_session_id, board_game_id)
        return "ยืมสำเร็จ" if res else "ยืมไม่สำเร็จ"
    except Exception as e:
        return f"Error: {e}"


@mcp.tool()
def return_board_game(play_session_id: str, board_game_id: str, is_damaged: bool = False) -> str:
    """Return a board game from a session
    Set is_damaged to true to flag the board game as broken (MAINTENANCE)
    """
    try:
        system.return_board_game(play_session_id, board_game_id, is_damaged=is_damaged)
        return "คืนสำเร็จ"
    except Exception as e:
        return f"Error: {e}"


@mcp.tool()
def take_order(play_session_id: str, menu_item_id: str) -> str:
    """Take an order for a session
    e.g. take_order("PS-00000", "FOOD-00000")
    """
    try:
        order = system.take_order(play_session_id, menu_item_id)
        return f"สั่งอาหารสำเร็จ Order ID: {order.order_id}" if order else "สั่งอาหารไม่สำเร็จ"
    except Exception as e:
        return f"Error: {str(e)}"


@mcp.tool()
def update_order_serve(play_session_id: str, order_id: str) -> str:
    """Update order status to served"""
    try:
        system.update_order_serve(play_session_id, order_id)
        return "อัปเดตสถานะเป็นเสิร์ฟแล้ว"
    except Exception as e:
        return f"Error: {e}"


@mcp.tool()
def update_order_cancel(play_session_id: str, order_id: str) -> str:
    """Cancel an order"""
    try:
        system.update_order_cancel(play_session_id, order_id)
        return "ยกเลิกออเดอร์แล้ว"
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
            
        receipt, total = system.check_out(play_session_id, method_type=method_type, **kwargs)
        return f"Check out successful. Total: {total}, Receipt ID: {receipt.payment_id}"
    except Exception as e:
        return f"Error: {e}"


if __name__ == "__main__":
    mcp.run()
