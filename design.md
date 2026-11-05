# Personal Finance Analyzer — Design Document

## Overview

Personal Finance Analyzer is a command-line Python application designed to help users record, store, search, and analyze personal expenses.

The project was developed as a final project for **CS50's Introduction to Programming with Python (CS50P)**. Its purpose is to combine multiple Python programming concepts into a single practical application.

The application allows users to create expenses, maintain them in memory during execution, persist them to CSV, reload previously saved expenses when the program starts, search by category or description, and calculate monthly totals.

The project intentionally uses only Python's standard library. This keeps the application lightweight while allowing the implementation to focus on concepts such as functions, classes, regular expressions, exception handling, file I/O, CSV processing, and date manipulation.

---

## Problem and Scope

Managing personal expenses can be done using spreadsheets, notes, or financial applications. However, these solutions can be unnecessarily complex for someone who wants a small tool while also practicing programming.

The goal of this project is not to replace complete financial management software. Instead, it provides a focused command-line application capable of performing fundamental expense-management operations.

The application's main responsibilities are:

1. Collecting and validating expense information.
2. Representing expenses as structured data.
3. Loading previously saved expenses from CSV.
4. Maintaining the current expense collection in memory.
5. Filtering and analyzing expenses.
6. Saving the current expense collection back to CSV.

The project does not currently include authentication, a database, a graphical interface, network functionality, or advanced financial analysis.

Keeping the scope limited was intentional. The project focuses on applying the Python concepts learned through CS50P while maintaining a codebase that is understandable and manageable.

---

## Program Architecture

The application is organized around one main class and several functions responsible for different operations.

At a high level, the program follows this flow:

```text
User
 │
 ▼
main()
 │
 ├── Validate username
 │
 ├── Create expenses directory
 │
 ├── Load existing CSV
 │       │
 │       ▼
 │   user_expenses
 │
 ▼
menu()
 │
 ├── add_expense()
 │       │
 │       ▼
 │   Expenses.get()
 │       │
 │       ▼
 │   user_expenses
 │
 ├── list_expenses()
 │       │
 │       ▼
 │   user_expenses
 │
 ├── monthly_summary()
 │       │
 │       ▼
 │   user_expenses
 │
 ├── search_expenses_by_category()
 │       │
 │       ▼
 │   user_expenses
 │
 ├── search_expenses_description()
 │       │
 │       ▼
 │   user_expenses
 │
 └── export_csv()
         │
         ▼
      CSV file
```

The application starts with `main()`.

The user provides a name, which is validated before being used to identify the user's expense file.

The program then creates the `expenses` directory if necessary and attempts to load the corresponding CSV file.

The contents of the CSV are stored in the global `user_expenses` list.

After initialization, the `menu()` function controls the rest of the application.

---

## Program Initialization

The `main()` function is responsible for preparing the application before the menu is displayed.

First, the username is requested:

```python
username = input("\nEnter your name: ").strip()
```

The username is then validated using a regular expression.

After validation, the application creates the storage directory:

```python
os.makedirs("expenses", exist_ok=True)
```

The `exist_ok=True` argument means that the program does not fail if the directory already exists.

The application then attempts to load the user's CSV file.

Each existing row is appended to:

```python
user_expenses
```

If the file does not exist, the `FileNotFoundError` is intentionally ignored because this simply means that the user does not have previously saved expenses.

This initialization design means that all previously saved expenses become available immediately after the program starts.

---

## The `Expenses` Class

The `Expenses` class represents a single expense.

Each instance contains:

```text
expense_date
description
category
amount
```

The constructor receives these values and stores them as attributes.

The class also contains the `get()` class method.

The method is responsible for collecting information interactively from the user, validating it, converting it to the appropriate format, and returning an `Expenses` object.

For example:

```python
expenses = Expenses.get()
```

creates an expense object when valid information is provided.

---

## Why Use a Class?

A class was chosen because an expense is a natural entity containing multiple related values.

Instead of passing four independent values throughout the program, the `Expenses` class groups those values into a single object.

For example:

```python
expenses.expense_date
expenses.description
expenses.category
expenses.amount
```

This provides a clear representation of what constitutes an expense.

The class also demonstrates object-oriented programming concepts covered in CS50P.

The `get()` class method further separates the process of obtaining and validating expense information from the rest of the application.

---

## Input Validation

Input validation is an important part of the application because the program receives information directly from users.

The application validates usernames, dates, and monetary values.

### Username Validation

The username is checked using:

```python
re.fullmatch(r"[\w -]+", username)
```

This allows letters, numbers, underscores, spaces, and hyphens.

The purpose is to prevent arbitrary characters from being used when constructing the CSV filename.

