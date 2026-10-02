# Personal Finance Analyzer

#### Video Demo: [TODO: Add YouTube link here]

#### Description:

Personal Finance Analyzer is a command-line application written in Python that allows users to record, store, search, and analyze their personal expenses.

This project was developed as my final project for **CS50's Introduction to Programming with Python (CS50P)**. The main goal was to apply the programming concepts learned throughout the course to a practical problem while building a complete, functional Python application from scratch.

The application focuses on managing expenses through a simple command-line interface. Users can enter expenses with a date, description, category, and amount, save their expenses to a CSV file, list previously saved expenses, search for expenses, and calculate the total expenses for a specific month.

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

The program validates the date and amount before adding an expense to the current session.

Dates can be entered using common separators such as `/`, `-`, `\`, or `,`, while the application internally stores dates using the `YYYY/MM/DD` format.

Amounts can use either a period or comma as the decimal separator. For example:

```text
25.90
25,90
```

The program also rejects invalid monetary formats and symbols.

---

### List Saved Expenses

The application can read the user's CSV file and display all previously saved expenses.

Each expense is displayed with its:

```text
Date
Description
Category
Amount
```

If no CSV file exists for the user, the application informs them that the file could not be found.

---

### Monthly Summary

Users can enter a month and year to find all expenses recorded during that period.

The application accepts:

```text
10/2026
Oct/2026
October/2026
```

The program then displays the matching expenses and calculates their total amount.

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

Users can search their saved expenses by category.

The search is case-insensitive and supports partial matches.

For example, searching for:

```text
food
```

can find an expense categorized as:

```text
Food
```

The application also calculates the total value of the matching expenses.

---

### Search by Description

Users can search expenses using their descriptions.

Like the category search, this search is case-insensitive and supports partial matches.

For example, searching for:

```text
market
```

can find:

```text
Supermarket
```

The total amount of all matching expenses is also displayed.

---

### CSV Persistence

Expenses are stored in CSV files named according to the user's name.

For example:

```text
Artur_expenses.csv
```

The CSV file contains the following fields:

```text
Date,Description,Category,Amount
```

CSV was chosen because it is a simple, human-readable format that is well suited to a small command-line application and can also be opened using spreadsheet software.

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

The program will ask for the user's name and then display the main menu.

---

## How to Use

After starting the program, the main menu displays the following options:

```text
1. Add expense
2. List expenses
3. Monthly summary
4. Search expenses by category
5. Search expenses by description
6. Export expenses to csv
7. Exit
```

### Example Workflow

A typical session can look like this:

```text
Enter your name: Artur

Hello, Artur!

1. Add expense
2. List expenses
3. Monthly summary
4. Search expenses by category
5. Search expenses by description
6. Export expenses to csv
7. Exit
```

The user can select option `1` and enter an expense:

```text
Date: 2026/10/01
Description: Groceries
Category: Food
Amount: 150,90
```

The application converts the comma decimal separator into a period and stores the amount as a numeric value.

The user can then add additional expenses or return to the main menu.

When the user selects option `6`, the current session's expenses are written to the user's CSV file.

---

## Project Structure

The project currently contains the following main source file:

```text
personal-finance-analyzer/
│
├── project.py
├── README.md
└── DESIGN.md
```

### `project.py`

Contains the complete application, including:

* The `Expenses` class
* User input and validation
* Main menu
* Expense creation
* CSV reading and writing
* Monthly summaries
* Category searches
* Description searches
* Error handling

### `README.md`

Provides instructions for installing, running, and using the application.

### `DESIGN.md`

Explains the technical architecture of the application and the reasoning behind its main design decisions.

---

## Technologies and Python Concepts

The project was intentionally implemented using Python's standard library so that the application could focus on the programming concepts covered by CS50P.

### Python

The application uses Python for all application logic and user interaction.

### Object-Oriented Programming

The `Expenses` class represents an expense as an object containing:

* Date
* Description
* Category
* Amount

This provides a structured representation of the data being processed by the application.

### Regular Expressions

The `re` module is used to validate user input.

Regular expressions are used to validate:

* User names
* Monetary amounts
* Date separators

### `datetime`

The `datetime` module is used to:

* Parse dates
* Validate dates
* Compare months and years
* Generate monthly summaries

### CSV

Python's `csv` module is used to persist expenses in a structured text format.

The application uses `csv.DictReader` and `csv.DictWriter` to read and write records using field names.

### Exception Handling

The application handles invalid user input and file-related errors using Python's exception-handling mechanisms.

Examples include:

* `ValueError`
* `FileNotFoundError`
* `FileExistsError`
* `OSError`

### File I/O

The application reads from and writes to CSV files using Python's built-in file handling functionality.

---

## Design Goals

The project was designed around four main goals:

1. **Practicality** — solve a simple real-world problem.
2. **Simplicity** — keep the application understandable and easy to run.
3. **Application of CS50P concepts** — use the Python concepts taught throughout the course in a meaningful way.
4. **Extensibility** — provide a foundation that could later be expanded with additional functionality.

The project deliberately avoids unnecessary frameworks and external dependencies. This keeps the application focused on Python fundamentals and makes it easy for users to run locally.

---

## Current Limitations

The current version is intentionally a small command-line application and has some limitations.

### Command-Line Interface

The application does not currently provide a graphical or web interface.

### CSV Storage

Expenses are stored in CSV files rather than a database. This is appropriate for the current scope, but a database would become more suitable for a larger application.

### Session-Based Expense Buffer

New expenses are kept in memory until the user chooses the CSV export option. Therefore, newly added expenses are not available to the listing and search functions until they have been saved to the CSV file.

### No Authentication

The username is used to determine the CSV filename, but the application does not provide authentication or user accounts.

### No Visualization

The current version provides textual summaries but does not generate charts or graphical reports.

---

## Possible Future Improvements

The project could be extended in several directions.

Possible improvements include:

* Adding automated tests
* Adding input validation for descriptions and categories
* Improving the formatting of monetary values
* Adding expense editing and deletion
* Adding income tracking
* Adding budget limits
* Adding graphical data visualization
* Using Pandas for more advanced data analysis
* Migrating from CSV to SQLite
* Creating a graphical user interface
* Creating a web-based version
* Adding more detailed financial reports

These improvements are outside the scope of the current CS50P implementation but could serve as possible future iterations of the project.

---

## Learning Outcomes

Developing this project helped reinforce several Python programming concepts, particularly:

* Functions and modular program design
* Classes and objects
* Class methods
* Regular expressions
* Exception handling
* File input and output
* CSV processing
* Date and time manipulation
* Loops and conditionals
* Data validation
* Searching and filtering data
* Command-line application design

More importantly, the project provided an opportunity to combine these concepts into a single application rather than practicing them independently.

---

## Author

**Artur Mota**

Computer Science / Systems Development student interested in Python, data analysis, and software development.

This project was developed as part of my studies in **CS50's Introduction to Programming with Python (CS50P)**.

---

## License

This project is intended primarily as an educational and portfolio project.

If you reuse or modify this project, please provide appropriate attribution to the original author.
