import sys
import os
from datetime import datetime, timedelta

# Add current directory to path
sys.path.append(os.getcwd())

from BGC_SYSTEM import CafeSystem
from ENUM_STATUS import ReservationStatus, TableStatus

def test_policies():
    system = CafeSystem()
    
    print("--- 1. Testing Bootstrap Authorization ---")
    # First owner should be allowed without requester_id if no owners exist
    owner = system.create_owner("Big Boss")
    print(f"Created Bootstrap Owner: {owner.user_id}")
    
    print("\n--- 2. Testing Management Authorization ---")
    # Unauthorized member tries to create a branch
    member_poor = system.create_customer_member("Poor Guy")
    try:
        system.create_cafe_branch("Illegal Branch", "Nowhere", requester_id=member_poor.user_id)
        print("FAILED: Unauthorized user created a branch")
    except PermissionError as e:
        print(f"SUCCESS: Authorization blocked as expected: {e}")

    # Authorized owner creates a branch
    branch = system.create_cafe_branch("Headquarters", "Bangkok", requester_id=owner.user_id)
    print(f"Created Branch: {branch.branch_id} by {owner.user_id}")

    # Add a table to the branch
    table = system.create_table_to_branch(branch.branch_id, 4, requester_id=owner.user_id)
    print(f"Created Table: {table.table_id} in {branch.branch_id}")

    print("\n--- 3. Testing Cancellation Policy (1-Day Rule) ---")
    # Setup: Current time 2026-03-10 10:00
    now = datetime(2026, 3, 10, 10, 0)
    system.set_simulated_time(now.strftime("%Y-%m-%d %H:%M:%S"))
    
    # Reservation 1: 2 days in future (Free)
    member_free = system.create_customer_member("Free Spirits")
    res_free = system.make_reservation(member_free.user_id, branch.branch_id, 2, "2026-03-12", "14:00", "16:00")
    print(f"Reservation Free: {res_free.reservation_id} on {res_free.date}")
    
    # Reservation 2: 5 hours in future (Late)
    member_late = system.create_customer_member("Late Comer")
    res_late = system.make_reservation(member_late.user_id, branch.branch_id, 2, "2026-03-10", "15:00", "17:00")
    print(f"Reservation Late: {res_late.reservation_id} on {res_late.date}")

    # Cancel Free
    system.cancel_reservation(res_free.reservation_id, current_time=now)
    print(f"Cancelled {res_free.reservation_id} status: {res_free.status} (Expected: CANCELLED)")

    # Cancel Late
    system.cancel_reservation(res_late.reservation_id, current_time=now)
    print(f"Cancelled {res_late.reservation_id} status: {res_late.status} (Expected: CANCELLED with 50% penalty - conceptually)")

    print("\n--- 4. Testing No-Show Policy (15-Minute Rule) ---")
    # Setup: Resv at 12:00, now is 10:00 (Passes 1-hour lead time)
    member_noshow = system.create_customer_member("No Show Guy")
    res_noshow = system.make_reservation(member_noshow.user_id, branch.branch_id, 2, "2026-03-10", "12:00", "14:00")
    print(f"Reservation for No-Show: {res_noshow.reservation_id} at 12:00")
    
    # Advance time to 12:20 (20 mins late)
    noshow_now = datetime(2026, 3, 10, 12, 20)
    system.set_simulated_time(noshow_now.strftime("%Y-%m-%d %H:%M:%S"))
    system.update_reserved_tables()
    
    print(f"Reservation {res_noshow.reservation_id} status at 12:20: {res_noshow.status} (Expected: NO_SHOW)")

if __name__ == "__main__":
    try:
        test_policies()
    except Exception as e:
        import traceback
        traceback.print_exc()
