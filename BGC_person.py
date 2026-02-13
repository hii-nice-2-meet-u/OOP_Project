"""
Board Game Cafe - System Module (Refactored)
Two-tier architecture: System (Corporate) -> Branch (Operations)
"""

from datetime import datetime, timedelta
from typing import List, Optional, Dict
import logging


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)


# ==========================================
# BRANCH-LEVEL MANAGERS (inside Branch)
# ==========================================

class AuthenticationManager:
    """Manages user authentication within a branch."""
    
    def __init__(self, branch_name: str):
        self._branch_name = branch_name
        self._authenticated_users: Dict[str, dict] = {}
        self._logger = logging.getLogger(f'{branch_name}.AuthenticationManager')

    def login_user(self, username: str, password: str, user_repository) -> Optional[object]:
        """Authenticate a user with username and password."""
        try:
            user = user_repository.find_by_username(username)
            
            if user and hasattr(user, 'verify_password'):
                if user.verify_password(password):
                    user.record_login()
                    
                    session_id = f"SESSION-{username}-{int(datetime.now().timestamp())}"
                    self._authenticated_users[session_id] = {
                        'user': user,
                        'login_time': datetime.now(),
                        'username': username
                    }
                    
                    self._logger.info(f"User {username} logged in successfully")
                    return user
            
            self._logger.warning(f"Failed login attempt for username: {username}")
            return None
            
        except Exception as e:
            self._logger.error(f"Login error: {e}")
            return None

    def logout_user(self, session_id: str) -> bool:
        """Logout a user by session ID."""
        if session_id in self._authenticated_users:
            username = self._authenticated_users[session_id]['username']
            del self._authenticated_users[session_id]
            self._logger.info(f"User {username} logged out")
            return True
        return False


class MembershipManager:
    """Manages customers and members within a branch."""
    
    def __init__(self, branch_name: str):
        self._branch_name = branch_name
        self._customers: Dict[str, object] = {}
        self._members: Dict[str, object] = {}
        self._logger = logging.getLogger(f'{branch_name}.MembershipManager')

    def register_customer(self, customer) -> bool:
        """Register a new customer."""
        try:
            if customer.person_id in self._customers:
                raise ValueError(f"Customer {customer.person_id} already exists")
            
            self._customers[customer.person_id] = customer
            self._logger.info(f"Registered customer: {customer.name}")
            return True
            
        except Exception as e:
            self._logger.error(f"Customer registration failed: {e}")
            raise

    def register_member(self, member) -> bool:
        """Register a new member with membership benefits."""
        try:
            if member.member_id in self._members:
                raise ValueError(f"Member {member.member_id} already exists")
            
            self._members[member.member_id] = member
            self._customers[member.person_id] = member
            self._logger.info(f"Registered member: {member.name} (Tier: {member.tier.value})")
            return True
            
        except Exception as e:
            self._logger.error(f"Member registration failed: {e}")
            raise

    def get_customer(self, customer_id: str) -> Optional[object]:
        """Retrieve a customer by ID."""
        return self._customers.get(customer_id)

    def get_member(self, member_id: str) -> Optional[object]:
        """Retrieve a member by member ID."""
        return self._members.get(member_id)

    def find_by_username(self, username: str) -> Optional[object]:
        """Find a member by username."""
        for member in self._members.values():
            if hasattr(member, 'username') and member.username == username:
                return member
        return None

    def deactivate_member(self, member_id: str, reason: str) -> bool:
        """Deactivate a member account."""
        member = self._members.get(member_id)
        if member:
            member.deactivate()
            self._logger.info(f"Deactivated member {member_id}: {reason}")
            return True
        return False


