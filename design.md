# Personal Finance Analyzer — Design Document

## Overview

Personal Finance Analyzer is a command-line Python application designed to help users record and analyze personal expenses.

The project was developed as a final project for **CS50's Introduction to Programming with Python (CS50P)**. Its purpose is to combine several Python programming concepts into a single practical application rather than implementing them as isolated exercises.

The application allows users to create expenses, temporarily store them during a session, save them to a CSV file, retrieve previously saved expenses, search by category or description, and calculate monthly totals.

The project intentionally uses only Python's standard library. This decision keeps the application lightweight while allowing the implementation to focus on programming fundamentals such as functions, classes, regular expressions, exception handling, file I/O, CSV processing, and date manipulation.

---

## Problem and Scope

Managing small personal expenses can be done with a spreadsheet, notes, or a dedicated financial application. However, these solutions can be unnecessarily complex for someone who simply wants to practice programming while maintaining a basic record of expenses.

The goal of this project is therefore not to compete with complete financial management software. Instead, it provides a small command-line tool capable of handling the fundamental operations required to record and analyze expenses.

The application's scope includes four main responsibilities:

1. Collecting and validating expense information.
2. Temporarily storing expenses during a session.
3. Persisting expenses to CSV files.
4. Reading, filtering, and summarizing saved expenses.

The project does not currently include authentication, a database, a graphical interface, network functionality, or advanced financial analysis.

Keeping the scope limited was an intentional design decision. The project was intended to demonstrate programming knowledge acquired through CS50P while remaining small enough to understand and maintain.

---

## Program Architecture

The application is organized around a collection of functions and one main class.

At a high level, the program follows this flow:

```text
User
 │
 ▼
main()
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
 │   CSV file
 │
 ├── monthly_summary()
 │       │
 │       ▼
 │   CSV file
 │
 ├── search_expenses_by_category()
 │       │
 │       ▼
 │   CSV file
 │
 ├── search_expenses_description()
 │       │
 │       ▼
 │   CSV file
 │
 └── export_csv()
         │
         ▼
      CSV file
```

The program starts with `main()`, which obtains and validates the user's name before passing it to the main menu.

The `menu()` function is responsible for displaying the available operations and dispatching the user's selection to the corresponding function.

This separation prevents the main menu from containing the implementation details of every operation.

---

## The `Expenses` Class

The `Expenses` class represents an individual expense.

An expense contains four attributes:

```text
expense_date
description
category
amount
```

The class is defined in `project.py` and receives these values through its constructor.

The class also contains the `get()` class method, which handles interactive creation of an expense.

The method asks the user for the required values, validates the date and amount, and returns an `Expenses` object when the input is valid.

If the input is invalid, the method returns `None`.

This design keeps the creation and validation of an expense together instead of spreading those responsibilities across multiple functions.

---

## Why Use a Class?

A class was chosen because an expense is a natural real-world entity that contains several related pieces of information.

Without a class, the program could represent an expense using a dictionary from the beginning. However, using the `Expenses` class provides a clear object-oriented representation of an expense and demonstrates the use of classes and class methods covered in CS50P.

For example:

```python
expenses = Expenses.get()
```

creates an object representing the user's expense.

The application can then access:

```python
expenses.expense_date
expenses.description
expenses.category
expenses.amount
```

This makes the relationship between the data and the object explicit.

---

## Input Validation

Input validation is an important part of the application's design because users interact with the program directly through the command line.

The application validates several types of input.

### Date Validation

The entered date is normalized before being passed to `datetime.strptime()`.

The program accepts common separators and converts them to `/`.

For example:

```text
2026-10-01
2026/10/01
2026\10\01
2026,10,01
```

are normalized before being interpreted as a date.

The resulting date is parsed using:

```python
datetime.strptime(expense_date, "%Y/%m/%d")
```

This also ensures that impossible dates are rejected.

---

### Amount Validation

The amount is validated using a regular expression.

The application accepts values such as:

```text
10
10.50
10,50
```

and rejects values containing unsupported symbols or more than two decimal places.

After validation, commas are replaced with periods and the value is converted to a `float`.

