# Personal Finance Analyzer

#### Video Demo: [TODO: Add YouTube link here]

#### Description:

Personal Finance Analyzer is a command-line application written in Python that allows users to record, store, search, and analyze their personal expenses.

This project was developed as my final project for **CS50's Introduction to Programming with Python (CS50P)**. Its purpose is to apply the programming concepts learned throughout the course to a practical problem while building a complete Python application from scratch.

The application provides a simple command-line interface where users can add expenses containing a date, description, category, and amount. Expenses can then be listed, filtered by category or description, analyzed by month, and saved to a CSV file.

The project uses only Python's standard library, including `csv`, `datetime`, `re`, `os`, and `sys`. No external libraries or frameworks are required.

---

## Features

### Add Expenses

Users can add one or multiple expenses during the same session.

Each expense contains:

* Date
* Description
* Category
* Amount

The application validates the date and amount before adding the expense to the current collection.

Dates can be entered using common separators such as `/`, `-`, `\`, or `,`. Regardless of the separator used, dates are stored internally using the `YYYY/MM/DD` format.

For example:

```text
2026/10/01
2026-10-01
2026\10\01
2026,10,01
```

Amounts accept either a period or comma as the decimal separator:

```text
25.90
25,90
```

The application rejects unsupported monetary formats and symbols.

---

### List Expenses

The application can display all expenses currently loaded into the user's expense collection.

Each expense is displayed with its:

```text
Date
Description
Category
Amount
```

If there are no expenses available, the application displays:

```text
No expenses found
```

---

### Monthly Summary

Users can select a month and year to find all expenses recorded during that period.

The application accepts the following formats:

```text
10/2026
Oct/2026
October/2026
```

The program displays all matching expenses and calculates their total amount.

For example:

```text
Date: 2026/10/01
Description: Groceries
Category: Food
Amount: 150.0

Date: 2026/10/05
Description: Bus ticket
Category: Transportation
Amount: 20.0

Total expenses: 170.0
```

---

### Search by Category

Users can search their expenses by category.

The search is case-insensitive and supports partial matches.

For example, searching for:

```text
food
```

can find categories such as:

```text
Food
FOOD
Fast Food
```

The application also calculates the total amount of the matching expenses.

---

### Search by Description

Users can search expenses using their descriptions.

The search is case-insensitive and supports partial matches.

For example, searching for:

```text
market
```

can find:

```text
Supermarket
```

The total value of the matching expenses is also calculated and displayed.

---

### CSV Persistence

The application uses CSV files to persist the user's expenses.

Each user has a CSV file named according to the following pattern:

```text
<username>_expenses.csv
```

The files are stored inside the project's `expenses` directory.

For example:

```text
expenses/Artur_expenses.csv
```

The CSV file contains the following fields:

```text
Date,Description,Category,Amount
```

When the application starts, it creates the `expenses` directory if necessary and attempts to load the user's existing CSV file into memory.

This allows previously saved expenses to be immediately available for listing, searching, and analysis.

---

## How to Run

### Requirements

You only need:

* Python 3
* A terminal or command prompt

No third-party Python packages are required.

---

### Running the Program

Clone or download the repository and navigate to the project directory.

Then run:

```bash
python project.py
```

Depending on your operating system, you may need to use:

```bash
python3 project.py
```

The application will ask for the user's name and then load any previously saved expenses associated with that name.

---

## How to Use

After starting the program, the main menu provides the following options:

```text
1. Add expense
2. List expenses
3. Monthly summary
4. Search expenses by category
5. Search expenses by description
6. Save and export expenses to csv
7. Exit
```

### 1. Add Expense

Select option `1` and enter the requested information.

Example:

```text
Date: 2026/10/01
Description: Groceries
Category: Food
Amount: 150,90
```

The application validates the information and adds the expense to the current expense collection.

The user can continue adding expenses or return to the main menu.

---

### 2. List Expenses

Select option `2` to display all expenses currently available.

Previously saved expenses are loaded automatically when the program starts, while newly added expenses are kept in memory until they are saved.

---

### 3. Monthly Summary

Select option `3` and enter a month and year.

For example:

```text
Enter the month and the year (mm/yyyy): 10/2026
```

The program searches the expense collection for matching dates and calculates the total.

---

### 4. Search by Category

Select option `4` and enter a category.

For example:

```text
Enter the category of the expenses: food
```

The program searches for case-insensitive partial matches and displays the matching expenses and their total.

---

### 5. Search by Description

Select option `5` and enter a description.

For example:

```text
Enter the description of the expenses: market
```

The application displays matching expenses and calculates their total.

---

### 6. Save and Export Expenses

Select option `6` to save the current expense collection to the user's CSV file.

If the CSV file does not exist, it is created with the appropriate header.

If the file already exists, it is rewritten using the current contents of the expense collection.

This ensures that the CSV file reflects the current state of the application.

---

### 7. Exit

Select option `7` to close the application.

---

## Project Structure

The project uses the following structure:

```text
personal-finance-analyzer/
│
├── project.py
├── README.md
├── DESIGN.md
└── expenses/
    └── <username>_expenses.csv
