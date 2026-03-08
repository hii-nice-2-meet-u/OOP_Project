# MCP Prompt Test Cases for BoardGameCafe

Below is a complete suite of test prompts designed to evaluate the functionality of the BoardGameCafe MCP tools.
You can copy and paste these prompts directly into a Claude chat (where the MCP server is loaded) to test the system endpoints.

---

## 1. Information Retrieval (ตรวจสอบข้อมูลพื้นฐาน)

**Prompt 1.1:** ขอดูข้อมูลคนในร้านทั้งหมดหน่อย โดยแสดงของประเภท "staff"
* **Expected Tool Call:** `get_person_by_type("staff")`
* **Expected Outcome:** List of staff members (e.g., ID: STAFF-00000 Lana Rhoades, STAFF-00001 Jew).

**Prompt 1.2:** ขอเช็คสาขาทั้งหมดที่มีในระบบ พร้อมจำนวนโต๊ะรวม
* **Expected Tool Call:** `get_all_cafe_branches()`
* **Expected Outcome:** List of 2 branches: 'MasoPeeso 67 Cafe (ID: BRCH-00000)' and 'Ladkrabang Branch (ID: BRCH-00001)'.

**Prompt 1.3:** ขอรายชื่อบอร์ดเกมทั้งหมดที่อยู่ในสาขา BRCH-00001
* **Expected Tool Call:** `get_branch_board_games("BRCH-00001")`
* **Expected Outcome:** List of games including Ultimate Werewolf, Exploding Kittens, Salem 1692, etc.

**Prompt 1.4:** ในสาขา BRCH-00000 (MasoPeeso 67 Cafe) มีเกมอะไรบ้างที่เล่นตั้งแต่ 5 คนขึ้นไป?
* **Expected Tool Call:** `search_board_game_by_min_players("BRCH-00000", 5)`
* **Expected Outcome:** List of games requiring 5+ players (e.g., Avalon).

**Prompt 1.5:** ขอดูโต๊ะทั้งหมดที่มีอยู่ในสาขา BRCH-00000 หน่อย และช่วยหาว่าตอนนี้มีโต๊ะไหนที่รองรับคนได้ 6 คนและกำลังว่าง (Available) อยู่บ้าง
* **Expected Tool Calls:** `get_branch_tables("BRCH-00000")` -> `search_available_table("BRCH-00000", 6)`
* **Expected Outcome:** Table ID with capacity 6 and status showing available.

**Prompt 1.6:** ขอดูเมนูอาหารและเครื่องดื่มในสาขา BRCH-00001 หน่อย
* **Expected Tool Call:** `get_branch_menu("BRCH-00001")`
* **Expected Outcome:** List of food items (Pad Thai Goong, Green Curry) and drinks (Pink Milk, Thai Iced Tea) with prices.

---

## 2. Reservation & Member Management (ระบบสมาชิกและการจอง)

**Prompt 2.1:** สมัครสมาชิกใหม่ให้หน่อย ชื่อ "สมชายใจดี"
* **Expected Tool Call:** `create_customer_member("สมชายใจดี")`
* **Expected Outcome:** Confirmation of created member ID (e.g., CSTM-0000X).

**Prompt 2.2:** สมชายใจดี ต้องการจองโต๊ะที่ "Ladkrabang Branch" วันเพาะวันพรุ่งนี้ (ระบุวันที่ เช่น "2026-03-09") ตั้งแต่ 18:00 ถึง 20:00 สำหรับ 4 คน ช่วยทำการจองให้หน่อย!
* **Expected Tool Call:** `make_reservation("สมชายใจดี", "Ladkrabang Branch", 4, "2026-03-09", "18:00", "20:00")`
* **Expected Outcome:** Reservation ID (e.g., RSV-0000X) at a specific table.

**Prompt 2.3:** ลูกค้า 2 คน Walk-in เข้ามาที่สาขา BRCH-00000 ช่วยจัดโต๊ะ (Check-in) ให้หน่อย
* **Expected Tool Call:** `check_in("BRCH-00000", 2, "walk_in", "auto")`
* **Expected Outcome:** Session ID (e.g., PLYS-0000X) and Table ID.

---

## 3. Session & Board Game Management (จัดการ Session และบอร์ดเกม)

*(Note: Replace `PLYS-XXXXX` and `BGM-XXXXX` with actual IDs from previous steps)*

**Prompt 3.1:** มีเพื่อนแวะมาเพิ่ม 1 คน! ขอ Join เข้า Play Session รหัส [โชว์ Session ID ล่าสุด] ในฐานะ Walk-in
* **Expected Tool Call:** `join_session("PLYS-XXXXX", "walk_in")`
* **Expected Outcome:** "เข้าร่วมสำเร็จ" (Success message).

