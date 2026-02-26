from abc import ABC, abstractmethod
from ENUM_STATUS import MemberTier


class Person(ABC):
    def __init__(self, name, user_id):
        self.__name = name
        self.__user_id = user_id

    # / ================================================================
    # - Getters
    # / ================================================================

    @property
    def name(self):
        return self.__name

    @property
    def user_id(self):
        return self.__user_id

    # / ================================================================
    # - Setters
    # / ================================================================

    @name.setter
    def name(self, value):
        self.__name = value

    @user_id.setter
    def user_id(self, value):
        self.__user_id = value

    # / ================================================================
    # - Methods
    # / ================================================================

    # / ================================================================


class Customer(Person):
    def __init__(self, name, user_id):
        super().__init__(name, user_id)

    # / ================================================================
    # - Getters
    # / ================================================================

    # / ================================================================
    # - Setters
    # / ================================================================

    # / ================================================================
    # - Methods
    # / ================================================================

    # / ================================================================


class Member(Customer):
    __counter = 0

    def __init__(self, name):
        temp_id = "MEMBER-" + str(Member.__counter).zfill(5)
        Member.__counter += 1
        super().__init__(name, temp_id)

        self.__total_spent = 0
        self.__member_tier = MemberTier.NONE_TIER
        self.__birth_date = ""
        # self.__is_student = False

    # / ================================================================
    # - Getters
    # / ================================================================

    @property
    def total_spent(self):
        return self.__total_spent

    @property
    def member_tier(self):
        return self.__member_tier

    @property
    def birth_date(self):
        return self.__birth_date

    @property
    def is_student(self):
        return self.__is_student

    # / ================================================================
    # - Setters
    # / ================================================================

    @total_spent.setter
    def total_spent(self, amount):
        self.__total_spent += amount
        self.__update_member_tier()

    @member_tier.setter
    def member_tier(self, tier):
        self.__member_tier = tier

    @birth_date.setter
    def birth_date(self, date):
        self.__birth_date = date

    @is_student.setter
    def is_student(self, value):
        self.__is_student = value

    # / ================================================================
    # - Methods
    # / ================================================================

    def __update_member_tier(self):
        if self.__total_spent >= 2000:
            self.__member_tier = MemberTier.PLATINUM
        elif self.__total_spent >= 1000:
            self.__member_tier = MemberTier.GOLD
        elif self.__total_spent >= 500:
            self.__member_tier = MemberTier.SILVER
        elif self.__total_spent > 250:
            self.__member_tier = MemberTier.BRONZE
        else:
            self.__member_tier = MemberTier.NONE_TIER

    def get_discount(self):
        if self.__member_tier == MemberTier.PLATINUM:
            return 0.25
        if self.__member_tier == MemberTier.GOLD:
            return 0.20
        if self.__is_student:
            return 0.15
        if self.__member_tier == MemberTier.SILVER:
            return 0.10
        if self.__member_tier == MemberTier.BRONZE:
            return 0.05
        return 0.0

    # / ================================================================


class WalkInCustomer(Customer):
    __counter = 0

    def __init__(self):
        temp_id = "WALK-" + str(WalkInCustomer.__counter).zfill(5)
        WalkInCustomer.__counter += 1
        super().__init__("J-doe", temp_id)

    # / ================================================================
    # - Getters
    # / ================================================================

    # / ================================================================
    # - Setters
    # / ================================================================

    # / ================================================================
    # - Methods
    # / ================================================================

    # / ================================================================


class NonCustomer(Person):
    def __init__(self, name, user_id):
        super().__init__(name, user_id)
        self.__salary = 0

    # / ================================================================
    # - Getters
    # / ================================================================

    @property
    def salary(self):
        return self.__salary

    # / ================================================================
    # - Setters
    # / ================================================================

    @salary.setter
    def salary(self, amount):
        self.__salary = amount

    # / ================================================================
    # - Methods
    # / ================================================================

    # / ================================================================


class Manager(NonCustomer):
    __counter = 0

    def __init__(self, name):
        temp_id = "MANAGER-" + str(Manager.__counter).zfill(5)
        Manager.__counter += 1
        super().__init__(name, temp_id)
        self.__managed_branches = None

    # / ================================================================
    # - Getters
    # / ================================================================

    @property
    def managed_branches(self):
        return self.__managed_branches

    # / ================================================================
    # - Setters
    # / ================================================================

    @managed_branches.setter
    def managed_branches(self, branches):
        self.__managed_branches = branches

    # / ================================================================
    # - Methods
    # / ================================================================

    # / ================================================================


class Owner(NonCustomer):
    __counter = 0

    def __init__(self, name):
        temp_id = "OWNER-" + str(Owner.__counter).zfill(5)
        Owner.__counter += 1
        super().__init__(name, temp_id)
        self.__owned_branches = []

    # / ================================================================
    # - Getters
    # / ================================================================

    @property
    def owned_branches(self):
        return self.__owned_branches.copy()

    # / ================================================================
    # - Setters
    # / ================================================================

    @owned_branches.setter
    def owned_branches(self, branches):
        self.__owned_branches = branches

    # / ================================================================
    # - Methods
    # / ================================================================

    # / ================================================================


class Staff(NonCustomer):
    __counter = 0

    def __init__(self, name, user_id):
        temp_id = "STAFF-" + str(Staff.__counter).zfill(5)
        Staff.__counter += 1
        super().__init__(name, user_id)
        self.__assigned_branch = None

    # / ================================================================
    # - Getters
    # / ================================================================

    @property
    def assigned_branch(self):
        return self.__assigned_branch

    # / ================================================================
    # - Setters
    # / ================================================================

    @assigned_branch.setter
    def assigned_branch(self, branch):
        self.__assigned_branch = branch

    # / ================================================================
    # - Methods
    # / ================================================================

    # / ================================================================
