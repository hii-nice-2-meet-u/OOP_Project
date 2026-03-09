from BGC_SYSTEM import CafeSystem
from BGC_PLAY_SESSION import Table
from datetime import datetime, timedelta
import math

def test_duration_logic():
    system = CafeSystem()
    print("--- Testing Duration & Fee Logic ---")
    
    # 1. Setup Branch & Table
    branch = system.create_cafe_branch("Siam Branch")
    table = system.create_table_to_branch(branch.branch_id, 4)
    Table.price_per_hour = 15.0 # Ensure fixed price for test
    
    # 2. Check-in Alice
    member = system.create_customer_member("Alice")
    session = system.check_in(branch.branch_id, 1, customer_id=member.user_id, table_id=table.table_id)
    print(f"Alice checked in. Session: {session.session_id}")
    
    # 3. Test Active Session Duration (Should be 1 hour minimum even if immediate)
    active_duration = session.duration()
    print(f"Active Session Duration (immediate check): {active_duration} hour(s)")
    if active_duration == 1:
        print("SUCCESS: Active session correctly displays 1 hour minimum.")
    else:
        print(f"FAILED: Active session should show 1 hour, but got {active_duration}.")

    # 4. Test Checkout Fee (Should be 15.0 for 1 player * 1 hr * 15/hr)
    print("\nAttempting immediate checkout...")
    payment, total = system.check_out(session.session_id, "cash", paid_amount=100)
    print(f"Checkout Total: ฿{total:.2f}")
    if total == 15.0:
        print("SUCCESS: Checkout correctly charged 1 hour minimum (฿15.00).")
    else:
        print(f"FAILED: Expected ฿15.00, but got ฿{total:.2f}.")

if __name__ == "__main__":
    test_duration_logic()
