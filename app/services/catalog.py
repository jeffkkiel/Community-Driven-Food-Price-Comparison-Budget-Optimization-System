# for add_product values and more?
from decimal import Decimal
from app import app


CITIES = [
    ("bacoor", "Bacoor"),
    ("dasmarinas", "Dasmariñas"),
    ("imus", "Imus"),
]

DEFAULT_STORES = ["Robinsons", "Savemore",
                  "SM Supermarket", "Puregold", "Palengke"]

CATEGORIES = [
    ("rice-grains", "Rice and Grains"),
    ("fruits", "Fruits"),
    ("vegetables", "Vegetables"),
    ("meat-poultry", "Meat and Poultry"),
    ("seafood", "Seafood"),
    ("eggs", "Eggs"),
    ("dairy", "Dairy / Chilled Goods"),
    ("frozen-goods", "Frozen Goods"),
    ("pantry", "Pantry / Dry Goods"),
    ("snacks-sweets", "Snacks and Sweets"),
    ("beverages", "Beverages"),
]

UNITS = ["kg", "g", "L", "ml", "pc", "dozen", "pack", "bundle"]

CATEGORY_UNITS = {
    "rice-grains": ["kg", "g", "pack"],
    "fruits": ["kg", "g", "pc", "pack", "bundle"],
    "vegetables": ["kg", "g", "pc", "pack", "bundle"],
    "meat-poultry": ["kg", "g", "pc", "pack"],
    "seafood": ["kg", "g", "pc", "pack"],
    "eggs": ["pc", "dozen", "pack"],
    "dairy": ["ml", "L", "g", "kg", "pc", "pack"],
    "frozen-goods": ["kg", "g", "pack"],
    "pantry": ["kg", "g", "ml", "L", "pc", "pack"],
    "snacks-sweets": ["g", "pc", "pack"],
    "beverages": ["ml", "L", "pc", "pack"],
}

UNIT_CONVERSION = {
    "kg": ("kg", Decimal("1")),
    "g": ("kg", Decimal("0.001")),
    "L": ("L", Decimal("1")),
    "ml": ("L", Decimal("0.001")),
    "pc": ("pc", Decimal("1")),
    "dozen": ("pc", Decimal("12")),
    "pack": ("pack", Decimal("1")),
    "bundle": ("bundle", Decimal("1")),
}


def allowed_units(category_value):
    return CATEGORY_UNITS.get(category_value, UNITS)


def get_add_price_options():
    return {
        "cities": CITIES,
        "default_stores": DEFAULT_STORES,
        "categories": CATEGORIES,
        "units": UNITS,
    }
