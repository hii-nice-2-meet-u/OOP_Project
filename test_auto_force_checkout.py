from BGC_SYSTEM import CafeSystem
from datetime import datetime

# | ════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════

def test_auto_force_checkout_flow():
    system = CafeSystem()
    branch = system.create_cafe_branch("Automated Branch")
    branch.add_table(4) # TABLE-00000
    
    # 1. Setup authorized staff
    staff = system.create_staff("Staff Member") # STAFF-00000
    
    # 2. Setup Alice and Bob
    alice = system.create_member("Alice")
    bob = system.create_member("Bob")
    
    # 3. Reservations: Alice (10:00-11:00), Bob (11:00-12:00)
    print("Creating reservations...")
    res_alice = system.make_reservation(alice.user_id, branch.branch_id, 1, "10:00", "11:00")
    res_bob = system.make_reservation(bob.user_id, branch.branch_id, 1, "11:00", "12:00")
    
    # 4. Alice checks in at 10:00
    system.set_simulated_time("2026-03-10 10:00")
    session_alice = system.check_in_reserved(res_alice.reservation_id, alice.user_id) # current_time taken from system
    print(f"System Time: {system.get_time()}")
    print(f"Alice checked in. Session: {session_alice.session_id}, Reserved End: {session_alice.reserved_end_time}")
    
    # 5. Bob arrives at 11:05 (Alice is overstayed)
    system.set_simulated_time("2026-03-10 11:05")
    print(f"\nSystem Time: {system.get_time()}")
    print(f"Bob arrives. Attempting to check in Bob...")
    
    session_id_to_clear = ""
    try:
        system.check_in_reserved(res_bob.reservation_id, bob.user_id)
        print("FAILED: Bob checked in while Alice was still there!")
    except ValueError as e:
        print(f"SUCCESS (Expected Conflict): {e}")
        if "FORCE CHECKOUT REQUIRED" in str(e):
             session_id_to_clear = session_alice.session_id
             
    # 6. Resolve Conflict using the new automated method
    if session_id_to_clear:
        print(f"\nStaff {staff.user_id} resolving conflict using auto_force_checkout...")
        
        system.auto_force_checkout(
            session_id_to_clear, 
            staff.user_id, 
            method_type="cash", 
            paid_amount=30.0 # 2 hours x 15 baht
        )
        print(f"Conflict resolved. Alice checked out.")
        
    # 7. Bob checks in again
    print("\nBob checking in again...")
    session_bob = system.check_in_reserved(res_bob.reservation_id, bob.user_id)
    print(f"SUCCESS: Bob checked in. Session: {session_bob.session_id}")
    
    # Verify Alice's history
    history = system.bill_history(session_alice.session_id)
    print("\nAlice's Final Bill Details:")
    for label, amount in history:
        print(f"  {label}: ฿{amount:.2f}")

if __name__ == "__main__":
    test_auto_force_checkout_flow()
