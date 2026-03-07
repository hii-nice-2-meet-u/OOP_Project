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
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Name must be a non-empty string")
        self.__name = value

    # / ════════════════════════════════════════════════════════════════
    # - Abstract Methods (Polymorphism — subclass ทุกตัวต้อง override)
    # / ════════════════════════════════════════════════════════════════

    @abstractmethod
    def get_role(self) -> str:
        """คืนชื่อ role ของ person นั้นๆ"""
        pass

    # / ════════════════════════════════════════════════════════════════
    # - Methods
    # / ════════════════════════════════════════════════════════════════

    def __repr__(self):
        return f"<{self.get_role()} id={self.__user_id} name='{self.__name}'>"

    # / ════════════════════════════════════════════════════════════════


# | ════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
# | #EFFF11


class Customer(Person):
    def __init__(self, name, user_id):
        super().__init__(name, user_id)

    # / ════════════════════════════════════════════════════════════════
    # - Abstract Methods
    # / ════════════════════════════════════════════════════════════════

    @abstractmethod
    def get_role(self) -> str:
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
    def member_tier(self):
        return self.__member_tier

    @property
    def birth_date(self):
        return self.__birth_date

    # / ════════════════════════════════════════════════════════════════
    # - Setters
    # / ════════════════════════════════════════════════════════════════

    @total_spent.setter
    def total_spent(self, amount):
        if not isinstance(amount, (int, float)) or amount < 0:
            raise ValueError("Amount must be a non-negative number")
        self.__total_spent += amount
        self.__update_member_tier()

    @member_tier.setter
    def member_tier(self, tier):
        if not isinstance(tier, MemberTier):
            raise ValueError("Tier must be a MemberTier enum value")
        self.__member_tier = tier

    @birth_date.setter
    def birth_date(self, date):
        self.__birth_date = date

    # / ════════════════════════════════════════════════════════════════
    # - Methods
    # / ════════════════════════════════════════════════════════════════

    def get_role(self) -> str:
        return "Member"

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
    # - Methods
    # / ════════════════════════════════════════════════════════════════

    def get_role(self) -> str:
        return "WalkInCustomer"

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
        if not isinstance(amount, (int, float)) or amount < 0:
            raise ValueError("Salary must be a non-negative number")
        self.__salary = amount

    # / ════════════════════════════════════════════════════════════════
    # - Abstract Methods
    # / ════════════════════════════════════════════════════════════════

    @abstractmethod
    def get_role(self) -> str:
        pass

    # / ════════════════════════════════════════════════════════════════


# | ════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
# | #EFFF11


class Manager(NonCustomer):
    __counter = 0

    def __init__(self, name):
        temp_id = "MANAGER-" + str(Manager.__counter).zfill(5)
        Manager.__counter += 1
        super().__init__(name, temp_id)
        self.__managed_branch = None

    # / ════════════════════════════════════════════════════════════════
    # - Getters
    # / ════════════════════════════════════════════════════════════════

    @property
    def managed_branch(self):
        return self.__managed_branch

    # / ════════════════════════════════════════════════════════════════
    # - Setters
    # / ════════════════════════════════════════════════════════════════

    @managed_branch.setter
    def managed_branch(self, branch):
        self.__managed_branch = branch

    # / ════════════════════════════════════════════════════════════════
    # - Methods
    # / ════════════════════════════════════════════════════════════════

    def get_role(self) -> str:
        return "Manager"

    # / ════════════════════════════════════════════════════════════════


# | ════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
# | #EFFF11


class Owner(NonCustomer):
    __counter = 0

    def __init__(self, name):
        temp_id = "OWNER-" + str(Owner.__counter).zfill(5)
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
    # - Methods
    # / ════════════════════════════════════════════════════════════════

    def get_role(self) -> str:
        return "Owner"

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

    def get_role(self) -> str:
        return "Staff"

    # / ════════════════════════════════════════════════════════════════


# | ════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════