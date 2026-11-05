# test_project.py
import os
import sys
import csv
from io import StringIO

import pytest
import project


# ---------- Fixtures ----------

@pytest.fixture
def user_input():
    """Sets what input() will receive, one line per answer."""
    original = sys.stdin

    def set_lines(*lines):
        sys.stdin = StringIO("\n".join(lines) + "\n")

    yield set_lines
    sys.stdin = original


@pytest.fixture(autouse=True)
def clear_expenses():
    """Empties the global list before and after every test."""
    project.user_expenses.clear()
    yield
    project.user_expenses.clear()


@pytest.fixture
def temp_dir(tmp_path):
    """Moves into a temporary folder that already contains 'expenses/'."""
    original = os.getcwd()
    os.chdir(tmp_path)
    (tmp_path / "expenses").mkdir()
    yield tmp_path
    os.chdir(original)


def make_expense(date="2024/01/15", description="Lunch", category="Food", amount=10.0):
    return {
        "Date": date,
        "Description": description,
        "Category": category,
        "Amount": amount,
    }


# ---------- Menu ----------

def test_option_7_exits_with_message(user_input):
    user_input("7")

    with pytest.raises(SystemExit) as exc:
        project.menu("ana")

    assert exc.value.code == "Closing..."


def test_invalid_option(user_input, capsys):
    user_input("9", "7")

    with pytest.raises(SystemExit):
        project.menu("ana")

    assert "Invalid option" in capsys.readouterr().out


def test_option_2_without_expenses(user_input, capsys):
    user_input("2", "7")

    with pytest.raises(SystemExit):
        project.menu("ana")

    assert "No expenses found" in capsys.readouterr().out


def test_option_2_lists_expenses(user_input, capsys):
    project.user_expenses.append(make_expense())
    user_input("2", "7")

    with pytest.raises(SystemExit):
        project.menu("ana")

    output = capsys.readouterr().out
    assert "Description: Lunch" in output
    assert "Category: Food" in output


def test_option_1_adds_expense(user_input):
    # option 1, date, description, category, amount, "n" (no more expenses), exit
    user_input("1", "2024/01/15", "Lunch", "Food", "25,50", "n", "7")

    with pytest.raises(SystemExit):
        project.menu("ana")

    assert project.user_expenses == [
        {"Date": "2024/01/15", "Description": "Lunch", "Category": "Food", "Amount": 25.5}
    ]


def test_option_3_monthly_summary(user_input, capsys):
    project.user_expenses.append(make_expense("2024/01/10", amount=10))
    project.user_expenses.append(make_expense("2024/01/20", amount=20.5))
    project.user_expenses.append(make_expense("2024/02/05", amount=99))  # another month
    user_input("3", "01/2024", "7")

    with pytest.raises(SystemExit):
        project.menu("ana")

    output = capsys.readouterr().out
    assert "Total expenses: 30.5" in output
    assert "99" not in output


def test_option_4_search_by_category(user_input, capsys):
    project.user_expenses.append(make_expense(category="Food", amount=10))
    project.user_expenses.append(make_expense(category="Transport", amount=5))
    user_input("4", "food", "7")

    with pytest.raises(SystemExit):
        project.menu("ana")

    output = capsys.readouterr().out
    assert "Total expenses in food: 10.0" in output
    assert "Transport" not in output


def test_option_5_search_by_description(user_input, capsys):
    project.user_expenses.append(make_expense(description="Pizza night", amount=40))
    project.user_expenses.append(make_expense(description="Bus ticket", amount=5))
    user_input("5", "pizza", "7")

    with pytest.raises(SystemExit):
        project.menu("ana")

    output = capsys.readouterr().out
    assert "Total expenses in pizza: 40.0" in output
    assert "Bus ticket" not in output


def test_option_6_exports_csv(user_input, capsys, temp_dir):
    project.user_expenses.append(make_expense())
    user_input("6", "7")

    with pytest.raises(SystemExit):
        project.menu("ana")

    file_path = temp_dir / "expenses" / "ana_expenses.csv"
    assert file_path.exists()

    with open(file_path, newline="") as file:
        rows = list(csv.DictReader(file))
    assert rows[0]["Description"] == "Lunch"

    assert "exported successfully to ana_expenses.csv" in capsys.readouterr().out
    assert project.user_expenses == []  # list is cleared after exporting


# ---------- Expenses.get ----------

def test_get_with_valid_data(user_input):
    user_input("2024-1-5", "Coffee", "Food", "3,5")

    expense = project.Expenses.get()

    assert expense.expense_date.strftime("%Y/%m/%d") == "2024/01/05"
    assert expense.description == "Coffee"
    assert expense.amount == 3.5


def test_get_with_invalid_amount(user_input, capsys):
    user_input("2024/01/15", "Coffee", "Food", "abc")

    assert project.Expenses.get() is None
    assert "Invalid amount" in capsys.readouterr().out


def test_get_with_invalid_date(user_input, capsys):
    user_input("not a date")

    assert project.Expenses.get() is None
    assert "Invalid date" in capsys.readouterr().out


# ---------- monthly_summary ----------

def test_summary_with_invalid_month(user_input, capsys):
    user_input("13/2024")

    project.monthly_summary("ana")

    assert "Invalid month" in capsys.readouterr().out


def test_summary_with_no_expenses_in_month(user_input, capsys):
    project.user_expenses.append(make_expense("2024/01/10"))
    user_input("03/2024")

    project.monthly_summary("ana")

    assert "No expenses found" in capsys.readouterr().out


# ---------- main ----------

def test_main_with_invalid_name(user_input, capsys):
    user_input("invalid/name")

    project.main()

    assert "Invalid name" in capsys.readouterr().out


def test_main_loads_existing_csv(user_input, capsys, temp_dir):
    file_path = temp_dir / "expenses" / "ana_expenses.csv"
    file_path.write_text("Date,Description,Category,Amount\n2024/01/15,Lunch,Food,10.0\n")
    user_input("ana", "7")

    with pytest.raises(SystemExit):
        project.main()

    assert project.user_expenses[0]["Description"] == "Lunch"
    assert "Hello, ana!" in capsys.readouterr().out