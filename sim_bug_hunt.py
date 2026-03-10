"""
sim_bug_hunt.py — จำลองสถานการณ์ต่างๆ เพื่อหาบัค
"""
import sys as _sys
_sys.path.insert(0, r"c:\Users\champ\Desktop\OOP_Project\OOP_Project")
from BGC import *

PASS = "✅ PASS"
FAIL = "❌ FAIL"
results = []

def run(label, fn):
    try:
        result = fn()
        status = PASS if result is not False else FAIL
        results.append((status, label, ""))
        print(f"{status}  {label}")
    except Exception as e:
        results.append((FAIL, label, str(e)))
        print(f"{FAIL}  {label}\n        └─ {e}")

def expect_error(label, fn, keyword=None):
    try:
        fn()
        results.append((FAIL, label, "Expected error but got none"))
        print(f"{FAIL}  {label}  ← ควร Error แต่ไม่ Error!")
    except Exception as e:
        msg = str(e)
        if keyword and keyword.lower() not in msg.lower():
            results.append((FAIL, label, f"Wrong error: {msg}"))
            print(f"{FAIL}  {label}  ← Error ผิด: {msg}")
        else:
            results.append((PASS, label, msg))
            print(f"{PASS}  {label}  [error: {msg[:70]}]")

# ─────────────────────────────────────────────────────────
print("\n" + "="*60)
print("  BOARD GAME CAFE — BUG HUNT SIMULATION")
print("="*60)

sys2 = CafeSystem()
sys2.set_simulated_time("2026-04-01 10:00")

# ── Setup ─────────────────────────────────────────────
owner = sys2.create_owner("Owner A")
branch = sys2.create_cafe_branch("Siam Cafe", "Bangkok", requester_id=owner.user_id)
bid = branch.branch_id

t1 = sys2.create_table_to_branch(bid, 4, requester_id=owner.user_id)  # capacity 4
t2 = sys2.create_table_to_branch(bid, 2, requester_id=owner.user_id)  # capacity 2
t3 = sys2.create_table_to_branch(bid, 2, requester_id=owner.user_id)  # capacity 2

bg1 = sys2.create_board_game_to_branch(bid, "Catan", "Strategy", 800, 3, 6, requester_id=owner.user_id)
bg2 = sys2.create_board_game_to_branch(bid, "Chess", "Classic", 600, 2, 2, requester_id=owner.user_id)
bg3 = sys2.create_board_game_to_branch(bid, "Risk",  "Strategy", 700, 2, 6, requester_id=owner.user_id)

food  = sys2.create_menu_item_food_to_branch(bid, "Fries", 80, requester_id=owner.user_id)
drink = sys2.create_menu_item_drink_to_branch(bid, "Coke", 60, "M", requester_id=owner.user_id)

member  = sys2.create_customer_member("Alice")
member2 = sys2.create_customer_member("Bob")

# ── Section 1: Walk-in Check-in ──────────────────────
print("\n── 1. WALK-IN CHECK-IN ─────────────────────────────")
wi_session = sys2.check_in(bid, 2, table_id=t2.table_id)  # บน t2 (cap=2)
wi_ps_id   = wi_session.session_id
wi_tbl_id  = wi_session.table_id

run("walk-in checkin สร้าง session ได้", lambda: wi_session is not None)
run("session มี PS- prefix",             lambda: wi_ps_id.startswith("PS-"))

# ── Section 2: Member Check-in ───────────────────────
print("\n── 2. MEMBER CHECK-IN ──────────────────────────────")
run("member checkin ด้วย customer_id ได้", lambda:
    sys2.check_in(bid, 1, customer_id=member.user_id, table_id=t1.table_id) is not None)

mem_session = sys2.check_in(bid, 1, customer_id=member2.user_id, table_id=t3.table_id)
mem_ps_id   = mem_session.session_id

# ── Section 3: Join Session ──────────────────────────
print("\n── 3. JOIN SESSION ─────────────────────────────────")
# t3 cap=2, member2 อยู่คนเดียว → join ได้ 1 คน
run("join session ด้วย PS-ID ได้", lambda:
    sys2.join_session(mem_ps_id) is not False)

expect_error("member ที่อยู่ใน session แล้ว join อีกไม่ได้",
    lambda: sys2.join_session(mem_ps_id, customer_id=member2.user_id),
    keyword="already")

# t3 เต็มแล้ว (member2 + walk-in = 2/2)
expect_error("join session ที่ full ไม่ได้",
    lambda: sys2.join_session(mem_ps_id),
    keyword="capacity")

# ── Section 4: Borrow Board Game ─────────────────────
print("\n── 4. BORROW BOARD GAME ────────────────────────────")
run("ยืมเกมด้วย PS-ID ได้",
    lambda: sys2.borrow_board_game(wi_ps_id, bg1.game_id) is not None)

run("ยืมเกมด้วย TABLE-ID ได้",
    lambda: sys2.borrow_board_game(wi_tbl_id, bg2.game_id) is not None)

