from datetime import datetime
from typing import Dict, List, Optional


# ==========================================
# BRANCH (DATA HOLDER)
# ==========================================

class BoardGameCafeBranch:
    """
    Branch = แค่เก็บข้อมูล
    ไม่มี business logic หนัก ๆ
    """

    def __init__(self, cafe_id: str, name: str, location: str):
        self.cafe_id = cafe_id
        self.name = name
        self.location = location

        # data containers
        self.customers: Dict[str, object] = {}
        self.members: Dict[str, object] = {}
        self.staff: Dict[str, object] = {}

        self.orders: Dict[str, object] = {}
        self.reservations: Dict[str, object] = {}
        self.payments: Dict[str, object] = {}

        self.board_games: List[object] = []
        self.play_tables: List[object] = []
        self.menu = None


# ==========================================
# SYSTEM (ALL LOGIC)
# ==========================================

class BoardGameCafeSystem:
    """
    System = สมองทั้งหมด
    คุมทุก branch และทุก logic
    """

    def __init__(self, version="3.0"):
        self.version = version
        self.branches: Dict[str, BoardGameCafeBranch] = {}

    # ------------------
    # BRANCH
    # ------------------

    def add_branch(self, branch: BoardGameCafeBranch):
        self.branches[branch.cafe_id] = branch

    def get_branch(self, cafe_id: str) -> Optional[BoardGameCafeBranch]:
        return self.branches.get(cafe_id)

    # ------------------
    # MEMBER / AUTH
    # ------------------

    def register_member(self, branch: BoardGameCafeBranch, member):
        if member.member_id in branch.members:
            raise ValueError("Member already exists")

        branch.members[member.member_id] = member
        branch.customers[member.person_id] = member

    def login_user(self, branch: BoardGameCafeBranch, username, password):
        for member in branch.members.values():
            if member.username == username:
                if member.verify_password(password):
                    member.record_login()
                    return member
        return None

    # ------------------
    # RESERVATION
    # ------------------

    def create_reservation(self, branch: BoardGameCafeBranch, reservation):
        for r in branch.reservations.values():
            if r.table.table_id == reservation.table.table_id:
                if reservation.start_datetime < r.end_datetime and \
                   reservation.end_datetime > r.start_datetime:
                    raise ValueError("Reservation conflict")

        branch.reservations[reservation.reservation_id] = reservation

    def confirm_reservation(self, branch: BoardGameCafeBranch, reservation_id):
        res = branch.reservations.get(reservation_id)
        if res:
            res.confirm_booking()

    def cancel_reservation(self, branch: BoardGameCafeBranch, reservation_id):
        res = branch.reservations.get(reservation_id)
        if res:
            res.cancel_booking("Cancelled by system")

    # ------------------
    # ORDER
    # ------------------

    def create_order(self, branch: BoardGameCafeBranch, customer, table=None):
        from BGC_menu import Order
        order_id = f"ORD-{len(branch.orders)+1:04d}"
        order = Order(order_id, customer, table)
        branch.orders[order_id] = order
        return order

    def place_order(self, branch: BoardGameCafeBranch, order):
        branch.orders[order.order_id] = order

    # ------------------
    # PAYMENT
    # ------------------

    def process_payment(self, branch: BoardGameCafeBranch, payment):
        branch.payments[payment.payment_id] = payment
        payment.complete_payment()

    # ------------------
    # INVENTORY
    # ------------------

    def add_board_game(self, branch: BoardGameCafeBranch, board_game):
        branch.board_games.append(board_game)

    def add_play_table(self, branch: BoardGameCafeBranch, table):
        branch.play_tables.append(table)

    # ------------------
    # REPORT
    # ------------------

    def get_branch_report(self, branch: BoardGameCafeBranch):
        revenue = 0
        for p in branch.payments.values():
            if p.status.value == "Completed":
                revenue += p.total_amount

        return {
            "branch": branch.name,
            "revenue": revenue,
            "orders": len(branch.orders),
            "reservations": len(branch.reservations)
        }

    def get_corporate_report(self):
        return [self.get_branch_report(b) for b in self.branches.values()]