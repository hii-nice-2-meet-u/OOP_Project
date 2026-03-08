from BGC import *
from datetime import datetime, timedelta

fake_time = datetime(2026, 3, 9, 15, 5, 0)

if __name__ == "__main__":
    sys = CafeSystem()

    # / ════════════════════════════════════════════════════════════════

    sys.create_owner("OWNER_A")
    sys.create_manager("MANAGER_A")
    sys.create_staff("STAFF_A")
    sys.create_customer_member("MEMBER_A")
    sys.create_customer_member("MEMBER_B")

    # / ════════════════════════════════════════════════════════════════

    sys.create_cafe_branch("Cafe - A", "A 123/456")

    # / ════════════════════════════════════════════════════════════════

    sys.create_table_to_branch("BRCH-00000", 2)
    sys.create_table_to_branch("BRCH-00000", 4)

    # / ════════════════════════════════════════════════════════════════

    sys.create_board_game_to_branch(
        "BRCH-00000", "Uno", "classic card game", 100.00, 2, 10,
        "A card game where players match cards by color or number.",
    )
    sys.create_board_game_to_branch(
        "BRCH-00000", "Monopoly", "classic board game", 200.00, 2, 6,
        "A board game about buying and selling properties.",
    )

    # / ════════════════════════════════════════════════════════════════

    sys.create_menu_to_branch("BRCH-00000")
    sys.create_menu_item_food_to_branch("BRCH-00000", "ITEM_FOOD_1",  50,  "ข้าวผัด")
    sys.create_menu_item_food_to_branch("BRCH-00000", "ITEM_FOOD_2", 120,  "สเต็ก")
    sys.create_menu_item_drink_to_branch("BRCH-00000", "ITEM_DRINK_1", 60, "กาแฟ")
    sys.create_menu_item_drink_to_branch("BRCH-00000", "ITEM_DRINK_2", 80, "ชานมไข่มุก")

    # / ════════════════════════════════════════════════════════════════

    sys.add_owner_to_branch("BRCH-00000", "OWNER-00000")
    sys.add_manager_to_branch("BRCH-00000", "MANAGER-00000")
    sys.add_staff_to_branch("BRCH-00000", "STAFF-00000")

    # / ════════════════════════════════════════════════════════════════
    # SESSION 1 : MEMBER_A + MEMBER_B

    sys.make_reservation(
        "MEMBER-00000", "BRCH-00000", 2,
        "2026-03-09", "15:00", "16:00", "TABLE-00000",
    )

    play_session_1 = sys.check_in_reserved(
        "RESV-00000", "MEMBER-00000", current_time=fake_time
    )

    sys.join_session("PS-00000", "MEMBER-00001")
    sys.borrow_board_game("TABLE-00000", "BG-00000")
    sys.take_order("TABLE-00000", "FOOD-00000")   # ข้าวผัด  50
    sys.take_order("TABLE-00000", "FOOD-00001")   # สเต็ก  120
    sys.take_order("TABLE-00000", "DRINK-00000")  # กาแฟ    60

    sys.update_order_preparing("PS-00000", "ORDER-00000")
    sys.update_order_serve("PS-00000", "ORDER-00000")
    sys.update_order_preparing("PS-00000", "ORDER-00001")
    sys.update_order_serve("PS-00000", "ORDER-00001")
    sys.update_order_cancel("PS-00000", "ORDER-00002")  # กาแฟ ถูกยกเลิก

    sys.check_out(
        "TABLE-00000",
        method_type="cash",
        end_time=fake_time + timedelta(hours=2),
        paid_amount=9999,
    )

    # / ════════════════════════════════════════════════════════════════
    # SESSION 2 : MEMBER_A อีกครั้ง (โต๊ะเดิม)

    fake_time_2 = datetime(2026, 3, 9, 18, 0, 0)

    play_session_2 = sys.check_in(
        "BRCH-00000", 1, "MEMBER-00000", "TABLE-00000",
        start_time=fake_time_2
    )

    sys.take_order("TABLE-00000", "DRINK-00001")  # ชานมไข่มุก  80
    sys.update_order_preparing("PS-00001", "ORDER-00003")
    sys.update_order_serve("PS-00001", "ORDER-00003")

    sys.check_out(
        "TABLE-00000",
        method_type="cash",
        end_time=fake_time_2 + timedelta(hours=1),
        paid_amount=9999,
    )

    # / ════════════════════════════════════════════════════════════════

    print(f'\n{" TEST - BILL HISTORY (PS-00000) ":═^64}\n')

    items = sys.bill_history("PS-00000")
    for entry in items:
        prefix = ">>> " if entry["item"] == "TOTAL" else "    "
        sign = "-" if entry["price"] < 0 else " "
        print(f"{prefix}{entry['item']:<45} {sign}฿{abs(entry['price']):.2f}")

    print(f'\n{"":═^64}\n')

    # / ════════════════════════════════════════════════════════════════

    print(f'\n{" TEST - BILL HISTORY (PS-00001) ":═^64}\n')

    items2 = sys.bill_history("PS-00001")
    for entry in items2:
        prefix = ">>> " if entry["item"] == "TOTAL" else "    "
        sign = "-" if entry["price"] < 0 else " "
        print(f"{prefix}{entry['item']:<45} {sign}฿{abs(entry['price']):.2f}")

    print(f'\n{"":═^64}\n')

    # / ════════════════════════════════════════════════════════════════

    print(f'\n{" TEST - BILL HISTORY BY PERSON (MEMBER-00000) ":═^64}\n')

    all_bills = sys.bill_history_by_person("MEMBER-00000")
    for record in all_bills:
        print(f"{'─'*64}")
        print(f"  Session : {record['session_id']}  |  Table : {record['table_id']}")
        print(f"  Time    : {record['start_time']} → {record['end_time']}")
        print()
        for entry in record["bill"]:
            prefix = "  >>> " if entry["item"] == "TOTAL" else "      "
            sign = "-" if entry["price"] < 0 else " "
            print(f"{prefix}{entry['item']:<43} {sign}฿{abs(entry['price']):.2f}")
    print(f"{'─'*64}")

    print(f'\n{"":═^64}\n')

    # / ════════════════════════════════════════════════════════════════

    print(f'\n{" TEST - BILL HISTORY BY PERSON (MEMBER-00001) ":═^64}\n')

    all_bills_2 = sys.bill_history_by_person("MEMBER-00001")
    for record in all_bills_2:
        print(f"{'─'*64}")
        print(f"  Session : {record['session_id']}  |  Table : {record['table_id']}")
        print(f"  Time    : {record['start_time']} → {record['end_time']}")
        print()
        for entry in record["bill"]:
            prefix = "  >>> " if entry["item"] == "TOTAL" else "      "
            sign = "-" if entry["price"] < 0 else " "
            print(f"{prefix}{entry['item']:<43} {sign}฿{abs(entry['price']):.2f}")
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

    empty = sys.bill_history_by_person("STAFF-00000")
    print(f'{"RESULT":<10}:\t{"ไม่พบประวัติการใช้บริการ" if not empty else empty}')

    print(f'\n{"":═^64}\n')

# / ════════════════════════════════════════════════════════════════