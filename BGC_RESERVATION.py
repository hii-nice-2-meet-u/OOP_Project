import ENUM_STATUS


class Reservation:
    def __init__(self, customer_id, table_id, start_time, end_time, branch_id):
        self.reservation_id = None
        self.__customer_id = customer_id
        self.__table_id = table_id
        self.__start_time = start_time
        self.__end_time = end_time
        self.__branch_id = branch_id
        self.__status = None

    @property
    def customer_id(self):
        return self.__customer_id

    @customer_id.setter
    def table_id(self):
        return self.__table_id

    @property
    def start_time(self):
        return self.__start_time

    @start_time.setter
    def start_time(self, value):
        self.__start_time = value

    @property
    def end_time(self):
        return self.__end_time

    @end_time.setter
    def end_time(self, value):
        self.__end_time = value

    @property
    def branch_id(self):
        return self.__branch_id

    @branch_id.setter
    def branch_id(self, value):
        self.__branch_id = value

    @property
    def status(self):
        return self.__status

    @status.setter
    def status(self, value):
        if isinstance(value, ENUM_STATUS.ReservationStatus):
            self.__status = value
        else:
            raise ValueError("Invalid reservation status")
