from abc import ABC, abstractmethod
import datetime


# | ════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
# | #EFFF11


class Payment:
    __counter = 0

    def __init__(self, amount, payment_method):
        self.__payment_id = "PAYMENT-" + str(Payment.__counter).zfill(5)
        self.__amount = amount
        Payment.__counter += 1
        self.__payment_method = payment_method
        self.__payment_time = None

    # / ════════════════════════════════════════════════════════════════
    # - Getters
    # / ════════════════════════════════════════════════════════════════

    @property
    def payment_id(self):
        return self.__payment_id

    @property
    def amount(self):
        return self.__amount

    @property
    def payment_method(self):
        return self.__payment_method

    @property
    def payment_time(self):
        return self.__payment_time

    # / ════════════════════════════════════════════════════════════════
    # - Setters
    # / ════════════════════════════════════════════════════════════════

    @property
    def process_payment(self):
        return self.__payment_time is not None

    @process_payment.setter
    def process_payment(self, v):
        if v:
            self.__payment_time = datetime.datetime.now()

    def __str__(self):
        return (
            f"Payment ID: {self.__payment_id} | "
            f"Amount: {self.__amount:.2f} | "
            f"Method: {self.__payment_method.__class__.__name__} | "
            f"Time: {self.__payment_time}"
        )

    # / ════════════════════════════════════════════════════════════════
    # - Methods
    # / ════════════════════════════════════════════════════════════════

    # / ════════════════════════════════════════════════════════════════


# | ════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
# | #EFFF11


class PaymentMethod(ABC):

    def __init__(self, method_id):
        self.__method_id = method_id

    # / ════════════════════════════════════════════════════════════════
    # - Getters
    # / ════════════════════════════════════════════════════════════════

    @property
    def method_id(self):
        return self.__method_id

    # / ════════════════════════════════════════════════════════════════
    # - Setters
    # / ════════════════════════════════════════════════════════════════

    # / ════════════════════════════════════════════════════════════════
    # - Methods
    # / ════════════════════════════════════════════════════════════════

    @abstractmethod
    def validate_method(self):
        pass

    # / ════════════════════════════════════════════════════════════════


# | ════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
# | #EFFF11


class CreditCard(PaymentMethod):
    __counter = 0

    def __init__(self, card_number, expiry_date, cvv):
        CreditCard.__counter += 1
        method_id = "CREDIT" + str(CreditCard.__counter).zfill(5)
        super().__init__(method_id)
        self.__card_number = card_number
        self.__expiry_date = expiry_date
        self.__cvv = cvv

    # / ════════════════════════════════════════════════════════════════
    # - Getters
    # / ════════════════════════════════════════════════════════════════

    @property
    def card_number(self):
        return self.__card_number

    @property
    def expiry_date(self):
        return self.__expiry_date

    @property
    def cvv(self):
        return self.__cvv

    # / ════════════════════════════════════════════════════════════════
    # - Setters
    # / ════════════════════════════════════════════════════════════════

    # / ════════════════════════════════════════════════════════════════
    # - Methods
    # / ════════════════════════════════════════════════════════════════

    def validate_method(self):
        return True

    # / ════════════════════════════════════════════════════════════════


# | ════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
# | #EFFF11


class Cash(PaymentMethod):
    __counter = 0

    def __init__(self, paid_amount):
        Cash.__counter += 1
        method_id = "CASH" + str(Cash.__counter).zfill(5)
        super().__init__(method_id)
        self.__paid_amount = paid_amount
        self.__change = 0

    # / ════════════════════════════════════════════════════════════════
    # - Getters
    # / ════════════════════════════════════════════════════════════════
    @property
    def change(self):
        return self.__change

    # / ════════════════════════════════════════════════════════════════
    # - Setters
    # / ════════════════════════════════════════════════════════════════
    @change.setter
    def change(self, change):
        self.__change = change

    # / ════════════════════════════════════════════════════════════════
    # - Methods
    # / ════════════════════════════════════════════════════════════════

    def validate_method(self):
        return True

    # / ════════════════════════════════════════════════════════════════


# | ════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
# | #EFFF11


class OnlinePayment(PaymentMethod):
    __counter = 0

    def __init__(self, email):
        OnlinePayment.__counter += 1
        method_id = "ONLINE" + str(OnlinePayment.__counter).zfill(5)
        super().__init__(method_id)
        self.__email = email

    # / ════════════════════════════════════════════════════════════════
    # - Getters
    # / ════════════════════════════════════════════════════════════════

    @property
    def email(self):
        return self.__email

    # / ════════════════════════════════════════════════════════════════
    # - Setters
    # / ════════════════════════════════════════════════════════════════

    # / ════════════════════════════════════════════════════════════════
    # - Methods
    # / ════════════════════════════════════════════════════════════════

    def validate_method(self):
        return True

    # / ════════════════════════════════════════════════════════════════


# | ════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
