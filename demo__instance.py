from BGC import *

system = CafeSystem()

# / ════════════════════════════════════════════════════════════════

system.create_owner("Jordi El Niño Polla")
system.create_manager("Mia Kalifa")
system.create_manager("Rae Lil Black")
system.create_staff("Lana Rhoades")
system.create_staff("Jew")
system.create_staff("jeddo")
system.create_staff("Champ")
system.create_staff("Peaud")
system.create_staff("Wave")
system.create_customer_member("Pao")
system.create_customer_member("Sua")

# | ════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
# | #FFFF67

# / ════════════════════════════════════════════════════════════════
# / Cafe branch 1

system.create_cafe_branch(
    "MasoPeeso 67 Cafe", "Soi HornPub, district BIG-BIG 67, Bankok"
)

system.add_owner_to_branch("BRCH-00000", "OWNER-00000")
system.add_manager_to_branch("BRCH-00000", "MANAGER-00000")
system.add_staff_to_branch("BRCH-00000", "STAFF-00000")
system.add_staff_to_branch("BRCH-00000", "STAFF-00001")
system.add_staff_to_branch("BRCH-00000", "STAFF-00002")

# / ════════════════════════════════════════════════════════════════

system.create_table_to_branch("BRCH-00000", 2)
system.create_table_to_branch("BRCH-00000", 4)
system.create_table_to_branch("BRCH-00000", 6)
system.create_table_to_branch("BRCH-00000", 8)
system.create_table_to_branch("BRCH-00000", 10)

# / ════════════════════════════════════════════════════════════════

system.create_board_game_to_branch(
    "BRCH-00000",
    "Uno",
    "classic card game",
    100.00,
    2,
    10,
    "A card game where players take turns matching a card in their hand with the current card shown on top of the deck either by color or number.",
)
system.create_board_game_to_branch(
    "BRCH-00000",
    "Monopoly",
    "classic board game",
    200.00,
    2,
    6,
    "A board game where players buy and sell properties, collect rent, and try to bankrupt other players by landing on their properties.",
)
system.create_board_game_to_branch(
    "BRCH-00000",
    "Scrabble",
    "classic word game",
    100.00,
    2,
    4,
    "A word game where players take turns to form words from a set of letters.",
)

system.create_board_game_to_branch(
    "BRCH-00000",
    "Catan",
    "Strategy",
    600,
    3,
    4,
    "Build settlements and trade resources.",
)

system.create_board_game_to_branch(
    "BRCH-00000",
    "Avalon",
    "Social Deduction",
    350,
    5,
    10,
    "Find the minions of Mordred.",
)

system.create_board_game_to_branch(
    "BRCH-00000",
    "Exploding Kittens",
    "Party",
    300,
    2,
    5,
    "Don't get exploded by the kitten!",
)

system.create_board_game_to_branch(
    "BRCH-00000",
    "Root",
    "Strategy",
    900,
    2,
    4,
    "Asymmetric warfare in the forest.",
)

# / ════════════════════════════════════════════════════════════════

system.create_menu_to_branch("BRCH-00000")

# เพิ่มเมนูอาหารลงในระบบ
system.create_menu_item_food_to_branch(
    "BRCH-00000",
    "Spicy BBQ Wings",
    129,
    "Deep-fried wings with spicy BBQ sauce",
)
system.create_menu_item_food_to_branch(
    "BRCH-00000",
    "Larb French Fries",
    89,
    "French fries with spicy Larb seasoning",
)
system.create_menu_item_food_to_branch(
    "BRCH-00000",
    "Spicy Tuna Sandwich",
    79,
    "Tuna sandwich with a spicy Sriracha kick",
)
system.create_menu_item_food_to_branch(
    "BRCH-00000",
    "Crispy Gyoza Chili Oil",
    95,
    "Fried gyoza served with spicy chili oil",
)
system.create_menu_item_food_to_branch(
    "BRCH-00000",
    "Cheesy Nachos Jalapeno",
    115,
    "Nachos with cheese and spicy jalapenos",
)

# เพิ่มเมนูเครื่องดื่มลงในระบบ (พารามิเตอร์: branch_id, name, price, cup_size, description)
system.create_menu_item_drink_to_branch(
    "BRCH-00000",
    "Thai Milk Tea",
    55,
    "M",
    "Signature Thai iced tea",
)
system.create_menu_item_drink_to_branch(
    "BRCH-00000",
    "Pink Lemonade Soda",
    65,
    "L",
    "Sparkling pink lemonade",
)
system.create_menu_item_drink_to_branch(
    "BRCH-00000",
    "Iced Matcha Latte",
    75,
    "M",
    "Premium Japanese matcha with fresh milk",
)
system.create_menu_item_drink_to_branch(
    "BRCH-00000",
    "Lychee Rose Tea",
    60,
    "L",
    "Refreshing lychee tea with rose aroma",
)
system.create_menu_item_drink_to_branch(
    "BRCH-00000",
    "Dark Chocolate Frappe",
    85,
    "M",
    "Rich dark chocolate blended drink",
)

# / ════════════════════════════════════════════════════════════════

# | ════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
# | #FFFF67

# / ════════════════════════════════════════════════════════════════
# / Cafe Branch 2: Ladkrabang

system.create_cafe_branch(
    "Ladkrabang Branch", "Soi Ladkrabang, district Ladkrabang, Bankok"
)

