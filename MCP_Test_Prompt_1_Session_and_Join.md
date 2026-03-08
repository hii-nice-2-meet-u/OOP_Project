# MCP Test Prompt 1: Play Session & Join Session

ก็อปปี้ Prompt ด้านล่างนี้ไปวางใน Claude Desktop ที่เชื่อมต่อกับ MCP Server `BoardGameCafe` แล้ว เพื่อให้ Claude ทำการทดสอบระบบ Play Session

---

**[Copy from here]**

คุณคือผู้ช่วยทดสอบระบบ Board Game Cafe ผ่าน MCP Tools กรุณาทำการทดสอบระบบ **Play Session และการ Join Session** ตามขั้นตอนด้านล่างนี้ โดยรายงานผลลัพธ์ว่าสำเร็จ (Success) หรือล้มเหลว (Failed ตรงตามที่คาดหวังหรือไม่)

### 1. การเตรียมข้อมูล (Setup)
- ใช้ `get_all_cafe_branches` เพื่อเลือก 1 สาขา (เช่น "Ladkrabang")
- ใช้ `get_branch_tables` เพื่อตรวจดูรายการโต๊ะทั้งหมด และเลือกโต๊ะว่าง (`AVAILABLE`) ที่มีความจุ (Capacity) จำนวน **4 คน** มา 1 โต๊ะ (สมมติว่าเป็น โต๊ะ A)

### 2. Test Auto-assign & Capacity Limit (เกินความจุโต๊ะ)
- ใช้ `check_in` สาขาเดิมสำหรับลูกค้า Walk-in จำนวน **4 คน** แบบ Auto-assign (ไม่ระบุโต๊ะ) คาดว่าระบบจะจัด โต๊ะ A ให้ และตอนจบได้ Play Session ID มา 1 อัน
- ใช้ `join_session` ค่อยๆ เพิมลูกค้า Walk-in เข้าไปใน Play Session ID นี้ทีละคน
  - **คาดหวัง:** หูดับ (Failed) เมื่อพยายามเพิ่มคนที่ 5 เข้าไปในโต๊ะ A เพราะความจุของโต๊ะเต็มแค่ 4 คน (ตรวจสอบว่ามี Error แจ้งเตือนเรื่อง Capacity ทะลุหรือไม่)

### 3. Test Check-in to Occupied Table (ซ้อนสถานะโต๊ะ)
- ตรวจดูโต๊ะในสาขาจนเจอโต๊ะที่มีสถานะ `OCCUPIED` (เช่น โต๊ะ A)
- ใช้ `check_in` สาขานี้ ให้ลูกค้าระบุ ID ตรงกับโต๊ะที่ `OCCUPIED` ไปเลยตรงๆ
- **คาดหวัง:** ต้องล้มเหลว (Failed) เพราะระบบต้องดักไม่ให้ลูกค้ากลุ่มใหม่ยัดลงโต๊ะที่คนอื่นนั่งอยู่แล้ว

### 4. Test Late Check-in for Reservation (มาสายเกิน 15 นาที)
*หมายเหตุ: เนื่องจาก Tool อาจไม่รองรับการ Time Travel จึงขอให้จำลองเท่าที่ทูลทำได้*
- ใช้ `create_customer_member` สร้างคน 1 คนชื่อ "Late Customer"
- ใช้ `make_reservation` จองโต๊ะวันนี้ โดยกำหนดเวลา Start เป็นเวลาที่ *ผ่านไปแล้ว 30 นาที* (ตัวอย่าง: ตอนนี้ 10:00 แต่จองให้เป็น 09:30)
- ลองใช้ `check_in_reserved` เพื่อเช็คอิน (ให้ Customer ID เข้ากับ Reservation ID นั้น)
- **คาดหวัง:** ล้มเหลว (Failed) พร้อมกับข้อความว่ามาสายเกิน 15 นาที และสถานะ (ถ้าเช็คได้) เปลี่ยนเป็น `NO_SHOW`

หลังจากทำครบทุกข้อ โปรดสรุปเป็นตาราง Expected VS Actual ว่าระบบป้องกันตรงตามเงื่อนไขหรือไม่

---
**[End of Copy]**
