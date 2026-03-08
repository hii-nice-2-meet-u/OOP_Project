from abc import ABC, abstractmethod

from ENUM_STATUS import MemberTier

# | ════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
# | #EFFF11


class Person(ABC):
    def __init__(self, name, user_id):
        self.__name = name
        self.__user_id = user_id

    # / ════════════════════════════════════════════════════════════════
    # - Getters
    # / ════════════════════════════════════════════════════════════════

    @property
    def name(self):
        return self.__name

    @property
    def user_id(self):
        return self.__user_id

    # / ════════════════════════════════════════════════════════════════
    # - Setters
    # / ════════════════════════════════════════════════════════════════

    @name.setter
    def name(self, value):
        self.__name = value

    # / ════════════════════════════════════════════════════════════════
    # - Methods
    # / ════════════════════════════════════════════════════════════════

    # / ════════════════════════════════════════════════════════════════


# | ════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
# | #EFFF11


class Customer(Person):
    def __init__(self, name, user_id):
        super().__init__(name, user_id)
        self.__phone_number = ""
        self.__note = ""
        self.__email = ""
    # / ════════════════════════════════════════════════════════════════
    # - Getters
    # / ════════════════════════════════════════════════════════════════
    @property
    def phone_number(self):
        return self.__phone_number

    @property
    def note(self):
        return self.__note
    # / ════════════════════════════════════════════════════════════════
    # - Setters
    # / ════════════════════════════════════════════════════════════════
    @phone_number.setter
    def phone_number(self, value):
        self.__phone_number = value

    @note.setter
    def note(self, value):
        self.__note = value
    # / ════════════════════════════════════════════════════════════════
    # - Methods
    # / ════════════════════════════════════════════════════════════════

    @abstractmethod
    def get_total_spent(self):
        pass

    @abstractmethod
    def get_discount(self):
        pass

    @abstractmethod
    def get_member_tier(self):
        pass

    # / ════════════════════════════════════════════════════════════════


# | ════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
# | #EFFF11


class Member(Customer):
    __counter = 0

    def __init__(self, name):
        temp_id = "MEMBER-" + str(Member.__counter).zfill(5)
        Member.__counter += 1
        super().__init__(name, temp_id)

        self.__total_spent = 0
        self.__member_tier = MemberTier.NONE_TIER
        self.__birth_date = ""

    # / ════════════════════════════════════════════════════════════════
    # - Getters
    # / ════════════════════════════════════════════════════════════════

    @property
    def total_spent(self):
        return self.__total_spent

    @property
    def birth_date(self):
        return self.__birth_date

    # / ════════════════════════════════════════════════════════════════
    # - Setters
    # / ════════════════════════════════════════════════════════════════

    @total_spent.setter
    def total_spent(self, amount):
        self.__total_spent += amount
        self.update_member_tier()

    @birth_date.setter
    def birth_date(self, date):
        self.__birth_date = date

    # / ════════════════════════════════════════════════════════════════
    # - Methods
    # / ════════════════════════════════════════════════════════════════

    def get_total_spent(self):
        return self.__total_spent

    def get_member_tier(self):
        return self.__member_tier

    def update_member_tier(self):
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
        if self.__member_tier == MemberTier.SILVER:
            return 0.10
        if self.__member_tier == MemberTier.BRONZE:
            return 0.05
        return 0.0

    # / ════════════════════════════════════════════════════════════════


# | ════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
# | #EFFF11


class WalkInCustomer(Customer):
    __counter = 0

    def __init__(self):
        temp_id = "WALK-" + str(WalkInCustomer.__counter).zfill(5)
        WalkInCustomer.__counter += 1
        super().__init__("J-doe", temp_id)

    # / ════════════════════════════════════════════════════════════════
    # - Getters
    # / ════════════════════════════════════════════════════════════════

    # / ════════════════════════════════════════════════════════════════
    # - Setters
    # / ════════════════════════════════════════════════════════════════

    # / ════════════════════════════════════════════════════════════════
    # - Methods
    # / ════════════════════════════════════════════════════════════════

    def get_total_spent(self):
        return 0

    def get_member_tier(self):
        return MemberTier.NONE_TIER

    def get_discount(self):
        return 0

    # / ════════════════════════════════════════════════════════════════


# | ════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
# | #EFFF11


class NonCustomer(Person):
    def __init__(self, name, user_id):
        super().__init__(name, user_id)
        self.__salary = 0

    # / ════════════════════════════════════════════════════════════════
    # - Getters
    # / ════════════════════════════════════════════════════════════════

    @property
    def salary(self):
        return self.__salary

    # / ════════════════════════════════════════════════════════════════
    # - Setters
    # / ════════════════════════════════════════════════════════════════

    @salary.setter
    def salary(self, amount):
        self.__salary = amount

    # / ════════════════════════════════════════════════════════════════
    # - Methods
    # / ════════════════════════════════════════════════════════════════

    # / ════════════════════════════════════════════════════════════════


# | ════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
# | #EFFF11


class Manager(NonCustomer):
    __counter = 0

    def __init__(self, name):
        temp_id = "MANAGER-" + str(Manager.__counter).zfill(5)
        Manager.__counter += 1
        super().__init__(name, temp_id)
        self.__managed_branches = None

    # / ════════════════════════════════════════════════════════════════
    # - Getters
    # / ════════════════════════════════════════════════════════════════

    @property
    def managed_branches(self):
        return self.__managed_branches

    # / ════════════════════════════════════════════════════════════════
    # - Setters
    # / ════════════════════════════════════════════════════════════════

    @managed_branches.setter
    def managed_branches(self, branches):
        self.__managed_branches = branches

    # / ════════════════════════════════════════════════════════════════
    # - Methods
    # / ════════════════════════════════════════════════════════════════

    # / ════════════════════════════════════════════════════════════════


# | ════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
# | #EFFF11


class Owner(NonCustomer):
    __counter = 0

    def __init__(self, name):
        temp_id = "OWNER-PESO67"
        Owner.__counter += 1
        super().__init__(name, temp_id)
        self.__owned_branches = []

    # / ════════════════════════════════════════════════════════════════
    # - Getters
    # / ════════════════════════════════════════════════════════════════

    @property
    def owned_branches(self):
        return self.__owned_branches.copy()

    # / ════════════════════════════════════════════════════════════════
    # - Setters
    # / ════════════════════════════════════════════════════════════════

    # / ════════════════════════════════════════════════════════════════
    # - Methods
    # / ════════════════════════════════════════════════════════════════

    def add_owned_branch(self, branch_id):
        self.__owned_branches.append(branch_id)

    # / ════════════════════════════════════════════════════════════════


# | ════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
# | #EFFF11


class Staff(NonCustomer):
    __counter = 0

    def __init__(self, name):
        temp_id = "STAFF-" + str(Staff.__counter).zfill(5)
        Staff.__counter += 1
        super().__init__(name, temp_id)
        self.__assigned_branch = None

    # / ════════════════════════════════════════════════════════════════
    # - Getters
    # / ════════════════════════════════════════════════════════════════

    @property
    def assigned_branch(self):
        return self.__assigned_branch

    # / ════════════════════════════════════════════════════════════════
    # - Setters
    # / ════════════════════════════════════════════════════════════════

    @assigned_branch.setter
    def assigned_branch(self, branch):
        self.__assigned_branch = branch

    # / ════════════════════════════════════════════════════════════════
    # - Methods
    # / ════════════════════════════════════════════════════════════════

    # / ════════════════════════════════════════════════════════════════


# | ════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════