system.add_owner_to_branch("BRCH-00001", "OWNER-00000")
system.add_manager_to_branch("BRCH-00001", "MANAGER-00001")
system.add_staff_to_branch("BRCH-00001", "STAFF-00003")
system.add_staff_to_branch("BRCH-00001", "STAFF-00004")
system.add_staff_to_branch("BRCH-00001", "STAFF-00005")

system.create_table_to_branch("BRCH-00001", 2)
system.create_table_to_branch("BRCH-00001", 4)
system.create_table_to_branch("BRCH-00001", 6)
system.create_table_to_branch("BRCH-00001", 8)
system.create_table_to_branch("BRCH-00001", 10)

# เพิ่มบอร์ดเกม 7 เกม
system.create_board_game_to_branch(
    "BRCH-00001",
    "Ultimate Werewolf",
    "Party",
    300,
    7,
    35,
    "A game of social deduction for large groups.",
)
system.create_board_game_to_branch(
    "BRCH-00001",
    "Exploding Kittens",
    "Party",
    350,
    2,
    5,
    "A strategic, kitty-powered version of Russian Roulette.",
)
system.create_board_game_to_branch(
    "BRCH-00001",
    "Salem 1692",
    "Social Deduction",
    450,
    4,
    12,
    "Hunt the witches before they take over the town of Salem.",
)
system.create_board_game_to_branch(
    "BRCH-00001",
    "Usagyuuun",
    "Party",
    300,
    2,
    6,
    "A fun and fast-paced game featuring the energetic Usagyuuun characters.",
)
system.create_board_game_to_branch(
    "BRCH-00001",
    "Coup",
    "Bluffing",
    250,
    2,
    6,
    "Bluff and deceive your way to power in this quick strategy game.",
)
system.create_board_game_to_branch(
    "BRCH-00001",
    "Sheriff of Nottingham",
    "Bluffing",
    500,
    3,
    5,
    "Deceive and bribe the Sheriff to smuggle your goods into the city.",
)
system.create_board_game_to_branch(
    "BRCH-00001",
    "Cheese Thief",
    "Social Deduction",
    350,
    4,
    8,
    "A quick-playing game where everyone tries to find who stole the cheese.",
)

system.create_menu_to_branch("BRCH-00001")
# อาหารไทย 4 อย่าง
system.create_menu_item_food_to_branch(
    "BRCH-00001",
    "Pad Thai Goong",
    120,
    "Stir-fried rice noodles with shrimp, tofu, and bean sprouts.",
)
system.create_menu_item_food_to_branch(
    "BRCH-00001",
    "Green Curry with Chicken",
    150,
    "Rich and spicy Thai green curry served with tender chicken.",
)
system.create_menu_item_food_to_branch(
    "BRCH-00001",
    "Basil Pork over Rice",
    110,
    "Spicy stir-fried minced pork with holy basil and a fried egg.",
)
system.create_menu_item_food_to_branch(
    "BRCH-00001",
    "Tom Yum Goong",
    180,
    "Famous Thai spicy and sour soup with succulent prawns.",
)

# ของกินเล่น 4 อย่าง
system.create_menu_item_food_to_branch(
    "BRCH-00001",
    "Crispy Spring Rolls",
    80,
    "Golden fried vegetable spring rolls served with sweet chili sauce.",
)
system.create_menu_item_food_to_branch(
    "BRCH-00001",
    "Chicken Satay",
    95,
    "Grilled marinated chicken skewers served with peanut sauce.",
)
system.create_menu_item_food_to_branch(
    "BRCH-00001",
    "Fried Wontons",
    70,
    "Crispy fried wontons stuffed with seasoned minced pork.",
)
system.create_menu_item_food_to_branch(
    "BRCH-00001",
    "Spicy Pork Jerky",
    90,
    "Authentic Thai-style deep-fried marinated pork jerky.",
)

# เครื่องดื่ม 7 อย่าง
system.create_menu_item_drink_to_branch(
    "BRCH-00001",
    "Pink Milk (Nom Yen)",
    45,
    "M",
    "Sweet and creamy Thai-style rose syrup milk.",
)
system.create_menu_item_drink_to_branch(
    "BRCH-00001",
    "Thai Iced Tea",
    50,
    "M",
    "Classic Thai tea brewed and served with sweetened condensed milk.",
)
system.create_menu_item_drink_to_branch(
    "BRCH-00001",
    "Iced Matcha Green Tea",
    55,
    "M",
    "Refreshing iced premium Japanese green tea with milk.",
)
system.create_menu_item_drink_to_branch(
    "BRCH-00001",
    "Iced Americano",
    60,
    "M",
    "Bold and smooth espresso topped with water and ice.",
)
system.create_menu_item_drink_to_branch(
    "BRCH-00001",
    "Blue Hawaii Italian Soda",
    55,
    "L",
    "Sparkling blue hawaii syrup mixed with refreshing soda.",
)
system.create_menu_item_drink_to_branch(
    "BRCH-00001",
    "Mineral Water",
    20,
    "S",
    "Chilled bottled natural mineral water.",
)
system.create_menu_item_drink_to_branch(
    "BRCH-00001",
    "Iced Fresh Milk",
    40,
    "M",
    "Pure, creamy, and chilled fresh milk.",
)

# | ════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
