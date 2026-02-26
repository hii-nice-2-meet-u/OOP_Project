from BGC import *

if __name__ == "__main__":
    sys = CafeSystem()

    sys.add_owner("Alice")
    sys.add_manager("Bob")
    sys.add_customer_member("Charlie")
    sys.add_customer_member("David")
    sys.add_customer_walk_in()

    print([f"{a.name} - {a.user_id}" for a in sys.person])

    sys.add_cafe_branch("MASOPESO Cafe", "123 Main St")
    sys.add_cafe_branch("TOMATOMA Cafe", "465 Broadway Ave")

    print([f"{a.name} - {a.branch_id}" for a in sys.cafe_branches])