For example:

```text
Artur
Artur Mota
Artur-Mota
```

are valid examples.

---

### Date Validation

The application accepts multiple date separators.

Before parsing the date, the input is normalized:

```python
re.sub(r"\s*[-/\\,]\s*", "/", ...)
```

This allows inputs such as:

```text
2026/10/01
2026-10-01
2026\10\01
2026,10,01
```

to be converted into a common representation.

The normalized value is then passed to:

```python
datetime.strptime(expense_date, "%Y/%m/%d")
```

This validates both the structure and the actual calendar date.

The resulting `datetime` object is retained by the expense object and later formatted as `YYYY/MM/DD` when stored.

---

### Amount Validation

The amount is first normalized by replacing commas with periods.

A regular expression then verifies that the value contains either:

```text
whole number
```

or:

```text
whole number + decimal point + one or two decimal digits
```

Examples of valid values include:

```text
10
10.5
10.50
10,50
```

After validation, the value is converted to a `float`.

This conversion allows the application to perform calculations when generating totals.

---

## Data Storage

The project uses a combination of **in-memory storage and CSV persistence**.

The global list:

```python
user_expenses = []
```

contains the expenses currently loaded into the application.

When the program starts, previously saved CSV records are loaded into this list.

When the user adds a new expense, its data is converted into a dictionary and appended to the same list.

This means that all listing, searching, and analysis operations work against one consistent collection during the program's execution.

---

## Why Use a Global Expense Collection?

The `user_expenses` list acts as the application's current data store while it is running.

This approach allows different functions to access the same expense collection without repeatedly opening and reading the CSV file.

For example:

```text
CSV
 │
 ▼
user_expenses
 │
 ├── List
 ├── Monthly summary
 ├── Category search
 └── Description search
```

This simplifies the implementation and avoids repeated file operations for every query.

The trade-off is that the application currently keeps the complete expense collection in memory, which would become less appropriate for a very large dataset.

For the scale of this educational project, the approach is sufficient.

---

## CSV Persistence

CSV is used as the persistent storage format.

Each user has a file following this pattern:

```text
expenses/<username>_expenses.csv
```

For example:

```text
expenses/Artur_expenses.csv
```

The CSV contains four fields:

```text
Date
Description
Category
Amount
```

These fields are defined in:

```python
FIELDNAMES = ["Date", "Description", "Category", "Amount"]
```

The program uses `csv.DictReader` to load existing records and `csv.DictWriter` to save records.

---

## Why CSV?

CSV was chosen because it provides a simple persistence mechanism without requiring external packages or database configuration.

It also has several practical advantages for this project:

* It is human-readable.
* It can be opened using spreadsheet applications.
* It is supported directly by Python's standard library.
* It is sufficient for a small dataset.
* It keeps the project focused on Python fundamentals.

A database such as SQLite would provide stronger querying and data-management capabilities, but it would also introduce additional concepts that are unnecessary for the current scope.

---

## Saving and Exporting

The `export_csv()` function is responsible for persisting the current contents of `user_expenses`.

If the user's CSV file does not exist, the program opens it using:

```python
"x"
```

The header is then written before the expenses.

If the file already exists, the program opens it using:

```python
"w"
```

and rewrites the file from the current contents of `user_expenses`.

This design means that the saved CSV represents the current state of the in-memory expense collection.

After a successful save, the list is cleared:

```python
user_expenses.clear()
```

This prepares the list for the next session of expense additions.

Because previously saved expenses are loaded into the list when the program starts, rewriting the file does not intentionally discard existing records.

---

## Listing Expenses

The `list_expenses()` function displays the expenses contained in `user_expenses`.

Rather than opening the CSV file again, it works directly with the in-memory collection.

For each expense, the function iterates through its dictionary entries and displays the field name and value.

This keeps listing consistent with the data currently being used by the search and summary functions.

---

## Monthly Summary

The `monthly_summary()` function allows the user to select a month and year.

Three input formats are accepted:

```text
%m/%Y
%b/%Y
%B/%Y
```

Examples include:

```text
10/2026
Oct/2026
October/2026
```

Each expense date is converted into a `datetime` object.

The month and year are then compared with the selected month and year.

When a matching expense is found:

1. The expense is displayed.
2. `found` is set to `True`.
3. Its amount is added to the total.

The separate `found` Boolean is important because the total amount should not be used to determine whether results exist. A matching expense could theoretically have a value of zero.

---

## Search Functionality

The application provides two search functions:

```text
search_expenses_by_category()
search_expenses_description()
```

Both operate on `user_expenses`.

### Category Search

The category search is case-insensitive and supports partial matches.

For example:

