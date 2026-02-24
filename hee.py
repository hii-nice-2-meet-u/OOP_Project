import datetime
from abc import ABC, abstractmethod
class Person(ABC):
    def __init__(self, name, user_id):
        self.__name = name
        self.__user_id = user_id
    @property
    def name(self):
        return self.__name
    @property
    def user_id(self):
        return self.__user_id
class Customer(Person):
    def __init__(self, name, user_id):
        super().__init__(name, user_id)
        self.__total_spent = 0
        self.__birth_date = None
        self.__member_tier = "Bronze"
        self.__is_student = False
    @property
    def total_spent(self):
        return self.__total_spent
    @total_spent.setter
    def total_spent(self, amount):
        self.__total_spent += amount
        self.__update_member_tier()
    @property
    def birth_date(self):
        return self.__birth_date
    @birth_date.setter
    def birth_date(self, date):
        self.__birth_date = date
    @property
    def member_tier(self):
        return self.__member_tier   
    def __update_member_tier(self): #แก้เลขด้วย
        if self.__total_spent >= 1000:
            self.__member_tier = "Gold"
        elif self.__total_spent >= 500:
            self.__member_tier = "Silver"
        elif self.__total_spent > 69:
            self.__member_tier = "Bronze"
        else:
            self.__member_tier = "None"
    def get_discount(self):
        if self.__member_tier == "Gold":
            return 0.20
        if self.__is_student:
            return 0.15
        elif self.__member_tier == "Silver":
            return 0.10
        elif self.__member_tier == "Bronze":
            return 0.05
        else:
            return 0.0
    @property
    def is_student(self):
        return self.__is_student
    @is_student.setter
    def is_student(self, value):
        self.__is_student = value
        
        
class NonCustomer(Person):
    def __init__(self, name, user_id):
        super().__init__(name, user_id)
        self.__salary = 0
    @property
    def salary(self):
        return self.__salary
    @salary.setter
    def salary(self, amount):   
        self.__salary = amount
class Manager(NonCustomer):
    def __init__(self, name, user_id):
        super().__init__(name, user_id)
        self.__managed_branches = []
    @property
    def managed_branches(self):
        return self.__managed_branches
    
    
class Owner(NonCustomer):
    def __init__(self, name, user_id):
        super().__init__(name, user_id)
        self.__owned_branches = []
    @property
    def owned_branches(self):
        return self.__owned_branches
    
class Staff(NonCustomer):
    def __init__(self, name, user_id):
        super().__init__(name, user_id)
        self.__assigned_branch = None

    @property
    def assigned_branch(self):
        return self.__assigned_branch
    @assigned_branch.setter
    def assigned_branch(self, branch):
        self.__assigned_branch = branch
        
class Reservation:
    def __init__(self, customer, table, start_time, end_time, branch_id):
        self.reservation_id = None
        self.__customer = customer
        self.__table = table
        self.__start_time = start_time
        self.__end_time = end_time
        self.__branch_id = branch_id
        self.__status = None
    @property
    def customer(self):
        return self.__customer
    @property
    def table(self):
        return self.__table
    @property
    def start_time(self):
        return self.__start_time
    @property
    def end_time(self):
        return self.__end_time  
    @property
    def branch_id(self):    
        return self.__branch_id
    @property
    def status(self):
        return self.__status
    @status.setter
    def status(self, value):
        if value in [ReservationStatus.PENDING, ReservationStatus.CONFIRMED, ReservationStatus.CANCELLED, ReservationStatus.NO_SHOW]:
            self.__status = value
        else:
            raise ValueError("Invalid reservation status")
class Payment:
    def __init__(self, amount, payment_method):
        self.__payment_id = None
        self.__amount = amount
        self.__payment_method = payment_method
        self.__payment_time = None
    @property
    def payment_id(self):
        return self.__payment_id
    @payment_id.setter
    def payment_id(self, value):
        self.__payment_id = value
    @property
    def amount(self):
        return self.__amount
    @property
    def payment_method(self):
        return self.__payment_method
    @property
    def payment_time(self):
        return self.__payment_time
    @payment_time.setter
    def process_payment(self):
        self.__payment_time = datetime.datetime.now()
class PaymentMethod(ABC):
    def __init__(self, method_id):
        self.__method_id = method_id
    @property
    def method_id(self):
        return self.__method_id
    def validate_method(self):
        pass
class CreditCard(PaymentMethod):
    def __init__(self, method_id, card_number, expiry_date, cvv):
        super().__init__(method_id)
        self.__card_number = card_number
        self.__expiry_date = expiry_date
        self.__cvv = cvv
    @property
    def card_number(self):
        return self.__card_number
    @property
    def expiry_date(self):
        return self.__expiry_date
    @property
    def cvv(self):
        return self.__cvv
    def validate_method(self):
        return True
    
class Cash(PaymentMethod):
    def __init__(self, method_id):
        super().__init__(method_id)
    def validate_method(self):
        return True
class OnlinePayment(PaymentMethod):
    def __init__(self, method_id, account_email):
        super().__init__(method_id)
        self.__account_email = account_email
    @property
    def account_email(self):
        return self.__account_email
    def validate_method(self):
        return True