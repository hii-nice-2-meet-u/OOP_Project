from BGC import *

if __name__ == "__main__":
    sys = CafeSystem()

    sys.add_owner("OWNER_A")
    sys.add_owner("OWNER_B")
    sys.add_manager("MANAGER_A")
    sys.add_manager("MANAGER_B")
    sys.add_manager("MANAGER_C")
    sys.add_manager("MANAGER_D")
    sys.add_customer_member("MEMBER_A")
    sys.add_customer_member("MEMBER_B")
    sys.add_customer_member("MEMBER_C")
    sys.add_customer_member("MEMBER_D")
    sys.add_customer_walk_in()

    for o in [f"{a.name:<15}-  {a.user_id}" for a in sys.person]:
        print(o)
    print(" ")

    # / ================================================================

    sys.add_cafe_branch("Cafe - A", "A 123/456")
    sys.add_cafe_branch("Cafe - B", "B 123/456")
    sys.add_cafe_branch("Cafe - C", "C 123/456")
    sys.add_cafe_branch("Cafe - D", "D 123/456")

    for o in [f"{a.name} | {a.branch_id}" for a in sys.cafe_branches]:
        print(o)
    print(" ")

    # / ================================================================

    for iii in range(4):
        sys.add_table_to_branch("BRCH-0000" + str(iii), 2)
        sys.add_table_to_branch("BRCH-0000" + str(iii), 4)
        sys.add_table_to_branch("BRCH-0000" + str(iii), 6)
        sys.add_table_to_branch("BRCH-0000" + str(iii), 8)

    for iii in range(4):
        branch_id = "BRCH-0000" + str(iii)
        for o in [
            f"{a.table_id} - {a.capacity} - {a.status}"
            for a in sys.get_branch_tables(branch_id)
        ]:
            print(o)
        print(" ")

    # / ================================================================

    for iii in range(4):
        branch_id = "BRCH-0000" + str(iii)
        sys.add_board_game_to_branch(
            branch_id,
            "Uno",
            "classic card game",
            100.00,
            2,
            10,
            "A card game where players take turns matching a card in their hand with the current card shown on top of the deck either by color or number.",
        )
        sys.add_board_game_to_branch(
            branch_id,
            "Monopoly",
            "classic board game",
            200.00,
            2,
            6,
            "A board game where players buy and sell properties, collect rent, and try to bankrupt other players by landing on their properties.",
        )
        sys.add_board_game_to_branch(
            branch_id,
            "Scrabble",
            "classic word game",
            100.00,
            2,
            4,
            "A word game where players take turns to form words from a set of letters.",
        )

    for iii in range(4):
        branch_id = "BRCH-0000" + str(iii)
        print(f"Board Games for {branch_id}:")
        for o in [
            f"{a.name:<15}- {a.genre:20} | {a.price} ฿ | {a.min_players}-{a.max_players} players"
            for a in sys.get_branch_board_games(branch_id)
        ]:
            print(o)
        print(" ")

    # / ================================================================

    for iii in range(4):
        branch_id = "BRCH-0000" + str(iii)
        sys.add_menu_to_branch(branch_id)
        sys.add_menu_item_food_to_branch(branch_id, "ITEM_F1", 11.11)
        sys.add_menu_item_food_to_branch(branch_id, "ITEM_F2", 22.22)
        sys.add_menu_item_drink_to_branch(branch_id, "ITEM_D1", 33.33)
        sys.add_menu_item_drink_to_branch(branch_id, "ITEM_D2", 44.44)

    for iii in range(4):
        branch_id = "BRCH-0000" + str(iii)
        print(f"Menu for {branch_id}:")
        for o in [
            f"{a.name:<10} - {a.price} ฿ | {a.item_id} "
            for a in sys.get_branch_menu_items(branch_id)
        ]:
            print(o)
        print(" ")

    # / ================================================================
