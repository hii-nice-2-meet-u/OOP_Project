import datetime
from BGC_SYSTEM import CafeSystem
from BGC_PLAY_SESSION import Table
from ENUM_STATUS import TableStatus, OrderStatus

def test_smart_force_checkout():
    system = CafeSystem()
    branch = system.create_cafe_branch("Smart Branch")
    table = branch.add_table(4)
    Table.price_per_hour = 20.0
    
    staff = system.create_staff("Staff")
    member = system.create_customer_member("Alice")
    
    # 1. Alice checks in
    start_time = datetime.datetime(2026, 3, 11, 10, 0)
    session = system.check_in(branch.branch_id, 2, customer_id=member.user_id, table_id=table.table_id, start_time=start_time)
    
    # 2. Alice borrows a game and orders food
    game = system.create_board_game_to_branch(branch.branch_id, "Chess", "Strategy", 100, 2, 2)
    system.borrow_board_game(session.session_id, game.game_id, current_time=start_time)
    
    food = system.create_menu_item_food_to_branch(branch.branch_id, "Burger", 50)
    system.take_order(session.session_id, food.item_id, current_time=start_time)
    
    print(f"Initial Session Status:")
    print(f"  Games borrowed: {session.current_board_games_id}")
    print(f"  Orders count: {len(session.current_order)}")
    print(f"  Order 0 status: {session.current_order[0].status}")
    
    # 3. Bob wants the table at 12:00 (Alice is overstayed)
    checkout_time = datetime.datetime(2026, 3, 11, 12, 0)
    
    print(f"\nPerforming Smart Force Checkout...")
    # This should auto-return the game and auto-cancel the order
    system.auto_force_checkout(session.session_id, staff.user_id, method_type="cash", current_time=checkout_time, paid_amount=100.0)
    
    print(f"\nPost-Force Checkout Status:")
    print(f"  Table status: {table.status}")
    print(f"  Games borrowed (should be 0): {len(session.current_board_games_id)}")
    
    # Find the completed session in history
    history = branch.get_play_sessions_history()
    hist_session = next(s for s in history if s.session_id == session.session_id)
    
    print(f"  Order status (should be CANCELLED): {hist_session.current_order[0].status}")
    
    if len(session.current_board_games_id) == 0 and hist_session.current_order[0].status == OrderStatus.CANCELLED:
        print("\nSUCCESS: Smart Force Checkout worked as expected!")
    else:
        print("\nFAILED: Smart Cleanup did not work correctly.")

if __name__ == "__main__":
    test_smart_force_checkout()
