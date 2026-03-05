from BGC import *

if __name__ == "__main__":
    sys = CafeSystem()

    sys.add_owner("OWNER_A")
    sys.add_manager("MANAGER_A")
    sys.add_staff("STAFF_A")
    sys.add_customer_member("MEMBER_A")

    sys.add_cafe_branch("Cafe - A", "A 123/456")

    sys.add_table_to_branch("BRCH-00000", 2)
    sys.add_table_to_branch("BRCH-00000", 4)
    sys.add_table_to_branch("BRCH-00000", 6)
    sys.add_table_to_branch("BRCH-00000", 8)
    sys.add_table_to_branch("BRCH-00000", 10)

    sys.add_board_game_to_branch(
        "BRCH-00000",
        "Uno",
        "classic card game",
        100.00,
        2,
        10,
        "A card game where players take turns matching a card in their hand with the current card shown on top of the deck either by color or number.",
    )
    sys.add_board_game_to_branch(
        "BRCH-00000",
        "Monopoly",
        "classic board game",
        200.00,
        2,
        6,
        "A board game where players buy and sell properties, collect rent, and try to bankrupt other players by landing on their properties.",
    )
    sys.add_board_game_to_branch(
        "BRCH-00000",
        "Scrabble",
        "classic word game",
        100.00,
        2,
        4,
        "A word game where players take turns to form words from a set of letters.",
    )

    sys.add_menu_to_branch("BRCH-00000")
    sys.add_menu_item_food_to_branch(
        "BRCH-00000", "ITEM_FOOD_1", 11.11, "DESCRIPTION FOOD TEST 1"
    )
    sys.add_menu_item_food_to_branch(
        "BRCH-00000", "ITEM_FOOD_2", 22.22, "DESCRIPTION FOOD TEST 2"
    )
    sys.add_menu_item_drink_to_branch(
        "BRCH-00000", "ITEM_DRINK_1", 33.33, "DESCRIPTION DRINK TEST 1"
    )
    sys.add_menu_item_drink_to_branch(
        "BRCH-00000", "ITEM_DRINK_2", 44.44, "DESCRIPTION DRINK TEST 2"
    )
