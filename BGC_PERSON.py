import ENUM_STATUS


class Person(ABC):
    def __init__(self, name, user_id):
        self.__name = name
        self.__user_id = user_id

    @property
    def name(self):
        return self.__name

    @property
    def user_id(self):
        return self.__user_id


class Customer(Person):
    def __init__(self, name, user_id):
        super().__init__(name, user_id)
        self.__total_spent = 0
        self.__birth_date = None
        self.__member_tier = "Bronze"
        self.__is_student = False

    @property
    def total_spent(self):
        return self.__total_spent

    @total_spent.setter
    def total_spent(self, amount):
        self.__total_spent += amount
        self.__update_member_tier()

    @property
    def birth_date(self):
        return self.__birth_date

    @birth_date.setter
    def birth_date(self, date):
        self.__birth_date = date

    @property
    def member_tier(self):
        return self.__member_tier

    def __update_member_tier(self):  # ! แก้เลขด้วย
        if self.__total_spent >= 1000:
            self.__member_tier = "Gold"
        elif self.__total_spent >= 500:
            self.__member_tier = "Silver"
        elif self.__total_spent > 69:
            self.__member_tier = "Bronze"
        else:
            self.__member_tier = "None"

    def get_discount(self):
        if self.__member_tier == "Gold":
            return 0.20
        if self.__is_student:
            return 0.15
        elif self.__member_tier == "Silver":
            return 0.10
        elif self.__member_tier == "Bronze":
            return 0.05
        else:
            return 0.0

    @property
    def is_student(self):
        return self.__is_student

    @is_student.setter
    def is_student(self, value):
        self.__is_student = value


class NonCustomer(Person):
    def __init__(self, name, user_id):
        super().__init__(name, user_id)
        self.__salary = 0

    @property
    def salary(self):
        return self.__salary

    @salary.setter
    def salary(self, amount):
        self.__salary = amount


class Manager(NonCustomer):
    def __init__(self, name, user_id):
        super().__init__(name, user_id)
        self.__managed_branches = []

    @property
    def managed_branches(self):
        return self.__managed_branches


class Owner(NonCustomer):
    def __init__(self, name, user_id):
        super().__init__(name, user_id)
        self.__owned_branches = []

    @property
    def owned_branches(self):
        return self.__owned_branches


class Staff(NonCustomer):
    def __init__(self, name, user_id):
        super().__init__(name, user_id)
        self.__assigned_branch = None

    @property
    def assigned_branch(self):
        return self.__assigned_branch

    @assigned_branch.setter
    def assigned_branch(self, branch):
        self.__assigned_branch = branch
