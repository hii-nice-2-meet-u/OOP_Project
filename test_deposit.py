from _Project_instance import system
from BGC_PAYMENT import OnlinePayment
from ENUM_STATUS import ReservationStatus
import datetime

def test_deposit_system():
    print("--- Testing Reservation Deposit System ---")
    
    # 1. Test Cash Rejection
    print("\n1. Testing Cash Rejection...")
    try:
        system.make_reservation(
            customer_id="MEMBER-00001", # Somchai
            branch_id="BRCH-00000",
            total_player=2,
        date=(datetime.datetime.now() + datetime.timedelta(days=1)).strftime("%Y-%m-%d"),
            start_time="10:00",
            end_time="12:00",
            method_type="cash"
        )
        print("FAIL: Cash was accepted for reservation!")
    except ValueError as e:
        print(f"SUCCESS: Caught expected error: {e}")

    test_date = (datetime.datetime.now() + datetime.timedelta(days=1)).strftime("%Y-%m-%d")
    res = system.make_reservation(
        customer_id="MEMBER-00001",
        branch_id="BRCH-00000",
        total_player=2,
        date=test_date,
        start_time="10:00",
        end_time="12:00",
        method_type="online",
        email="somchai@example.com"
    )
    print(f"SUCCESS: Reservation {res.reservation_id} created with deposit: ฿{res.deposit}")
    
    # 3. Test Check-in (Carrying over deposit)
    print("\n3. Testing Check-in...")
    test_date = (datetime.datetime.now() + datetime.timedelta(days=1)).strftime("%Y-%m-%d")
    check_in_time = datetime.datetime.strptime(f"{test_date} 10:00", "%Y-%m-%d %H:%M")
    session = system.check_in_reserved(res.reservation_id, "MEMBER-00001", current_time=check_in_time)
    print(f"SUCCESS: Session {session.session_id} created with carried-over deposit: ฿{session.deposit}")

    # 4. Test Checkout (Deduction)
    print("\n4. Testing Checkout Deduction...")
    # Simulate 2 hours stay
    check_out_time = datetime.datetime.strptime(f"{test_date} 12:00", "%Y-%m-%d %H:%M")
    bill = system.get_active_bill(session.session_id, current_time=check_out_time)
    
    found_deduction = False
    for label, amount in bill["items"]:
        print(f"  {label:<40} : ฿{amount:>7.2f}")
        if "Deposit Deduction" in label and amount == -30.0:
            found_deduction = True
            
    if found_deduction:
        print("\nOVERALL SUCCESS: Deposit logic verified.")
    else:
        print("\nFAIL: Deposit deduction not found in bill!")

if __name__ == "__main__":
    test_deposit_system()