```python
if category.lower() in expense["Category"].lower():
```

allows a query such as:

```text
food
```

to match:

```text
Food
Fast Food
FOOD
```

The amounts of matching expenses are also accumulated.

---

### Description Search

The description search follows the same approach.

For example:

```python
if description.lower() in expense["Description"].lower():
```

allows a partial description to find matching records.

The total amount of the matching expenses is calculated and displayed.

---

## Error Handling

The application uses exception handling to deal with invalid input and file-related conditions.

### `ValueError`

Used when invalid date information cannot be converted into a valid `datetime`.

### `FileNotFoundError`

Used during application initialization when the user's CSV file does not yet exist.

This exception is intentionally ignored because a missing file simply indicates that there are no previously saved expenses.

### `FileExistsError`

Handled by `export_csv()` when the user's CSV file already exists.

### `PermissionError` and `OSError`

Handled during CSV saving to prevent the application from reporting a successful save when the operating system does not allow the file operation to complete.

---

## Function Responsibilities

The application separates its responsibilities into several functions.

### `main()`

Initializes the application, validates the username, creates the storage directory, loads existing expenses, and starts the menu.

### `menu()`

Displays the available operations and directs the user to the selected function.

### `add_expense()`

Obtains new expenses through `Expenses.get()` and adds their data to the in-memory expense collection.

### `list_expenses()`

Displays the expenses currently stored in `user_expenses`.

### `monthly_summary()`

Filters expenses by month and year and calculates the total.

### `search_expenses_by_category()`

Searches expenses using their category.

### `search_expenses_description()`

Searches expenses using their description.

### `export_csv()`

Persists the current expense collection to the user's CSV file.

---

## Design Trade-offs

Several design decisions were made to keep the application appropriate for the project's scope.

### In-Memory Collection + CSV

Using `user_expenses` as the active data collection allows all operations to work with the same dataset.

CSV then provides persistence between program executions.

This is simpler than repeatedly accessing the file for every operation.

### CSV Instead of SQLite

SQLite would be more scalable and provide more advanced querying capabilities, but CSV is sufficient for the current dataset and avoids introducing unnecessary complexity.

### Command-Line Interface

A command-line interface keeps the application focused on Python programming rather than graphical interface development.

It also makes the application simple to run on different systems.

### Standard Library Only

The application does not require third-party packages.

This makes setup straightforward and demonstrates that the project's functionality can be implemented using Python's standard library.

### Rewriting the CSV on Save

The save operation rewrites the CSV based on the current in-memory collection.

This provides a simple way to keep the persistent file synchronized with the application's current state.

---

## Limitations

The current design has several limitations.

### No Database

CSV does not provide the querying, indexing, constraints, and scalability of a database.

### No Authentication

The username identifies a file but does not represent a secure user account.

### No Expense Editing or Deletion

The current interface does not provide dedicated commands for editing or deleting an individual expense.

### No Income Tracking

The application currently handles expenses only.

### No Visualization

The application produces textual results rather than charts or dashboards.

### In-Memory Dataset

All currently loaded expenses are kept in memory. This is appropriate for a small application but would become less efficient with a very large dataset.

### Floating-Point Monetary Values

Amounts are represented using `float`. This is sufficient for the educational purpose of the project, but financial software intended for production use would generally require a more precise approach to monetary values.

---

## Future Improvements

The current architecture provides several possible directions for future development.

### Automated Testing

Automated tests could be added to verify:

* Date validation
* Amount validation
* Expense creation
* Category searches
* Description searches
* Monthly summaries
* CSV persistence

### Expense Editing and Deletion

Additional operations could allow users to modify or remove individual records.

### Income and Balance Tracking

The application could be expanded to record income and calculate balances.

### SQLite

The CSV storage layer could eventually be replaced by SQLite to support more sophisticated queries and data management.

### Data Visualization

Pandas and Matplotlib could be introduced in a future version to generate charts showing spending patterns and category distributions.

### Graphical or Web Interface

The existing application logic could serve as a foundation for a GUI or web application.

---

## Conclusion

Personal Finance Analyzer was designed as a practical application of the Python concepts learned throughout CS50P.

The project combines:

* Object-oriented programming
* Functions
* Class methods
* Regular expressions
* Input validation
* Exception handling
* File I/O
* CSV processing
* Date manipulation
* Searching and filtering
* Numerical calculations
* Command-line application design

The architecture intentionally remains simple. Expenses are represented as objects during creation, maintained in an in-memory collection during execution, and persisted through CSV files.

This approach provides a balance between functionality and simplicity while leaving a clear foundation for future improvements such as automated testing, SQLite storage, data visualization, and a graphical or web interface.
