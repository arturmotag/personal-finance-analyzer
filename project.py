import sys
import os
import re
import csv
from datetime import datetime

# Base global variables
FIELDNAMES = ["Date", "Description", "Category", "Amount"]
user_expenses = []


# Setting the required expenses information
class Expenses:
    def __init__(self, expense_date, description, category, amount):
        self.expense_date = expense_date
        self.description = description
        self.category = category
        self.amount = amount

    # Initiating the object with the needed information in the right format
        # date can be accepted multiple ways, but will be saved as YYYY/MM/DD
        # amount will only be accepted as x.xx or x
    @classmethod
    def get(cls):
        try:
            expense_date = re.sub(r"\s*[-/\\,]\s*", "/", input("Date: ").strip())
            expense_date = datetime.strptime(expense_date, "%Y/%m/%d")
            description = input("Description: ")
            category = input("Category: ")
            amount = input("Amount: ").replace(",", ".").strip()
            if not re.fullmatch(r"\d+((\.)\d{1,2})?", amount):
                print("\nInvalid amount. Try again (do not include symbols).\n")
                return None
            amount = float(amount)
        except ValueError:
            print("\nInvalid date. Enter a date in YYYY/MM/DD format.\n")
            return None
        else:
            return cls(expense_date, description, category, amount)


def main():
    # Receiving username to create or access expense file
    username = input("\nEnter your name: ").strip()

    # Username must only accept characters permitted to name a file
    if not re.fullmatch(r"[\w -]+", username):
        print("Invalid name\n")
        return None

    os.makedirs("expenses", exist_ok=True)

    try:
        with open("expenses/"+ username + "_expenses.csv", "r", newline="") as file:
            reader = csv.DictReader(file)

            for row in reader:
                user_expenses.append(row)
    except FileNotFoundError:
        pass

    print(f"Hello, {username}!\n")

    menu(username)


def menu(user):
    while True:
        # Menu with the options the user can access
        print("=" * 40 + "\n" + "PERSONAL FINANCE ANALYSER".center(40) + "\n" + "=" * 40)

        print(
            "1. Add expense\n"
            "2. List expenses\n"
            "3. Monthly summary\n"
            "4. Search expenses by category\n"
            "5. Search expenses by description\n"
            "6. Save and export expenses to csv\n"
            "7. Exit\n"
        )

        option = input("Select an option from the menu above: ")

        # Redirect the user to the option selected
        match option:
            case "1":
                add_expense()
            case "2":
                list_expenses(user)
            case "3":
                monthly_summary(user)
            case "4":
                search_expenses_by_category(user)
            case "5":
                search_expenses_description(user)
            case "6":
                export_csv(user)
            case "7":
                sys.exit("Closing...")
            case _:
                print("Invalid option\n")


# Prompt the user for the required expense information
def add_expense():
    while True:
        expenses = Expenses.get()

        if expenses is None:
            continue

        # Temporarily save the expense information in the global list variable
        user_expenses.append(
            {
                "Date": expenses.expense_date.strftime("%Y/%m/%d"),
                "Description": expenses.description,
                "Category": expenses.category,
                "Amount": expenses.amount,
            }
        )

        # Check if the user is done with adding expenses
        if (
            input(
                "\nDo you want to add another expense? (y to add more/any other key to return to menu): "
            ).strip().lower()!= "y"
        ):
            break


# List previously added expenses to an external csv file
def list_expenses(username):
    print("\n" + "-" * 15 + " RESULTS " + "-" * 15)

    if not user_expenses:
        print("No expenses found\n")
        return

    for expense in user_expenses:
        for key, value in expense.items():
            print(f"{key}: {value}")
        print()


# List previously added expenses of a specific month to an external csv file
def monthly_summary(username):
    month_input = input("Enter the month and the year (mm/yyyy): ").strip()
    print("\n" + "-" * 15 + " RESULTS " + "-" * 15)
    total = 0
    found = False

    # Checking if the month entered is in the right format
    for fmt in ["%m/%Y", "%b/%Y", "%B/%Y"]:
        try:
            month_fmt = datetime.strptime(f"{month_input}", fmt)
            break
        except ValueError:
            continue
    else:
        print("Invalid month. Try again.")
        return

    # Checking expenses in the month the user selected
    for expense in user_expenses:
        expense_date = datetime.strptime(expense["Date"], "%Y/%m/%d")
        if expense_date.month == month_fmt.month and expense_date.year == month_fmt.year:
            found = True
            for key, value in expense.items():
                print(f"{key}: {value}")
            total += float(expense["Amount"])
            print()

    if found == False:
        print("No expenses found\n")
        return

    print(f"Total expenses: {total}\n")


# List previously added expenses of a specific category to an external csv file
def search_expenses_by_category(username):
    category = input("Enter the category of the expenses: ").strip()
    print("\n" + "-" * 15 + " RESULTS " + "-" * 15)
    total = 0
    found = False

    # Checking expenses in the category the user selected
    for expense in user_expenses:
        if category.lower() in expense["Category"].lower():
            found = True
            for key, value in expense.items():
                print(f"{key}: {value}")
            total += float(expense["Amount"])
            print()

    if found == False:
        print("No expenses found\n")
        return

    print(f"Total expenses in {category}: {total}\n")


# List previously added expenses of a specific description to an external csv file
def search_expenses_description(username):
    description = input("Enter the description of the expenses: ").strip()
    print("\n" + "-" * 15 + " RESULTS " + "-" * 15)
    total = 0
    found = False

    for expense in user_expenses:
        if description.lower() in expense["Description"].lower():
            found = True
            for key, value in expense.items():
                print(f"{key}: {value}")
            total += float(expense["Amount"])
            print()

    if found == False:
        print("No expenses found\n")
        return

    print(f"Total expenses in {description}: {total}\n")


# Exporting the user's expenses to a csv file
def export_csv(username):
    try:
        with open("expenses/" + username + "_expenses.csv", "x", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=FIELDNAMES)
            writer.writeheader()
            writer.writerows(user_expenses)
            file_name = os.path.basename(file.name)
    except FileExistsError:
        with open("expenses/" + username + "_expenses.csv", "w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=FIELDNAMES)
            writer.writeheader()
            writer.writerows(user_expenses)
            file_name = os.path.basename(file.name)
    except (PermissionError, OSError):
        print("\nUnable to export expenses.\n")
        return

    print(f"\nExpenses exported successfully to {file_name}!\n")
    user_expenses.clear()


if __name__ == "__main__":
    main()