class ReservationManager:
    """Manages table reservations within a branch."""
    
    def __init__(self, branch_name: str):
        self._branch_name = branch_name
        self._reservations: Dict[str, object] = {}
        self._logger = logging.getLogger(f'{branch_name}.ReservationManager')

    def create_reservation(self, reservation) -> bool:
        """Create a new reservation with conflict checking."""
        try:
            if self._has_conflict(reservation):
                raise ValueError("Reservation conflicts with existing booking")
            
            if hasattr(reservation.customer, 'get_max_active_bookings'):
                active_count = self._count_active_reservations(reservation.customer)
                max_allowed = reservation.customer.get_max_active_bookings()
                
                if active_count >= max_allowed:
                    raise ValueError(f"Customer has reached maximum active bookings ({max_allowed})")
            
            self._reservations[reservation.reservation_id] = reservation
            self._logger.info(f"Created reservation {reservation.reservation_id}")
            return True
            
        except Exception as e:
            self._logger.error(f"Reservation creation failed: {e}")
            raise

    def _has_conflict(self, new_reservation) -> bool:
        """Check if reservation conflicts with existing ones."""
        for existing in self._reservations.values():
            if existing.status.value in ['Cancelled', 'Completed', 'No Show']:
                continue
            
            if existing.table.table_id != new_reservation.table.table_id:
                continue
            
            if (new_reservation.start_datetime < existing.end_datetime and
                new_reservation.end_datetime > existing.start_datetime):
                return True
        
        return False

    def _count_active_reservations(self, customer) -> int:
        """Count active reservations for a customer."""
        count = 0
        for reservation in self._reservations.values():
            if (reservation.customer.person_id == customer.person_id and
                reservation.status.value in ['Pending', 'Confirmed', 'Checked In']):
                count += 1
        return count

    def confirm_reservation(self, reservation_id: str) -> bool:
        """Confirm a pending reservation."""
        reservation = self._reservations.get(reservation_id)
        if reservation:
            try:
                reservation.confirm_booking()
                self._logger.info(f"Confirmed reservation {reservation_id}")
                return True
            except ValueError as e:
                self._logger.error(f"Failed to confirm reservation: {e}")
                raise
        return False

    def cancel_reservation(self, reservation_id: str, reason: str = "") -> bool:
        """Cancel a reservation."""
        reservation = self._reservations.get(reservation_id)
        if reservation:
            try:
                reservation.cancel_booking(reason)
                self._logger.info(f"Cancelled reservation {reservation_id}: {reason}")
                return True
            except ValueError as e:
                self._logger.error(f"Failed to cancel reservation: {e}")
                raise
        return False

    def get_reservation(self, reservation_id: str) -> Optional[object]:
        """Retrieve a reservation by ID."""
        return self._reservations.get(reservation_id)

    def get_reservations_for_date(self, date: datetime) -> List[object]:
        """Get all reservations for a specific date."""
        date_str = date.strftime("%Y-%m-%d")
        return [
            res for res in self._reservations.values()
            if res.get_date() == date_str
        ]

    def get_reservation_schedule(self, date: datetime) -> List[object]:
        """Get reservation schedule for a specific date."""
        return self.get_reservations_for_date(date)


class OrderManager:
    """Manages orders within a branch."""
    
    def __init__(self, branch_name: str):
        self._branch_name = branch_name
        self._orders: Dict[str, object] = {}
        self._order_counter = 0
        self._logger = logging.getLogger(f'{branch_name}.OrderManager')

    def create_order(self, customer, table=None) -> object:
        """Create a new order."""
        from BGC_menu import Order
        
        self._order_counter += 1
        order_id = f"ORD-{datetime.now().strftime('%Y%m%d')}-{self._order_counter:04d}"
        
        order = Order(order_id, customer, table)
        self._orders[order_id] = order
        
        self._logger.info(f"Created order {order_id}")
        return order

    def place_order(self, order) -> bool:
        """Place an order (make it active)."""
        try:
            if order.order_id not in self._orders:
                self._orders[order.order_id] = order
            
            self._logger.info(f"Placed order {order.order_id}")
            return True
            
        except Exception as e:
            self._logger.error(f"Failed to place order: {e}")
            raise

    def get_order(self, order_id: str) -> Optional[object]:
        """Retrieve an order by ID."""
        return self._orders.get(order_id)

    def get_active_orders(self) -> List[object]:
        """Get all active orders."""
        return [order for order in self._orders.values() if order.status == "Open"]


