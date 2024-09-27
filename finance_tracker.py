
class FinanceTracker:
    finance_history = {
        'income_value': [], 'income_date': [], 'income_detail': [], 'expense_value': [], 'expense_date': [], 'expense_detail': []
    }


    def __init__(self, account_balance, budget):
        self.account_balance = account_balance
        self.budget = budget



    def add_income(self, income, date, detail):
        self.account_balance += income

        self.finance_history['income_value'].append(income)
        self.finance_history['income_date'].append(date)
        self.finance_history['income_detail'].append(detail)
    

    def add_expense(self, expense, date, detail):
        self.account_balance -= expense

        self.finance_history['expense_value'].append(expense)
        self.finance_history['expense_date'].append(date)
        self.finance_history['expense_detail'].append(detail)

        total_expenses = self.get_total_expenses()
        if total_expenses > self.budget:
            raise BudgetExceededException(f"You've exceeded your budget of {self.budget}! Your total expenses is now {total_expenses}.")
    
    def set_budget(self, new_budget):
        self.budget = new_budget
        print(f"Budget has been update to: {self.budget}")

    
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
            if self.finance_history['income_date'][i].month == month and self.finance_history['income_date'][i].year == year:
                total_income += self.finance_history['income_value'][i]
                income_details.append(self.finance_history['income_detail'][i])
        
        for i in range(len(self.finance_history['expense_date'])):
            if self.finance_history['expense_date'][i].month == month and self.finance_history['expense_date'][i].year == year:
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
    
class BudgetExceededException(Exception):
    pass