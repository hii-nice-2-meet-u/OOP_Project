from BGC import *
from datetime import datetime, timedelta

fake_time = datetime(2026, 3, 9, 15, 5, 0)

if __name__ == "__main__":
    sys = CafeSystem()

    # / ════════════════════════════════════════════════════════════════

    owner    = sys.create_owner("OWNER_A")
    manager  = sys.create_manager("MANAGER_A")
    staff    = sys.create_staff("STAFF_A")
    member_a = sys.create_customer_member("MEMBER_A")
    member_b = sys.create_customer_member("MEMBER_B")

    # / ════════════════════════════════════════════════════════════════

    branch = sys.create_cafe_branch("Cafe - A", "A 123/456")

    # / ════════════════════════════════════════════════════════════════

    sys.create_table_to_branch(branch.branch_id, 2)
    sys.create_table_to_branch(branch.branch_id, 4)

    # / ════════════════════════════════════════════════════════════════

    sys.create_board_game_to_branch(
        branch.branch_id, "Uno", "classic card game", 100.00, 2, 10,
        "A card game where players match cards by color or number.",
    )
    sys.create_board_game_to_branch(
        branch.branch_id, "Monopoly", "classic board game", 200.00, 2, 6,
        "A board game about buying and selling properties.",
    )

    # / ════════════════════════════════════════════════════════════════

    sys.create_menu_to_branch(branch.branch_id)
    sys.create_menu_item_food_to_branch(branch.branch_id, "ITEM_FOOD_1",  50,  "ข้าวผัด")
    sys.create_menu_item_food_to_branch(branch.branch_id, "ITEM_FOOD_2", 120,  "สเต็ก")
    sys.create_menu_item_drink_to_branch(branch.branch_id, "ITEM_DRINK_1", 60, "กาแฟ")
    sys.create_menu_item_drink_to_branch(branch.branch_id, "ITEM_DRINK_2", 80, "ชานมไข่มุก")

    # / ════════════════════════════════════════════════════════════════

    sys.add_owner_to_branch(branch.branch_id, owner.user_id)
    sys.add_manager_to_branch(branch.branch_id, manager.user_id)
    sys.add_staff_to_branch(branch.branch_id, staff.user_id)

    # / ════════════════════════════════════════════════════════════════
    # SESSION 1 : MEMBER_A + MEMBER_B

    reservation = sys.make_reservation(
        member_a.user_id, branch.branch_id, 2,
        "2026-03-09", "15:00", "16:00", "TABLE-00000",
    )

    play_session_1 = sys.check_in_reserved(
        reservation.reservation_id, member_a.user_id, current_time=fake_time
    )

    sys.join_session(play_session_1.session_id, member_b.user_id)
    sys.borrow_board_game(play_session_1.session_id, "BG-00000")

    order_0 = sys.take_order(play_session_1.session_id, "FOOD-00000")   # ข้าวผัด  50
    order_1 = sys.take_order(play_session_1.session_id, "FOOD-00001")   # สเต็ก  120
    order_2 = sys.take_order(play_session_1.session_id, "DRINK-00000")  # กาแฟ    60

    sys.update_order_preparing(play_session_1.session_id, order_0.order_id)
    sys.update_order_serve(play_session_1.session_id, order_0.order_id)
    sys.update_order_preparing(play_session_1.session_id, order_1.order_id)
    sys.update_order_serve(play_session_1.session_id, order_1.order_id)
    sys.update_order_cancel(play_session_1.session_id, order_2.order_id)  # กาแฟ ถูกยกเลิก

    sys.check_out(
        play_session_1.session_id,
        method_type="cash",
        end_time=fake_time + timedelta(hours=2),
        paid_amount=9999,
    )

    # / ════════════════════════════════════════════════════════════════
    # SESSION 2 : MEMBER_A อีกครั้ง (โต๊ะเดิม)

    fake_time_2 = datetime(2026, 3, 9, 18, 0, 0)

    play_session_2 = sys.check_in(
        branch.branch_id, 1, member_a.user_id, "TABLE-00000",
        start_time=fake_time_2
    )

    order_3 = sys.take_order(play_session_2.session_id, "DRINK-00001")  # ชานมไข่มุก  80
    sys.update_order_preparing(play_session_2.session_id, order_3.order_id)
    sys.update_order_serve(play_session_2.session_id, order_3.order_id)

    sys.check_out(
        play_session_2.session_id,
        method_type="cash",
        end_time=fake_time_2 + timedelta(hours=1),
        paid_amount=9999,
    )

    # / ════════════════════════════════════════════════════════════════

    print(f'\n{" TEST - BILL HISTORY (SESSION 1) ":═^64}\n')

    for label, price in sys.bill_history(play_session_1.session_id):
        prefix = ">>> " if label == "TOTAL" else "    "
        sign = "-" if price < 0 else " "
        print(f"{prefix}{label:<45} {sign}฿{abs(price):.2f}")

    print(f'\n{"":═^64}\n')

    # / ════════════════════════════════════════════════════════════════

    print(f'\n{" TEST - BILL HISTORY (SESSION 2) ":═^64}\n')

    for label, price in sys.bill_history(play_session_2.session_id):
        prefix = ">>> " if label == "TOTAL" else "    "
        sign = "-" if price < 0 else " "
        print(f"{prefix}{label:<45} {sign}฿{abs(price):.2f}")

    print(f'\n{"":═^64}\n')

    # / ════════════════════════════════════════════════════════════════

    print(f'\n{" TEST - BILL HISTORY BY PERSON (MEMBER_A) ":═^64}\n')

    for label, price in sys.bill_history_by_person(member_a.user_id):
        if price is None:
            print(f"{'─'*64}")
            print(f"  {label}")
        elif label == "TOTAL":
            print(f"  >>> {label:<43}  ฿{price:.2f}")
        else:
            sign = "-" if price < 0 else " "
            print(f"      {label:<43} {sign}฿{abs(price):.2f}")
    print(f"{'─'*64}")

    print(f'\n{"":═^64}\n')

    # / ════════════════════════════════════════════════════════════════

    print(f'\n{" TEST - BILL HISTORY BY PERSON (MEMBER_B) ":═^64}\n')

    for label, price in sys.bill_history_by_person(member_b.user_id):
        if price is None:
            print(f"{'─'*64}")
            print(f"  {label}")
        elif label == "TOTAL":
            print(f"  >>> {label:<43}  ฿{price:.2f}")
        else:
            sign = "-" if price < 0 else " "
            print(f"      {label:<43} {sign}฿{abs(price):.2f}")
    print(f"{'─'*64}")

    print(f'\n{"":═^64}\n')

    # / ════════════════════════════════════════════════════════════════
    # TEST BILL HISTORY NOT FOUND (SHOULD ERROR)

    try:
        sys.bill_history("PS-99999")
    except Exception as e:
        print(f'\n{" TEST - BILL HISTORY NOT FOUND ":═^64}\n')
        print(f'{"ERROR":<10}:\t{e}')
        print(f'\n{"":═^64}\n')

    # / ════════════════════════════════════════════════════════════════
    # TEST BILL HISTORY BY PERSON ที่ไม่เคยใช้บริการ (SHOULD EMPTY)

    print(f'\n{" TEST - BILL HISTORY BY PERSON NO HISTORY ":═^64}\n')

    empty = sys.bill_history_by_person(staff.user_id)
    print(f'{"RESULT":<10}:\t{"ไม่พบประวัติการใช้บริการ" if not empty else empty}')

    print(f'\n{"":═^64}\n')

# / ════════════════════════════════════════════════════════════════