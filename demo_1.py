from BGC import *

if __name__ == "__main__":
    sys = CafeSystem()

    sys.add_owner("OWNER_A")
    sys.add_owner("OWNER_B")
    sys.add_manager("MANAGER_A")
    sys.add_manager("MANAGER_B")
    sys.add_manager("MANAGER_C")
    sys.add_manager("MANAGER_D")
    sys.add_customer_member("MEMBER_A")
    sys.add_customer_member("MEMBER_B")
    sys.add_customer_member("MEMBER_C")
    sys.add_customer_member("MEMBER_D")
    sys.add_customer_walk_in()

    for o in [f"{a.name:<15}-  {a.user_id}" for a in sys.person]:
        print(o)
    print(" ")

    sys.add_cafe_branch("Cafe - A", "A 123/456")
    sys.add_cafe_branch("Cafe - B", "B 123/456")
    sys.add_cafe_branch("Cafe - C", "C 123/456")
    sys.add_cafe_branch("Cafe - D", "D 123/456")

    for o in [f"{a.name} | {a.branch_id}" for a in sys.cafe_branches]:
        print(o)
    print(" ")

    for i in range(4):
        sys.add_table_to_branch("BRCH-0000" + str(i), 2)
        sys.add_table_to_branch("BRCH-0000" + str(i), 4)
        sys.add_table_to_branch("BRCH-0000" + str(i), 6)
        sys.add_table_to_branch("BRCH-0000" + str(i), 8)

    for p in range(4):
        branch_id = "BRCH-0000" + str(p)
        for o in [
            f"{a.table_id} - {a.capacity} - {a.status}"
            for a in sys.get_branch_tables(branch_id)
        ]:
            print(o)
        print(" ")