```

### `project.py`

Contains the complete application, including:

* The `Expenses` class
* Input validation
* Main program flow
* Command-line menu
* Expense creation
* Expense storage
* CSV reading and writing
* Monthly summaries
* Category searches
* Description searches
* Error handling

### `README.md`

Provides instructions for installing, running, and using the application.

### `DESIGN.md`

Explains the architecture and design decisions behind the application.

### `expenses/`

Stores CSV files containing the user's saved expenses.

The directory is automatically created by the application when it starts.

---

## Technologies and Python Concepts

The project was implemented using Python's standard library and applies several concepts covered by CS50P.

### Python

Python is used for the entire application, including user interaction, data processing, validation, and file management.

### Object-Oriented Programming

The `Expenses` class represents an individual expense containing:

* Date
* Description
* Category
* Amount

### Class Methods

The `Expenses.get()` class method is responsible for collecting and validating expense information before creating an `Expenses` object.

### Regular Expressions

The `re` module is used to validate:

* Usernames
* Monetary amounts
* Date separators

### `datetime`

The `datetime` module is used to:

* Validate dates
* Parse dates
* Compare months and years
* Generate monthly summaries

### CSV

Python's `csv` module is used to store and retrieve expenses.

The project uses:

* `csv.DictReader`
* `csv.DictWriter`

to work with structured expense records.

### File I/O

The project reads and writes CSV files using Python's built-in file handling functionality.

### Exception Handling

The application handles invalid input and file-related errors using Python's exception-handling mechanisms.

Examples include:

* `ValueError`
* `FileNotFoundError`
* `FileExistsError`
* `OSError`

### Data Processing

The application performs filtering, searching, and aggregation operations over the expense collection.

---

## Design Goals

The project was designed around four main goals:

1. **Practicality** — solve a simple real-world problem.
2. **Simplicity** — keep the application understandable and easy to run.
3. **Application of CS50P concepts** — use Python concepts from the course in a meaningful application.
4. **Extensibility** — create a foundation that can be expanded with additional functionality.

The application intentionally avoids external frameworks and dependencies, keeping the focus on Python fundamentals and problem solving.

---

## Current Limitations

The current version is a command-line application and therefore has several limitations.

### Command-Line Interface

The application does not currently provide a graphical or web interface.

### CSV Storage

Expenses are stored in CSV files instead of a database.

This keeps the project simple but would become less suitable as the amount of data and the complexity of operations increase.

### No Authentication

The username determines which CSV file is used, but it does not provide authentication or account security.

### Expense Management

The current version focuses on adding, listing, searching, and analyzing expenses. It does not currently provide dedicated operations for editing or deleting individual expenses.

### No Income Tracking

The application currently focuses exclusively on expenses.

### No Data Visualization

Financial information is presented as text and numerical totals rather than charts or dashboards.

### Floating-Point Monetary Representation

Amounts are stored as floating-point numbers. This is appropriate for the educational scope of the project, but production financial software would generally use a more precise monetary representation.

---

## Possible Future Improvements

The project could be extended in several directions.

Possible improvements include:

* Adding automated tests
* Adding expense editing and deletion
* Adding income tracking
* Adding budget management
* Improving monetary formatting
* Adding expense sorting
* Adding graphical data visualization
* Using Pandas for more advanced data analysis
* Migrating from CSV to SQLite
* Creating a graphical user interface
* Creating a web-based version
* Adding more detailed financial reports

These improvements are outside the scope of the current CS50P implementation but provide possible directions for future development.

---

## Learning Outcomes

Developing this project provided practical experience with:

* Python programming
* Functions and modular design
* Classes and objects
* Class methods
* Regular expressions
* Exception handling
* File input and output
* CSV processing
* Date and time manipulation
* Data validation
* Searching and filtering
* Numerical calculations
* Command-line application design

The project also provided an opportunity to combine these concepts into a single application with persistent data rather than using them only in isolated exercises.

---

## Author

**Artur Mota**

Systems Development student interested in Python, data analysis, and software development.

This project was developed as part of my studies in **CS50's Introduction to Programming with Python (CS50P)**.

---

## License

This project is intended primarily as an educational and portfolio project.

If you reuse or modify this project, please provide appropriate attribution to the original author.
