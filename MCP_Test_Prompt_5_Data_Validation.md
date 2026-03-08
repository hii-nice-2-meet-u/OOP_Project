# MCP Test Prompt 5: Data Validation

ก็อปปี้ Prompt ด้านล่างนี้ไปวางใน Claude Desktop ที่เชื่อมต่อกับ MCP Server `BoardGameCafe` แล้ว เพื่อให้ Claude ทำการทดสอบ Data Validation ดักจับบัคเบื้องหลัง

---

**[Copy from here]**

คุณคือผู้ช่วยทดสอบระบบ Board Game Cafe ผ่าน MCP Tools กรุณาทำการทดสอบขอบเขตข้อมูล **(Data Validation)** เพื่อหาช่องโหว่ด้านระบบ โดยไม่ต้องสนใจ User Flow 

### 1. Test ID Type Spoofing (ใส่ ID ปลอม/สลับประเภท)
- ลองใช้ `cancel_reservation` โดยใส่ ID ของโต๊ะแทน (`TABLE-00000` แทน `RESV-00000`)
- ลองใช้ `search_board_game_by_min_players` โดยใส่รหัสสาขาเป็น `EMP-00000` แทน 
- **คาดหวัง:** ระบบต้องตรวจจับ Format ของ ID และไม่แครช (Failed พร้อมบอกว่า Invalid ID Type)

### 2. Test Negative Numbers & Zero Limit (ค่าติดลบ)
- ใช้ `search_available_table` แต่ใส่ `required_capacity = -5`
- ใช้ `check_in` แต่จงใจใส่ Parameter `player_amount = -1` หรือ `0` 
- **คาดหวัง:** ระบบต้องไม่อนุญาตให้เปิดโต๊ะเพื่อคน -1 คน (Failed บอกว่าจำนวนต้องเป็นค่าบวก)

### 3. Test Invalid Time format Strings
- ใช้ `make_reservation` โดยระบุ `date_str` เป็นรูปแบบที่ผิด (เช่น "2024/07/01" หรือ "วันพุธหน้า") และ `start_t` เป็น "บ่ายสามโมง" แทน "15:00"
- **คาดหวัง:** ระบบตอบรับ Failed อย่างถูกสุขลักษณะ ไม่ใช่การรันล้มเหลวแบบ Python Traceback 

### 4. Test Missing Arguments (ส่งไปไม่ครบ)
- (ถ้าประยุกต์ทำได้ใน Claude) ลองเรียก Tool `take_order` โดยส่งให้แค่ Play Session ID แต่ไม่ใส่ Menu Item ID
- **คาดหวัง:** Claude หรือ MCP Server เตือนกลับมาว่า Missing required variables

ทำจบแล้วโปรดสรุปว่าในแง่ของ Robustness (ความทนทาน) ของระบบ โค้ดมีการทิ้ง Error แปลกๆ ที่ไม่ได้ถูกเขียนครอบไว้หลุดออกมาหรือไม่

---
**[End of Copy]**
