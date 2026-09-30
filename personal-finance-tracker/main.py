import tracker
import savings
import visualization
import database
from utils import CancelInput

MENU = [
    ("Add Income", tracker.add_income),
    ("Add Expense", tracker.add_expense),
    ("View Summary", tracker.view_summary),
    ("View Transactions", tracker.view_transactions),
    ("Delete Transaction", tracker.delete_transaction),
    ("Set Savings Goal", savings.set_goal),
    ("Visualize Spending", visualization.visualize_data),
    ("Export to CSV", tracker.export_csv),
]
EXIT_OPTION = str(len(MENU) + 1)


def main_menu():
    while True:
        print("\n--- Personal Finance Tracker ---")
        for i, (label, _) in enumerate(MENU, 1):
            print(f"{i}. {label}")
        print(f"{EXIT_OPTION}. Exit")

        choice = input("Choose an option: ").strip()

        if choice == EXIT_OPTION:
            print("Exiting... Goodbye!")
            break
        if choice.isdigit() and 1 <= int(choice) <= len(MENU):
            try:
                MENU[int(choice) - 1][1]()
            except CancelInput:
                print("Cancelled. Returning to main menu.")
        else:
            print(f"Invalid option. Please enter a number from 1 to {EXIT_OPTION}.")


if __name__ == "__main__":
    database.initialize_database()
    try:
        main_menu()
    except (KeyboardInterrupt, EOFError):
        print("\nExiting... Goodbye!")