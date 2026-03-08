import sys
import os
from datetime import datetime
from mcp.server.fastmcp import FastMCP

# --- STEP 1: จัดการ PATH ให้ถูกต้อง ---
# บังคับให้ Python มองเห็นไฟล์ BGC_... ทุกไฟล์ในโฟลเดอร์ปัจจุบัน
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

# --- STEP 2: สร้าง MCP Instance ---
mcp = FastMCP("BoardGameCafe")

# --- STEP 3: โหลดระบบ (ดัก Error การ Import) ---
try:
    from BGC_SYSTEM import CafeSystem

    system = CafeSystem()
    # สร้างข้อมูลจำลอง (ถ้าต้องการทดสอบ)
    branch = system.create_cafe_branch("BRCH-00000", "Ladkrabang")
    system.create_table_to_branch(branch.branch_id, 4)
except Exception as e:
    # พิมพ์ Error ลง stderr เท่านั้น (ห้าม print ลง stdout)
    print(f"Server Setup Error: {e}", file=sys.stderr)
    sys.exit(1)


# / ════════════════════════════════════════════════════════════════

system.create_owner("OWNER_A")
system.create_manager("MANAGER_A")
system.create_staff("STAFF_A")
system.create_customer_member("MEMBER_A")
system.create_customer_member("MEMBER_B")

# / ════════════════════════════════════════════════════════════════

# / ════════════════════════════════════════════════════════════════

system.create_table_to_branch("BRCH-00000", 2)
system.create_table_to_branch("BRCH-00000", 4)
system.create_table_to_branch("BRCH-00000", 6)
system.create_table_to_branch("BRCH-00000", 8)
system.create_table_to_branch("BRCH-00000", 10)

# / ════════════════════════════════════════════════════════════════

system.create_board_game_to_branch(
    "BRCH-00000",
    "Uno",
    "classic card game",
    100.00,
    2,
    10,
    "A card game where players take turns matching a card in their hand with the current card shown on top of the deck either by color or number.",
)
system.create_board_game_to_branch(
    "BRCH-00000",
    "Monopoly",
    "classic board game",
    200.00,
    2,
    6,
    "A board game where players buy and sell properties, collect rent, and try to bankrupt other players by landing on their properties.",
)
system.create_board_game_to_branch(
    "BRCH-00000",
    "Scrabble",
    "classic word game",
    100.00,
    2,
    4,
    "A word game where players take turns to form words from a set of letters.",
)

# / ════════════════════════════════════════════════════════════════

system.create_menu_to_branch("BRCH-00000")
system.create_menu_item_food_to_branch(
    "BRCH-00000", "ITEM_FOOD_1", 10, "DESCRIPTION FOOD TEST 1"
)
system.create_menu_item_food_to_branch(
    "BRCH-00000", "ITEM_FOOD_2", 20, "DESCRIPTION FOOD TEST 2"
)
system.create_menu_item_drink_to_branch(
    "BRCH-00000", "ITEM_DRINK_1", 10, "DESCRIPTION DRINK TEST 1"
)
system.create_menu_item_drink_to_branch(
    "BRCH-00000", "ITEM_DRINK_2", 20, "DESCRIPTION DRINK TEST 2"
)

# / ════════════════════════════════════════════════════════════════

system.add_owner_to_branch("BRCH-00000", "OWNER-00000")
system.add_manager_to_branch("BRCH-00000", "MANAGER-00000")
system.add_staff_to_branch("BRCH-00000", "STAFF-00000")


# --- STEP 4: สร้าง Tools ให้ Claude ---


@mcp.tool()
def make_reservation(
    customer_name: str,
    branch_name: str,
    players: int,
    date_str: str,
    start_t: str,
    end_t: str,
) -> str:
    """จองโต๊ะ (date_str format: YYYY-MM-DD, time format: HH:MM)
    ตัวอย่างการเรียก: make_reservation("MEMBER_A", "Ladkrabang", 4, "2024-07-01", "18:00", "20:00")
    ใช้ชื่อสาขาในการจองแทน ID เพื่อความสะดวกในการทดสอบ"""
    try:
        # สมมติว่าสร้าง Member ใหม่เพื่อทดสอบการจอง
        member = system.create_customer_member(customer_name)
        branch = system.find_cafe_branch_by_name(branch_name)
        if not branch:
            return "สาขาไม่พบ"
        res = system.make_reservation(
            member.user_id, branch.branch_id, players, date_str, start_t, end_t
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
        result.append(f"สาขา: {b.name} (ID: {b.branch_id}) - โต๊ะ: {b.total_tables}")
    return "\n".join(result) if result else "ไม่มีข้อมูลสาขา"


if __name__ == "__main__":
    mcp.run()
