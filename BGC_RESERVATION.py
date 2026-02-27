from ENUM_STATUS import ReservationStatus
import datetime

# | ================================================================================================================================


class Reservation:
    __counter = 0

    def __init__(
        self,
        customer_id,
        branch_id,
        table_id,
        reservation_date,
        reservation_time,
        duration,
    ):
        self.__reservation_id = "RESV-" + str(Drink.__counter).zfill(5)
        self.__current_reservation_date = datetime.now().date()
        self.__customer_id = customer_id
        self.__branch_id = branch_id
        self.__table_id = table_id
        self.__reservation_date = reservation_date
        self.__reservation_time = reservation_time
        self.__duration = duration
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
    def reservation_date(self):
        return self.__reservation_date

    @property
    def reservation_time(self):
        return self.__reservation_time

    @property
    def duration(self):
        return self.__duration

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

    @reservation_date.setter
    def reservation_date(self, value):
        self.__reservation_date = value

    @reservation_time.setter
    def reservation_time(self, value):
        self.__reservation_time = value

    @duration.setter
    def duration(self, value):
        self.__duration = value

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


# | ================================================================================================================================