class PaymentManager:
    """Manages payment processing within a branch."""
    
    def __init__(self, branch_name: str):
        self._branch_name = branch_name
        self._payments: Dict[str, object] = {}
        self._payment_counter = 0
        self._logger = logging.getLogger(f'{branch_name}.PaymentManager')

    def process_payment(self, order, payment_method: str, **kwargs) -> object:
        """Process a payment for an order."""
        from BGC_operation import Cash, Card, OnlinePayment
        
        try:
            self._payment_counter += 1
            payment_id = f"PAY-{datetime.now().strftime('%Y%m%d')}-{self._payment_counter:04d}"
            
            if payment_method.lower() == "cash":
                payment = Cash(payment_id, order, kwargs.get('amount_received'))
            elif payment_method.lower() == "card":
                payment = Card(payment_id, order, 
                             kwargs.get('last_four_digits'),
                             kwargs.get('bank_name'))
            elif payment_method.lower() == "online":
                payment = OnlinePayment(payment_id, order,
                                      kwargs.get('transaction_ref'),
                                      kwargs.get('platform'))
            else:
                raise ValueError(f"Unknown payment method: {payment_method}")
            
            payment.complete_payment()
            self._payments[payment_id] = payment
            
            self._logger.info(f"Processed payment {payment_id} for order {order.order_id}")
            return payment
            
        except Exception as e:
            self._logger.error(f"Payment processing failed: {e}")
            raise

    def get_payment(self, payment_id: str) -> Optional[object]:
        """Retrieve a payment by ID."""
        return self._payments.get(payment_id)

    def get_daily_revenue(self, date: Optional[datetime] = None) -> float:
        """Calculate total revenue for a specific date."""
        target_date = (date or datetime.now()).date()
        total = 0.0
        
        for payment in self._payments.values():
            if payment.timestamp.date() == target_date and payment.status.value == "Completed":
                total += payment.total_amount
        
        return total


class StaffManager:
    """Manages staff and managers within a branch."""
    
    def __init__(self, branch_name: str):
        self._branch_name = branch_name
        self._staff: Dict[str, object] = {}
        self._managers: Dict[str, object] = {}
        self._logger = logging.getLogger(f'{branch_name}.StaffManager')

    def register_staff(self, staff) -> bool:
        """Register a new staff member."""
        try:
            if staff.staff_id in self._staff:
                raise ValueError(f"Staff {staff.staff_id} already exists")
            
            self._staff[staff.staff_id] = staff
            self._logger.info(f"Registered staff: {staff.name}")
            return True
            
        except Exception as e:
            self._logger.error(f"Staff registration failed: {e}")
            raise

    def register_manager(self, manager) -> bool:
        """Register a new manager."""
        try:
            if manager.person_id in self._managers:
                raise ValueError(f"Manager {manager.person_id} already exists")
            
            self._managers[manager.person_id] = manager
            self._logger.info(f"Registered manager: {manager.name}")
            return True
            
        except Exception as e:
            self._logger.error(f"Manager registration failed: {e}")
            raise

    def deactivate_staff(self, staff_id: str, reason: str) -> bool:
        """Deactivate a staff member."""
        staff = self._staff.get(staff_id)
        if staff:
            staff.deactivate()
            self._logger.info(f"Deactivated staff {staff_id}: {reason}")
            return True
        return False

    def get_staff(self, staff_id: str) -> Optional[object]:
        """Retrieve a staff member by ID."""
        return self._staff.get(staff_id)


