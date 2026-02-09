class Registration:
    def __init__(self):
        self.__registration_id = None
        self.__timestamp = None
        self.__customer = None
        self.__status = None
        
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
        self.__coupon = []
        self.__birth_date = ""
        self.__point = 0


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