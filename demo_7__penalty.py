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

    # / ════════════════════════════════════════════════════════════════

    sys.create_cafe_branch("Cafe - A", "A 123/456")

    # / ════════════════════════════════════════════════════════════════

    sys.create_table_to_branch("BRCH-00000", 2)
    sys.create_table_to_branch("BRCH-00000", 4)

    # / ════════════════════════════════════════════════════════════════

    sys.create_board_game_to_branch(
        "BRCH-00000",
        "Catan",
        "strategy",
        850.00,
        3,
        6,
        "A strategy board game where players collect resources and build settlements.",
    )
    sys.create_board_game_to_branch(
        "BRCH-00000",
        "Pandemic",
        "cooperative",
        1200.00,
        2,
        4,
        "A cooperative game where players work together to stop global disease outbreaks.",
    )

    # / ════════════════════════════════════════════════════════════════

    sys.create_menu_to_branch("BRCH-00000")
    sys.create_menu_item_food_to_branch(
        "BRCH-00000", "Croissant", 85, "Butter croissant"
    )
    sys.create_menu_item_drink_to_branch(
        "BRCH-00000", "Americano", 65, "Hot americano"
    )

    # / ════════════════════════════════════════════════════════════════

    sys.add_owner_to_branch("BRCH-00000", "OWNER-00000")
    sys.add_manager_to_branch("BRCH-00000", "MANAGER-00000")
    sys.add_staff_to_branch("BRCH-00000", "STAFF-00000")

    # / ════════════════════════════════════════════════════════════════

    play_session = sys.check_in("BRCH-00000", 2, start_time=fake_time)

    # / ════════════════════════════════════════════════════════════════

    sys.join_session("PS-00000", "MEMBER-00001")
    sys.join_session("PS-00000")

    # / ════════════════════════════════════════════════════════════════

    sys.borrow_board_game("TABLE-00000", "BG-00000")   # Catan
    sys.borrow_board_game("TABLE-00000", "BG-00001")   # Pandemic

    # / ════════════════════════════════════════════════════════════════

    sys.take_order("TABLE-00000", "FOOD-00000")   # Croissant
    sys.take_order("TABLE-00000", "DRINK-00000")  # Americano

    sys.update_order_preparing("PS-00000", "ORDER-00000")
    sys.update_order_serve("PS-00000", "ORDER-00000")
    sys.update_order_preparing("PS-00000", "ORDER-00001")
    sys.update_order_serve("PS-00000", "ORDER-00001")

    # / ════════════════════════════════════════════════════════════════
    # TEST — RETURN BOARD GAME (ปกติ)
    # / ════════════════════════════════════════════════════════════════

    print(f'\n{" TEST - RETURN BOARD GAME (OK) ":═^64}\n')
    print(f'{"BEFORE":<10}:\tgame_penalty = { play_session.game_penalty }')
    sys.return_board_game("TABLE-00000", "BG-00000", is_damaged=False)
    print(f'{"AFTER":<10}:\tgame_penalty = { play_session.game_penalty }')
    print(f'{"BG-00000":<10}:\t{ sys.find_board_game_by_id("BG-00000") }')
    print(f'\n{"":═^64}\n')

    # / ════════════════════════════════════════════════════════════════
    # TEST — RETURN BOARD GAME (เสียหาย → เพิ่ม penalty)
    # / ════════════════════════════════════════════════════════════════

    print(f'\n{" TEST - RETURN BOARD GAME (DAMAGED) ":═^64}\n')
    print(f'{"BEFORE":<10}:\tgame_penalty = { play_session.game_penalty }')
    sys.return_board_game("TABLE-00000", "BG-00001", is_damaged=True)
    print(f'{"AFTER":<10}:\tgame_penalty = { play_session.game_penalty }')
    print(f'{"BG-00001":<10}:\t{ sys.find_board_game_by_id("BG-00001") }')
    print(f'\n{"":═^64}\n')

    # / ════════════════════════════════════════════════════════════════
    # TEST — CHECK OUT (มี penalty รวมอยู่ใน total)
    # / ════════════════════════════════════════════════════════════════

    payment = sys.check_out(
        "TABLE-00000",
        method_type="cash",
        end_time=fake_time + timedelta(hours=2),
        paid_amount=2000,
    )
    print(f'\n{" TEST - CHECK OUT (WITH PENALTY) ":═^64}\n')
    print(f'{"PAYMENT":<10}:\t{ payment }')
    print(f'\n{"":═^64}\n')

    # / ════════════════════════════════════════════════════════════════
    # TEST — CHECK OUT ซ้ำ (ต้อง raise ValueError)
    # / ════════════════════════════════════════════════════════════════

    try:
        sys.check_out(
            "TABLE-00000",
            method_type="cash",
            end_time=fake_time + timedelta(hours=2),
            paid_amount=2000,
        )
    except ValueError as e:
        print(f'\n{" TEST - CHECK OUT AGAIN ":═^64}\n')
        print(f'{"ERROR":<10}:\t{ e }')
        print(f'\n{"":═^64}\n')

# / ════════════════════════════════════════════════════════════════