from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import JSONResponse
from enum import Enum
from typing import Dict
import uuid
import uvicorn

app = FastAPI()


# =========================
# ENUMS
# =========================


class MemberTier(str, Enum):
    NONE = "NONE"
    BRONZE = "BRONZE"
    SILVER = "SILVER"
    GOLD = "GOLD"


class PaymentMethod(str, Enum):
    CASH = "CASH"
    CREDIT_CARD = "CREDIT_CARD"
    QR = "QR"


class PaymentStatus(str, Enum):
    PENDING = "PENDING"
    CONFIRMED = "CONFIRMED"
    FAILED = "FAILED"


# =========================
# DOMAIN
# =========================


class Customer:
    def __init__(self, customer_id: str, total_spent: float = 0):
        self.customer_id = customer_id
        self.total_spent = total_spent
        self.member_tier = MemberTier.NONE
        self._update_member_tier()

    def add_spending(self, amount: float):
        self.total_spent += amount
        self._update_member_tier()

    def _update_member_tier(self):
        if self.total_spent >= 1000:
            self.member_tier = MemberTier.GOLD
        elif self.total_spent >= 500:
            self.member_tier = MemberTier.SILVER
        elif self.total_spent > 69:
            self.member_tier = MemberTier.BRONZE
        else:
            self.member_tier = MemberTier.NONE

    def get_discount_rate(self):
        return {
            MemberTier.GOLD: 0.20,
            MemberTier.SILVER: 0.10,
            MemberTier.BRONZE: 0.05,
            MemberTier.NONE: 0.0,
        }[self.member_tier]


class Payment:
    def __init__(self, amount: float, method: PaymentMethod):
        self.id = str(uuid.uuid4())
        self.amount = amount
        self.method = method
        self.status = PaymentStatus.PENDING


# =========================
# SERVICE
# =========================


class CafeService:
    def __init__(self):
        self.customers: Dict[str, Customer] = {}
        self._seed()

    def _seed(self):
        self.customers["C001"] = Customer("C001", 120)
        self.customers["C002"] = Customer("C002", 600)
        self.customers["C003"] = Customer("C003", 50)

        print("\n=== CUSTOMER LIST ===")
        for cid, c in self.customers.items():
            print(f"{cid} | Total: {c.total_spent} | Tier: {c.member_tier}")
        print("=====================\n")

    def get_customer(self, customer_id: str) -> Customer:
        if customer_id not in self.customers:
            raise HTTPException(status_code=404, detail="ไม่พบเมมเบอร์นี้")
        return self.customers[customer_id]

    async def complete_purchase(self, customer_id, amount, payment_method):
        customer = self.get_customer(customer_id)

        payment = Payment(amount, payment_method)
        payment.status = PaymentStatus.CONFIRMED

        customer.add_spending(amount)

        return {
            "status": "success",
            "customerId": customer_id,
            "memberTier": customer.member_tier,
            "discountRate": customer.get_discount_rate(),
            "totalSpent": customer.total_spent,
        }


cafe_service = CafeService()


# =========================
# ERROR FORMAT
# =========================


@app.exception_handler(HTTPException)
async def custom_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code, content={"status": "error", "message": exc.detail}
    )


# =========================
# ENDPOINT
# =========================


@app.post("/completePurchase")
async def complete_purchase(
    customerId: str = Query(...),
    amount: float = Query(..., gt=0),
    paymentMethod: PaymentMethod = Query(...),
):
    return await cafe_service.complete_purchase(customerId, amount, paymentMethod)


# =========================
# RUN
# =========================

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