# wi_session มี bg1+bg2 แล้ว (2/2)
expect_error("ยืมเกินกว่า 2 เกม/session ไม่ได้",
    lambda: sys2.borrow_board_game(wi_ps_id, bg3.game_id),
    keyword="Maximum")

expect_error("ยืมเกมที่ IN_USE ไม่ได้",
    lambda: sys2.borrow_board_game(mem_ps_id, bg1.game_id),
    keyword="not available")

# ── Section 5: Order Food ────────────────────────────
print("\n── 5. ORDER FOOD ────────────────────────────────────")
run("สั่งอาหารด้วย PS-ID ได้",
    lambda: sys2.take_order(wi_ps_id, food.item_id) is not None)

run("สั่งอาหารด้วย TABLE-ID ได้",
    lambda: sys2.take_order(wi_tbl_id, drink.item_id) is not None)

orders = sys2.get_play_session_orders(wi_ps_id)
run("get_play_session_orders คืน list ≥ 2 รายการ",
    lambda: len(orders) >= 2)

# ── Section 6: Return Board Game ─────────────────────
print("\n── 6. RETURN BOARD GAME ────────────────────────────")
run("คืนเกมปกติ (ไม่เสียหาย)",
    lambda: sys2.return_board_game(wi_ps_id, bg1.game_id, is_damaged=False) is not None)

sys2.borrow_board_game(mem_ps_id, bg3.game_id)
run("คืนเกมพร้อมแจ้งเสียหาย",
    lambda: sys2.return_board_game(mem_ps_id, bg3.game_id, is_damaged=True) is not None)

expect_error("คืนเกมที่ไม่ได้ยืมใน session นี้ Error",
    lambda: sys2.return_board_game(wi_ps_id, bg3.game_id),
    keyword="did not borrow")

# ── Section 7: Active Bill ───────────────────────────
print("\n── 7. ACTIVE BILL ───────────────────────────────────")
sys2.set_simulated_time("2026-04-01 11:30")
now  = sys2.get_time()
bill = sys2.get_active_bill(wi_ps_id, current_time=now)

run("get_active_bill คืน dict ที่มี 'items' และ 'total_amount'",
    lambda: isinstance(bill, dict) and "items" in bill and "total_amount" in bill)

run("ค่า total_amount > 0",
    lambda: bill["total_amount"] > 0)

# ── Section 8: Checkout ──────────────────────────────
print("\n── 8. CHECKOUT ──────────────────────────────────────")
# wi_session ยังมี bg2 ค้างอยู่!
expect_error("checkout session ที่ยังมีเกมค้างอยู่ไม่ได้",
    lambda: sys2.check_out(wi_ps_id, method_type="cash", paid_amount=9999),
    keyword="unreturned")

sys2.return_board_game(wi_ps_id, bg2.game_id)  # คืนก่อน checkout
run("checkout ด้วย cash ได้",
    lambda: sys2.check_out(wi_ps_id, method_type="cash", paid_amount=9999) is not None)

expect_error("checkout session ที่ checkout ไปแล้ว Error",
    lambda: sys2.check_out(wi_ps_id, method_type="cash", paid_amount=9999),
    keyword="already checked out")

# ── Section 9: Bill History ──────────────────────────
print("\n── 9. BILL HISTORY ──────────────────────────────────")
run("bill_history session ที่ checkout แล้วได้",
    lambda: sys2.bill_history(wi_ps_id) is not None)

expect_error("bill_history session ที่ยังไม่ checkout Error",
    lambda: sys2.bill_history(mem_ps_id),
    keyword="not found")

# ── Section 10: Reservation Policy ──────────────────
print("\n── 10. RESERVATION POLICY ───────────────────────────")
wi_id = sys2.create_customer_walk_in().user_id
expect_error("walk-in จองไม่ได้ (ต้องสมัครสมาชิก)",
    lambda: sys2.make_reservation(wi_id, bid, 2,
        "2026-04-04", "14:00", "16:00", method_type="online", email="x@x.com"),
    keyword="not allowed")

# NONE_TIER max 5 วัน: วันนี้ 2026-04-01 → ใช้ 2026-04-04 (+3 วัน)
run("member จองได้ (ภายใน 5 วัน)",
    lambda: sys2.make_reservation(member.user_id, bid, 2,
        "2026-04-04", "14:00", "16:00", method_type="online", email="alice@test.com") is not None)

expect_error("member จองด้วย cash ไม่ได้",
    lambda: sys2.make_reservation(member.user_id, bid, 2,
        "2026-04-03", "14:00", "16:00", method_type="cash"),
    keyword="cash")

# ─────────────────────────────────────────────────────────
print("\n" + "="*60)
passed = sum(1 for s,_,_ in results if s == PASS)
failed = sum(1 for s,_,_ in results if s == FAIL)
total  = len(results)
print(f"  RESULTS: {passed}/{total} passed  |  {failed} failed")
print("="*60)

if failed:
    print("\n🐛 BUGS FOUND:")
    for s, label, msg in results:
        if s == FAIL:
            print(f"  • {label}")
            if msg:
                print(f"    └─ {msg}")
else:
    print("\n🎉 All tests passed!")
