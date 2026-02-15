"""
Board Game Cafe - System Module
Main system and branch management
"""

from datetime import datetime
from typing import List, Optional


# ==========================================
# BRANCH (DATA HOLDER)
# ==========================================

class BoardGameCafeBranch:
    def __init__(self, cafe_id: str, name: str, location: str):
        self.cafe_id = cafe_id
        self.name = name
        self.location = location

        # Data containers (using Lists)
        self.customers: List[object] = []
        self.members: List[object] = []
        self.staff: List[object] = []

        self.orders: List[object] = []
        self.reservations: List[object] = []
        self.payments: List[object] = []

        self.board_games: List[object] = []
        self.play_tables: List[object] = []
        self.menu = None


# ==========================================
# SYSTEM (ALL LOGIC)
# ==========================================

class BoardGameCafeSystem:
    def __init__(self, version="3.0"):
        self.version = version
        self.branches: List[BoardGameCafeBranch] = []

    # ------------------
    # BRANCH MANAGEMENT
    # ------------------

class BoardGameCafe:
    def __init__(self):
        self.__cafe_name = None
        self.__cafe_id = None
        self.__cafe_status = None
        self.__location = None
        self.__lobbies = []
        self.__board_games = []
        # self.__menu_list = BGC_menu.MenuList()
        # self.__order_system = BGC_log.OrderSystem()
        # self.__reservation_manager = BGC_log.ReservationManager()
        self.__managers = []
        self.__staffs = []
        self.__transactions = []
        self.__audit_logs = []

    def get_branch(self, cafe_id: str) -> Optional[BoardGameCafeBranch]:
        for branch in self.branches:
            if branch.cafe_id == cafe_id:
                return branch
        return None

    def remove_branch(self, cafe_id: str) -> bool:
        for branch in self.branches:
            if branch.cafe_id == cafe_id:
                self.branches.remove(branch)
                return True
        return False

    # ------------------
    # MEMBER / AUTH
    # ------------------

    def register_member(self, branch: BoardGameCafeBranch, member) -> None:
        for existing_member in branch.members:
            if existing_member.member_id == member.member_id:
                raise ValueError("Member already exists")

        branch.members.append(member)
        branch.customers.append(member)

    def login_user(self, branch: BoardGameCafeBranch, username: str, password: str):
        for member in branch.members:
            if member.username == username:
                if member.verify_password(password):
                    member.record_login()
                    return member
        
        for staff in branch.staff:
            if staff.username == username:
                if staff.verify_password(password):
                    staff.record_login()
                    return staff
        
        return None

    # ------------------
    # CUSTOMER MANAGEMENT
    # ------------------

    def add_customer(self, branch: BoardGameCafeBranch, customer) -> None:
        branch.customers.append(customer)

    def get_customer(self, branch: BoardGameCafeBranch, person_id: str):
        for customer in branch.customers:
            if customer.person_id == person_id:
                return customer
        return None

    # ------------------
    # RESERVATION
    # ------------------

    def create_reservation(self, branch: BoardGameCafeBranch, reservation) -> None:
        for r in branch.reservations:
            if r.table.table_id == reservation.table.table_id:
                if reservation.start_datetime < r.end_datetime and \
                   reservation.end_datetime > r.start_datetime:
                    raise ValueError("Reservation conflict - table already booked")

        branch.reservations.append(reservation)

    def confirm_reservation(self, branch: BoardGameCafeBranch, reservation_id: str) -> bool:
        for res in branch.reservations:
            if res.reservation_id == reservation_id:
                res.confirm_booking()
                return True
        return False

    def cancel_reservation(self, branch: BoardGameCafeBranch, reservation_id: str, 
                          reason: str = "") -> bool:
        for res in branch.reservations:
            if res.reservation_id == reservation_id:
                res.cancel_booking(reason)
                return True
        return False

    def get_reservation(self, branch: BoardGameCafeBranch, reservation_id: str):
        for res in branch.reservations:
            if res.reservation_id == reservation_id:
                return res
        return None

    # ------------------
    # ORDER MANAGEMENT
    # ------------------

    def create_order(self, branch: BoardGameCafeBranch, customer, table=None):
        from BGC_menu import Order
        order_id = f"ORD-{len(branch.orders)+1:04d}"
        order = Order(order_id, customer, table)
        branch.orders.append(order)
        return order

    def place_order(self, branch: BoardGameCafeBranch, order) -> None:
        for existing_order in branch.orders:
            if existing_order.order_id == order.order_id:
                return
        
        branch.orders.append(order)

    def get_order(self, branch: BoardGameCafeBranch, order_id: str):
        for order in branch.orders:
            if order.order_id == order_id:
                return order
        return None

    # ------------------
    # PAYMENT
    # ------------------

    def process_payment(self, branch: BoardGameCafeBranch, payment) -> None:
        branch.payments.append(payment)
        payment.complete_payment()

    def get_payment(self, branch: BoardGameCafeBranch, payment_id: str):
        for payment in branch.payments:
            if payment.payment_id == payment_id:
                return payment
        return None

    # ------------------
    # INVENTORY - GAMES
    # ------------------

    def add_board_game(self, branch: BoardGameCafeBranch, board_game) -> None:
        branch.board_games.append(board_game)

    def get_board_game(self, branch: BoardGameCafeBranch, game_id: str):
        for game in branch.board_games:
            if game.game_id == game_id:
                return game
        return None

    def get_available_games(self, branch: BoardGameCafeBranch) -> List:
        return [game for game in branch.board_games if game.is_available]

    # ------------------
    # INVENTORY - TABLES
    # ------------------

    def add_play_table(self, branch: BoardGameCafeBranch, table) -> None:
        branch.play_tables.append(table)

    def get_play_table(self, branch: BoardGameCafeBranch, table_id: str):
        for table in branch.play_tables:
            if table.table_id == table_id:
                return table
        return None

    def get_available_tables(self, branch: BoardGameCafeBranch) -> List:
        return [table for table in branch.play_tables if table.is_available]

    # ------------------
    # MENU
    # ------------------

    def set_menu(self, branch: BoardGameCafeBranch, menu) -> None:
        branch.menu = menu

    def get_menu(self, branch: BoardGameCafeBranch):
        return branch.menu

    # ------------------
    # REPORTS
    # ------------------

    def get_branch_report(self, branch: BoardGameCafeBranch) -> dict:   
        revenue = 0
        for p in branch.payments:
            if p.status.value == "Completed":
                revenue += p.total_amount

        return {
            "branch": branch.name,
            "location": branch.location,
            "revenue": revenue,
            "total_orders": len(branch.orders),
            "total_reservations": len(branch.reservations),
            "total_customers": len(branch.customers),
            "total_members": len(branch.members),
            "total_games": len(branch.board_games),
            "total_tables": len(branch.play_tables),
            "available_tables": len(self.get_available_tables(branch)),
            "available_games": len(self.get_available_games(branch))
        }

    def get_corporate_report(self) -> List[dict]:
        return [self.get_branch_report(b) for b in self.branches]

    def get_total_revenue(self) -> float:
        total = 0
        for branch in self.branches:
            for payment in branch.payments:
                if payment.status.value == "Completed":
                    total += payment.total_amount
        return total

    # ------------------
    # STAFF MANAGEMENT
    # ------------------

    def add_staff(self, branch: BoardGameCafeBranch, staff) -> None:
        branch.staff.append(staff)

    def get_staff(self, branch: BoardGameCafeBranch, staff_id: str):
        for staff in branch.staff:
            if staff.staff_id == staff_id:
                return staff
        return None