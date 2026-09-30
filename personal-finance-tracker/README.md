# Personal Finance Tracker

A command-line application that helps you track income, expenses, and savings goals, and visualize your spending patterns. Data is stored locally in SQLite, and charts are generated with Matplotlib.

## Features

- **Add Income:** pick a source category, enter the amount, an optional description, and a date.
- **Add Expense:** pick a category (Rent, Groceries, Transport, etc.), enter the amount, description, and date.
- **View Summary:** total income, expenses, balance, savings rate, this month's figures, top spending category, and savings goal progress.
- **View Transactions:** see the last 10, all, income only, or expenses only, in an aligned table.
- **Delete Transaction:** remove a mistaken entry by its ID, with a confirmation step.
- **Set Savings Goal:** define a goal and track progress with a progress bar.
- **Visualize Spending:** bar, pie, line, monthly income-vs-expense, and histogram charts, with an option to save each chart as an image.
- **Export to CSV:** save all transactions to a spreadsheet-friendly file.

## Improvements in this version

- **Input validation:** invalid numbers, zero or negative amounts, and bad dates are rejected with a helpful message instead of crashing the program.
- **Guided input flow:** numbered category menus, a custom "Other" category, date shortcuts, and a preview with confirmation before saving.
- **Cancel anywhere:** type `q` at any prompt to return to the main menu.
- **Descriptions stored:** transactions now have a description field. Existing databases are upgraded automatically, and no data is lost.
- **Bug fixes:** charts now group by day or month correctly, dates are sorted, and the previously broken stacked bar chart was replaced with a monthly grouped bar chart.
- **Reliable database path:** the database works no matter which folder you run the program from.
- **Cleaner code:** shared input helpers live in `utils.py`, and the main menu is data-driven so new options are easy to add.

## Technologies Used

- **Python 3:** core language
- **SQLite3:** local database for transactions and savings goal
- **Matplotlib:** charts and visualizations

## Project Structure

```
Personal Finance Tracker/
├── main.py            # Entry point and main menu
├── tracker.py         # Add income/expense, summary, view, delete, CSV export
├── savings.py         # Savings goal and progress tracking
├── visualization.py   # Charts (bar, pie, line, monthly, histogram)
├── database.py        # SQLite connection, table creation, migration
├── utils.py           # Input validation and formatting helpers
├── data/              # finance.db is created here automatically
├── charts/            # Saved chart images (created when you save a chart)
└── exports/           # CSV exports (created on first export)
```

## Installation and Running

1. Clone the repository:
   ```bash
   git clone <repository-url>
   ```
2. Navigate to the Personal Finance Tracker folder:
   ```bash
   cd "Personal Finance Tracker"
   ```
3. Install the dependency:
   ```bash
   pip install matplotlib
   ```
4. Run the program:
   ```bash
   python main.py
   ```

## Menu Options

```
1. Add Income
2. Add Expense
3. View Summary
4. View Transactions
5. Delete Transaction
6. Set Savings Goal
7. Visualize Spending
8. Export to CSV
9. Exit
```

## Usage Tips

- **Dates:** press Enter for today, or type `yesterday`, `YYYY-MM-DD`, or `DD-MM-YYYY`. Future dates are not allowed.
- **Amounts:** commas are accepted (for example `1,500`), and values are rounded to two decimals.
- **Categories:** choose a number from the list, type a name, or choose "Other" to enter your own.
- **Cancel:** type `q` at any prompt to abandon the current action.
- **Currency:** the symbol defaults to `Rs.`. Change `CURRENCY` at the top of `utils.py` to use another (for example `₹` if your terminal supports Unicode).

## Example Session

```
--- Add Expense ---

Select expense category:
  1. Rent
  2. Groceries
  ...
Choose number or type a name (q = cancel): 2
Enter amount (q = cancel): 850
Description (optional) (q = cancel): Weekly vegetables
Date [Enter = today, or YYYY-MM-DD] (q = cancel):

Expense: Rs. 850.00 | Groceries | 2026-09-30 | Weekly vegetables
Save this entry? [Y/n]: y
Expense added successfully! Current balance: Rs. 34,150.00
```

## Data Storage

- Transactions and the savings goal are stored in `data/finance.db`.
- Charts you choose to save go to `charts/`.
- CSV exports go to `exports/transactions.csv`.

## Possible Future Enhancements

- Monthly budgets per category with overspend alerts
- Filtering transactions by date range or category
- Editing existing transactions
- Recurring transactions