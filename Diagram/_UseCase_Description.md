# Use Case Description — Board Game Cafe System

## Actor Descriptions

| Actor | Description |
|---|---|
| **Member** | ลูกค้าที่ลงทะเบียนแล้ว มีสิทธิ์จอง, เช็คอิน, และสะสมแต้มระดับสมาชิก |
| **Walk-in Customer** | ลูกค้าทั่วไปที่เดินเข้ามาโดยไม่จอง ล็อกอินเป็นแค่ Anonymous |
| **Staff** | พนักงานสาขา ดูแล Session, รับออเดอร์, และ Force Checkout |
| **Manager** | ผู้จัดการสาขา (Inherits จาก Staff) บวกสิทธิ์จัดการเมนู, พนักงาน |
| **Owner** | เจ้าของ สร้างสาขาใหม่ และจัดการผู้จัดการ |
| **Payment Gateway** | ระบบภายนอก (ธนาคาร/บัตรเครดิต/ออนไลน์) รองรับการชำระเงิน |

---

## Use Case Descriptions

### Group 1 — Registration
| UC | ชื่อ | คำอธิบาย |
|---|---|---|
| UC1 🟡 | Register as Member | ลูกค้าสมัครเป็นสมาชิก ระบบสร้าง Member ID และกำหนด Tier เริ่มต้น |
| UC1a 🟡 | Validate Unique Name | ตรวจสอบว่าชื่อที่สมัครไม่ซ้ำกับระบบ |
| UC1b 🟡 | Assign Member ID & Tier | สร้าง MEMBER-XXXXX และตั้ง Tier = NONE_TIER |

### Group 2 — Reservation
| UC | ชื่อ | คำอธิบาย |
|---|---|---|
| UC2 🔵 | **Make Reservation** | สมาชิกจองโต๊ะล่วงหน้า ระบบตรวจสอบกฎและ Assign โต๊ะ |
| UC2a 🟡 | Check Table Availability | ตรวจว่ามีโต๊ะว่างตามวัน/เวลา/จำนวนคน |
| UC2b 🟡 | Validate Booking Rules | ตรวจ Lead Time (≥ 30 นาที), Duration (สูงสุดตาม Tier), Quota ต่อวัน |
| UC2c 🟡 | Assign Table | ล็อกโต๊ะและสร้าง Reservation Record |
| UC3 🔵 | **Cancel Reservation** | สมาชิกยกเลิกการจอง ระบบตรวจ Window เวลาและอัปเดตสถานะ |
| UC3a 🟡 | Verify Reservation Status | ตรวจว่า Reservation ยังเป็น PENDING |
| UC3b 🟡 | Check Cancellation Window | ตรวจว่ายกเลิกก่อนเวลาที่กำหนด (เช่น ≥ 1 ชั่วโมงก่อนเวลาจอง) |
| UC3c 🟡 | Update Status to CANCELLED | เปลี่ยน Reservation Status → CANCELLED |

### Group 3 — Check-in & Session
| UC | ชื่อ | คำอธิบาย |
|---|---|---|
| UC4 🔵 | **Walk-in Check-in** | เปิด Session ใหม่สำหรับลูกค้าที่เดินเข้ามา |
| UC4a 🟡 | Find Available Table | ค้นหาโต๊ะว่างที่จุได้ตามจำนวน |
| UC4b 🟡 | Create Walk-in Profile | สร้าง WalkInCustomer แบบ Anonymous (WALK-XXXXX) |
| UC4c 🟡 | Open Play Session | สร้าง PlaySession และ Assign โต๊ะ → สถานะโต๊ะ = OCCUPIED |
| UC5 🔵 | **Check-in via Reservation** | เช็คอินสำหรับผู้ที่จองล่วงหน้า ตรวจ Window เวลา |
| UC5a 🟡 | Verify Reservation & Time | ตรวจ Reservation Status = PENDING และเวลาอยู่ใน Window ±15 นาที |
| UC5b 🟡 | Mark Reservation COMPLETED | เปลี่ยน Reservation → COMPLETED |
| UC6 🟡 | **Join Existing Session** | เพื่อนเข้าร่วม Session ที่เปิดอยู่แล้ว |
| UC6a 🟡 | Check Session Capacity | ตรวจว่าจำนวนผู้เล่นยังไม่เต็ม Capacity โต๊ะ |

