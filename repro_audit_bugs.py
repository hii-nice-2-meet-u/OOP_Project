from _Project_instance import system
from BGC_PERSON import Member, WalkInCustomer
from BGC_SYSTEM import Table
from ENUM_STATUS import MemberTier
import datetime

def test_audit_bugs():
    print("--- 1. Testing Initial Tier Bug ---")
    member = Member("New Guy")
    print(f"New Member Tier: {member.get_member_tier()} (Expected: MemberTier.BRONZE?)")
    
    print("\n--- 2. Testing Damage Penalty Visibility ---")
    # Setup a session
    branch_id = "BRCH-00000"
    table_id = "TABLE-00000"
    game_id = "BG-00000" # Uno
    
    # Force check-in
    now = datetime.datetime.now()
    session = system.check_in(branch_id, player_amount=1, customer_id="WALK-99999", table_id=table_id, start_time=now)
    print(f"Session Created: {session.session_id}")
    
    # Borrow and return damaged
    system.borrow_board_game(session.session_id, game_id, current_time=now)
    system.return_board_game(session.session_id, game_id, is_damaged=True)
    
    # Check bill
    bill = system.get_active_bill(session.session_id, current_time=now + datetime.timedelta(hours=1))
    print("Bill Items:")
    found_penalty = False
    for label, amount in bill["items"]:
        print(f"  {label}: {amount}")
        if "Penalty" in label: found_penalty = True
    
    if not found_penalty:
        print("BUG CONFIRMED: Penalty not visible in active bill.")

    print("\n--- 3. Testing Session State Inconsistency ---")
    # This is trickier to reproduce without staff_id and exact sequence, 
    # but let's try a regular checkout first.
    try:
        system.check_out(session.session_id, method_type="cash", paid_amount=500)
        print(f"First Checkout Success for {session.session_id}")
        
        # Second checkout should fail with "already checked out"
        try:
            system.check_out(session.session_id, method_type="cash", paid_amount=500)
        except ValueError as e:
            print(f"Second Checkout Expected Failure: {e}")
            
    except Exception as e:
        print(f"Checkout Error: {e}")

if __name__ == "__main__":
    test_audit_bugs()
