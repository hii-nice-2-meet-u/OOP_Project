import datetime
from BGC_SYSTEM import CafeSystem
from BGC_PLAY_SESSION import Table
from ENUM_STATUS import TableStatus

def test_force_checkout_flow():
    system = CafeSystem()
    branch = system.create_cafe_branch("Siam Branch")
    table = branch.add_table(4)
    Table.price_per_hour = 15.0
    
    member1 = system.create_customer_member("Alice")
    member2 = system.create_customer_member("Bob")
    
    # 1. Alice reserves 10:00 - 11:00
    res1 = system.make_reservation(member1.user_id, branch.branch_id, 2, "2026-03-11", "10:00", "11:00", table.table_id)
    
    # 2. Bob reserves 11:00 - 12:00
    res2 = system.make_reservation(member2.user_id, branch.branch_id, 2, "2026-03-11", "11:00", "12:00", table.table_id)
    
    print(f"Alice Reservation: {res1.reservation_id} (10:00-11:00)")
    print(f"Bob Reservation: {res2.reservation_id} (11:00-12:00)")
    
    # 3. Alice checks in at 10:00
    checkin_time = datetime.datetime(2026, 3, 11, 10, 0)
    session1 = system.check_in_reserved(res1.reservation_id, member1.user_id, current_time=checkin_time)
    print(f"Alice checked in. Session: {session1.session_id}, Reserved End: {session1.reserved_end_time}")
    
    # 4. Bob arrives at 11:05 (Alice's time is up)
    late_time = datetime.datetime(2026, 3, 11, 11, 5)
    print(f"\nBob arrives at 11:05. Attempting to check in Bob...")
    
    try:
        system.check_in_reserved(res2.reservation_id, member2.user_id, current_time=late_time)
        print("FAILED: Bob checked in while Alice was still there!")
    except ValueError as e:
        print(f"SUCCESS (Expected Error): {e}")
        if "FORCE CHECKOUT REQUIRED" in str(e):
            print("Verified: System correctly identified that Alice must be force-checked out.")
        else:
            print(f"FAILED: Wrong error message: {e}")

    # 5. Staff performs Force Checkout for Alice
    print(f"\nStaff performing checkout for Alice (Session: {session1.session_id})...")
    system.check_out(session1.session_id, end_time=late_time, paid_amount=30.0)
    print(f"Alice checked out. Table status: {table.status}")
    
    # 6. Now Bob can check in
    print("\nAttempting to check in Bob again...")
    session2 = system.check_in_reserved(res2.reservation_id, member2.user_id, current_time=late_time)
    print(f"SUCCESS: Bob checked in. Session: {session2.session_id}")

if __name__ == "__main__":
    test_force_checkout_flow()
