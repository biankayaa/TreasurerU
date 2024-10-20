import json
from datetime import datetime 
import tkinter.messagebox as messagebox


class FinanceTracker:



    def __init__(self, account_balance, budget):
        self.account_balance = account_balance
        self.budget = budget
        # self.spent = 0
        self.finance_history = {
        'income_value': [], 'income_date': [], 'income_detail': [], 'expense_value': [], 'expense_date': [], 'expense_detail': []
        }
        self.load_data()



    def add_income(self, income, date, detail):
        self.account_balance += income

        self.finance_history['income_value'].append(income)
        self.finance_history['income_date'].append(date.isoformat())
        self.finance_history['income_detail'].append(detail)
        self.save_data()
    

    def add_expense(self, expense, date, detail):
        self.account_balance -= expense

        self.finance_history['expense_value'].append(expense)
        self.finance_history['expense_date'].append(date.isoformat())
        self.finance_history['expense_detail'].append(detail)
        self.spent += expense

        total_expenses = self.get_total_expenses()
        if self.budget is not None and self.spent > self.budget:
            raise BudgetExceededException(f"You've exceeded your budget of {self.budget}! Your total expenses is now {total_expenses}.")
        self.save_data()
    
    def set_budget(self, new_budget):
        self.budget = new_budget
        print(f"Budget has been update to: {self.budget}")
        self.save_data()
    
    def get_recent_expenses(self, count=3):
        recent_expenses = list(zip(self.finance_history['expense_value'],
                                    self.finance_history['expense_date'],
                                    self.finance_history['expense_detail']))
        recent_expenses.sort(key=lambda x: x[1], reverse=True)
        return recent_expenses[:count]

    def get_recent_transactions(self, count=3):
        recent_transactions = list(zip(self.finance_history['income_value'],
                                        self.finance_history['income_date'],
                                        self.finance_history['income_detail']))
        recent_transactions.sort(key=lambda x: x[1], reverse=True)
        return recent_transactions[:count]


    
    def get_total_income(self):
        return sum(self.finance_history['income_value'])
    
    def get_total_expenses(self):
        return sum(self.finance_history['expense_value'])

    def get_budget(self):
        return self.budget
    
    def get_net_balance(self):
        return self.account_balance
    
    def generate_monthly_report(self, month, year):
        total_income = 0
        total_expenses = 0
        income_details = []
        expense_details = []

        for i in range(len(self.finance_history['income_date'])):
            income_date = datetime.fromisoformat(self.finance_history['income_date'][i])
            if income_date.month == month and income_date.year == year:
                total_income += self.finance_history['income_value'][i]
                income_details.append(self.finance_history['income_detail'][i])
        
        for i in range(len(self.finance_history['expense_date'])):
            expense_date = datetime.fromisoformat(self.finance_history['expense_date'][i])
            if expense_date.month == month and expense_date.year == year:
                total_expenses += self.finance_history['expense_value'][i]
                expense_details.append(self.finance_history['expense_detail'][i])
        
        return {
            'total_income': total_income,
            'total_expenses': total_expenses,
            'disposable_income': total_income - total_expenses,
            'income_details': income_details,
            'expense_details': expense_details
        }
    
    def get_insights(self):
        total_income = self.get_total_income()
        total_expenses = self.get_total_expenses()

        insights = {
            'total_income': total_income,
            'total_expenses': total_expenses,
            'net_balance': self.get_net_balance(),
            'expenses_vs_income': total_expenses / total_income if total_income else 0
        }

        return insights
    
    def save_data(self):
        try:
            with open('finance_data.json', 'w') as f:
                json.dump({
                    'account_balance': self.account_balance,
                    'budget': self.budget, 'spent': self.spent,
                    'finance_history': self.finance_history
                }, f)
                
        except Exception as e:
            print(f"Error saving data: {e}")
    
    def load_data(self):
        try:
            with open('finance_data.json', 'r') as f:
                data = json.load(f)
                self.account_balance = data.get('account_balance', 0)
                self.budget = data.get('budget', 0)
                self.spent = data.get('spent', 0)
                self.finance_history = data.get('finance_history', {})
        except FileNotFoundError:
            self.finance_history = {
        'income_value': [], 'income_date': [], 'income_detail': [], 'expense_value': [], 'expense_date': [], 'expense_detail': []
        }
            self.spent = 0
    
    def remove_income(self, date, detail):
        date_iso = date.isoformat() if isinstance(date, datetime) else date

        for i in range(len(self.finance_history['income_value'])):
            if self.finance_history['income_date'][i] == date_iso and self.finance_history['income_detail'][i] == detail:
                del self.finance_history['income_value'][i]
                del self.finance_history['income_date'][i]
                del self.finance_history['income_detail'][i]
                self.account_balance -= self.finance_history['income_value'][i] 
                self.save_data()
                print(f"Income removed: {detail} on {date_iso}")
                return
        print("Income not found.")

    def remove_expense(self, date, detail):
        date_iso = date.isoformat() if isinstance(date, datetime) else date

        for i in range(len(self.finance_history['expense_value'])):
            if self.finance_history['expense_date'][i] == date_iso and self.finance_history['expense_detail'][i] == detail:
                del self.finance_history['expense_value'][i]
                del self.finance_history['expense_date'][i]
                del self.finance_history['expense_detail'][i]
                self.account_balance += self.finance_history['expense_value'][i] 
                self.save_data()
                print(f"Expense removed: {detail} on {date_iso}")
                return
        print("Expense not found.")

    def clear_budget(self):
        self.budget = 0
        self.spent = 0
        self.save_data()
        print("Budget and expenses have been cleared.")

    def edit_entry(self, entry_type, original_date, original_detail, new_value=None, new_date=None, new_detail=None):
        original_date_iso = original_date.isoformat() if isinstance(original_date, datetime) else original_date

        if entry_type == 'expense':
            for i in range(len(self.finance_history['expense_date'])):
                if self.finance_history['expense_date'][i] == original_date_iso and self.finance_history['expense_detail'][i] == original_detail:
                    if new_value is not None:
                        # Adjust account balance if the value is changing
                        self.account_balance += self.finance_history['expense_value'][i] - new_value
                        self.finance_history['expense_value'][i] = new_value
                    if new_date is not None:
                        self.finance_history['expense_date'][i] = new_date.isoformat()
                    if new_detail is not None:
                        self.finance_history['expense_detail'][i] = new_detail
                    self.save_data()
                    print(f"Updated expense: {original_detail} on {original_date_iso}")
                    return
            print("Expense not found.")

        elif entry_type == 'income':
            for i in range(len(self.finance_history['income_date'])):
                if self.finance_history['income_date'][i] == original_date_iso and self.finance_history['income_detail'][i] == original_detail:
                    if new_value is not None:
                        self.account_balance += new_value - self.finance_history['income_value'][i]
                        self.finance_history['income_value'][i] = new_value
                    if new_date is not None:
                        self.finance_history['income_date'][i] = new_date.isoformat()
                    if new_detail is not None:
                        self.finance_history['income_detail'][i] = new_detail
                    self.save_data()
                    print(f"Updated income: {original_detail} on {original_date_iso}")
                    return
            print("Income not found.")

    def view_full_income_history(self):
        full_income_history = list(zip(self.finance_history['income_value'],
                                        self.finance_history['income_date'],
                                        self.finance_history['income_detail']))
        full_income_history.sort(key=lambda x: x[1], reverse=True) 
        return full_income_history

    def view_full_expense_history(self):
        full_expense_history = list(zip(self.finance_history['expense_value'],
                                         self.finance_history['expense_date'],
                                         self.finance_history['expense_detail']))
        full_expense_history.sort(key=lambda x: x[1], reverse=True) 
        return full_expense_history    
    
    def clear_income_history(self):
        if messagebox.askyesno("Confirm", "Are you sure you want to clear the income history?"):
            self.finance_history['income_value'] = []
            self.finance_history['income_date'] = []
            self.finance_history['income_detail'] = []
            self.save_data()

    def clear_expense_history(self):
        if messagebox.askyesno("Confirm", "Are you sure you want to clear the expense history?"):
            self.finance_history['expense_value'] = []
            self.finance_history['expense_date'] = []
            self.finance_history['expense_detail'] = []
            self.save_data()
    
    def reset_balance(self):
        self.account_balance = 0
        self.save_data()

    
class BudgetExceededException(Exception):
    pass