This allows the application to perform arithmetic when calculating totals.

---

### Username Validation

The user's name is validated using a regular expression before it is used to construct the CSV filename.

The validation allows letters, numbers, underscores, spaces, and hyphens.

This prevents arbitrary path characters from being included in the generated filename and keeps the filename predictable.

For example:

```text
Artur
Artur Mota
Artur-Mota
```

are valid examples.

---

## Data Storage

The project uses CSV files as its persistent storage mechanism.

Each user's file follows the naming pattern:

```text
<username>_expenses.csv
```

For example:

```text
Artur_expenses.csv
```

The CSV file uses the following fields:

```text
Date
Description
Category
Amount
```

The field names are stored in the `FIELDNAMES` constant.

---

## Why CSV?

CSV was chosen instead of a database for several reasons.

First, CSV is part of Python's standard library, so no external dependencies are necessary.

Second, the amount of data expected by this project is relatively small. A full database system would introduce additional complexity without providing a significant benefit for the current scope.

Third, CSV files are human-readable and can be opened using common spreadsheet applications.

The trade-off is that CSV does not provide the same querying, constraints, indexing, concurrency, and data integrity capabilities that a database such as SQLite would provide.

For this project's scale, the simplicity of CSV outweighs those limitations.

---

## Session Data and Persistence

The program uses the global list:

```python
user_expenses = []
```

as a temporary in-memory buffer.

When a user adds an expense, the expense is converted into a dictionary with the appropriate CSV field names and appended to this list.

For example:

```python
{
    "Date": "2026/10/01",
    "Description": "Groceries",
    "Category": "Food",
    "Amount": 150.0
}
```

The data remains in memory until the user chooses the export option.

At that point, `export_csv()` writes the accumulated records to the user's CSV file and clears the temporary list.

This design separates the process of creating expenses from the process of persisting them.

A consequence of this design is that expenses added during the current session are not available to the CSV-based search and listing functions until they are saved.

This is a known limitation of the current implementation rather than an accidental behavior.

---

## Reading and Writing CSV Data

The `csv.DictWriter` class is used to write dictionaries to CSV files.

When a user's CSV file does not yet exist, the program creates it and writes the header before adding the expenses.

When the file already exists, the program opens it in append mode and adds the new expenses.

The relevant file modes are:

```text
"x"  → create a new file
"a"  → append to an existing file
"r"  → read an existing file
```

`csv.DictReader` is used when retrieving saved data.

Using dictionaries makes the code easier to understand because each value can be accessed using its corresponding field name, such as:

```python
row["Date"]
row["Category"]
row["Amount"]
```

---

## Monthly Summary

The monthly summary function allows the user to select a month and year.

The input is parsed using several accepted formats:

```text
%m/%Y
%b/%Y
%B/%Y
```

This allows inputs such as:

```text
10/2026
Oct/2026
October/2026
```

The program then reads each saved expense and converts its date back into a `datetime` object.

The month and year of each expense are compared with the month and year selected by the user.

When a match is found, the expense is displayed and its amount is added to the running total.

A separate Boolean variable named `found` is used to determine whether any matching expenses were found.

This is preferable to using the total itself to determine whether a result exists because an expense could theoretically have a value of zero.

---

## Search Functionality

The project contains two search operations:

```text
Search by category
Search by description
```

Both searches are case-insensitive.

For example:

```text
food
```

can match:

```text
Food
FOOD
Fast Food
```

The search also supports partial matches because the query is checked using the `in` operator.

For example:

```python
if category.lower() in row["Category"].lower():
```

This provides a more flexible user experience than requiring an exact match.

The matching expenses are displayed and their amounts are accumulated into a total.

---

## Error Handling

The application uses exception handling to deal with invalid input and file-related problems.

For input validation, invalid dates result in a `ValueError`, which is handled by the application.

The application also handles situations where the user's CSV file does not exist using:

```python
FileNotFoundError
```

When saving data, the application handles:

```python
FileExistsError
```

because the file creation mode intentionally requires the file not to already exist.

The application also handles operating-system-level file errors with:

```python
OSError
```

