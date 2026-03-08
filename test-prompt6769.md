# 🎲 Board Game Cafe — MCP Demo Test Prompts
> ไฟล์นี้ใช้สาธิตการใช้งาน MCP Tools ทุก Flow ตั้งแต่เริ่มต้นจนจ่ายเงิน

---

## ═══════════════════════════════════════════════
## 🔍 PHASE 0 — ดูข้อมูลระบบเบื้องต้น
## ═══════════════════════════════════════════════

### 0.1 ดูสาขาทั้งหมด
```
Show me all cafe branches in the system.
```

### 0.2 ดูโต๊ะในสาขา
```
Show me all tables in branch BRCH-00000.
```

### 0.3 ดูเมนูในสาขา
```
Show me the full menu of branch BRCH-00000.
```

### 0.4 ดูบอร์ดเกมในสาขา
```
Show me all board games available in branch BRCH-00000.
```

### 0.5 ดูสมาชิกในระบบ
```
Show me all Members in the system.
```

### 0.6 ค้นหาโต๊ะว่าง
```
Search for available tables in branch BRCH-00000 for 4 players.
```

---

## ═══════════════════════════════════════════════
## 📅 PHASE 1A — การจอง (Reservation) — ล่วงหน้า
## ═══════════════════════════════════════════════

### 1A.1 จองโต๊ะล่วงหน้า (Member จอง)
```
I want to make a reservation.
- Customer name: Pao
- Branch: MasoPeeso 67 Cafe
- Number of players: 4
- Date: 2026-03-15
- Start time: 18:00
- End time: 21:00
- Table ID: TABLE-00001

Please book this table for me.
```

### 1A.2 จองโต๊ะสาขาอื่น (Member คนละคน)
```
Make a reservation for Sua at Ladkrabang Branch,
2 players, date 2026-03-20, from 14:00 to 16:00, table TABLE-00005.
```

### 1A.3 ยกเลิกการจอง
```
Please cancel reservation RESV-00000. Current time is 2026-03-14 10:00.
```

### 1A.4 Check-in ด้วย Reservation
```
Check in using reservation RESV-00001.
Customer ID: MEMBER-00001
Current time: 2026-03-20 14:00
```

---

## ═══════════════════════════════════════════════
## 🚶 PHASE 1B — Walk-in (ไม่จอง มาถึงเลย)
## ═══════════════════════════════════════════════

### 1B.1 Walk-in แบบไม่ระบุโต๊ะ (auto assign)
```
A walk-in customer wants to check in at branch BRCH-00000.
There are 3 players. No reservation. Please check them in automatically.
```

### 1B.2 Walk-in แบบระบุโต๊ะเอง
```
Check in a walk-in group at branch BRCH-00000,
4 players, assign them to table TABLE-00002 please.
```

### 1B.3 Walk-in แบบ Member มาเอง (ไม่จองล่วงหน้า)
```
Member "Pao" walks in at branch BRCH-00000 with 2 players.
Check her in without a reservation. Auto-assign table.
```

---

## ═══════════════════════════════════════════════
## 🎮 PHASE 2 — ระหว่างเล่น (During Session)
## ═══════════════════════════════════════════════

> สมมติว่า Session ID คือ PS-00000 (ปรับตาม output จริงจาก check-in)

### 2.1 ยืมบอร์ดเกม
```
Borrow board game BG-00000 (Uno) for session PS-00000.
```

### 2.2 ยืมบอร์ดเกมชิ้นที่สอง
```
Also borrow board game BG-00001 (Monopoly) for session PS-00000.
```

### 2.3 คืนบอร์ดเกม (ปกติ)
```
Return board game BG-00000 for session PS-00000. It's not damaged.
```

### 2.4 คืนบอร์ดเกม (ชำรุด)
```
Return board game BG-00001 for session PS-00000. The game is damaged.
```

### 2.5 เพิ่มคนเข้า Session
```
A new walk-in customer wants to join session PS-00000.
```

### 2.6 สั่งอาหาร
```
Order "Spicy BBQ Wings" (FOOD-00000) for session PS-00000.
Order "Spicy BBQ Wings" (FOOD-00000) for session PS-00001.
Order "Spicy BBQ Wings" (FOOD-00000) for session PS-00002.
```

### 2.7 สั่งเครื่องดื่ม
```
Order "Thai Milk Tea" (DRINK-00000) for session PS-00000.
Order "Thai Milk Tea" (DRINK-00000) for session PS-00001.
Order "Thai Milk Tea" (DRINK-00000) for session PS-00002.
```

### 2.8 สั่งอาหารเพิ่มอีก
```
Order (FOOD-00002) for session PS-00000.
Order (FOOD-00001) for session PS-00001.
Order (FOOD-00002) for session PS-00001.
```

### 2.9 ดู Order ที่รอดำเนินการ
```
Show me all pending orders for branch BRCH-00000.
```

### 2.10 อัปเดต Order → Served
```
Mark order ORDER-00000 as served in session PS-00000.
```

### 2.11 ยกเลิก Order
```
Cancel order ORDER-00001 in session PS-00000.
```

---

## ═══════════════════════════════════════════════
## 💳 PHASE 3 — Check-out & Payment
## ═══════════════════════════════════════════════

