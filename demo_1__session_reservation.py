from BGC import *

if __name__ == "__main__":
    sys = CafeSystem()

    sys.create_owner("OWNER_A")
    sys.create_manager("MANAGER_A")
    sys.create_staff("STAFF_A")
    sys.create_customer_member("MEMBER_A")

    sys.create_cafe_branch("Cafe - A", "A 123/456")

    sys.create_table_to_branch("BRCH-00000", 2)
    sys.create_table_to_branch("BRCH-00000", 4)
    sys.create_table_to_branch("BRCH-00000", 6)
    sys.create_table_to_branch("BRCH-00000", 8)
    sys.create_table_to_branch("BRCH-00000", 10)

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

    sys.create_menu_to_branch("BRCH-00000")
    sys.create_menu_item_food_to_branch(
        "BRCH-00000", "ITEM_FOOD_1", 11.11, "DESCRIPTION FOOD TEST 1"
    )
    sys.create_menu_item_food_to_branch(
        "BRCH-00000", "ITEM_FOOD_2", 22.22, "DESCRIPTION FOOD TEST 2"
    )
    sys.create_menu_item_drink_to_branch(
        "BRCH-00000", "ITEM_DRINK_1", 33.33, "DESCRIPTION DRINK TEST 1"
    )
    sys.create_menu_item_drink_to_branch(
        "BRCH-00000", "ITEM_DRINK_2", 44.44, "DESCRIPTION DRINK TEST 2"
    )

    sys.add_owner_to_branch("BRCH-00000", "OWNER-00000")
    sys.add_manager_to_branch("BRCH-00000", "MANAGER-00000")
    sys.add_staff_to_branch("BRCH-00000", "STAFF-00000")

    sys.make_reservation(
        "MEMBER-00000", "BRCH-00000", "TABLE-00000", "2025-01-01", "10:00", "11:00"
    )

    
    play_session = sys.check_in_reserved("RESV-00000", "MEMBER-00000")
    # play_session2 = sys.check_in_reserved("RESV-00000", "MEMBER-00000")
    print(play_session.session_id)
    print(play_session.table_id)
    print(play_session.current_players_id)
    print(play_session.current_board_games_id)
    print(play_session.current_order)
    print(play_session.payment)
    # print(play_session2.session_id)
    # print(play_session2.table_id)
    # print(play_session2.current_players_id)
    # print(play_session2.current_board_games_id)
    # print(play_session2.current_order)
    # print(play_session2.payment)