### Group 4 — In-Session Activities
| UC | ชื่อ | คำอธิบาย |
|---|---|---|
| UC7 🔵 | **Order Food & Drinks** | ลูกค้าสั่งอาหาร/เครื่องดื่มระหว่างเล่น |
| UC7a 🟡 | Check Menu Availability | ตรวจว่า MenuItem มีในสาขาและพร้อมเสิร์ฟ |
| UC7b 🟡 | Record Order (PENDING) | สร้าง Order object, Status = PENDING, บันทึก snapshot ราคา |
| UC8 🟡 | **Serve & Update Order** | พนักงานอัปเดตสถานะออเดอร์ |
| UC8a 🟡 | Update Order Status | เปลี่ยน Status → PREPARING / SERVED / CANCELLED |
| UC9 🔵 | **Borrow Board Game** | ยืมบอร์ดเกมจาก Session |
| UC9a 🟡 | Check Game Availability | ตรวจ BoardGameStatus = AVAILABLE |
| UC9b 🟡 | Check Session Time Limit | ตรวจว่า Session ยังไม่หมดเวลาที่จอง |
| UC9c 🟡 | Mark Game as IN-USE | เปลี่ยน BoardGameStatus → IN_USE |
| UC10 🔵 | **Return Board Game** | คืนบอร์ดเกม |
| UC10a 🟡 | Apply Damage Penalty | (extend) ถ้าเกมพัง → เพิ่ม GamePenalty ใน Session |
| UC10b 🟡 | Update Game Status | เปลี่ยน Status → AVAILABLE หรือ MAINTENANCE |

### Group 5 — Checkout & Billing
| UC | ชื่อ | คำอธิบาย |
|---|---|---|
| UC11 🔵 | **Checkout & Pay** | ปิด Session คำนวณบิล และรับชำระเงิน |
| UC11a 🟡 | Verify Session State | ตรวจว่าไม่มีเกมค้าง และไม่มีออเดอร์ PENDING/PREPARING |
| UC11b 🟡 | Calculate Table Fee | คำนวณ Duration × ผู้เล่น × ราคาต่อชั่วโมง |
| UC11c 🟡 | Apply Member Discount | (extend) ถ้ามีสมาชิก → หักส่วนลดตาม Tier |
| UC11d 🟡 | Process Payment | ส่งข้อมูลไปยัง Payment Gateway |
| UC11e 🟡 | Update Member Tier | บวก Total Spent และอัปเดต Tier สมาชิก |
| UC12 🟡 | **Preview Active Bill** | ดูยอดล่าสุดก่อน Checkout |
| UC13 🟡 | **View Bill History** | ดูใบเสร็จย้อนหลัง |
| UC14 🔵 | **Force Checkout (Overstay)** | Staff บังคับ Checkout Session ที่เกินเวลาจอง |

### Group 6 — Management
| UC | ชื่อ | คำอธิบาย |
|---|---|---|
| UC15 🟡 | **Manage Menu** | เพิ่ม/แก้ไข/ลบรายการอาหาร-เครื่องดื่มในสาขา |
| UC16 🟡 | **Manage Board Games** | เพิ่ม/แก้ไขบอร์ดเกม, ส่งซ่อม (MAINTENANCE) |
| UC17 🟡 | **Manage Tables** | เพิ่มโต๊ะ, ตรวจสอบสถานะ |
| UC18 🟡 | **Manage Branch Staff** | เพิ่ม/ย้ายพนักงานในสาขา |
| UC19 🟡 | **Create Cafe Branch** | เปิดสาขาใหม่ (Owner เท่านั้น) |

---

## Color Legend

| สี | ความหมาย |
|---|---|
| 🔵 **LightBlue** | Use Case ที่มีความซับซ้อน เกี่ยวกับ Transaction / ธุรกรรม → นำไปเขียน Sequence Diagram |
| 🟡 **LightYellow** | Use Case ย่อย / ง่าย เป็น Sub-step ของ Use Case หลัก |
