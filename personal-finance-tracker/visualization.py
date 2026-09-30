import os
import matplotlib.pyplot as plt
from database import get_connection, BASE_DIR
from utils import confirm

CHART_DIR = os.path.join(BASE_DIR, "charts")
DAY = "substr(date, 1, 10)"
MONTH = "substr(date, 1, 7)"


def _query(sql):
    conn = get_connection()
    rows = conn.execute(sql).fetchall()
    conn.close()
    return rows


def _show(filename):
    """Optionally save the current figure as a PNG, then display it."""
    plt.tight_layout()
    if confirm("Save this chart as an image?", default=False):
        os.makedirs(CHART_DIR, exist_ok=True)
        path = os.path.join(CHART_DIR, filename)
        plt.savefig(path, dpi=150)
        print(f"Chart saved to {path}")
    plt.show()


def bar_chart_expense():
    rows = _query("SELECT category, SUM(amount) FROM transactions "
                  "WHERE type = 'Expense' GROUP BY category ORDER BY 2 DESC")
    if not rows:
        print("No expenses recorded yet.")
        return
    categories, amounts = zip(*rows)
    plt.figure(figsize=(9, 5))
    bars = plt.bar(categories, amounts, color="#4C78A8")
    plt.bar_label(bars, fmt="%.0f", padding=2)
    plt.xlabel("Category")
    plt.ylabel("Amount")
    plt.title("Spending by Category")
    plt.xticks(rotation=45, ha="right")
    _show("spending_by_category_bar.png")


def pie_chart_expense():
    rows = _query("SELECT category, SUM(amount) FROM transactions "
                  "WHERE type = 'Expense' GROUP BY category ORDER BY 2 DESC")
    if not rows:
        print("No expenses recorded yet.")
        return
    categories, amounts = zip(*rows)
    plt.figure(figsize=(7, 7))
    plt.pie(amounts, labels=categories, autopct="%1.1f%%", startangle=90)
    plt.title("Spending by Category")
    _show("spending_by_category_pie.png")


def line_chart_expense_over_time():
    rows = _query(f"SELECT {DAY}, SUM(amount) FROM transactions "
                  f"WHERE type = 'Expense' GROUP BY {DAY} ORDER BY {DAY}")
    if not rows:
        print("No expenses recorded yet.")
        return
    dates, amounts = zip(*rows)
    plt.figure(figsize=(9, 5))
    plt.plot(dates, amounts, marker="o", color="#E45756")
    plt.xlabel("Date")
    plt.ylabel("Amount")
    plt.title("Expenses Over Time")
    plt.xticks(rotation=45, ha="right")
    plt.grid(alpha=0.3)
    _show("expenses_over_time.png")


def income_vs_expense_monthly():
    income = dict(_query(f"SELECT {MONTH}, SUM(amount) FROM transactions "
                         f"WHERE type = 'Income' GROUP BY {MONTH}"))
    expense = dict(_query(f"SELECT {MONTH}, SUM(amount) FROM transactions "
                          f"WHERE type = 'Expense' GROUP BY {MONTH}"))
    months = sorted(set(income) | set(expense))
    if not months:
        print("Not enough data to generate this chart.")
        return

    x = range(len(months))
    width = 0.4
    plt.figure(figsize=(9, 5))
    plt.bar([i - width / 2 for i in x], [income.get(m, 0) for m in months],
            width, label="Income", color="#54A24B")
    plt.bar([i + width / 2 for i in x], [expense.get(m, 0) for m in months],
            width, label="Expense", color="#E45756")
    plt.xticks(list(x), months, rotation=45, ha="right")
    plt.xlabel("Month")
    plt.ylabel("Amount")
    plt.title("Income vs Expenses (Monthly)")
    plt.legend()
    _show("income_vs_expense_monthly.png")


def histogram_expense_distribution():
    rows = _query("SELECT amount FROM transactions WHERE type = 'Expense'")
    if not rows:
        print("No expenses recorded yet.")
        return
    amounts = [row[0] for row in rows]
    plt.figure(figsize=(8, 5))
    plt.hist(amounts, bins=min(10, max(len(amounts), 1)), color="#72B7B2", edgecolor="white")
    plt.xlabel("Expense Amount")
    plt.ylabel("Frequency")
    plt.title("Expense Distribution")
    _show("expense_distribution.png")


def visualize_data():
    charts = {
        "1": ("Bar Chart (Spending by Category)", bar_chart_expense),
        "2": ("Pie Chart (Spending by Category)", pie_chart_expense),
        "3": ("Line Chart (Expenses Over Time)", line_chart_expense_over_time),
        "4": ("Grouped Bar Chart (Income vs Expenses, Monthly)", income_vs_expense_monthly),
        "5": ("Histogram (Expense Distribution)", histogram_expense_distribution),
    }
    print("\n--- Visualization Menu ---")
    for key, (label, _) in charts.items():
        print(f"{key}. {label}")
    print("6. Back to main menu")

    choice = input("Select a visualization option (1-6): ").strip()
    if choice in charts:
        charts[choice][1]()
    elif choice != "6":
        print("Invalid choice. Please select a valid option.")