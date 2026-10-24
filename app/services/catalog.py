# for add_price values and more?

CITIES = [
    ("bacoor", "Bacoor"),
    ("dasmarinas", "Dasmariñas"),
    ("imus", "Imus"),
]

STORES = [
    ("robinsons", "Robinsons"),
    ("savemore", "Savemore"),
    ("sm-supermarket", "SM Supermarket"),
    ("puregold", "Puregold"),
    ("palengke", "Palengke")
]


CATEGORIES = [
    ("fruits", "Fruits"),
    ("vegetables", "Vegetables"),
    ("meat-poultry", "Meat and Poultry"),
    ("seafood", "Seafood"),
    ("dairy", "Dairy / Chilled Goods"),
    ("frozen-goods", "Frozen Goods"),
    ("fresh-produce", "Pantry / Drygoods"),
    ("snacks-sweets", "Snacks and Swees"),
    ("beverages", "Beverages"),
]


def get_add_price_options():
    return {
        "cities": CITIES,
        "stores": STORES,
        "categories": CATEGORIES,
    }
