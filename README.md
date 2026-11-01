# Community-Driven Food Price Comparison & Budget Optimization System

**Group Name:** Philippine Six Seveners
**Course:** S-CSPC212 - Discrete Structures
**Section:** BCS22
**Language / Framework:** Python, Flask, SQL
**Application Type:** Web-based prototype (Flask + HTML/CSS/JS)

## Group Members

- Belnas, Jeff Ezekiel F.
- Quintela, Justin Matthew O.
- Trinidad, Ian Kyle F.

---

## 1. Project Overview

Food prices vary by store, branch, location, product variant, and date. Consumers often cannot tell which store is cheapest or whether a price they saw last week has changed. This is hardest for individuals and families on a limited budget.

This system organizes food prices into structured, community-contributed records. Registered users submit prices they see in supermarkets and public markets. Anyone logged in can then browse and search records, compare stores, review price history, and plan grocery purchases within a budget.

The project applies concepts from Discrete Structures (sets, relations, logic, and algorithms) to a practical decision-making problem: **where should I buy my groceries to spend the least?**

**Target area:** Bacoor, Dasmariñas, and Imus, Cavite.

---

## 2. Features

| Feature | Description | Status |
|---|---|---|
| Register / Login | Username and password accounts (Flask-Login, hashed passwords) | Done |
| Add Price | Pick category, product, city, and store, then enter quantity and total price. Price per item is computed automatically | Done |
| Browse Products | Filter by category and open a product to see and compare its price in every store | Done |
| Search | Search a food name from the navbar and see results grouped by city | Done |
| Day Summary | Pick a date and see all prices reported that day (Manila time) | Done |
| Price History | Filter every price report by category and city | Done |
| My Contributions | See the prices you submitted | Done |
| Dashboard | Community stats (users, stores, foods, updates today) and recent activity | Done |
| Optimize Budget | Enter a budget and basket, get the cheapest store or a suggested split | Done |

---

## 3. Discrete Structures Applied

| Topic | Where it appears |
|---|---|
| **Sets** | Tables are sets of records. `COUNT(DISTINCT location)` is set cardinality. The optimizer's candidate stores are the intersection of the stores that sell each basket item. |
| **Relations** | `product_stores` is a relation, a subset of Products × Stores, with price as an extra attribute. Many-to-many and one-to-many relationships, foreign keys, and joins (composition) are used throughout. |
| **Propositional logic / Boolean algebra** | Add Price saves only if the form, category, location, and store checks all pass: `Save = F ∧ C ∧ L ∧ M`. The error condition follows De Morgan's law: `¬F ∨ ¬C ∨ ¬L ∨ ¬M`. |
| **Algorithms** | Search (linear scan with filter), grouping results by city, latest-price selection, and the optimizer (total per candidate store, then minimum). |
| **Quantifiers** *(optimizer)* | A store is valid if for every basket item there exists a listing in that store: `∀ item ∈ basket, ∃ listing(store, item)`. |

---

## 4. Tech Stack

- **Backend:** Python 3.13, Flask
- **Database:** SQLite via Flask-SQLAlchemy and Flask-Migrate
- **Forms and security:** Flask-WTF (CSRF protection), Flask-Login, Werkzeug password hashing
- **Frontend:** HTML (Jinja2 templates), CSS, vanilla JavaScript, Font Awesome icons
- **Hosting:** PythonAnywhere

---

## 5. Project Structure

```
Food-Price-Comparison-Budget-Optimization-System/
├── run.py                  # starts the server
├── config.py               # settings (SECRET_KEY, database path)
├── requirements.txt        # Python dependencies
├── .env                    # secrets (not in Git)
├── migrations/             # database migration files
└── app/
    ├── __init__.py         # creates app, db, and login manager
    ├── routes.py           # all routes
    ├── models.py           # User, Product, Store, ProductStore, PriceHistory
    ├── forms.py            # Flask-WTF forms, CATEGORIES, LOCATIONS
    ├── services/           # business logic (add product, search, helpers)
    ├── templates/          # Jinja2 pages
    └── static/             # css/, js/, images/
```

### Database

```
users
products ──< product_stores >── stores
                  │
                  └──< price_history >── users
```

- `product_stores` holds the current price of a product in a store.
- `price_history` logs every price report, with the user who submitted it.

---

## 6. Installation

Requires **Python 3.10+** and **Git**.

```bash
# 1. Clone
git clone https://github.com/jeffkkiel/Community-Driven-Food-Price-Comparison-Budget-Optimization-System.git
cd Community-Driven-Food-Price-Comparison-Budget-Optimization-System

# 2. Create and activate a virtual environment
python -m venv venv
venv\Scripts\activate          # Windows
# source venv/bin/activate     # macOS / Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Create the database
flask db upgrade

# 5. Run
python run.py
```

Open **http://127.0.0.1:5000** and register an account.

### Environment variables

Create a `.env` file in the project root. It is ignored by Git.

```
SECRET_KEY=put-a-long-random-string-here
PA_API_TOKEN=your-pythonanywhere-api-token
```

`SECRET_KEY` must stay the same between restarts, or users are logged out and forms fail CSRF checks.

---

## 7. How to Use

1. **Register** a username (4 to 20 characters) and a password (8 or more characters).
2. **Add Price:** choose a category, then a product (or add a new one), then a city and store, then enter the quantity and total price.
3. **Browse** products by category and open a product to compare its price across stores, or **search** a food name in the navbar.
4. Open **Day Summary** or **Price History** to review reports by date, category, or city.
5. Open **My Contributions** to see what you have submitted.

---

## 8. Team Workflow

- The database file (`app.db`) is **not** in Git. Each person has a local database.
- After every `git pull`, run `flask db upgrade`.
- After changing `models.py`, run `flask db migrate -m "describe change"`, then `flask db upgrade`, and commit the new file in `migrations/versions/`.
- Work on a branch for large changes, and tell the team before editing shared files (`models.py`, `routes.py`, `forms.py`).

```bash
git checkout -b feature-name
git add .
git commit -m "describe the change"
git push -u origin feature-name
```

---

## 9. Deployment (PythonAnywhere)

1. `git pull` in the project folder using a Bash console.
2. `pip install -r requirements.txt` in the web app's virtualenv.
3. `flask db upgrade` to update the live database.
4. Make sure `.env` exists on the server with a fixed `SECRET_KEY`.
5. Reload the web app from the **Web** tab.

---

## 10. Limitations and Future Work

- Prices depend on community contributions, so records can be outdated or wrong. There is no moderation yet.
- Product names are free text (for example "Jasmine Rice 1kg"), so the same item typed differently becomes two products.
- No password reset, because accounts have no email.
- Planned: price-per-unit normalization (per kg or liter), a "Lowest price" tag, product images, and ignoring prices older than 30 days in the optimizer.

---

## 11. License and Academic Note

This project was made for academic purposes in S-CSPC212 (Discrete Structures). Prices shown are community-submitted and sample data, and are not official market prices.
