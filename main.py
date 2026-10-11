
import json
from pathlib import Path
from datetime import date


DATA_FILE = Path("expenses.json")


def load_expenses():
    """Load saved expenses from the JSON file."""

    if not DATA_FILE.exists():
        return []

    try:
        with DATA_FILE.open("r", encoding="utf-8") as file:
            expenses = json.load(file)

        if not isinstance(expenses, list):
            print("The expense file has an invalid format.")
            return []

        return [
            expense for expense in expenses
            if isinstance(expense, dict)
            and isinstance(expense.get("id"), int)
            and isinstance(expense.get("amount"), (int, float))
            and not isinstance(expense.get("amount"), bool)
            and expense.get("amount") >= 0
            and isinstance(expense.get("title"), str)
            and isinstance(expense.get("category"), str)
        ]

    except (OSError, json.JSONDecodeError) as error:
        print(f"Could not load expenses: {error}")
        return []


def save_expenses(expenses):
    """Save all expenses to the JSON file."""

    try:
        with DATA_FILE.open("w", encoding="utf-8") as file:
            json.dump(
                expenses,
                file,
                ensure_ascii=False,
                indent=4
            )

        return True

    except OSError as error:
        print(f"Could not save expenses: {error}")
        return False


def get_next_id(expenses):
    """Return the next available expense ID."""

    if not expenses:
        return 1

    return max(expense["id"] for expense in expenses) + 1


def add_expense(expenses):
    """Ask for expense details and add a new record."""

    title = input("Expense title: ").strip()

    if not title:
        print("Title cannot be empty.")
        return

    try:
        amount = float(input("Amount: ").strip())

        if not 0 < amount < float("inf"):
            print("Amount must be a positive, finite number.")
            return

    except ValueError:
        print("Please enter a valid number.")
        return

    category = input("Category: ").strip()

    if not category:
        print("Category cannot be empty.")
        return

    expense = {
        "id": get_next_id(expenses),
        "title": title,
        "amount": amount,
        "category": category,
        "date": date.today().isoformat()
    }

    expenses.append(expense)

    if save_expenses(expenses):
        print("Expense added successfully.")
    else:
        expenses.pop()


def show_expenses(expenses):
    """Display all saved expenses."""

    if not expenses:
        print("No expenses found.")
        return

    print("\nYour expenses")
    print("-" * 58)

    for expense in expenses:
        print(
            f"ID: {expense['id']} | "
            f"{expense['date']} | "
            f"{expense['title']} | "
            f"{expense['category']} | "
            f"{expense['amount']:,.2f}"
        )

    print("-" * 58)


def show_total(expenses):
    """Calculate and display the total amount spent."""

    total = sum(expense["amount"] for expense in expenses)

    print(f"Total expenses: {total:,.2f}")


def filter_by_category(expenses):
    """Display expenses belonging to a selected category."""

    category = input("Enter category: ").strip().casefold()

    if not category:
        print("Category cannot be empty.")
        return

    matching_expenses = [
        expense for expense in expenses
        if expense["category"].casefold() == category
    ]

    if not matching_expenses:
        print("No expenses found in this category.")
        return

    show_expenses(matching_expenses)

    category_total = sum(
        expense["amount"] for expense in matching_expenses
    )

    print(f"Category total: {category_total:,.2f}")


def show_categories(expenses):
    """Display each category once."""

    categories = sorted({
        expense["category"] for expense in expenses
    }, key=str.casefold)

    if not categories:
        print("No categories found.")
        return

    print("\nCategories:")

    for category in categories:
        print(f"- {category}")


def delete_expense(expenses):
    """Delete an expense using its ID."""

    if not expenses:
        print("No expenses to delete.")
        return

    try:
        expense_id = int(input("Enter expense ID to delete: ").strip())
    except ValueError:
        print("Please enter a valid ID.")
        return

    for index, expense in enumerate(expenses):
        if expense["id"] == expense_id:
            removed_expense = expenses.pop(index)

            if save_expenses(expenses):
                print(f"Deleted: {removed_expense['title']}")
            else:
                expenses.insert(index, removed_expense)

            return

    print("No expense found with that ID.")


def show_menu():
    """Print the main menu."""

    print("\nExpense Tracker")
    print("-" * 26)
    print("1. Add expense")
    print("2. Show all expenses")
    print("3. Show total expenses")
    print("4. Filter by category")
    print("5. Show categories")
    print("6. Delete expense")
    print("7. Exit")


def main():
    expenses = load_expenses()

    print("Welcome to Expense Tracker!")

    while True:
        show_menu()
        choice = input("Choose an option: ").strip()

        if choice == "1":
            add_expense(expenses)

        elif choice == "2":
            show_expenses(expenses)

        elif choice == "3":
            show_total(expenses)

        elif choice == "4":
            filter_by_category(expenses)

        elif choice == "5":
            show_categories(expenses)

        elif choice == "6":
            delete_expense(expenses)

        elif choice == "7":
            print("Goodbye!")
            break

        else:
            print("Invalid option. Choose a number from 1 to 7.")


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\nProgram stopped.")
