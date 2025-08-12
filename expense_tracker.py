import csv
import datetime
import os
import matplotlib.pyplot as plt

EXPENSES_FILE = 'expenses.csv'
CATEGORIES = ['Food', 'Transport', 'Entertainment', 'Bills', 'Other']

def add_expense(date, amount, category, description):
    if category not in CATEGORIES:
        print(f"Category must be one of: {', '.join(CATEGORIES)}")
        return
    with open(EXPENSES_FILE, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([date, amount, category, description])
    print("Expense added successfully.")

def read_expenses():
    expenses = []
    if not os.path.exists(EXPENSES_FILE):
        return expenses
    with open(EXPENSES_FILE, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            try:
                expenses.append({
                    'date': datetime.datetime.strptime(row[0], '%Y-%m-%d').date(),
                    'amount': float(row[1]),
                    'category': row[2],
                    'description': row[3]
                })
            except Exception as e:
                print(f"Skipping invalid row: {row} ({e})")
    return expenses

def monthly_summary(year, month):
    expenses = read_expenses()
    filtered = [e for e in expenses if e['date'].year == year and e['date'].month == month]
    summary = {cat: 0.0 for cat in CATEGORIES}
    for e in filtered:
        summary[e['category']] += e['amount']
    return summary

def plot_summary(summary, year, month):
    categories = list(summary.keys())
    amounts = list(summary.values())
    plt.bar(categories, amounts, color='skyblue')
    plt.title(f'Expense Summary for {year}-{month:02d}')
    plt.ylabel('Amount Spent')
    plt.xlabel('Category')
    plt.tight_layout()
    plt.show()

def list_expenses(year=None, month=None, category=None):
    expenses = read_expenses()
    filtered = expenses
    if year:
        filtered = [e for e in filtered if e['date'].year == year]
    if month:
        filtered = [e for e in filtered if e['date'].month == month]
    if category:
        filtered = [e for e in filtered if e['category'].lower() == category.lower()]
    if not filtered:
        print("No expenses found for given filters.")
        return
    print(f"\n{'Date':10} | {'Amount':10} | {'Category':12} | Description")
    print("-"*55)
    for e in filtered:
        print(f"{e['date']} | {e['amount']:10.2f} | {e['category']:12} | {e['description']}")

def main_menu():
    print("\nPersonal Expense Tracker")
    print("-----------------------")
    print("1. Add Expense")
    print("2. View Monthly Summary")
    print("3. List Expenses")
    print("4. Exit")

def get_date_input(prompt):
    while True:
        date_str = input(prompt + " (YYYY-MM-DD): ")
        try:
            date = datetime.datetime.strptime(date_str, '%Y-%m-%d').date()
            return date
        except ValueError:
            print("Invalid date format. Please enter date in YYYY-MM-DD format.")

def get_float_input(prompt):
    while True:
        try:
            val = float(input(prompt + ": "))
            if val < 0:
                print("Amount must be positive.")
                continue
            return val
        except ValueError:
            print("Please enter a valid number.")

def run():
    while True:
        main_menu()
        choice = input("Choose an option (1-4): ")
        if choice == '1':
            date = get_date_input("Enter date of expense")
            amount = get_float_input("Enter amount spent")
            print(f"Categories: {', '.join(CATEGORIES)}")
            category = input("Enter category: ").strip()
            description = input("Enter description: ").strip()
            add_expense(date.isoformat(), amount, category, description)
        elif choice == '2':
            year = int(input("Enter year (e.g., 2025): "))
            month = int(input("Enter month (1-12): "))
            summary = monthly_summary(year, month)
            print("\nExpense Summary:")
            for cat, amt in summary.items():
                print(f"{cat}: {amt:.2f}")
            plot_summary(summary, year, month)
        elif choice == '3':
            print("Filter expenses (leave blank for no filter):")
            year_str = input("Year (YYYY): ").strip()
            month_str = input("Month (1-12): ").strip()
            category_str = input("Category: ").strip()
            year = int(year_str) if year_str else None
            month = int(month_str) if month_str else None
            category = category_str if category_str else None
            list_expenses(year, month, category)
        elif choice == '4':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please select 1-4.")

if __name__ == '__main__':
    run()
