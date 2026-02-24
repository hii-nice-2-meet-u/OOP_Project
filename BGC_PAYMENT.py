from abc import ABC, abstractmethod


class Payment:
    def __init__(self, amount, payment_method):
        self.__payment_id = None
        self.__amount = amount
        self.__payment_method = payment_method
        self.__payment_time = None

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
