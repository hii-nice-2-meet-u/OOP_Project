from BGC import *
from datetime import datetime, timedelta

if __name__ == "__main__":
    sys = CafeSystem()

    # / ════════════════════════════════════════════════════════════════
    # SETUP: สร้างข้อมูลพื้นฐาน (สาขา โต๊ะ ลูกค้า)
    # / ════════════════════════════════════════════════════════════════

    sys.create_cafe_branch("Cafe - A", "A 123/456")
    sys.create_table_to_branch("BRCH-00000", 2)
    sys.create_table_to_branch("BRCH-00000", 4)
    sys.create_table_to_branch("BRCH-00000", 6)
    sys.create_table_to_branch("BRCH-00000", 8)
    sys.create_table_to_branch("BRCH-00000", 10)

    # สร้างสมาชิกระดับต่างๆ เพื่อใช้เทสกฎ
    member_bronze = Member("Bronze User")
    member_bronze.member_tier = MemberTier.BRONZE
    sys.add_person(member_bronze)

    member_silver = Member("Silver User")
    member_silver.member_tier = MemberTier.SILVER
    sys.add_person(member_silver)

    member_gold = Member("Gold User")
    member_gold.member_tier = MemberTier.GOLD
    sys.add_person(member_gold)

    member_platinum = Member("Platinum User")
    member_platinum.member_tier = MemberTier.PLATINUM
    sys.add_person(member_platinum)

    # ลูกค้าพิเศษสำหรับเทส Double Booking
    member_db = Member("DB Tester")
    member_db.member_tier = MemberTier.PLATINUM
    sys.add_person(member_db)

    # / ════════════════════════════════════════════════════════════════
    # HELPER FUNCTION: ตัวช่วยปริ้นท์ผลการทดสอบ
    # / ════════════════════════════════════════════════════════════════
    now = datetime.now()

    def test_reservation(
        description,
        customer_id,
        branch_id,
        total_player,
        resv_date,
        start_t,
        end_t,
        table_id="auto",
    ):

        print(f"\n{'-'*64}")
        print(f" TEST     : {description}")
        print(f" NOW      : {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        print(f" BOOK FOR : {resv_date} at {start_t} - {end_t}")
        print(f"{'-'*64}")

        try:
            resv = sys.make_reservation(
                customer_id,
                branch_id,
                total_player,
                resv_date,
                start_t,
                end_t,
                table_id,
            )
            print(
                f" ✅ SUCCESS -> Resv ID: {resv.reservation_id} | Table: {resv.table_id} | Status: {resv.status.name}"
            )
        except Exception as e:
            print(f" ❌ FAILED  -> {type(e).__name__}: {str(e)}")

    print(f'\n{" COMPREHENSIVE RESERVATION RULE TESTS ":═^64}\n')

    # ==================================================================
    # 1. TEST MINIMUM LEAD TIME (ทุกระดับต้องจองล่วงหน้า 1 ชม.)
    # ==================================================================
    time_30m = now + timedelta(minutes=30)
    time_2h_30m = time_30m + timedelta(hours=2)

    test_reservation(
        "LEAD TIME (< 1 Hour) [EXPECT FAIL]",
        member_bronze.user_id,
        "BRCH-00000",
        2,
        time_30m.strftime("%Y-%m-%d"),
        time_30m.strftime("%H:%M"),
        time_2h_30m.strftime("%H:%M"),
    )

    # ==================================================================
    # 2. TEST MAX DURATION (เทสใช้วันพรุ่งนี้ เพื่อหลีกเลี่ยงกฎ Lead Time)
    # ==================================================================
    tmr = (now + timedelta(days=1)).strftime("%Y-%m-%d")

    test_reservation(
        "DURATION - Bronze (> 2 Hrs) [EXPECT FAIL]",
        member_bronze.user_id,
        "BRCH-00000",
        2,
        tmr,
        "10:00",
        "13:00",
    )

    test_reservation(
        "DURATION - Silver (> 3.5 Hrs) [EXPECT FAIL]",
        member_silver.user_id,
        "BRCH-00000",
        2,
        tmr,
        "10:00",
        "14:00",
    )

    test_reservation(
        "DURATION - Gold (> 7 Hrs) [EXPECT FAIL]",
        member_gold.user_id,
        "BRCH-00000",
        2,
        tmr,
        "10:00",
        "18:00",
    )

    test_reservation(
        "DURATION - Platinum (12 Hrs) [EXPECT SUCCESS]",
        member_platinum.user_id,
        "BRCH-00000",
        2,
        tmr,
        "08:00",
        "20:00",
    )

    # ==================================================================
    # 3. TEST ADVANCE BOOKING LIMITS (วันจองล่วงหน้าสูงสุด)
    # ==================================================================
    test_reservation(
        "ADVANCE - Bronze (6 Days) [EXPECT FAIL]",
        member_bronze.user_id,
        "BRCH-00000",
        2,
        (now + timedelta(days=6)).strftime("%Y-%m-%d"),
        "14:00",
        "16:00",
    )

    test_reservation(
        "ADVANCE - Silver (15 Days) [EXPECT FAIL]",
        member_silver.user_id,
        "BRCH-00000",
        2,
        (now + timedelta(days=15)).strftime("%Y-%m-%d"),
        "14:00",
        "16:00",
    )

    test_reservation(
        "ADVANCE - Gold (22 Days) [EXPECT FAIL]",
        member_gold.user_id,
        "BRCH-00000",
        2,
        (now + timedelta(days=22)).strftime("%Y-%m-%d"),
        "14:00",
        "16:00",
    )

    test_reservation(
        "ADVANCE - Platinum (31 Days) [EXPECT FAIL]",
        member_platinum.user_id,
        "BRCH-00000",
        2,
        (now + timedelta(days=31)).strftime("%Y-%m-%d"),
        "14:00",
        "16:00",
    )

    test_reservation(
        "ADVANCE - Platinum (28 Days) [EXPECT SUCCESS]",
        member_platinum.user_id,
        "BRCH-00000",
        2,
        (now + timedelta(days=28)).strftime("%Y-%m-%d"),
        "14:00",
        "16:00",
    )

    # ==================================================================
    # 4. TEST ACTIVE QUOTA (โควตาการจองค้างในระบบ - อิงกฎใหม่ของเพื่อน)
    # ==================================================================

    # --- Silver: Quota 2 ---
    test_reservation(
        "QUOTA - Silver (1st Booking) [EXPECT SUCCESS]",
        member_silver.user_id,
        "BRCH-00000",
        2,
        (now + timedelta(days=2)).strftime("%Y-%m-%d"),
        "10:00",
        "12:00",
    )
    test_reservation(
        "QUOTA - Silver (2nd Booking) [EXPECT SUCCESS]",
        member_silver.user_id,
        "BRCH-00000",
        2,
        (now + timedelta(days=3)).strftime("%Y-%m-%d"),
        "10:00",
        "12:00",
    )
    test_reservation(
        "QUOTA - Silver (3rd Booking) [EXPECT FAIL]",
        member_silver.user_id,
        "BRCH-00000",
        2,
        (now + timedelta(days=4)).strftime("%Y-%m-%d"),
        "10:00",
        "12:00",
    )

    # --- Gold: Quota 3 ---
    test_reservation(
        "QUOTA - Gold (1st Booking) [EXPECT SUCCESS]",
        member_gold.user_id,
        "BRCH-00000",
        2,
        (now + timedelta(days=2)).strftime("%Y-%m-%d"),
        "10:00",
        "12:00",
    )
    test_reservation(
        "QUOTA - Gold (2nd Booking) [EXPECT SUCCESS]",
        member_gold.user_id,
        "BRCH-00000",
        2,
        (now + timedelta(days=3)).strftime("%Y-%m-%d"),
        "10:00",
        "12:00",
    )
    test_reservation(
        "QUOTA - Gold (3rd Booking) [EXPECT SUCCESS]",
        member_gold.user_id,
        "BRCH-00000",
        2,
        (now + timedelta(days=4)).strftime("%Y-%m-%d"),
        "10:00",
        "12:00",
    )
    test_reservation(
        "QUOTA - Gold (4th Booking) [EXPECT FAIL]",
        member_gold.user_id,
        "BRCH-00000",
        2,
        (now + timedelta(days=5)).strftime("%Y-%m-%d"),
        "10:00",
        "12:00",
    )

    # --- Platinum: Quota 4 (มีจองสำเร็จจากข้อ 2 และ 3 ไปแล้ว 2 อัน) ---
    test_reservation(
        "QUOTA - Platinum (3rd Booking) [EXPECT SUCCESS]",
        member_platinum.user_id,
        "BRCH-00000",
        2,
        (now + timedelta(days=2)).strftime("%Y-%m-%d"),
        "10:00",
        "12:00",
    )
    test_reservation(
        "QUOTA - Platinum (4th Booking) [EXPECT SUCCESS]",
        member_platinum.user_id,
        "BRCH-00000",
        2,
        (now + timedelta(days=3)).strftime("%Y-%m-%d"),
        "10:00",
        "12:00",
    )
    test_reservation(
        "QUOTA - Platinum (5th Booking) [EXPECT FAIL]",
        member_platinum.user_id,
        "BRCH-00000",
        2,
        (now + timedelta(days=4)).strftime("%Y-%m-%d"),
        "10:00",
        "12:00",
    )

    # ==================================================================
    # 5. TEST DOUBLE BOOKING ON SAME TABLE AND TIME
    # ==================================================================
    test_date_db = (now + timedelta(days=4)).strftime("%Y-%m-%d")

    test_reservation(
        "DOUBLE BOOK - 1st Valid Booking [EXPECT SUCCESS]",
        member_db.user_id,
        "BRCH-00000",
        2,
        test_date_db,
        "14:00",
        "16:00",
        "TABLE-00000",
    )

    test_reservation(
        "DOUBLE BOOK - Overlap Time [EXPECT FAIL]",
        member_db.user_id,
        "BRCH-00000",
        2,
        test_date_db,
        "15:00",
        "17:00",
        "TABLE-00000",
    )

    print(f'\n{"":═^64}\n')
