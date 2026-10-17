# Community-Driven Food Price Comparison & Budget Optimization System

**Group Name:** Six Seveners  
**Course:** S-CSPC212 — Discrete Structures  
**Section:** BCS22  
**Programming Language:** Python  
**Application Type:** Console-Based Prototype

## Group Members

1. Belnas, Jeff Ezekiel F.
2. Quintela, Justin Matthew O.
3. Trinidad, Ian Kyle F.

---

## 1. Project Overview

The Community-Driven Food Price Comparison & Budget Optimization System is a Python console application designed to help consumers compare food prices across registered supermarkets and local public markets. It allows users to contribute prices, explore existing community records, monitor price changes, and plan grocery purchases based on their needs and available budget.

Food prices can vary depending on the store, branch, location, product variant, and date. Consumers may not always know which store offers the lowest price or whether a previously observed price has changed. This can make grocery shopping more difficult, especially for individuals and families working with a limited budget.

The proposed system addresses this problem by organizing food prices into a structured collection of records. Users can manually submit prices based on receipts or prices they observe in stores. Other users can then search the available records, compare prices, review historical data, and identify potentially cheaper purchasing options.

The application will initially use Python and JSON files to demonstrate its main features. A shared database will be required for automatic contributions and price updates across separate computers.

## 2. Project Objectives

The project aims to:

- Collect food price contributions from users through a terminal interface.
- Maintain a structured catalog of registered stores, locations, food categories, and product variants.
- Display available community-contributed prices for different stores.
- Compare current recorded prices using consistent units of measurement.
- Preserve historical price records for monitoring changes over time.
- Generate summaries of recorded prices for a selected date.
- Help users create shopping baskets based on their grocery needs.
- Recommend cost-efficient purchasing options within a specified budget.
- Apply Discrete Structures concepts to data organization, relationships, logical conditions, and optimization algorithms.

## 3. System Scope

The project will focus on a functional console-based prototype. Users will interact with the application through numbered menu choices and text inputs.

The initial system will support:

- Manual price contributions from receipts.
- Manual price contributions based on observed store prices.
- Predefined store and food catalogs.
- Price searching and comparison.
- Historical price records.
- Daily price summaries.
- Shopping basket calculations.
- Basic budget optimization.
- JSON-based data persistence.

The prototype will not require a graphical user interface, mobile application, web interface, receipt scanner, or automatic supermarket price scraping.

## 4. Main System Features

### 4.1 Main Menu

The system will display a numbered menu that lets users access its available functions.

The proposed menu includes:

1. Submit a Receipt Price
2. Submit an Observed Price
3. Browse Community Price Records
4. Search and Compare Food Prices
5. View Price History
6. View Daily Price Summary
7. Create a Shopping Basket
8. Optimize Shopping Budget
9. Exit

Invalid menu selections will be rejected, and the application will return the user to the main menu.

### 4.2 Receipt-Based Price Contribution

Users can manually encode product information from a grocery receipt.

The system will request the necessary details, including:

- Contributor name or nickname
- Store and registered location
- Food category and product variant
- Quantity and unit
- Total price paid
- Contribution date

The program will validate the inputs before saving the contribution. A receipt does not need to be scanned or uploaded; all information will be entered through the terminal.

### 4.3 Observed-Price Contribution

Users can also report a food price they personally observe in a store without requiring a receipt.

The contribution will use the same structured record as a receipt-based submission, but its source will be labeled as an observed price.

The system will distinguish the two contribution methods so that users can understand how each record was obtained.

### 4.4 Registered Stores and Locations

To reduce inconsistent or invalid store names, users will choose from predefined options.

Initial supermarket choices:

- Robinsons Supermarket
- SM Supermarket
- SM Hypermarket
- Puregold

Initial local-market choices may include registered locations such as:

- Mary Homes Palengke
- Imus Public Market

Each registered market or supermarket branch will have an identifiable location. The system will not accept arbitrary store names during ordinary price contributions.