โดยทุก checkout ใช้เวลา โต๊ะต่างกัน 
PS-0000 1 ชั่วโมง
PS-0001 1.5 ชั่วโมง
PS-0002 2 ชั่วโมง

### 3.1 จ่ายด้วย 💵 เงินสด (Cash)
```
Check out session PS-00000 using cash. The customer pays 1000 baht.
```

---

### 3.2 จ่ายด้วย 💳 บัตรเครดิต (Credit Card)
> (ใช้กับ Session ใหม่ เช่น PS-00001)
```
Check out session PS-00001 using credit card.
Card number: 4111111111111111
Expiry date: 12/28
CVV: 123
```

---

### 3.3 จ่ายด้วย 📱 Online Payment (PromptPay / QR)
> (ใช้กับ Session ใหม่ เช่น PS-00002)
```
Check out session PS-00002 using online payment.
Email: customer@email.com
```

---

## ═══════════════════════════════════════════════
## 🧾 PHASE 4 — ดูบิล & ประวัติ
## ═══════════════════════════════════════════════

### 4.1 ดูบิลของ Session นั้น
```
Show the bill / receipt for session PS-00000.
```

### 4.2 ดูประวัติบิลของลูกค้า Member
```
Show the full billing history for member MEMBER-00000.
```

### 4.3 ดู Tier ของสมาชิก (หลัง checkout)
```
Show me all Members and their current tier and total spent.
```

---

## ═══════════════════════════════════════════════
## ⚙️ PHASE 5 — Admin Tools (Owner / Manager)
## ═══════════════════════════════════════════════

### 5.1 เพิ่มโต๊ะใหม่
```
Add a new table with capacity 6 to branch BRCH-00000.
Authorized by OWNER-PESO67.
```

### 5.2 เพิ่มเมนูอาหารใหม่
```
Add a new food item to branch BRCH-00000:
Name: "Mango Sticky Rice", Price: 85 baht, Description: "Classic Thai dessert"
Authorized by MANAGER-00000.
```

### 5.3 เพิ่มเมนูเครื่องดื่มใหม่
```
Add a new drink to branch BRCH-00000:
Name: "Coconut Shake", Price: 70 baht, Cup size: L, Description: "Fresh blended coconut"
Authorized by OWNER-PESO67.
```

### 5.4 เพิ่ม Staff ใหม่
```
Add a new staff member named "Nong" to branch BRCH-00001.
Authorized by MANAGER-00001.
```

### 5.5 เพิ่ม Spent ให้สมาชิก (manual)
```
Add 500 baht of spent to customer MEMBER-00000.
Authorized by OWNER-PESO67.
```

### 5.6 สร้าง Member ใหม่
```
Create a new customer member named "Beam".
```

---

## ═══════════════════════════════════════════════
## 🔁 FULL DEMO SCRIPT — รันทีเดียวต่อเนื่อง
## ═══════════════════════════════════════════════
> คัดลอก prompt นี้ไปรันกับ Claude + MCP เพื่อสาธิตครั้งเดียวจบ

```
Let's run a full demo of the Board Game Cafe system. Please follow these steps one by one:

STEP 1: Show all cafe branches and all members in the system.

STEP 2: Search for available tables at branch BRCH-00000 for 4 people.

STEP 3: Walk-in check-in — 4 players at branch BRCH-00000, auto-assign table.

STEP 4: Show the session ID from step 3. Then borrow board game BG-00000 for that session.

STEP 5: Show the full menu of branch BRCH-00000, then order:
  - FOOD-00000 (first food item)
  - DRINK-00000 (first drink item)
  - FOOD-00001 (second food item)
  for the session.

STEP 6: Show all pending orders for branch BRCH-00000.

STEP 7: Mark the first order (ORDER-00000) as served.

STEP 8: Return board game BG-00000 — it's not damaged.

STEP 9: Check out the session using cash, paying 2000 baht.

STEP 10: Show the receipt/bill for that session.
```

---

## ═══════════════════════════════════════════════
## 📝 NOTES สำหรับผู้สาธิต
## ═══════════════════════════════════════════════

| ตัวแปร | ค่าตัวอย่าง | หมายเหตุ |
|---|---|---|
| Branch สาขา 1 | `BRCH-00000` | MasoPeeso 67 Cafe |
| Branch สาขา 2 | `BRCH-00001` | Ladkrabang Branch |
| Owner | `OWNER-PESO67` | Jordi El Niño Polla |
| Manager สาขา 1 | `MANAGER-00000` | Mia Kalifa |
| Manager สาขา 2 | `MANAGER-00001` | Rae Lil Black |
| Member | `MEMBER-00000` | Pao |
| Member | `MEMBER-00001` | Sua |
| Payment Methods | `cash` / `credit` / `online` | ใส่ใน `method_type` |
| Session ID | `PS-XXXXX` | ได้จาก check_in response |
| Order ID | `ORDER-XXXXX` | ได้จาก take_order response |

> ⚠️ **Session ID และ Order ID จะเปลี่ยนทุกครั้งที่รันใหม่** — ควรจด ID จาก response จริงก่อนใช้ใน step ถัดไป