class ReportingManager:
    """Generates reports and analytics for a branch."""
    
    def __init__(self, branch_name: str, order_manager, payment_manager, reservation_manager):
        self._branch_name = branch_name
        self._order_manager = order_manager
        self._payment_manager = payment_manager
        self._reservation_manager = reservation_manager
        self._logger = logging.getLogger(f'{branch_name}.ReportingManager')

    def get_sales_report(self, date: Optional[datetime] = None) -> Dict:
        """Generate sales report for a specific date."""
        target_date = date or datetime.now()
        daily_revenue = self._payment_manager.get_daily_revenue(target_date)
        
        orders = [
            order for order in self._order_manager.get_active_orders()
            if order.created_at.date() == target_date.date()
        ]
        
        return {
            'branch': self._branch_name,
            'date': target_date.strftime('%Y-%m-%d'),
            'total_revenue': daily_revenue,
            'order_count': len(orders),
            'average_order_value': daily_revenue / len(orders) if orders else 0
        }


# ==========================================
# BRANCH CLASS
# ==========================================

class BoardGameCafeBranch:
    """
    Represents a physical branch location.
    Contains all operational managers and resources for the branch.
    """
    
    def __init__(self, cafe_id: str, name: str, location: str):
        if not cafe_id or not name or not location:
            raise ValueError("Cafe ID, name, and location cannot be empty")
        
        self._cafe_id = cafe_id
        self._name = name
        self._location = location
        self._board_games: List[object] = []
        self._play_tables: List[object] = []
        self._inventory = None  # MenuList
        
        # Initialize all branch-level managers
        self._auth_manager = AuthenticationManager(name)
        self._membership_manager = MembershipManager(name)
        self._reservation_manager = ReservationManager(name)
        self._order_manager = OrderManager(name)
        self._payment_manager = PaymentManager(name)
        self._staff_manager = StaffManager(name)
        self._reporting_manager = ReportingManager(
            name, 
            self._order_manager,
            self._payment_manager,
            self._reservation_manager
        )
        
        self._logger = logging.getLogger(f'Branch.{name}')
        self._logger.info(f"Initialized branch: {name}")

    # ==========================================
    # PROPERTIES
    # ==========================================

    @property
    def cafe_id(self) -> str:
        """Unique branch identifier."""
        return self._cafe_id

    @property
    def name(self) -> str:
        """Branch name."""
        return self._name

    @property
    def location(self) -> str:
        """Branch address/location."""
        return self._location

    @property
    def board_games(self) -> List[object]:
        """Board games available at this branch."""
        return self._board_games.copy()

    @property
    def play_tables(self) -> List[object]:
        """Play tables available at this branch."""
        return self._play_tables.copy()

    # ==========================================
    # INVENTORY MANAGEMENT
    # ==========================================

    def add_board_game(self, board_game) -> None:
        """Add a board game to branch inventory."""
        self._board_games.append(board_game)
        self._logger.info(f"Added board game: {board_game.name}")

    def remove_board_game(self, board_game) -> None:
        """Remove a board game from branch inventory."""
        if board_game in self._board_games:
            self._board_games.remove(board_game)
            self._logger.info(f"Removed board game: {board_game.name}")

    def add_play_table(self, play_table) -> None:
        """Add a play table to the branch."""
        self._play_tables.append(play_table)
        self._logger.info(f"Added table: {play_table.table_name}")

    def remove_play_table(self, play_table) -> None:
        """Remove a play table from the branch."""
        if play_table in self._play_tables:
            self._play_tables.remove(play_table)
            self._logger.info(f"Removed table: {play_table.table_name}")

    def get_available_tables(self) -> List[object]:
        """Get all currently available tables."""
        return [table for table in self._play_tables if table.is_available]

    def get_available_games(self) -> List[object]:
        """Get all currently available games."""
        return [game for game in self._board_games if game.is_available]

    # ==========================================
    # MENU MANAGEMENT
    # ==========================================

    def view_menu(self) -> object:
        """Get the branch menu."""
        return self._inventory

    def get_menu(self) -> object:
        """Get the branch menu (alias for view_menu)."""
        return self._inventory

    # ==========================================
    # MEMBER MANAGEMENT
    # ==========================================

    def register_new_member(self, member) -> bool:
        """Register a new member at this branch."""
        return self._membership_manager.register_member(member)

    def login_user(self, username: str, password: str) -> Optional[object]:
        """Authenticate a user at this branch."""
        return self._auth_manager.login_user(username, password, self._membership_manager)

    # ==========================================
    # RESERVATION MANAGEMENT
    # ==========================================

    def check_availability(self, table_id: str, date: datetime) -> bool:
        """Check if a table is available on a specific date."""
        reservations = self._reservation_manager.get_reservations_for_date(date)
        for res in reservations:
            if res.table.table_id == table_id and res.status.value in ['Confirmed', 'Checked In']:
                return False
        return True

    def create_reservation(self, reservation) -> bool:
        """Create a reservation at this branch."""
        return self._reservation_manager.create_reservation(reservation)

    def confirm_reservation(self, reservation_id: str) -> bool:
        """Confirm a reservation."""
        return self._reservation_manager.confirm_reservation(reservation_id)

    def cancel_reservation(self, reservation_id: str) -> bool:
        """Cancel a reservation."""
        return self._reservation_manager.cancel_reservation(reservation_id)

    def check_in_play_table(self, table_id: str) -> Optional[object]:
        """Check in a customer to a play table."""
        for table in self._play_tables:
            if table.table_id == table_id and table.is_available:
                return table
        return None

    def check_out_play_table(self, table_id: str) -> Optional[object]:
        """Check out a customer from a play table."""
        for table in self._play_tables:
            if table.table_id == table_id and not table.is_available:
                table.clear_table()
                return table
        return None

    def get_reservation_schedule(self, date: datetime) -> List[object]:
        """Get reservation schedule for a specific date."""
        return self._reservation_manager.get_reservation_schedule(date)

    # ==========================================
    # ORDER MANAGEMENT
    # ==========================================

    def place_order(self, order) -> bool:
        """Place an order at this branch."""
        return self._order_manager.place_order(order)

    # ==========================================
    # PAYMENT MANAGEMENT
    # ==========================================

    def process_payment(self, payment) -> bool:
        """Process a payment at this branch."""
        try:
            # Payment is already created, just record it
            return True
        except Exception as e:
            self._logger.error(f"Payment processing failed: {e}")
            return False

    # ==========================================
    # REPORTING
    # ==========================================

    def get_sales_report(self, date: Optional[datetime] = None) -> Dict:
        """Get sales report for this branch."""
        return self._reporting_manager.get_sales_report(date)


