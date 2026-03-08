from BGC import *
from datetime import datetime, timedelta

fake_time = datetime(2026, 3, 9, 15, 5, 0)

if __name__ == "__main__":

    # / ════════════════════════════════════════════════════════════════
    # SETUP — system เดียว สาขาเดียว
    # / ════════════════════════════════════════════════════════════════

    sys = CafeSystem()

    owner = sys.create_owner("OWNER_A")
    manager = sys.create_manager("MANAGER_A")
    staff = sys.create_staff("STAFF_A")
    sys.create_customer_member("MEMBER_A")

    branch = sys.create_cafe_branch("Cafe - A", "A 123/456")
    bid = branch.branch_id

    # สร้างโต๊ะ 6 โต๊ะ (1 โต๊ะต่อ 1 test)
    t = [sys.create_table_to_branch(bid, 2) for _ in range(6)]

    sys.create_board_game_to_branch(bid, "Uno", "classic card game", 100.00, 2, 10, "")
    sys.create_board_game_to_branch(
        bid, "Monopoly", "classic board game", 200.00, 2, 6, ""
    )

    sys.create_menu_to_branch(bid)
    food = sys.create_menu_item_food_to_branch(bid, "ITEM_FOOD_1", 50.00, "Food 1")
    drink = sys.create_menu_item_drink_to_branch(bid, "ITEM_DRINK_1", 40.00, "Drink 1")

    sys.add_owner_to_branch(bid, owner.user_id)
    sys.add_manager_to_branch(bid, manager.user_id)
    sys.add_staff_to_branch(bid, staff.user_id)

    # / ════════════════════════════════════════════════════════════════
    # HELPER — เริ่ม session และสั่ง food + drink (serve แล้ว)
    # / ════════════════════════════════════════════════════════════════

    def start_session(table):
        ps = sys.check_in(bid, 2, table.table_id, start_time=fake_time)
        sys.take_order(table.table_id, food.item_id)
        sys.take_order(table.table_id, drink.item_id)
        order_id = ps.current_order[0].order_id
        sys.update_order_preparing(ps.session_id, order_id)
        sys.update_order_serve(ps.session_id, order_id)
        return ps

    # / ════════════════════════════════════════════════════════════════
    # TEST 1 — CASH
    # / ════════════════════════════════════════════════════════════════

    print(f'\n{" TEST 1 - PAYMENT : CASH ":═^64}\n')

    start_session(t[0])
    try:
        a = sys.check_out(
            t[0].table_id,
            method_type="cash",
            end_time=fake_time + timedelta(hours=2),
            paid_amount=500,
        )
        print(f'{"PAYMENT":<10}:\t{a}')
        print(f'{"METHOD":<10}:\t{a.payment_method.__class__.__name__}')
        print(f'{"CHANGE":<10}:\t{a.payment_method.change:.2f}')
    except Exception as e:
        print(f'{"ERROR":<10}:\t{e}')

    print(f'\n{"":═^64}\n')

    # / ════════════════════════════════════════════════════════════════
    # TEST 2 — CREDIT CARD
    # / ════════════════════════════════════════════════════════════════

    print(f'\n{" TEST 2 - PAYMENT : CREDIT CARD ":═^64}\n')

    start_session(t[1])
    try:
        a = sys.check_out(
            t[1].table_id,
            method_type="card",
            end_time=fake_time + timedelta(hours=2),
            card_number="4111111111111111",
            expiry_date="12/28",
            cvv="123",
        )
        print(f'{"PAYMENT":<10}:\t{a}')
        print(f'{"METHOD":<10}:\t{a.payment_method.__class__.__name__}')
    except Exception as e:
        print(f'{"ERROR":<10}:\t{e}')

    print(f'\n{"":═^64}\n')

    # / ════════════════════════════════════════════════════════════════
    # TEST 3 — ONLINE PAYMENT
    # / ════════════════════════════════════════════════════════════════

    print(f'\n{" TEST 3 - PAYMENT : ONLINE ":═^64}\n')

    start_session(t[2])
    try:
        a = sys.check_out(
            t[2].table_id,
            method_type="online",
            end_time=fake_time + timedelta(hours=2),
            email="customer@example.com",
        )
        print(f'{"PAYMENT":<10}:\t{a}')
        print(f'{"METHOD":<10}:\t{a.payment_method.__class__.__name__}')
    except Exception as e:
        print(f'{"ERROR":<10}:\t{e}')

    print(f'\n{"":═^64}\n')

    # / ════════════════════════════════════════════════════════════════
    # TEST 4 — INVALID PAYMENT METHOD (SHOULD ERROR)
    # / ════════════════════════════════════════════════════════════════

    print(f'\n{" TEST 4 - PAYMENT : INVALID METHOD (SHOULD ERROR) ":═^64}\n')

    start_session(t[3])
    try:
        a = sys.check_out(
            t[3].table_id,
            method_type="bitcoin",
            end_time=fake_time + timedelta(hours=2),
        )
        print(f'{"PAYMENT":<10}:\t{a}')
    except ValueError as e:
        print(f'{"ERROR":<10}:\t{e}')

    print(f'\n{"":═^64}\n')

    # / ════════════════════════════════════════════════════════════════
    # TEST 5 — CASH ไม่พอ (SHOULD ERROR)
    # / ════════════════════════════════════════════════════════════════

    print(f'\n{" TEST 5 - PAYMENT : CASH NOT ENOUGH (SHOULD ERROR) ":═^64}\n')

    start_session(t[4])
    try:
        a = sys.check_out(
            t[4].table_id,
            method_type="cash",
            end_time=fake_time + timedelta(hours=2),
            paid_amount=10,
        )
        print(f'{"PAYMENT":<10}:\t{a}')
    except ValueError as e:
        print(f'{"ERROR":<10}:\t{e}')

    print(f'\n{"":═^64}\n')

    # / ════════════════════════════════════════════════════════════════
    # TEST 6 — จ่ายซ้ำ (SHOULD ERROR)
    # / ════════════════════════════════════════════════════════════════

    print(f'\n{" TEST 6 - PAYMENT : DUPLICATE CHECKOUT (SHOULD ERROR) ":═^64}\n')

    start_session(t[5])
    try:
        a = sys.check_out(
            t[5].table_id,
            method_type="cash",
            end_time=fake_time + timedelta(hours=2),
            paid_amount=500,
        )
        print(f'{"1st PAYMENT":<12}:\t{a}')
    except Exception as e:
        print(f'{"ERROR":<12}:\t{e}')

    try:
        a = sys.check_out(
            t[5].table_id,
            method_type="cash",
            end_time=fake_time + timedelta(hours=2),
            paid_amount=500,
        )
        print(f'{"2nd PAYMENT":<12}:\t{a}')
    except ValueError as e:
        print(f'{"ERROR":<12}:\t{e}')

    print(f'\n{"":═^64}\n')

# / ════════════════════════════════════════════════════════════════
