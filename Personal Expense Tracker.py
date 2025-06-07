# 📝 Features to implement:
# Add an Expense
# Input: description, amount, category (e.g. food, transport), and date (YYYY-MM-DD).
# Store in a list of dictionaries.
# View Expenses
# Show all expenses.
# Optional: Filter by date range or category.
# View Summary
# Total amount spent.
# Breakdown by category.
# Delete an Expense
# Save/Load to/from File (JSON)


import json
import os.path
from colorama import Fore, init, Style
from datetime import datetime
from tabulate import tabulate
import pandas as pd
import matplotlib.pyplot as plt

init(autoreset = True)

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

class ExpenseTracker:

    def __init__(self):
        self.expense_list = [{"description": "poptates", "amount" : 500, "category" : "food", "date" : "2025-05-15"}
                        ,{"description": "dollaly", "amount" : 1000, "category" : "food", "date" : "2025-01-15"}
                        ]
        self.path = os.path.expanduser("/Users/chaahatamesar/Desktop/PythonPractise/expense.json")
        if os.path.exists(self.path):
            with open(self.path, "r") as f:
                self.expense_list = json.load(f)
            print("Loaded expenses from file.")
        else:
            self.expense_list = []

    def new_expense(self):
        description_new = input("Enter description: ")
        try:
            amount_new = int(input("Enter the amount: "))
        except ValueError:
            print("Invalid input, enter number only!")
            return
        category_new = input("Enter the category (e.g. food, transport): ")
        try:
            date_new = input("Enter date (YYYY-MM-DD): ")
            parsed_date = datetime.strptime(date_new, "%Y-%m-%d").date()
            expensedate_new = parsed_date.isoformat()
        except Exception as e:
            print("Invalid date format! ", e)
            return
        self.expense_list.append({
            "description" : description_new,
            "amount" :amount_new,
            "category" : category_new,
            "date" :expensedate_new })

    def view_expense(self):
        print("\n1. View All\n2. Filter by Category\n3. Filter by Date Range\n4. Sort by date or amount")
        choice = input("Choose filter option: ")
        filtered = self.expense_list
        if choice == "2":
            category_filter = input("Enter category to filter: ").lower()
            filtered = [e for e in self.expense_list if e['category'].lower() == category_filter]

        elif choice == "3":
            try:
                start = datetime.strptime(input("Start date (YYYY-MM-DD): "), "%Y-%m-%d").date()
                end = datetime.strptime(input("End date (YYYY-MM-DD): "), "%Y-%m-%d").date()
                filtered = [e for e in self.expense_list if start <= datetime.strptime(e['date'], "%Y-%m-%d").date() <= end]
            except Exception as e:
                print(e)
                return
        elif choice == "4":
            view_choice = int(input("Sort by (1: date, 2: amount): "))
            if view_choice == 1:
                filtered.sort(key=lambda x: x['date'])
            elif view_choice == 2:
                filtered.sort(key=lambda x: x['amount'])

        if not filtered:
            print("No expenses found for the given filter.")
            return

        for i, line in enumerate(filtered, start=1):
            print(f"{i} : Description: {Fore.MAGENTA + line.get('description')} \033[0m Amount: $ {Fore.RED + str(line.get('amount'))} "
                  f"\033[0m Category: {Fore.YELLOW + line.get('category')} Date: {Fore.CYAN + line.get('date')}")


    def summary_expense(self):
        total = 0
        print("-"*60 + Style.BRIGHT, Fore.MAGENTA +"\n" +" "* 25 +"Summary")
        mydict = pd.DataFrame(self.expense_list)
        print(tabulate(mydict.values.tolist(), headers= mydict.columns, tablefmt= 'grid'))

        for i in self.expense_list:
            total = total + int(i.get('amount'))
        print(f"\nTotal Amount Spent is: ${Fore.RED + str(total) }")

        print("\nBreakdown by Category:")
        category_totals = {}
        for item in self.expense_list:
            cat = item['category']
            category_totals[cat] = category_totals.get(cat, 0) + float(item['amount'])

        for category, cat_total in category_totals.items():
            print(f"{Fore.YELLOW}{category.capitalize()}: {Fore.GREEN}${cat_total:.2f}")
        print("-"*60)

    def delete_expense(self):
        del_choice = input("Are you sure (y/n)?")
        if del_choice.lower() == 'n':
            return
        else:
            for i, line in enumerate(self.expense_list, start=1):
                print(f"{i} : Description: {Fore.MAGENTA + line.get('description')} \033[0m "
                      f"Amount: $  { Fore.RED + str(line.get('amount')) } \033[0m "
                      f"Category: {Fore.YELLOW +line.get('category') + Fore.RESET} "
                      f"Date: {Fore.CYAN + line.get('date')}")
            try:
                del_expense = int(input("Enter the expense number: "))
                del self.expense_list[del_expense - 1]
                print("Expense Deleted")
            except ValueError as e:
                print(e)
                return

    def save_infile(self):
        with open(self.path, "w") as expense:
            json.dump(self.expense_list,expense)
        print("File Saved!")

    def edit_expense(self):
        for i, line in enumerate(self.expense_list, start= 1):
            print(f"{i} : Description: {Fore.MAGENTA + line.get('description')} \033[0m "
                  f"Amount: $  {Fore.RED + str(line.get('amount'))} \033[0m "
                  f"Category: {Fore.YELLOW + line.get('category') + Fore.RESET} "
                  f"Date: {Fore.CYAN + line.get('date')}")
        try:
            edit_choice = int(input("Enter the number of expense you want to edit: "))
            print(f"{self.expense_list[edit_choice - 1]}")
            edit_description = input("Enter the new description: ")
            try:
                edit_amt  = float(input("Enter the new amount: "))
            except ValueError:
                print("Invalid Amount!")
                return
            edit_category = input("Enter the new category: ")
            edit_date = input("Enter the new date: ")
            self.expense_list[edit_choice -1].update({
            "description" : edit_description,
            "amount" :edit_amt,
            "category" : edit_category,
            "date" :edit_date})
        except Exception as e:
            print(e)
            return

    def export_to_csv(self):
        df = pd.DataFrame(self.expense_list)
        export_path = os.path.expanduser("~/Desktop/expense.csv")
        df.to_csv(export_path, index = False)
        print(f"Exported to {export_path}")

    def monthly_chart(self):
        df = pd.DataFrame(self.expense_list)
        df['date'] = pd.to_datetime(df['date'])
        df['month'] = df['date'].dt.to_period('M')
        summary = df.groupby(['month'])['amount'].sum()
        summary.plot(kind='bar', title="Monthly Expense Summary")
        plt.show()

    def run(self):
        while True:
            try:
                clear_screen()
                print("-" * 60)
                choice = int(input("!!Personal Expense Tracker!!"
                                   "\n1. Add Expense "
                                   "\n2. View Expenses "
                                   "\n3. Show Summary/ Total Amount Spent"
                                   "\n4. Delete Expense "
                                   "\n5. Save to File (JSON) "
                                   "\n6. Edit Expense"
                                   "\n7. Export to CSV"
                                   "\n8. Monthly Chart "
                                   "\n9. Exit "
                                   "\nEnter the choice:"))
                if choice == 1:
                    self.new_expense()
                elif choice == 2:
                    self.view_expense()
                elif choice == 3:
                    self.summary_expense()
                elif choice == 4:
                    self.delete_expense()
                elif choice == 5:
                    self.save_infile()
                elif choice == 6:
                    self.edit_expense()
                elif choice == 7:
                    self.export_to_csv()
                elif choice == 8:
                    self.monthly_chart()
                elif choice == 9:
                    if input("Enter (y/n) if you want to save before closing?").lower() == 'y':
                        self.save_infile()
                    break
                else:
                    print("Enter a number from 1- 6")
            except ValueError:
                print(Fore.RED + "Enter a number")
                return

if __name__ == '__main__':
    app = ExpenseTracker()
    app.run()