**Prompt 3.2:** ลูกค้า Session [โชว์ Session ID ล่าสุด] อยากยืมเกม "Uno" ในสาขานั้น ช่วยยืมให้หน่อย
* **Expected Tool Calls:** `get_branch_board_games("BRCH-00000")` (to find Uno ID) -> `borrow_board_game("PLYS-XXXXX", "BGM-XXXXX")`
* **Expected Outcome:** "ยืมสำเร็จ" (Success message).

**Prompt 3.3:** ลูกค้าเล่นเกม "Uno" เสร็จแล้ว ขอคืนเกมกลับไปที่แคชเชียร์
* **Expected Tool Call:** `return_board_game("PLYS-XXXXX", "BGM-XXXXX")`
* **Expected Outcome:** "คืนสำเร็จ" (Success message).

---

## 4. Order & Checkout (สั่งอาหาร/เครื่องดื่ม และเช็คบิล)

*(Note: Requires active Session ID and Menu Item IDs)*

**Prompt 4.1:** ลูกค้า Session นี้ หิว! จัดสั่ง "Pink Lemonade Soda" 1 แก้ว และ "Larb French Fries" 1 ที่ให้หน่อย
* **Expected Tool Calls:** `get_branch_menu("BRCH-XXXXX")` (to find menu IDs) -> `take_order("PLYS-XXXXX", "MENU-XXXXX")` (twice)
* **Expected Outcome:** Order IDs for both items.

**Prompt 4.2:** ลองเช็คคิวออเดอร์ (Pending Orders) ของสาขานี้ดูหน่อย ว่ามีออเดอร์ค้างไหม
* **Expected Tool Call:** `get_pending_orders("BRCH-XXXXX")`
* **Expected Outcome:** List of pending orders showing the recently ordered items.

**Prompt 4.3:** ครัวทำ "Pink Lemonade Soda" เสร็จแล้ว! ช่วย Update ออเดอร์ของน้ำแก้วนี้เป็นสถานะ "Served" หน่อย
* **Expected Tool Call:** `update_order_serve("PLYS-XXXXX", "ORDR-XXXXX")`
* **Expected Outcome:** "อัปเดตสถานะเป็นเสิร์ฟแล้ว" (Success message).

**Prompt 4.4:** สุดท้ายนี้ ลูกค้าเล่นเสร็จแล้ว ขอ Check-out ด้วย! คิดเงินให้ด้วยนะ แบบจ่ายเป็น "cash"
* **Expected Tool Call:** `check_out("PLYS-XXXXX", "cash")`
* **Expected Outcome:** Success message with Total amount and Receipt ID (e.g., PYMT-XXXXX).
คุณคือเจ้าหน้าที่ร้าน Board Game Cafe กรุณาทำตามขั้นตอนต่อไปนี้ตามลำดับ

--- เตรียมข้อมูล ---

1. ดูรายชื่อสาขาทั้งหมด แล้วจำ branch_id สาขาแรกไว้
2. สร้างสมาชิกใหม่ชื่อ "อลิซ" แล้วจำ member_id ไว้
3. สร้างสมาชิกใหม่ชื่อ "บ็อบ" แล้วจำ member_id ไว้

--- เซสชัน 1: อลิซ สั่งอาหาร ---

4. เช็คอินอลิซที่สาขาที่ได้มา จำนวน 2 คน แล้วจำ session_id ไว้
5. ดูเมนูของสาขา แล้วจำ item_id อย่างน้อย 2 รายการ
6. สั่งเมนูรายการที่ 1 ให้เซสชันนี้
7. สั่งเมนูรายการที่ 2 ให้เซสชันนี้
8. เสิร์ฟเมนูรายการที่ 1
9. ยกเลิกเมนูรายการที่ 2
10. เช็คเอาต์เซสชันนี้ด้วยเงินสด
11. ✅ เรียก bill_history ของเซสชันนี้ แล้วบอกว่าผลที่ได้ถูกต้องไหม

--- เซสชัน 2: อลิซ อีกครั้ง ---

12. เช็คอินอลิซอีกครั้ง จำนวน 1 คน
13. สั่งเมนูรายการที่ 1
14. เช็คเอาต์
15. ✅ เรียก bill_history_by_person ของอลิซ แล้วบอกว่าเห็นกี่เซสชัน และยอดรวมถูกต้องไหม

--- เซสชัน 3: บ็อบ ไม่สั่งอาหาร ---

16. เช็คอินบ็อบ จำนวน 3 คน
17. เช็คเอาต์ทันทีโดยไม่สั่งอะไร
18. ✅ เรียก bill_history และ bill_history_by_person ของบ็อบ แล้วบอกผลที่ได้

--- กรณีพิเศษ ---

19. สร้างสมาชิกใหม่ชื่อ "ผี" แต่ไม่ทำอะไรเพิ่ม
20. ✅ เรียก bill_history_by_person ของผี แล้วบอกว่าระบบตอบว่าอะไร

--- สรุปผล ---

สรุปผลการทดสอบทั้งหมดว่า test ไหนผ่าน ✅ และ test ไหนมีปัญหา ❌