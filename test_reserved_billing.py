from BGC_SYSTEM import CafeSystem
from BGC_PLAY_SESSION import Table
from datetime import datetime, timedelta
import math

def test_reserved_billing():
    system = CafeSystem()
    print("--- Testing Reserved Duration Billing ---")
    
    # 1. Setup Branch & Table
    branch = system.create_cafe_branch("Siam Branch")
    table = system.create_table_to_branch(branch.branch_id, 4)
    Table.price_per_hour = 15.0
    
    # 2. Setup Member
    member = system.create_customer_member("Alice")
    
    # 3. Create Reservation (2 hours: 10:00 - 12:00)
    # Alice is a basic member, limit is 2 hours.
    # Signature: (customer_id, branch_id, total_player, date, start_time, end_time, table_id="auto")
    res = system.make_reservation(member.user_id, branch.branch_id, 2, "2026-03-11", "10:00", "12:00")
    print(f"Reservation created: {res.reservation_id} (10:00 - 12:00, 2 hours)")
    
    # 4. Check-in Reserved (Arrival at 10:00 sharp)
    checkin_time = datetime.strptime("2026-03-11 10:00", "%Y-%m-%d %H:%M")
    session = system.check_in_reserved(res.reservation_id, member.user_id, current_time=checkin_time)
    print(f"Alice checked in. Session: {session.session_id}, Reserved Duration stored: {session.reserved_duration} hours")
    
    # 5. Immediate Checkout (Should still charge 2 hours because of reservation)
    checkout_time = datetime.strptime("2026-03-11 10:05", "%Y-%m-%d %H:%M")
    payment, total = system.check_out(session.session_id, "cash", end_time=checkout_time, paid_amount=500)
    
    print(f"\nCheckout at 10:05 (played 5 mins, reserved 2 hours)")
    print(f"Checkout Total: ฿{total:.2f}")
    
    # Total should be: 15.0 (price) * 2 (hours) * 1 (player Alice) = 30.0
    expected = 15.0 * 2 * 1
    if total == expected:
        print(f"SUCCESS: Charged 2 hours (฿{total:.2f}) as reserved.")
    else:
        print(f"FAILED: Expected ฿{expected:.2f}, but got ฿{total:.2f}.")

    # 6. Test Playing Longer than Reservation (e.g., 4 hours)
    # Note: Even if reservation is 1 hr, playing longer is allowed (it will just be charged more)
    print("\n--- Testing Playing Longer than Reservation ---")
    res2 = system.make_reservation(member.user_id, branch.branch_id, 2, "2026-03-12", "10:00", "11:00")
    session2 = system.check_in_reserved(res2.reservation_id, member.user_id, current_time=datetime.strptime("2026-03-12 10:00", "%Y-%m-%d %H:%M"))
    
    # Playing until 14:00 (4 hours)
    checkout_time2 = datetime.strptime("2026-03-12 14:00", "%Y-%m-%d %H:%M")
    payment2, total2 = system.check_out(session2.session_id, "cash", end_time=checkout_time2, paid_amount=500)
    
    print(f"Checkout at 14:00 (played 4 hours, reserved 1 hour)")
    print(f"Checkout Total: ฿{total2:.2f}")
    expected2 = 15.0 * 4 * 1
    if total2 == expected2:
        print(f"SUCCESS: Charged 4 hours (฿{total2:.2f}) as played.")
    else:
        print(f"FAILED: Expected ฿{expected2:.2f}, but got ฿{total2:.2f}.")

if __name__ == "__main__":
    test_reserved_billing()
