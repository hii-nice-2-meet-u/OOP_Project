import BGC_menu


class BoardGameCafeSystem:
    def __init__(self):
        self.__owners = []
        self.__board_game_cafes = []


class BoardGameCafe:
    def __init__(self):
        self.__cafe_name = None
        self.__cafe_id = None
        self.__cafe_status = None
        self.__location = None
        self.__lobbies = []
        self.__board_games = []
        # self.__menu_list = MenuList()
        self.__managers = []
        self.__staffs = []
        self.__reservations = []
        self.__transactions = []
        self.__audit_logs = []


class Lobby:
    def __init__(self):
        self.__lobby_id = None
        self.__play_tables = []


class PlayTable:
    def __init__(self):
        self.__table_id = None
        self.__status = None
        self.__customers = []
        self.__board_game = []


class BoardGame:
    def __init__(self, _name: str, _item_id: str):
        self.__name = _name
        self.__item_id = _item_id
        self.__status = None
        self.__description = None
        self.__difficulty = None
        self.__category = None


class Person:
    def __init__(self, _name: str, _id: str):
        self.__name = _name
        self.__user_id = _id

    def get_name(self):
        return self.__name

    def set_name(self, _name):
        if not isinstance(_name, str):
            raise ValueError("\t• ⚠️ \t- Name must be a string")
        self.__name = _name

    def get_user_id(self):
        return self.__user_id

    def set_user_id(self, _id):
        if not isinstance(_id, str):
            raise ValueError("\t• ⚠️ \t- User ID must be a string")
        self.__user_id = _id


class Owner(Person):
    def __init__(self, _name: str, _id: str):
        super().__init__(_name, _id)


class Manager(Person):
    def __init__(self, _name: str, _id: str):
        super().__init__(_name, _id)


class Staff(Person):
    def __init__(self, _name: str, _id: str):
        super().__init__(_name, _id)


class Reception(Staff):
    def __init__(self, _name: str, _id: str):
        super().__init__(_name, _id)


class Customer(Person):
    def __init__(self, _name: str, _id: str):
        super().__init__(_name, _id)


class Member(Customer):
    def __init__(self, _name: str, _id: str):
        super().__init__(_name, _id)


class MemberSilver(Member):
    def __init__(self, _name: str, _id: str):
        super().__init__(_name, _id)


class MemberGold(Member):
    def __init__(self, _name: str, _id: str):
        super().__init__(_name, _id)


class MemberPlatinum(Member):
    def __init__(self, _name: str, _id: str):
        super().__init__(_name, _id)


class NonMember(Customer):
    def __init__(self, _name: str, _id: str):
        super().__init__(_name, _id)
