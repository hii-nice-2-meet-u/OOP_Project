from BGC_SYSTEM import CafeSystem

def test_menu_init():
    system = CafeSystem()
    print("Creating a new branch...")
    branch = system.create_cafe_branch("Test Branch", "Test Location")
    branch_id = branch.branch_id
    print(f"Branch created: {branch_id}")
    
    try:
        print("Attempting to add menu item without manual menu initialization...")
        system.create_menu_item_food_to_branch(branch_id, "Test Food", 100, "Test Description")
        print("SUCCESS: Menu item added successfully!")
    except Exception as e:
        print(f"FAILED: {e}")

if __name__ == "__main__":
    test_menu_init()
