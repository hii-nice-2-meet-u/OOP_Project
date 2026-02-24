import ENUM_STATUS


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
        if value in [
            ReservationStatus.PENDING,
            ReservationStatus.CONFIRMED,
            ReservationStatus.CANCELLED,
            ReservationStatus.NO_SHOW,
        ]:
            self.__status = value
        else:
            raise ValueError("Invalid reservation status")
