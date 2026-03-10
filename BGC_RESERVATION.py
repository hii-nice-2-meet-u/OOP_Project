from datetime import datetime

from ENUM_STATUS import ReservationStatus

# | ════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
# | #EFFF11


class Reservation:
    __counter = 0

    def __init__(
        self,
        customer_id: str,
        branch_id: str,
        table_id: str,
        date: str,
        start_time: str,
        end_time: str,
        total_player: int = 1,
        current_time: datetime = None,
        deposit: float = 0.0
    ):
        self.__reservation_id = "RESV-" + str(Reservation.__counter).zfill(5)
        Reservation.__counter += 1
        now = current_time if current_time is not None else datetime.now()
        self.__current_reservation_date = now.date()
        self.__reservation_time = datetime.strptime(
            f"{date} {start_time}", "%Y-%m-%d %H:%M"
        )
        self.__customer_id = customer_id
        self.__branch_id = branch_id
        self.__table_id = table_id
        self.__date = date
        self.__start_time = start_time
        self.__end_time = end_time
        self.__total_player = total_player
        self.__status = ReservationStatus.PENDING
        self.__deposit = deposit

    # / ════════════════════════════════════════════════════════════════
    # - Getters
    # / ════════════════════════════════════════════════════════════════

    @property
    def reservation_id(self):
        return self.__reservation_id

    @property
    def current_reservation_date(self):
        return self.__current_reservation_date

    @property
    def customer_id(self):
        return self.__customer_id

    @property
    def branch_id(self):
        return self.__branch_id

    @property
    def table_id(self):
        return self.__table_id

    # @property
    # def reservation_date(self):
    #     return self.__reservation_date

    @property
    def reservation_time(self):
        return self.__reservation_time

    # @property
    # def duration(self):
    #     return self.__duration

    @property
    def status(self):
        return self.__status

    @property
    def date(self):
        return self.__date

    @property
    def start_time(self):
        return self.__start_time

    @property
    def end_time(self):
        return self.__end_time

    @property
    def total_player(self):
        return self.__total_player

    @property
    def deposit(self):
        return self.__deposit

    # / ════════════════════════════════════════════════════════════════
    # - Setters
    # / ════════════════════════════════════════════════════════════════

    @customer_id.setter
    def customer_id(self, value):
        self.__customer_id = value

    @branch_id.setter
    def branch_id(self, value):
        self.__branch_id = value

    @table_id.setter
    def table_id(self, value):
        self.__table_id = value

    # @reservation_date.setter
    # def reservation_date(self, value):
    #     self.__reservation_date = value

    @reservation_time.setter
    def reservation_time(self, value):
        self.__reservation_time = value

    # @duration.setter
    # def duration(self, value):
    #     self.__duration = value

    @status.setter
    def status(self, value):
        if isinstance(value, ReservationStatus):
            self.__status = value
        else:
            raise ValueError(
                "Invalid reservation status. Must be an instance of ReservationStatus Enum."
            )

    # / ════════════════════════════════════════════════════════════════
    # - Methods (เพิ่มเติมสำหรับเตรียมทำ MCP)
    # / ════════════════════════════════════════════════════════════════

    def update_status(self, new_status: str) -> None:
        """
        Method ใหม่ที่เพิ่มมาตาม Class Diagram: + update_status(new_status : str) : void
        """

        try:
            self.status = ReservationStatus(new_status)
        except ValueError:
            raise ValueError(
                f"Invalid status: {new_status}. Allowed values are: {[e.value for e in ReservationStatus]}"
            )

    def to_dict(self):
        """สำหรับแปลงเป็น JSON ส่งผ่าน API / MCP"""
        return {
            "reservation_id": self.__reservation_id,
            "created_at": str(self.__current_reservation_date),
            "customer_id": self.__customer_id,
            "branch_id": self.__branch_id,
            "table_id": self.__table_id,
            "date": self.__date,
            "start_time": self.__start_time,
            "end_time": self.__end_time,  # อัปเดตให้ส่ง end_time กลับไป
            "total_player": self.__total_player,
            "status": self.__status.value,
        }


# | ════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
