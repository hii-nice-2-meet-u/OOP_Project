# MCP Test Prompt 3: Order Management

ก็อปปี้ Prompt ด้านล่างนี้ไปวางใน Claude Desktop ที่เชื่อมต่อกับ MCP Server `BoardGameCafe` แล้ว เพื่อให้ Claude ทำการทดสอบระบบการสั่งซื้ออาหาร

---

**[Copy from here]**

คุณคือผู้ช่วยทดสอบระบบ Board Game Cafe กรุณาทำการทดสอบ **ระบบจัดการออเดอร์ร้านอาหาร (Order Management)** ในสถานการณ์ผิดปกติต่อไปนี้ และสรุป Expected VS Actual

### 1. การเตรียมข้อมูล (Setup)
- เลือกสาขาจาก `get_all_cafe_branches`
- ใช้ `get_branch_menu` เพื่อดูเมนูอาหาร/เครื่องดื่มในสาขานั้น เลือกรหัสอาหาร 1 อย่าง และรหัสเครื่องดื่ม 1 อย่างมาจดไว้
- ใช้ `check_in` จำลองลูกค้าเปิดโต๊ะมา 1 Play Session

### 2. Test Valid Ordering Flow (สั่ง เมนูมีจริง)
- ใช้ `take_order` เพื่อสั่งอาหารที่เลือกไว้มา 1 อย่าง
- ใช้ `get_pending_orders` เพื่อยืนยันว่าออเดอร์นี้เข้าไปค้างอยู่ในระบบของสาขานั้น (`PENDING`)
- **คาดหวัง:** Success ออเดอร์เข้าไปได้ และรอเสิร์ฟ

### 3. Test Invalid Item Order (สั่งเมนูผี)
- ทึกทักเอารหัสที่ไม่ได้อยู่ในเมนูแน่ๆ (เช่น `FOOD-99999`) แล้วใช้ `take_order` สั่งจาก Play Session นี้
- **คาดหวัง:** Failed ระบบปฏิเสธเพราะหาเมนูนั้นในสาขาไม่เจอ

### 4. Test Serving the Order (รันออเดอร์)
- ใช้ `update_order_serve` เพื่อจำลองว่าครัวทำเสร็จแล้ว (ระบรหัสสาขา กับ Order ID ที่สั่งข้อ 2)
- **คาดหวัง:** Success เปลี่ยนสถานะได้

### 5. Test Cancelling served Order (ยกเลิกหลังเสิร์ฟ)
- จากข้อ 4 เมื่อออเดอร์ `SERVED` ไปแล้ว ลองใช้ `update_order_cancel` ไปยกเลิกมัน
- **คาดหวัง:** ล้มเหลว (Failed) หรือทำไม่ได้ (ถ้าโค้ดเขียนดักเอาไว้ว่ายกเลิกได้แค่ตอน Pending หรือ Preparing) — ให้ประเมินผลว่าระบบทำงานยังไง

### 6. Test Ordering after Checkout (สั่งหลอน)
- ทำการชำระเงินปิดโต๊ะ ใช้ `check_out` ปิด Play Session นั้นไป 
- เมื่อ Session นั้นปิดตัวแล้ว ให้ลองเรียก `take_order` ให้ Session ID นั้นอีกครั้ง
- **คาดหวัง:** Failed ระบบต้องไม่อนุญาตให้สั่งของเข้าโต๊ะที่ปิดไปแล้ว

สรุปผลสิ่งที่เกิดขึ้นเทียบกับ Expected ให้ครบถ้วน

---
**[End of Copy]**
