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

    # สร้างสมาชิกระดับ Platinum เพื่อให้โควตาจองได้ 3 คิวพร้อมกัน
    member_cancel = Member("Cancel Tester")
    member_cancel.member_tier = MemberTier.PLATINUM
    sys.add_person(member_cancel)

    # / ════════════════════════════════════════════════════════════════
    # PREPARE DATA: สร้างใบจอง 3 ใบเพื่อนำมาใช้ทดสอบ
    # / ════════════════════════════════════════════════════════════════
    now = datetime.now()
    
    # ใช้วันที่ 5 วันล่วงหน้า เพื่อให้ผ่านกฎการจองทั้งหมด
    test_date = (now + timedelta(days=5)).strftime("%Y-%m-%d")

    # คิวที่ 1: เตรียมไว้ทดสอบ "ยกเลิกคิวที่กินเสร็จแล้ว (COMPLETED)"
    resv_1 = sys.make_reservation(member_cancel.user_id, "BRCH-00000", 2, test_date, "10:00", "12:00")
    
    # คิวที่ 2: เตรียมไว้ทดสอบ "ยกเลิกคิวที่เลยเวลาจองไปแล้ว (LATE)"
    resv_2 = sys.make_reservation(member_cancel.user_id, "BRCH-00000", 2, test_date, "14:00", "16:00")
    
    # คิวที่ 3: เตรียมไว้ทดสอบ "ยกเลิกแบบถูกต้อง (VALID)" และ "ยกเลิกซ้ำ (ALREADY CANCELLED)"
    resv_3 = sys.make_reservation(member_cancel.user_id, "BRCH-00000", 2, test_date, "18:00", "20:00")

    # / ════════════════════════════════════════════════════════════════
    # HELPER FUNCTION: ตัวช่วยปริ้นท์ผลการทดสอบ
    # / ════════════════════════════════════════════════════════════════
    def test_cancel(description, resv_id, fake_current_time=None):
        print(f"\n{'-'*64}")
        print(f" TEST     : {description}")
        
        if fake_current_time is not None:
            print(f" NOW      : {fake_current_time.strftime('%Y-%m-%d %H:%M')} (Simulated)")
        else:
            print(f" NOW      : {datetime.now().strftime('%Y-%m-%d %H:%M')}")
            
        print(f"{'-'*64}")
        
        try:
            sys.cancel_reservation(resv_id, current_time=fake_current_time)
            resv = sys.find_reservation_by_id(resv_id)
            print(f" ✅ SUCCESS -> Resv ID: {resv_id} | Status: {resv.status.name}")
        except Exception as e:
            print(f" ❌ FAILED  -> {type(e).__name__}: {str(e)}")


    print(f'\n{" COMPREHENSIVE CANCEL RESERVATION TESTS ":═^64}\n')

    # โชว์สถานะเริ่มต้น
    print(f'{"INITIAL":<10}:\t{ [f"{a.reservation_id} ({a.status.name})" for a in sys.reservations] } \n')

    # ==================================================================
    # TEST 1: ยกเลิกใบจองที่กินเสร็จไปแล้ว (COMPLETED) [EXPECT FAIL]
    # ==================================================================
    # เช็คอินคิวที่ 1 ให้กลายเป็น COMPLETED ก่อน
    fake_checkin_time = datetime.strptime(f"{resv_1.date} {resv_1.start_time}", "%Y-%m-%d %H:%M")
    sys.check_in_reserved(resv_1.reservation_id, member_cancel.user_id, current_time=fake_checkin_time)
    
    # ลองกดยกเลิก
    test_cancel("CANCEL COMPLETED [EXPECT FAIL]", resv_1.reservation_id)

    # ==================================================================
    # TEST 2: ยกเลิกเมื่อเลยเวลาจองไปแล้ว (LATE) [EXPECT FAIL]
    # ==================================================================
    # จำลองเวลาปัจจุบันให้เลยเวลา 14:00 ไปแล้ว (เป็น 14:30)
    fake_late_time = datetime.strptime(f"{resv_2.date} 14:30", "%Y-%m-%d %H:%M")
    
    # ลองกดยกเลิก
    test_cancel("CANCEL LATE (After Time) [EXPECT FAIL]", resv_2.reservation_id, fake_current_time=fake_late_time)

    # ==================================================================
    # TEST 3: ยกเลิกแบบถูกต้อง (ก่อนเวลา) [EXPECT SUCCESS]
    # ==================================================================
    # จำลองเวลาปัจจุบันให้อยู่ก่อน 18:00 (เป็น 16:00)
    fake_valid_time = datetime.strptime(f"{resv_3.date} 17:00", "%Y-%m-%d %H:%M")
    
    # ลองกดยกเลิก
    test_cancel("VALID CANCEL [EXPECT SUCCESS]", resv_3.reservation_id, fake_current_time=fake_valid_time)

    # ==================================================================
    # TEST 4: ยกเลิกซ้ำ (ALREADY CANCELLED) [EXPECT FAIL]
    # ==================================================================
    # พยายามยกเลิกคิวที่ 3 (ที่เพิ่งยกเลิกสำเร็จไปเมื่อสักครู่) อีกรอบ
    test_cancel("CANCEL ALREADY CANCELLED [EXPECT FAIL]", resv_3.reservation_id, fake_current_time=fake_valid_time)

    # ==================================================================
    print(f'\n{"FINAL":<10}:\t{ [f"{a.reservation_id} ({a.status.name})" for a in sys.reservations] } ')
    print(f'\n{"":═^64}\n')