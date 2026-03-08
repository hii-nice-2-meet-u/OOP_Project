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
        return (
            "\n".join([f"ID: {p.user_id}, Name: {p.name}" for p in persons])
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
def add_spent(customer_id: str, amount: float, authorizer_id: str) -> str:
    """Add total spent to a customer's account to increase their tier.
    Only an Owner or Manager can authorize this action.
    """
    try:
        customer = system.add_spent(customer_id, amount, authorizer_id)
        return f"Added {amount} spent to {customer.name}. New total: {customer.total_spent}. New tier: {customer.get_member_tier().name}"
    except Exception as e:
        return f"Error: {e}"


@mcp.tool()
def cancel_reservation(reservation_id: str) -> str:
    """Cancel a reservation by ID"""
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
def return_board_game(play_session_id: str, board_game_id: str) -> str:
    """Return a board game from a session"""
    try:
        res = system.return_board_game(play_session_id, board_game_id)
        return "คืนสำเร็จ" if res else "คืนไม่สำเร็จ"
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
def bill_history(play_session_id: str) -> str:
    """ดูใบเสร็จย้อนหลังของ session ที่ checkout แล้ว (ใช้ PS- เท่านั้น)
    e.g. bill_history("PS-00000")
    """
    try:
        items = system.bill_history(play_session_id)
        lines = []
        for entry in items:
            prefix = ">>> " if entry["item"] == "TOTAL" else "    "
            sign = "-" if entry["price"] < 0 else " "
            lines.append(f"{prefix}{entry['item']:<45} {sign}฿{abs(entry['price']):.2f}")
        return "\n".join(lines)
    except Exception as e:
        return f"Error: {e}"


@mcp.tool()
def bill_history_by_person(person_id: str) -> str:
    """ดูประวัติใบเสร็จทุก session ของ person คนนึง
    e.g. bill_history_by_person("MEMBER-00000")
    """
    try:
        all_bills = system.bill_history_by_person(person_id)
        if not all_bills:
            return "ไม่พบประวัติการใช้บริการ"
        lines = []
        for record in all_bills:
            lines.append(f"{'─'*64}")
            lines.append(f"  Session : {record['session_id']}  |  Table : {record['table_id']}")
            lines.append(f"  Time    : {record['start_time']} → {record['end_time']}")
            lines.append("")
            for entry in record["bill"]:
                prefix = "  >>> " if entry["item"] == "TOTAL" else "      "
                sign = "-" if entry["price"] < 0 else " "
                lines.append(f"{prefix}{entry['item']:<43} {sign}฿{abs(entry['price']):.2f}")
        lines.append(f"{'─'*64}")
        return "\n".join(lines)
    except Exception as e:
        return f"Error: {e}"
@mcp.tool()
def check_out(play_session_id: str, method_type: str = "cash") -> str:
    """Check out a session and generate receipt"""
    try:
        receipt, total = system.check_out(play_session_id, method_type=method_type)
        return f"Check out successful. Total: {total}, Receipt ID: {receipt.payment_id}"
    except Exception as e:
        return f"Error: {e}"


if __name__ == "__main__":
    mcp.run()