Additional branches and public markets can be added to the catalog when necessary.

### 4.5 Structured Food Catalog

Users will select products from predefined categories and product variants rather than entering unrestricted names.

Initial categories include:

- Rice and Grains
- Meat and Poultry
- Fish and Seafood
- Fruits
- Vegetables
- Dairy and Eggs
- Canned and Processed Foods
- Instant Noodles
- Cooking Ingredients
- Beverages

Examples of product specifications include:

- Rice variety or grade
- Banana variety
- Vegetable type
- Meat cut
- Pancit Canton brand and flavor
- Egg size or grade
- Package size for processed foods

The system will use suitable measurement units for each product, such as kilograms, grams, liters, milliliters, packs, pieces, or dozens.

Comparisons will use the same unit wherever possible. For example, the price of five kilograms of rice can be converted into a price per kilogram.

### 4.6 Community Price Records

Users can browse the records available in the system, including prices submitted by other contributors.

Each record can include:

- Product and variant
- Store and location
- Reported quantity and total price
- Normalized unit price
- Contribution source
- Contributor name or nickname
- Date of observation or purchase

The application will identify the latest recorded price for each product and store location using the recorded dates.

A newer contribution will not automatically erase the previous record. Instead, it will be added to the collection so that historical prices remain available.

### 4.7 Search and Price Comparison

Users can search for a specific product and examine the available records from different stores.

The system will display the store, location, reported price, unit price, and date of the latest available record.

When multiple stores have comparable records, the system can identify the lowest recorded unit price.

The system will clearly indicate when no matching records are available rather than inventing a price.

### 4.8 Price History

The system will preserve previous contributions so users can examine price changes over time.

The history viewer will display the available records for a selected product, including the store, location, reported price, unit price, date, and contribution source.

This feature can help users identify recorded price increases, decreases, and periods when price information has not been updated.

### 4.9 Daily Price Summary

Users can view a summary of the prices recorded for a particular date.

Depending on the available data, the summary may show:

- Number of price contributions
- Products reported
- Stores and locations represented
- Lowest and highest comparable prices
- Average comparable prices
- Recent price changes

The summary will use the dates associated with the records. It will not imply that all listed prices are live or independently verified.

### 4.10 Shopping Basket

Users can create a basket containing the products and quantities they need.

The system will calculate the estimated cost of the basket using available price records. Users can review the selected products and their estimated costs before proceeding to optimization.

A basket can contain several product categories and quantities. Products without usable price records will be identified so users know which items cannot yet be estimated.

### 4.11 Budget Optimization

The user can specify the grocery items they need, the required quantities, and their maximum budget.

The optimizer will examine the latest available prices for the requested items and identify lower-cost options.

The initial algorithm will:

1. Identify the requested products and quantities.
2. Find the latest available record for each product at each registered store location.
3. Compare the normalized unit prices.
4. Select the lowest available comparable price for each requested product.
5. Calculate the estimated cost of the proposed basket.
6. Compare the total with the user's budget.
7. Display the recommended products, stores, estimated total, and remaining budget or shortfall.

If a requested product has no available record, the system will inform the user.

The initial optimizer will prioritize the lowest recorded price for each item. It will not automatically guarantee the globally optimal shopping route or account for transportation costs unless those constraints are implemented separately.

## 5. Data Management

### JSON Storage

JSON files will be used in the initial prototype to save and retrieve structured price records.

A price record may contain fields such as:

- `item`
- `category`
- `variant`
- `store`
- `location`
- `quantity`
- `unit`
- `price`
- `date`
- `source`
- `contributor`

The program will load existing records when it starts and save new contributions when users submit prices.

### Current and Historical Prices

The system will retain previous contributions instead of replacing them whenever a new price is entered.

The latest applicable record will be used for current-price comparisons, while the complete collection will be used for the price history viewer.

### Community Sharing Limitation

A local JSON file is accessible only to the application and computers that have a copy of that file. Updating a local file does not automatically update another user's copy.

