from database import get_connection
from utils import prompt_amount, confirm, money


def get_goal():
    conn = get_connection()
    row = conn.execute("SELECT goal_amount FROM savings_goal WHERE id = 1").fetchone()
    conn.close()
    return row[0] if row else None


def set_goal():
    print("\n--- Set Savings Goal ---")
    current = get_goal()
    if current:
        print(f"Current goal: {money(current)}")
        if not confirm("Replace it with a new goal?"):
            return

    goal_amount = prompt_amount("Enter your savings goal")

    conn = get_connection()
    conn.execute(
        "INSERT OR REPLACE INTO savings_goal (id, goal_amount) VALUES (1, ?)",
        (goal_amount,),
    )
    conn.commit()
    conn.close()
    print(f"Savings goal of {money(goal_amount)} set successfully!")


def track_savings_progress(balance):
    goal_amount = get_goal()
    if goal_amount is None:
        print("\nNo savings goal set. Use 'Set Savings Goal' from the main menu.")
        return

    progress = max(0.0, min(balance / goal_amount, 1.0))
    filled = int(progress * 20)
    bar = "#" * filled + "-" * (20 - filled)
    print(f"\nSavings Goal: {money(goal_amount)}")
    print(f"Progress:     [{bar}] {progress * 100:.1f}%")

    remaining = goal_amount - balance
    if remaining > 0:
        print(f"You need to save {money(remaining)} more to reach your goal.")
    else:
        print("Congratulations! You've reached your savings goal.")