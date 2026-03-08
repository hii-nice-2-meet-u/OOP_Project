from BGC import *
from datetime import datetime, timedelta
from ENUM_STATUS import MemberTier

fake_time = datetime(2026, 3, 9, 15, 0, 0)

if __name__ == "__main__":
    sys = CafeSystem()

    # ═══════════════════════════════════════════════
    # CREATE PEOPLE
    # ═══════════════════════════════════════════════

    owner = sys.create_owner("OWNER_A")
    manager = sys.create_manager("MANAGER_A")
    staff = sys.create_staff("STAFF_A")

    m1 = sys.create_customer_member("Alice")
    m2 = sys.create_customer_member("Bob")

    m1.member_tier = MemberTier.SILVER
    m2.member_tier = MemberTier.GOLD

    # ═══════════════════════════════════════════════
    # CREATE BRANCH
    # ═══════════════════════════════════════════════

    sys.create_cafe_branch("Cafe A", "Bangkok")

    sys.add_owner_to_branch("BRCH-00000", owner.user_id)
    sys.add_manager_to_branch("BRCH-00000", manager.user_id)
    sys.add_staff_to_branch("BRCH-00000", staff.user_id)

    # ═══════════════════════════════════════════════

    sys.create_table_to_branch("BRCH-00000", 4)

    # ═══════════════════════════════════════════════
    # MENU
    # ═══════════════════════════════════════════════

    sys.create_menu_to_branch("BRCH-00000")

    sys.create_menu_item_food_to_branch("BRCH-00000", "Pizza", 200, "Pizza test")

    sys.create_menu_item_drink_to_branch("BRCH-00000", "Cola", 50, "Drink test")

    # ═══════════════════════════════════════════════
    # WALK IN
    # ═══════════════════════════════════════════════

    play_session = sys.check_in("BRCH-00000", 2, start_time=fake_time)

    sys.join_session(play_session.session_id, m1.user_id)
    sys.join_session(play_session.session_id, m2.user_id)

    # ═══════════════════════════════════════════════
    # ORDER
    # ═══════════════════════════════════════════════

    sys.take_order("TABLE-00000", "FOOD-00000")
    sys.take_order("TABLE-00000", "DRINK-00000")

    sys.update_order_preparing(play_session.session_id, "ORDER-00000")
    sys.update_order_serve(play_session.session_id, "ORDER-00000")

    sys.update_order_preparing(play_session.session_id, "ORDER-00001")
    sys.update_order_serve(play_session.session_id, "ORDER-00001")

    # ═══════════════════════════════════════════════
    # CHECK OUT
    # ═══════════════════════════════════════════════

    payment = sys.check_out(
        "TABLE-00000",
        method_type="cash",
        end_time=fake_time + timedelta(hours=2),
        paid_amount=1000,
    )

    # ═══════════════════════════════════════════════
    # PRINT RESULT
    # ═══════════════════════════════════════════════

    print("\n", " CHECKOUT RESULT ".center(60, "="), "\n")

    print("Players:", play_session.current_players_id)

    discount = 0
    for pid in play_session.current_players_id:
        p = sys.find_person_by_id(pid)
        if isinstance(p, Member):
            discount = max(discount, p.get_discount())

    print("Discount applied:", discount)
    print(payment)
    print("\n", "=" * 60)