The initial prototype can demonstrate community contributions using shared sample data and locally saved submissions. For automatic sharing among users on different computers, the project will need a shared database or backend service.

GitHub will be used to store and collaborate on the project's source code. It will not serve as the live database for price contributions.

## 6. Input Validation and Data Reliability

The application will validate user inputs to reduce errors and inconsistent records.

Validation rules will include:

- Menu selections must correspond to available choices.
- Store names and locations must come from the registered catalog.
- Product selections must come from the predefined catalog.
- Prices and quantities must be greater than zero.
- Budgets must be valid, nonnegative monetary amounts.
- Product units must be appropriate for the selected item.
- Required fields cannot be left empty.
- JSON data must be handled carefully to prevent errors when loading or saving records.

Community contributions will be treated as reported information, not automatically verified facts. Their reliability depends on the accuracy and recency of the submitted data.

## 7. Discrete Structures Concepts

### 7.1 Sets

Sets will represent collections of registered stores, locations, food items, categories, and shopping basket products.

They can be used to identify unique entries, check whether a product belongs to a category, and determine whether a store or food item is registered.

### 7.2 Relations

Relations will represent connections between products, stores, locations, and price records.

For example, a product-store relation can identify which registered stores have reported prices for rice. A price relation can associate an item, location, and date with a recorded amount.

### 7.3 Functions

Functions will perform operations such as retrieving a product's latest recorded price at a particular store, calculating basket subtotals, and computing the remaining budget.

A current-price lookup can be treated as a partial function because some products may not have any recorded price for a particular store.

### 7.4 Predicate Logic

Predicate logic will represent conditions used to validate data and evaluate shopping requirements.

Examples include:

- Whether a product has an available price record.
- Whether a reported price is valid.
- Whether a basket total is within the user's budget.
- Whether one comparable unit price is lower than another.
- Whether a store has a record for a requested product.

### 7.5 Algorithms

Algorithms will support catalog searching, record retrieval, price comparison, historical tracking, basket calculations, and budget optimization.

The optimizer will evaluate the available prices and requested quantities against the user's budget to generate a cost-efficient purchasing plan.

## 8. Proposed Python Project Structure

The initial version may begin with a single `main.py` file to keep development manageable.

As the system grows, the code can be separated into modules:

- `main.py` — Main menu and program execution.
- `price_manager.py` — Price contributions, searching, comparisons, and history.
- `data_manager.py` — Loading and saving JSON data.
- `budget_optimizer.py` — Basket calculations and budget optimization.
- `catalog.py` — Registered stores, locations, categories, and products.
- `data/price_records.json` — Stored price contributions.

This structure separates responsibilities and makes the project easier to maintain and test.

## 9. Development Plan

**Phase 1 — Basic Console Application**

Create the main menu, input validation, registered catalogs, and program navigation.

**Phase 2 — Price Contributions and JSON**

Implement receipt-based and observed-price submissions, persistent records, and historical storage.

**Phase 3 — Search and Price Analysis**

Implement community browsing, product search, price comparisons, history, and daily summaries.

**Phase 4 — Shopping Basket and Optimization**

Implement quantity calculations, basket totals, cheapest-price selection, and budget checking.

**Phase 5 — Testing and Refinement**

Test valid and invalid inputs, missing records, price comparisons, historical data, budget constraints, and JSON persistence.

**Phase 6 — Shared Community Data**

If required by the project scope, connect the program to a shared database so that contributions from separate computers become available to all users.

## 10. Expected Outcome

The expected outcome is a functional Python console prototype that demonstrates how community-contributed food prices can support grocery comparison and budget-conscious purchasing.

The project will demonstrate the practical application of Discrete Structures concepts through structured data, relationships, logical conditions, and algorithms.

The long-term goal is to help consumers make more informed purchasing decisions using accessible price information and cost-efficient shopping plans.

---

**Developed by Six Seveners**  
S-CSPC212 — Discrete Structures | BCS22

remember
