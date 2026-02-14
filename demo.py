"""
Board Game Cafe - Complete Features Demo
Demonstrates tier system AND cancellation penalty features
"""

from datetime import datetime, timedelta
from BGC import BoardGameCafeSystem, BoardGameCafeBranch
from BGC_person import Customer, Member, TempCustomer, Staff, Manager, TierEnum
from BGC_menu import MenuList, Food, Drink, Snack, Order
from BGC_operation import (
    BoardGame, PlayTableStandard, PlayTableVIP, 
    Reservation, Cash, Card, OnlinePayment,
    ReservationStatus
)


def print_header(title):
    """Print a section header"""
    print("\n" + "=" * 80)
    print(f"  {title}")
    print("=" * 80)


def print_subheader(title):
    """Print a subsection header"""
    print("\n" + "─" * 80)
    print(f"  {title}")
    print("─" * 80)


def demo_complete_features():
    """Complete demonstration of all features"""
    
    print_header("🎲 BOARD GAME CAFE - COMPLETE FEATURES DEMO")
    
    # ==========================================
    # SETUP
    # ==========================================
    print("\n🏗️  Setting up system...")
    
    system = BoardGameCafeSystem(version="3.0")
    branch = BoardGameCafeBranch(
        cafe_id="BGC001",
        name="Board Game Cafe Bangkok",
        location="Sukhumvit Soi 11, Bangkok"
    )
    system.add_branch(branch)
    
    # Add staff
    manager = Manager(
        person_id="MGR001",
        name="Somchai Manager",
        contact="081-111-1111",
        username="somchai",
        password="manager123",
        salary=50000
    )
    
    staff1 = Staff(
        person_id="STF001",
        name="Nong Service",
        contact="082-222-2222",
        username="nong",
        password="staff123",
        salary=18000
    )
    
    system.add_staff(branch, manager)
    system.add_staff(branch, staff1)
    
    # Create menu
    menu = MenuList("Main Menu")
    
    food1 = Food("F001", "Pad Thai", 120, "Thai noodles", "Thai")
    food1.set_stock_level(100)
    food2 = Food("F002", "Margherita Pizza", 280, "Classic pizza", "Italian")
    food2.set_stock_level(100)
    food3 = Food("F003", "Wagyu Steak", 890, "Premium steak", "Western")
    food3.set_stock_level(50)
    
    drink1 = Drink("D001", "Thai Iced Tea", 60, "Sweet tea", "Medium")
    drink1.set_stock_level(200)
    drink2 = Drink("D002", "Craft Beer", 150, "Local IPA", "Pint", is_alcoholic=True)
    drink2.set_stock_level(100)
    
    snack1 = Snack("S001", "Loaded Nachos", 180, "Cheese & jalapeños", is_shareable=True)
    snack1.set_stock_level(150)
    
    for item in [food1, food2, food3, drink1, drink2, snack1]:
        menu.add_item(item)
    
    system.set_menu(branch, menu)
    
    # Add board games
    game1 = BoardGame("BG001", "Settlers of Catan", "Strategy", 100, 3, 4, 90)
    game2 = BoardGame("BG002", "Pandemic", "Cooperative", 100, 2, 4, 60)
    game3 = BoardGame("BG003", "Ticket to Ride", "Strategy", 80, 2, 5, 60)
    
    for game in [game1, game2, game3]:
        system.add_board_game(branch, game)
    
    # Add tables
    table1 = PlayTableStandard("T001", 4, "Table 1", price_per_hour=50)
    table2 = PlayTableStandard("T002", 6, "Table 2", price_per_hour=60)
    table3 = PlayTableVIP("VIP01", 8, "VIP Room Alpha", room_service_fee=300, price_per_hour=100)
    
    for table in [table1, table2, table3]:
        system.add_play_table(branch, table)
    
    print("✓ System initialized")
    print(f"  Staff: {len(branch.staff)}")
    print(f"  Menu Items: {menu.item_count}")
    print(f"  Board Games: {len(branch.board_games)}")
    print(f"  Tables: {len(branch.play_tables)}")
    
    # ==========================================
    # PART 1: MEMBER TIER PROGRESSION
    # ==========================================
    print_header("PART 1: MEMBER TIER PROGRESSION")
    
    # Create member Alice
    alice = Member(
        person_id="CUS001",
        name="Alice Wonder",
        contact="089-111-1111",
        member_id="MEM001",
        username="alice",
        password="alice123",
        birthdate=datetime(1995, 5, 15)
    )
    system.register_member(branch, alice)
    
    print_subheader("Scenario 1.1: New Member (No Tier)")
    
    print(f"\n👤 {alice.name} joins as a new member")
    tier = alice.get_tier()
    print(f"   Current Tier: {tier.value if tier else 'No Tier'}")
    print(f"   Total Spend: ฿{alice.total_spend:,.2f}")
    print(f"   Points: {alice.points}")
    
    # First purchase
    print("\n📝 First order...")
    order1 = system.create_order(branch, alice)
    order1.add_item(food1, 1)  # ฿120
    order1.add_item(drink1, 1)  # ฿60
    
    total1 = order1.calculate_total()
    print(f"   Total: ฿{total1:.2f}")
    
    payment1 = Cash("PAY001", order1, 200)
    system.process_payment(branch, payment1)
    
    alice.add_points(int(total1 / 10))
    print(f"   ✓ Payment completed")
    print(f"   New total spend: ฿{alice.total_spend:,.2f}")
    print(f"   Points earned: {int(total1 / 10)}")
    
    print_subheader("Scenario 1.2: Reaching Silver Tier")
    
    # Multiple purchases to reach Silver (฿1,000)
    print("\n📝 Alice makes regular purchases over time...")
    for i in range(4):
        order = system.create_order(branch, alice)
        order.add_item(food2, 1)
        payment = Cash(f"PAY-A-{i}", order, 400)
        system.process_payment(branch, payment)
    
    alice.add_points(50)
    
    tier = alice.get_tier()
    print(f"   ✓ Reached Silver Tier!")
    print(f"   Total Spend: ฿{alice.total_spend:,.2f}")
    print(f"   Discount Rate: {alice.get_discount_rate() * 100:.0f}%")
    print(f"   Points Multiplier: {alice.get_points_multiplier()}x")
    print(f"   Max Booking Duration: {alice.get_booking_limits()['max_duration_hours']} hours")
    
    # Order with Silver discount
    print("\n📝 New order with Silver discount...")
    order2 = system.create_order(branch, alice)
    order2.add_item(food3, 1)  # ฿890
    order2.add_item(drink2, 1)  # ฿150
    
    subtotal = order2.calculate_subtotal()
    discount = subtotal * alice.get_discount_rate()
    order2.apply_discount(discount)
    total2 = order2.calculate_total()
    
    print(f"   Subtotal: ฿{subtotal:.2f}")
    print(f"   Silver Discount (5%): -฿{discount:.2f}")
    print(f"   Total: ฿{total2:.2f}")
    
    payment2 = Card("PAY002", order2, "1234", "Bangkok Bank")
    system.process_payment(branch, payment2)
    
    alice.add_points(int(total2 / 10))
    print(f"   ✓ Points earned: {int(total2 / 10)} (base rate)")
    
    # ==========================================
    # PART 2: RESERVATION & CANCELLATION PENALTIES
    # ==========================================
    print_header("PART 2: RESERVATION & CANCELLATION PENALTIES")
    
    # Create Gold member Bob for reservations
    bob = Member(
        person_id="CUS002",
        name="Bob Builder",
        contact="089-222-2222",
        member_id="MEM002",
        username="bob",
        password="bob123"
    )
    system.register_member(branch, bob)
    
    # Boost Bob to Gold tier (need ฿5,000 - ฿9,999)
    print("\n📝 Preparing Bob's account (boosting to Gold tier)...")
    # Target: around ฿7,000 (safely in Gold range)
    for i in range(7):
        order = system.create_order(branch, bob)
        order.add_item(food3, 1)  # ฿890 each
        payment = Cash(f"PAY-BOB-{i}", order, 1000)
        system.process_payment(branch, payment)
        # Add points (before tier upgrade, so multiplier = 1.0)
        bob.add_points(int(order.calculate_total() / 10))
    
    # Add one more smaller order to reach ~฿7,000
    order = system.create_order(branch, bob)
    order.add_item(food2, 1)  # ฿280
    payment = Cash("PAY-BOB-EXTRA", order, 400)
    system.process_payment(branch, payment)
    bob.add_points(int(order.calculate_total() / 10))
    
    print(f"   ✓ Bob's Total Spend: ฿{bob.total_spend:,.2f}")
    print(f"   ✓ Bob's Tier: {bob.get_tier().value}")
    
    print_subheader("Scenario 2.1: Normal Reservation (No Penalty)")
    
    # Reservation for next week (no penalty)
    next_week = datetime.now() + timedelta(days=7)
    date_str = next_week.strftime("%Y-%m-%d")
    
    print(f"\n📅 Bob makes a reservation for {date_str}")
    
    reservation1 = Reservation(
        reservation_id="RES001",
        customer=bob,
        table=table2,
        date_str=date_str,
        start_time_str="18:00",
        end_time_str="21:00",
        guest_count=4
    )
    
    system.create_reservation(branch, reservation1)
    system.confirm_reservation(branch, "RES001")
    
    print(f"   Table: {reservation1.table.table_name}")
    print(f"   Date: {reservation1.get_date()}")
    print(f"   Time: {reservation1.get_start_time()} - {reservation1.get_end_time()}")
    print(f"   Duration: {reservation1.duration_hours} hours")
    print(f"   Status: {reservation1.status.value}")
    
    # Cancel early (no penalty)
    print("\n🚫 Bob cancels the reservation (7 days in advance)")
    hours_before = (reservation1.start_datetime - datetime.now()).total_seconds() / 3600
    print(f"   Cancelling {hours_before:.1f} hours before reservation")
    
    reservation1.cancel_booking("Change of plans")
    
    print(f"   ✓ Status: {reservation1.status.value}")
    print(f"   Reason: {reservation1._cancellation_reason}")
    print(f"   ⭐ No penalty (cancelled more than 2 hours in advance)")
    
    print_subheader("Scenario 2.2: Late Cancellation (WITH Penalty)")
    
    # Reservation for today (will have penalty)
    in_90_mins = datetime.now() + timedelta(minutes=90)
    date_str2 = in_90_mins.strftime("%Y-%m-%d")
    start_time = in_90_mins.strftime("%H:%M")
    end_time = (in_90_mins + timedelta(hours=2)).strftime("%H:%M")
    
    print(f"\n📅 Bob makes another reservation for TODAY")
    print(f"   Starting in 90 minutes: {start_time}")
    
    reservation2 = Reservation(
        reservation_id="RES002",
        customer=bob,
        table=table2,
        date_str=date_str2,
        start_time_str=start_time,
        end_time_str=end_time,
        guest_count=4
    )
    
    system.create_reservation(branch, reservation2)
    system.confirm_reservation(branch, "RES002")
    
    print(f"   Table: {reservation2.table.table_name}")
    print(f"   Status: {reservation2.status.value}")
    
    # Calculate expected penalty
    expected_penalty = table2.calculate_table_charge(1) * 0.5  # 50% of 1 hour
    
    print(f"\n⚠️  Bob tries to cancel (only 1.5 hours before)")
    print(f"   Table rate: ฿{table2.price_per_hour}/hour")
    print(f"   Expected penalty: 50% of 1 hour = ฿{expected_penalty:.2f}")
    
    # Cancel late (with penalty)
    reservation2.cancel_booking("Emergency came up")
    
    print(f"\n   ✓ Status: {reservation2.status.value}")
    print(f"   Reason: {reservation2._cancellation_reason}")
    print(f"   💰 Late cancellation penalty applied!")
    
    print_subheader("Scenario 2.3: VIP Room Late Cancellation")
    
    # VIP reservation with higher penalty
    in_60_mins = datetime.now() + timedelta(minutes=60)
    date_str3 = in_60_mins.strftime("%Y-%m-%d")
    start_time3 = in_60_mins.strftime("%H:%M")
    end_time3 = (in_60_mins + timedelta(hours=3)).strftime("%H:%M")
    
    print(f"\n📅 Bob books VIP Room (starting in 60 minutes)")
    
    reservation3 = Reservation(
        reservation_id="RES003",
        customer=bob,
        table=table3,  # VIP table
        date_str=date_str3,
        start_time_str=start_time3,
        end_time_str=end_time3,
        guest_count=6
    )
    
    system.create_reservation(branch, reservation3)
    system.confirm_reservation(branch, "RES003")
    
    print(f"   Table: {reservation3.table.table_name}")
    print(f"   Hourly Rate: ฿{table3.price_per_hour}/hour")
    print(f"   Room Service Fee: ฿{table3.room_service_fee}")
    
    # Calculate VIP penalty
    vip_penalty = table3.calculate_table_charge(1) * 0.5
    
    print(f"\n⚠️  Bob cancels VIP reservation (less than 2 hours)")
    print(f"   Expected penalty: 50% of 1 hour = ฿{vip_penalty:.2f}")
    
    reservation3.cancel_booking("Client meeting rescheduled")
    
    print(f"\n   ✓ Status: {reservation3.status.value}")
    print(f"   Reason: {reservation3._cancellation_reason}")
    print(f"   💰 Higher penalty for VIP room!")
    
    # ==========================================
    # PART 3: TIER BENEFITS IN ACTION
    # ==========================================
    print_header("PART 3: TIER BENEFITS COMPARISON")
    
    # Create Platinum member
    charlie = Member(
        person_id="CUS003",
        name="Charlie Platinum",
        contact="089-333-3333",
        member_id="MEM003",
        username="charlie",
        password="charlie123"
    )
    system.register_member(branch, charlie)
    
    # Boost to Platinum
    print("\n📝 Creating Platinum member Charlie...")
    for i in range(25):
        order = system.create_order(branch, charlie)
        order.add_item(food3, 1)
        payment = Cash(f"PAY-CHARLIE-{i}", order, 1000)
        system.process_payment(branch, payment)
    
    print(f"   ✓ Charlie's Total Spend: ฿{charlie.total_spend:,.2f}")
    print(f"   ✓ Charlie's Tier: {charlie.get_tier().value}")
    
    # Compare booking capabilities
    print_subheader("Booking Capability Comparison")
    
    future_date = datetime.now() + timedelta(days=20)
    
    print(f"\n📅 Testing 4-hour booking for {future_date.strftime('%Y-%m-%d')}")
    print("   (20 days from now)\n")
    
    members = [
        ("Alice", alice),
        ("Bob", bob),
        ("Charlie", charlie)
    ]
    
    print("─" * 80)
    print(f"{'Member':<15} {'Tier':<12} {'Spend':<15} {'Can Book 4h?':<15} {'Reason':<25}")
    print("─" * 80)
    
    for name, member in members:
        tier = member.get_tier()
        tier_name = tier.value if tier else "No Tier"
        can_book = member.can_book(future_date, 4)
        limits = member.get_booking_limits()
        
        if can_book:
            reason = "✓ Within limits"
        else:
            reasons = []
            if limits['max_bookings'] == 0:
                reasons.append("No booking rights")
            if 4 > limits['max_duration_hours']:
                reasons.append(f"Max {limits['max_duration_hours']}h")
            if 20 > limits['max_advance_days']:
                reasons.append(f"Max {limits['max_advance_days']} days ahead")
            reason = "✗ " + ", ".join(reasons) if reasons else "Unknown"
        
        print(f"{name:<15} {tier_name:<12} ฿{member.total_spend:>10,.2f}  {str(can_book):<15} {reason:<25}")
    
    print("─" * 80)
    
    # ==========================================
    # PART 4: PLATINUM PERKS SHOWCASE
    # ==========================================
    print_header("PART 4: PLATINUM MEMBER PERKS")
    
    print("\n💎 Charlie (Platinum) enjoys premium benefits:")
    
    # Large order with maximum discount
    print("\n📝 Large party order...")
    
    order_charlie = system.create_order(branch, charlie)
    order_charlie.add_item(food3, 4)   # ฿3,560
    order_charlie.add_item(drink2, 6)  # ฿900
    order_charlie.add_item(snack1, 3)  # ฿540
    
    subtotal = order_charlie.calculate_subtotal()
    discount = subtotal * charlie.get_discount_rate()
    order_charlie.apply_discount(discount)
    total = order_charlie.calculate_total()
    
    print(f"   Subtotal: ฿{subtotal:,.2f}")
    print(f"   Platinum Discount (15%): -฿{discount:,.2f}")
    print(f"   Tax: ฿{order_charlie.calculate_tax():,.2f}")
    print(f"   Total: ฿{total:,.2f}")
    print(f"   💰 Saved: ฿{discount:,.2f}")
    
    payment_charlie = Card("PAY-CHARLIE-FINAL", order_charlie, "9999", "SCB")
    system.process_payment(branch, payment_charlie)
    
    # Points with 2x multiplier
    base_points = int(total / 10)
    points_before = charlie.points
    charlie.add_points(base_points)
    points_after = charlie.points
    actual_points_earned = points_after - points_before
    
    print(f"\n⭐ Points calculation:")
    print(f"   Base points: {base_points}")
    print(f"   Multiplier: {charlie.get_points_multiplier()}x")
    print(f"   Points earned: {actual_points_earned}")
    print(f"   Total points now: {charlie.points:,}")
    
    # ==========================================
    # FINAL SUMMARY
    # ==========================================
    print_header("FINAL SYSTEM SUMMARY")
    
    report = system.get_branch_report(branch)
    
    print(f"\n📊 {report['branch']}")
    print(f"    {report['location']}\n")
    
    print(f"💰 Revenue: ฿{report['revenue']:,.2f}")
    print(f"📝 Orders: {report['total_orders']}")
    print(f"📅 Reservations: {report['total_reservations']}")
    print(f"👥 Total Customers: {report['total_customers']}")
    print(f"⭐ Members: {report['total_members']}")
    
    # All Members Summary Table
    print("\n" + "─" * 90)
    print(f"{'Member Name':<20} {'Tier':<12} {'Total Spend':<15} {'Points':<10} {'Discount':<10}")
    print("─" * 90)
    
    for member in sorted(branch.members, key=lambda m: m.total_spend, reverse=True):
        tier = member.get_tier()
        tier_name = tier.value if tier else "No Tier"
        discount = f"{member.get_discount_rate() * 100:.0f}%"
        
        print(f"{member.name:<20} {tier_name:<12} ฿{member.total_spend:>11,.2f}  "
              f"{member.points:>8,}   {discount:>8}")
    
    print("─" * 90)
    
    # Member breakdown
    print("\n🏆 Member Tier Breakdown:")
    
    no_tier_members = [m for m in branch.members if m.get_tier() is None]
    silver_members = [m for m in branch.members if m.get_tier() == TierEnum.SILVER]
    gold_members = [m for m in branch.members if m.get_tier() == TierEnum.GOLD]
    platinum_members = [m for m in branch.members if m.get_tier() == TierEnum.PLATINUM]
    
    print(f"   No Tier:  {len(no_tier_members)}")
    if no_tier_members:
        for m in no_tier_members:
            print(f"      - {m.name}: ฿{m.total_spend:,.2f}, {m.points:,} points")
    
    print(f"   🥈 Silver:   {len(silver_members)}")
    if silver_members:
        for m in silver_members:
            print(f"      - {m.name}: ฿{m.total_spend:,.2f}, {m.points:,} points")
    
    print(f"   🥇 Gold:     {len(gold_members)}")
    if gold_members:
        for m in gold_members:
            print(f"      - {m.name}: ฿{m.total_spend:,.2f}, {m.points:,} points")
    
    print(f"   💎 Platinum: {len(platinum_members)}")
    if platinum_members:
        for m in platinum_members:
            print(f"      - {m.name}: ฿{m.total_spend:,.2f}, {m.points:,} points")
    
    # Reservation summary
    print("\n📅 Reservation Summary:")
    
    confirmed = sum(1 for r in branch.reservations if r.status == ReservationStatus.CONFIRMED)
    cancelled = sum(1 for r in branch.reservations if r.status == ReservationStatus.CANCELLED)
    
    print(f"   Total: {len(branch.reservations)}")
    print(f"   Confirmed: {confirmed}")
    print(f"   Cancelled: {cancelled}")
    
    # Top spender
    top_member = max(branch.members, key=lambda m: m.total_spend)
    print(f"\n🌟 Top Spender: {top_member.name}")
    print(f"   Total Spend: ฿{top_member.total_spend:,.2f}")
    print(f"   Tier: {top_member.get_tier().value}")
    print(f"   Points: {top_member.points:,}")
    
    print("\n" + "=" * 80)
    print("  ✓ COMPLETE FEATURES DEMO FINISHED!")
    print("=" * 80 + "\n")


if __name__ == "__main__":
    demo_complete_features()