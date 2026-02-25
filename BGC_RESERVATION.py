from ENUM_STATUS import ReservationStatus


class Reservation:
    __counter = 0

    def __init__(self, customer_id, branch_id, table_id, start_time, end_time):
        self.__reservation_id = "RESV-" + str(Drink.__counter).zfill(5)
        self.__customer_id = customer_id
        self.__branch_id = branch_id
        self.__table_id = table_id
        self.__start_time = start_time
        self.__end_time = end_time
        self.__status = ReservationStatus.PENDING

    # / ================================================================
    # - Getters
    # / ================================================================

    @property
    def reservation_id(self):
        return self.__reservation_id

    @property
    def customer_id(self):
        return self.__customer_id

    @property
    def branch_id(self):
        return self.__branch_id

    @property
    def table_id(self):
        return self.__table_id

    @property
    def start_time(self):
        return self.__start_time

    @property
    def end_time(self):
        return self.__end_time

    @property
    def status(self):
        return self.__status

    # / ================================================================
    # - Setters
    # / ================================================================

    @customer_id.setter
    def customer_id(self):
        self.__customer_id = customer_id

    @branch_id.setter
    def branch_id(self, value):
        self.__branch_id = value

    @table_id.setter
    def table_id(self, value):
        self.__table_id = value

    @start_time.setter
    def start_time(self, value):
        self.__start_time = value

    @end_time.setter
    def end_time(self, value):
        self.__end_time = value

    @status.setter
    def status(self, value):
        if isinstance(value, ENUM_STATUS.ReservationStatus):
            self.__status = value
        else:
            raise ValueError("Invalid reservation status")

    # / ================================================================
    # - Methods
    # / ================================================================

    # / ================================================================
