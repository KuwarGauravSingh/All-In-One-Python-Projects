import csv
import os
from database import get_connection, BASE_DIR
import savings
from utils import (prompt_amount, prompt_text, prompt_date, prompt_choice,
                   confirm, money)

INCOME_CATEGORIES = ["Salary", "Freelance", "Business", "Investments", "Gift", "Other"]
EXPENSE_CATEGORIES = ["Rent", "Groceries", "Food & Dining", "Transport", "Utilities",
                      "Shopping", "Health", "Entertainment", "Education", "Travel", "Other"]


def _totals(cursor):
    cursor.execute("SELECT SUM(amount) FROM transactions WHERE type = 'Income'")
    income = cursor.fetchone()[0] or 0.0
    cursor.execute("SELECT SUM(amount) FROM transactions WHERE type = 'Expense'")
    expenses = cursor.fetchone()[0] or 0.0
    return income, expenses


def _add_transaction(kind, categories):
    print(f"\n--- Add {kind} ---")
    category = prompt_choice(f"Select {kind.lower()} category", categories)
    amount = prompt_amount("Enter amount")
    description = prompt_text("Description (optional)", allow_empty=True)
    tx_date = prompt_date("Date [Enter = today, or YYYY-MM-DD]")

    print(f"\n{kind}: {money(amount)} | {category} | {tx_date} | {description or '-'}")
    if not confirm("Save this entry?"):
        print("Entry discarded.")
        return

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO transactions (type, category, amount, date, description) "
        "VALUES (?, ?, ?, ?, ?)",
        (kind, category, amount, tx_date, description),
    )
    conn.commit()
    income, expenses = _totals(cursor)
    conn.close()

    print(f"{kind} added successfully! Current balance: {money(income - expenses)}")


def add_income():
    _add_transaction("Income", INCOME_CATEGORIES)


def add_expense():
    _add_transaction("Expense", EXPENSE_CATEGORIES)


def view_summary():
    conn = get_connection()
    cursor = conn.cursor()

    total_income, total_expenses = _totals(cursor)
    balance = total_income - total_expenses

    cursor.execute(
        "SELECT SUM(amount) FROM transactions WHERE type = 'Income' "
        "AND substr(date, 1, 7) = strftime('%Y-%m', 'now', 'localtime')")
    month_income = cursor.fetchone()[0] or 0.0
    cursor.execute(
        "SELECT SUM(amount) FROM transactions WHERE type = 'Expense' "
        "AND substr(date, 1, 7) = strftime('%Y-%m', 'now', 'localtime')")
    month_expenses = cursor.fetchone()[0] or 0.0

    cursor.execute(
        "SELECT category, SUM(amount) AS total FROM transactions WHERE type = 'Expense' "
        "GROUP BY category ORDER BY total DESC LIMIT 1")
    top = cursor.fetchone()
    conn.close()

    print("\n=========== Summary ===========")
    print(f"Total Income:    {money(total_income)}")
    print(f"Total Expenses:  {money(total_expenses)}")
    print(f"Balance:         {money(balance)}")
    if total_income > 0:
        print(f"Savings Rate:    {balance / total_income * 100:.1f}%")

    print("\n--- This Month ---")
    print(f"Income:          {money(month_income)}")
    print(f"Expenses:        {money(month_expenses)}")
    print(f"Net:             {money(month_income - month_expenses)}")

    if top:
        share = top[1] / total_expenses * 100 if total_expenses else 0
        print(f"\nTop spending category: {top[0]} ({money(top[1])}, {share:.1f}% of expenses)")

    savings.track_savings_progress(balance)


def _print_rows(rows):
    if not rows:
        print("No transactions found.")
        return
    print(f"\n{'ID':<5}{'Date':<12}{'Type':<9}{'Category':<16}{'Amount':>14}  Description")
    print("-" * 78)
    for tx_id, tx_type, category, amount, tx_date, description in rows:
        print(f"{tx_id:<5}{tx_date:<12}{tx_type:<9}{category[:15]:<16}"
              f"{amount:>14,.2f}  {description or ''}")


def _fetch_transactions(where="", limit=None):
    query = ("SELECT id, type, category, amount, substr(date, 1, 10), description "
             f"FROM transactions {where} ORDER BY date DESC, id DESC")
    if limit:
        query += f" LIMIT {int(limit)}"
    conn = get_connection()
    rows = conn.execute(query).fetchall()
    conn.close()
    return rows


def view_transactions():
    print("\n--- View Transactions ---")
    print("1. Last 10 transactions")
    print("2. All transactions")
    print("3. Income only")
    print("4. Expenses only")
    choice = input("Select an option (1-4): ").strip()

    if choice == "1":
        _print_rows(_fetch_transactions(limit=10))
    elif choice == "2":
        _print_rows(_fetch_transactions())
    elif choice == "3":
        _print_rows(_fetch_transactions("WHERE type = 'Income'"))
    elif choice == "4":
        _print_rows(_fetch_transactions("WHERE type = 'Expense'"))
    else:
        print("Invalid choice.")


def delete_transaction():
    print("\n--- Delete Transaction ---")
    rows = _fetch_transactions(limit=10)
    _print_rows(rows)
    if not rows:
        return

    raw = prompt_text("Enter the ID to delete")
    if not raw.isdigit():
        print("ID must be a number.")
        return

    conn = get_connection()
    row = conn.execute("SELECT type, category, amount FROM transactions WHERE id = ?",
                       (int(raw),)).fetchone()
    if not row:
        conn.close()
        print("No transaction with that ID.")
        return

    if confirm(f"Delete {row[0]} '{row[1]}' of {money(row[2])}?", default=False):
        conn.execute("DELETE FROM transactions WHERE id = ?", (int(raw),))
        conn.commit()
        print("Transaction deleted.")
    else:
        print("Cancelled.")
    conn.close()


def export_csv():
    rows = _fetch_transactions()
    if not rows:
        print("Nothing to export yet.")
        return
    folder = os.path.join(BASE_DIR, "exports")
    os.makedirs(folder, exist_ok=True)
    path = os.path.join(folder, "transactions.csv")
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["ID", "Type", "Category", "Amount", "Date", "Description"])
        writer.writerows(rows)
    print(f"Exported {len(rows)} transactions to {path}")