# ==========================================
# SYSTEM CLASS (Corporate Level)
# ==========================================

class BoardGameCafeSystem:
    """
    Corporate-level system managing multiple branches.
    Coordinates high-level operations across the organization.
    """
    
    def __init__(self, version: str = "2.0"):
        self._version = version
        self._orders: List[object] = []
        self._reservations: List[object] = []
        self._branches: List[BoardGameCafeBranch] = []
        self._logger = logging.getLogger('BoardGameCafeSystem')
        self._logger.info(f"Initialized BoardGameCafeSystem v{self._version}")

    @property
    def version(self) -> str:
        """System version."""
        return self._version

    @property
    def orders(self) -> List[object]:
        """All orders across all branches."""
        return self._orders.copy()

    @property
    def reservations(self) -> List[object]:
        """All reservations across all branches."""
        return self._reservations.copy()

    @property
    def branches(self) -> List[BoardGameCafeBranch]:
        """All branches in the system."""
        return self._branches.copy()

    # ==========================================
    # BRANCH MANAGEMENT
    # ==========================================

    def add_branch(self, branch: BoardGameCafeBranch) -> None:
        """Add a new branch to the system."""
        self._branches.append(branch)
        self._logger.info(f"Added branch: {branch.name}")

    def remove_branch(self, cafe_id: str = None, name: str = None) -> bool:
        """Remove a branch from the system."""
        for branch in self._branches:
            if (cafe_id and branch.cafe_id == cafe_id) or (name and branch.name == name):
                self._branches.remove(branch)
                self._logger.info(f"Removed branch: {branch.name}")
                return True
        return False

    def get_branch(self, cafe_id: str) -> Optional[BoardGameCafeBranch]:
        """Get a branch by ID."""
        for branch in self._branches:
            if branch.cafe_id == cafe_id:
                return branch
        return None

    # ==========================================
    # CORPORATE-LEVEL OPERATIONS
    # ==========================================

    def register_new_member(self, member, branch: BoardGameCafeBranch) -> bool:
        """Register a member at a specific branch."""
        return branch.register_new_member(member)

    def login_user(self, username: str, password: str, branch: BoardGameCafeBranch) -> Optional[object]:
        """Login user at a specific branch."""
        return branch.login_user(username, password)

    def check_in_play_table(self, table_id: str, branch: BoardGameCafeBranch) -> Optional[object]:
        """Check in to a play table at a specific branch."""
        return branch.check_in_play_table(table_id)

    def check_out_play_table(self, table_id: str, branch: BoardGameCafeBranch) -> Optional[object]:
        """Check out from a play table at a specific branch."""
        return branch.check_out_play_table(table_id)

    def create_reservation(self, reservation, branch: BoardGameCafeBranch) -> bool:
        """Create a reservation at a specific branch."""
        success = branch.create_reservation(reservation)
        if success:
            self._reservations.append(reservation)
        return success

    def check_availability(self, table_id: str, reservation_time: datetime, 
                          branch: BoardGameCafeBranch) -> bool:
        """Check table availability at a specific branch."""
        return branch.check_availability(table_id, reservation_time)

    def confirm_reservation(self, reservation_id: str, branch: BoardGameCafeBranch) -> bool:
        """Confirm a reservation at a specific branch."""
        return branch.confirm_reservation(reservation_id)

    def cancel_reservation(self, reservation_id: str, branch: BoardGameCafeBranch) -> bool:
        """Cancel a reservation at a specific branch."""
        return branch.cancel_reservation(reservation_id)

    def view_menu(self, branch: BoardGameCafeBranch) -> object:
        """View menu of a specific branch."""
        return branch.view_menu()

    def place_order(self, order, branch: BoardGameCafeBranch) -> bool:
        """Place an order at a specific branch."""
        success = branch.place_order(order)
        if success:
            self._orders.append(order)
        return success

    def process_payment(self, payment, branch: BoardGameCafeBranch) -> bool:
        """Process payment at a specific branch."""
        return branch.process_payment(payment)

    # ==========================================
    # CORPORATE REPORTING
    # ==========================================

    def get_reservation_report(self) -> List[object]:
        """Get all reservations across all branches."""
        return self._reservations.copy()

    def get_sales_report(self, date: Optional[datetime] = None) -> Dict:
        """Get consolidated sales report across all branches."""
        total_revenue = 0.0
        total_orders = 0
        branch_reports = []
        
        for branch in self._branches:
            report = branch.get_sales_report(date)
            total_revenue += report['total_revenue']
            total_orders += report['order_count']
            branch_reports.append(report)
        
        return {
            'date': (date or datetime.now()).strftime('%Y-%m-%d'),
            'total_revenue': total_revenue,
            'total_orders': total_orders,
            'branch_count': len(self._branches),
            'average_revenue_per_branch': total_revenue / len(self._branches) if self._branches else 0,
            'branch_reports': branch_reports
        }

    def add_board_game_to_inventory(self, branch: BoardGameCafeBranch, board_game) -> None:
        """Add a board game to a branch's inventory."""
        branch.add_board_game(board_game)

    def remove_board_game_from_inventory(self, branch: BoardGameCafeBranch, board_game) -> None:
        """Remove a board game from a branch's inventory."""
        branch.remove_board_game(board_game)

    def add_play_table_to_branch(self, branch: BoardGameCafeBranch, play_table) -> None:
        """Add a play table to a branch."""
        branch.add_play_table(play_table)

    def remove_play_table_from_branch(self, branch: BoardGameCafeBranch, play_table) -> None:
        """Remove a play table from a branch."""
        branch.remove_play_table(play_table)