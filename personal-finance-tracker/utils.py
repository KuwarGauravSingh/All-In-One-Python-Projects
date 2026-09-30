"""Shared helpers for validated, user-friendly console input and output."""
import math
from datetime import date, datetime, timedelta

CURRENCY = "Rs."  # change to "₹" if your terminal supports Unicode


class CancelInput(Exception):
    """Raised when the user types 'q' to abandon the current action."""


def money(value):
    return f"{CURRENCY} {value:,.2f}"


def _read(prompt):
    value = input(f"{prompt} (q = cancel): ").strip()
    if value.lower() in ("q", "quit", "cancel"):
        raise CancelInput
    return value


def prompt_text(prompt, allow_empty=False):
    while True:
        value = _read(prompt)
        if value or allow_empty:
            return value
        print("  Input cannot be empty.")


def prompt_amount(prompt):
    while True:
        raw = _read(prompt).replace(",", "")
        try:
            amount = float(raw)
        except ValueError:
            print("  Please enter a valid number (e.g. 1500 or 249.50).")
            continue
        if not math.isfinite(amount) or amount <= 0:
            print("  Amount must be greater than zero.")
            continue
        return round(amount, 2)


def prompt_date(prompt):
    """Accepts Enter/today, 'yesterday', YYYY-MM-DD or DD-MM-YYYY. Returns 'YYYY-MM-DD'."""
    while True:
        raw = _read(prompt).lower()
        if raw in ("", "today", "t"):
            return date.today().isoformat()
        if raw in ("yesterday", "y"):
            return (date.today() - timedelta(days=1)).isoformat()
        for fmt in ("%Y-%m-%d", "%d-%m-%Y", "%d/%m/%Y"):
            try:
                parsed = datetime.strptime(raw, fmt).date()
            except ValueError:
                continue
            if parsed > date.today():
                print("  Date cannot be in the future.")
                break
            return parsed.isoformat()
        else:
            print("  Use YYYY-MM-DD, DD-MM-YYYY, 'today' or 'yesterday'.")


def prompt_choice(title, options):
    """Numbered list; user picks a number or types a name. 'Other' asks for a custom value."""
    print(f"\n{title}:")
    for i, option in enumerate(options, 1):
        print(f"  {i}. {option}")
    while True:
        raw = _read("Choose number or type a name")
        if raw.isdigit() and 1 <= int(raw) <= len(options):
            choice = options[int(raw) - 1]
        elif raw:
            match = [o for o in options if o.lower() == raw.lower()]
            choice = match[0] if match else raw.title()
        else:
            print("  Please choose an option.")
            continue
        if choice == "Other":
            return prompt_text("Enter custom category").title()
        return choice


def confirm(prompt, default=True):
    hint = "Y/n" if default else "y/N"
    while True:
        raw = input(f"{prompt} [{hint}]: ").strip().lower()
        if not raw:
            return default
        if raw in ("y", "yes"):
            return True
        if raw in ("n", "no"):
            return False
        print("  Please answer y or n.")