This prevents the program from reporting a successful export when the underlying file operation has failed.

---

## Function Responsibilities

The program uses separate functions for different tasks.

### `main()`

Responsible for starting the application, obtaining the username, validating it, and opening the main menu.

### `menu()`

Displays the available options and routes the user's selection to the appropriate function.

### `add_expense()`

Creates expense objects and adds their data to the temporary session buffer.

### `list_expenses()`

Reads and displays all expenses stored in the user's CSV file.

### `monthly_summary()`

Filters saved expenses by month and year and calculates their total.

### `search_expenses_by_category()`

Searches saved expenses using their category.

### `search_expenses_description()`

Searches saved expenses using their description.

### `export_csv()`

Writes the current session's expenses to the user's CSV file.

This separation makes the program easier to understand and maintain because each function has a relatively focused responsibility.

---

## Design Trade-offs

Several design decisions were made to keep the project within an appropriate scope.

### CSV Instead of SQLite

SQLite would provide stronger data management capabilities, but it would also introduce database-specific concepts that are not necessary for the current version.

CSV provides sufficient persistence for the project's intended scale.

### Command-Line Interface Instead of GUI

A graphical interface could make the application more accessible, but implementing one would shift the focus away from the Python programming concepts being demonstrated.

The command-line interface keeps the project lightweight and allows the core functionality to remain the focus.

### Standard Library Instead of Third-Party Packages

The application does not require external dependencies.

This makes installation simpler and demonstrates that a useful Python application can be built using the standard library.

### Session Buffer Instead of Immediate Persistence

The current design collects expenses in memory and saves them when the user chooses the export option.

This keeps the expense creation workflow simple, but it means that the user must explicitly save the session before the data becomes available to the CSV-based analysis functions.

A future version could persist each expense immediately after it is created.

---

## Limitations

The current design has several limitations.

### No Database

CSV is appropriate for the current scope but does not scale as well as a database.

### No User Authentication

The username identifies the CSV file but does not provide security or authentication.

### No Expense Editing or Deletion

The current application focuses on adding, viewing, searching, and summarizing expenses. It does not currently provide operations for modifying or deleting individual records.

### No Income Tracking

Only expenses are represented.

### No Graphical Analysis

The application provides numerical summaries but does not generate charts or visualizations.

### Session-Based Persistence

New expenses are stored in memory until the user explicitly chooses to save them.

### Floating-Point Monetary Representation

Amounts are currently converted to `float`. For a small educational application this is sufficient for demonstrating arithmetic and data processing, but a production financial application would generally require more careful monetary representation to avoid floating-point precision issues.

---

## Future Improvements

Several improvements could be made while preserving the core architecture.

The first improvement would be to add automated tests for validation, searching, calculations, and file operations. This would make future changes safer and would further demonstrate the testing concepts taught in CS50P.

The storage layer could eventually be migrated from CSV to SQLite. This would make it easier to support operations such as editing, deleting, sorting, and querying large numbers of expenses.

The application could also be extended to track income and calculate additional financial metrics such as balance, spending by category, and budget utilization.

A future data-analysis version could use libraries such as Pandas and Matplotlib to transform the stored expenses into charts and more advanced reports. A graphical or web interface could also be built on top of the same core concepts.

These improvements were intentionally left outside the scope of the current project so that the implementation could remain focused on the Python fundamentals learned in CS50P.

---

## Conclusion

Personal Finance Analyzer was designed as a practical way to bring together the Python concepts learned throughout CS50P.

The project combines object-oriented programming, functions, regular expressions, exception handling, file I/O, CSV processing, date manipulation, input validation, searching, filtering, and numerical calculations in a single application.

The design prioritizes simplicity and clarity over unnecessary complexity. CSV was selected as a lightweight persistence mechanism, the command-line interface keeps the application easy to run, and the program's functionality is divided into focused functions.

Although the current implementation has limitations, its architecture provides a foundation for future versions that could introduce automated testing, SQLite, data visualization, income tracking, and a graphical or web interface.

The project therefore represents not only a final CS50P assignment, but also a starting point for continuing to develop Python and data-analysis skills.
