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
    sys.create_table_to_branch("BRCH-00000", 6)
    sys.create_table_to_branch("BRCH-00000", 8)
    sys.create_table_to_branch("BRCH-00000", 10)

    # / ════════════════════════════════════════════════════════════════

    sys.create_board_game_to_branch(
        "BRCH-00000",
        "Uno",
        "classic card game",
        100.00,
        2,
        10,
        "A card game where players take turns matching a card in their hand with the current card shown on top of the deck either by color or number.",
    )
    sys.create_board_game_to_branch(
        "BRCH-00000",
        "Monopoly",
        "classic board game",
        200.00,
        2,
        6,
        "A board game where players buy and sell properties, collect rent, and try to bankrupt other players by landing on their properties.",
    )
    sys.create_board_game_to_branch(
        "BRCH-00000",
        "Scrabble",
        "classic word game",
        100.00,
        2,
        4,
        "A word game where players take turns to form words from a set of letters.",
    )

    # / ════════════════════════════════════════════════════════════════

    sys.create_menu_to_branch("BRCH-00000")
    sys.create_menu_item_food_to_branch(
        "BRCH-00000", "ITEM_FOOD_1", 10.00, "DESCRIPTION FOOD TEST 1"
    )
    sys.create_menu_item_food_to_branch(
        "BRCH-00000", "ITEM_FOOD_2", 20.00, "DESCRIPTION FOOD TEST 2"
    )
    sys.create_menu_item_drink_to_branch(
        "BRCH-00000", "ITEM_DRINK_1", 10.00, "DESCRIPTION DRINK TEST 1"
    )
    sys.create_menu_item_drink_to_branch(
        "BRCH-00000", "ITEM_DRINK_2", 20.00, "DESCRIPTION DRINK TEST 2"
    )

    # / ════════════════════════════════════════════════════════════════

    sys.add_owner_to_branch("BRCH-00000", "OWNER-00000")
    sys.add_manager_to_branch("BRCH-00000", "MANAGER-00000")
    sys.add_staff_to_branch("BRCH-00000", "STAFF-00000")

    # / ════════════════════════════════════════════════════════════════

    play_session = sys.check_in_member("BRCH-00000", 2, "MEMBER-00000", start_time=fake_time)

    # / ════════════════════════════════════════════════════════════════

    print(f'\n{" TEST - ADD CUSTOMER TO SESSION ":═^64}\n')
    print(
        f'{"BEFORE":<10}:\t{ play_session.current_players_id } ',
    )
    sys.join_session("PS-00000", "MEMBER-00001")
    sys.join_session("PS-00000")
    print(
        f'{"AFTER":<10}:\t{ play_session.current_players_id } ',
    )
    print(f'\n{"":═^64}\n')

    # / ════════════════════════════════════════════════════════════════

    print(f'\n{" TEST - BORROW BOARD GAME ":═^64}\n')
    print(
        f'{"BEFORE":<10}:\t{ play_session.current_board_games_id } ',
    )
    sys.borrow_board_game("TABLE-00000", "BG-00000")
    sys.borrow_board_game("TABLE-00000", "BG-00001")
    sys.borrow_board_game("TABLE-00000", "BG-00002")
    print(
        f'{"AFTER":<10}:\t{ play_session.current_board_games_id } ',
    )
    print(f'\n{"":═^64}\n')

    # / ════════════════════════════════════════════════════════════════

    print(f'\n{" TEST - TAKE ORDER ":═^64}\n')
    print(
        f'{"BEFORE":<10}:\t{ [a.menu_items.name for a in play_session.current_order] } ',
    )
    sys.take_order("TABLE-00000", "FOOD-00000")
    sys.take_order("TABLE-00000", "DRINK-00000")
    print(
        f'{"AFTER":<10}:\t{ [a.menu_items.name for a in play_session.current_order] } ',
    )
    print(f'\n{"":═^64}\n')

    # / ════════════════════════════════════════════════════════════════

    sys.update_order_preparing("PS-00000", "ORDER-00000")
    sys.update_order_serve("PS-00000", "ORDER-00000")

    # / ════════════════════════════════════════════════════════════════


    a = sys.check_out(
        "TABLE-00000",
        method_type="cash",
        end_time=fake_time + timedelta(hours=2),
        paid_amount=500,
    )
    print(f'\n{" TEST - CHECK OUT ":═^64}\n')
    print(f'{"PAYMENT":<10}:\t{ a } ')
    print(f'\n{"":═^64}\n')

    # / ════════════════════════════════════════════════════════════════