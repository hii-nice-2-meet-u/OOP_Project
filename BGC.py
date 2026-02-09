import BGC_person
import BGC_menu
import BGC_log
import BGC_operation


class BoardGameCafeSystem:
    def __init__(self):
        self.__board_game_cafes = []
        self.__Persons = []


class BoardGameCafe:
    def __init__(self):
        self.__cafe_name = None
        self.__cafe_id = None
        self.__cafe_status = None
        self.__location = None
        self.__lobbies = []
        self.__board_games = []
        self.__menu_list = BGC_menu.MenuList()
        self.__order_system = BGC_log.OrderSystem()
        self.__reservation_manager = BGC_log.ReservationManager()
        self.__managers = []
        self.__staffs = []
        self.__transactions = []
        self.__audit_logs = []



