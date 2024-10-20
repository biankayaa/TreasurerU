import customtkinter as ctk
from customtkinter import CTkImage
import tkinter as tk
from tkinter import messagebox, scrolledtext
from tkcalendar import DateEntry
from datetime import datetime
from finance_tracker import *
from PIL import Image, ImageTk

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

logo_path = "treasureru_logo.png"

class App(ctk.CTk):
    def __init__(self, *args, **kwargs):


        super().__init__(*args, **kwargs)
        self.title("TreasurerU - Finance Tracker")
        self.geometry("340x650")

        self.resizable(False, False)

        self.bind("<F11>", lambda e: "break")

        self.attributes("-fullscreen", False)

        self.tracker = FinanceTracker(account_balance=0, budget=None)

        self.welcome_frame = ctk.CTkFrame(self)
        self.main_frame = ctk.CTkFrame(self, width=340, height=650)
        self.selection_frame = None
        self.new_expense_frame = None

        

        self.init_welcome_frame()
        self.init_main_frame()
        
        self.welcome_frame.pack(fill="both", expand=True)
        self.auto_update_balance()
        self.update_budget_status()
    
    def init_welcome_frame(self):
        #LOGO
        logo = ctk.CTkImage(Image.open(logo_path), size=(300,300))
        logo_label = ctk.CTkLabel(self.welcome_frame, text=None, image=logo)
        logo_label.place(relx=0.5, rely=0.35, anchor='center') 

        #TITLE 
        greeting_label = ctk.CTkLabel(self.welcome_frame, text="Hello, U!", font=("Arial", 24, "bold"), text_color="white")
        greeting_label.place(relx=0.5, rely=0.63, anchor='center')

        welcome_label = ctk.CTkLabel(self.welcome_frame, text="We are TreasurerU,", font=("Helvetica Neue", 16, "bold"), text_color="gray")
        welcome_label.place(relx=0.5, rely=0.68, anchor='center')

        subtitle_label = ctk.CTkLabel(self.welcome_frame, text="Your Treasure Map to Financial Success!", font=("Helvetica Neue", 14), text_color="gray")
        subtitle_label.place(relx=0.5, rely=0.72, anchor='center')

        starting_label = ctk.CTkLabel(self.welcome_frame, text="Ready to track your finances?", font=("Helvetica Neue", 14, "italic"), text_color="white")
        starting_label.place(relx=0.5, rely=0.8, anchor='center')

        #BUTTON
        start_button = ctk.CTkButton(self.welcome_frame, text="LET'S GO!", corner_radius=5, border_color="lightgray", border_width=1, fg_color="transparent", command=self.show_main_frame)

        start_button.place(relx=0.5, rely=0.85, anchor='center')


    def auto_update_balance(self):
        self.update_balance_label()
        self.after(1000, self.auto_update_balance)
    
    def update_balance_label(self):
        current_balance = self.tracker.get_net_balance()
        self.balance_label.configure(text=f"${current_balance:.2f}")

    
    def init_main_frame(self):
        #GREETING TITLE
        greeting_title = ctk.CTkLabel(self.main_frame, text="Hey, U! ", font=("Arial", 27.7, "bold"), text_color="white")
        greeting_title.place(relx=0.1, rely=0.05)

        smiley_face = ctk.CTkLabel(self.main_frame, text=":D", font=("Arial", 27.7, "bold"), text_color="#A020F0")
        smiley_face.place(relx=0.47, rely=0.05)

        #CURRENT BALANCE
        self.balance_frame = ctk.CTkFrame(self.main_frame, width=300.8, height=136.5, corner_radius=10, fg_color="#737373")
        self.balance_frame.place(relx=0.5, rely=0.23, anchor='center')

        balance_label_title = ctk.CTkLabel(self.balance_frame, text="NET BALANCE", font=("Helvetica Neue", 11.5), text_color="white")
        balance_label_title.place(relx=0.08, rely=0.07, anchor='nw')

        self.balance_label = ctk.CTkLabel(self.balance_frame, text="$0.00", font=("Helvetica Neue", 35, "bold"), text_color="white")
        self.balance_label.place(relx=0.05, rely=0.38)

        #BUDGET
        self.budget_frame = ctk.CTkFrame(self.main_frame, width=132.2, height=127.4, corner_radius=10, fg_color="#737373")
        self.budget_frame.place(relx=0.055, rely=0.35)

        budget_label_button = ctk.CTkButton(self.budget_frame, text="BUDGET", font=("Helvetica Neue", 11.5), text_color="white", fg_color="transparent",  command=self.show_budget_popup)
        budget_label_button.place(relx=0.5, rely=0.15, anchor='center')

        # DISPLAY SPENT AND REMAINING BUDGET
        self.budget_status_label = ctk.CTkLabel(self.budget_frame, text=f"${self.tracker.spent}\n\n${self.tracker.get_budget()}", font=("Helvetica Neue", 20, "bold"), text_color="white")
        self.budget_status_label.place(relx=0.5, rely=0.56, anchor='center')

        out_of_label = ctk.CTkLabel(self.budget_frame, text="OUT OF", font=("Helvetica Neue", 12), text_color="white")
        out_of_label.place(relx=0.5, rely=0.55, anchor='center')

        self.update_budget_status()
        
        #REPORTS AND INSIGHTS
        self.reports_and_insights_frame = ctk.CTkFrame(self.main_frame, width=161.1, height=127.4, corner_radius=10, fg_color="#737373")
        self.reports_and_insights_frame.place(relx=0.474, rely=0.35)
        
        generate_label = ctk.CTkLabel(self.reports_and_insights_frame, text="GENERATE", font=("Helvetica Neue", 13), text_color="white", fg_color="transparent")
        generate_label.place(relx=0.5, rely=0.15, anchor='center')

        reports_button = ctk.CTkButton(self.reports_and_insights_frame, text="REPORTS", font=("Helvetica Neue", 15, "bold"), text_color="white", fg_color="transparent", command=self.generate_monthly_report_popup)
        reports_button.place(relx=0.5, rely=0.4, anchor='center')

        insights_button = ctk.CTkButton(self.reports_and_insights_frame, text="INSIGHTS", font=("Helvetica Neue", 15, "bold"), text_color="white", fg_color="transparent", command=self.show_insights_popup)
        insights_button.place(relx=0.5, rely=0.65, anchor='center')
       
        #TAB 
        self.tab_frame = ctk.CTkFrame(self.main_frame, width=300, height=200, corner_radius=10, fg_color="transparent")
        self.tab_frame.place(relx=0.5, rely= 0.72, anchor='center')

        view_tabs = ctk.CTkTabview(self.tab_frame, width=300, height=200, corner_radius=10, segmented_button_selected_color="#584454", fg_color="transparent", segmented_button_selected_hover_color="gray", segmented_button_fg_color=None, text_color="white", state="normal")
        view_tabs.pack(pady=(2,0))

        divider = ctk.CTkLabel(self.tab_frame, text="", font=("Arial", 1), height=0.1, fg_color="gray", width=300)
        divider.place(relx=0.5, rely=0.22, anchor='center')


        self.expense_tab = view_tabs.add("EXPENSE")
        self.transaction_tab = view_tabs.add("TRANSACTION")

        self.update_recent_expenses()
        self.update_recent_transaction()


        #ADD ENTRY BUTTON
        plus_button = ctk.CTkButton(self.main_frame, text="+", font=("Helvetica Neue", 30), corner_radius=30, width=60, height=60, fg_color="#A020F0" ,command=self.add_entry)
        plus_button.place(relx=0.95, rely=0.97, anchor='se')
        



    def update_recent_expenses(self):
        for widget in self.expense_tab.winfo_children():
            widget.destroy()
        
        recent_expenses = self.tracker.get_recent_expenses()
        for value, date, detail in recent_expenses:
            expense_text = f"${value} on {date} - {detail}"
            expense_label = ctk.CTkLabel(self.expense_tab, text=expense_text)
            expense_label.pack(pady=(5, 0))

    def update_recent_transaction(self):
        for widget in self.transaction_tab.winfo_children():
            widget.destroy()
        
        recent_transactions = self.tracker.get_recent_transactions()
        for value, date, detail in recent_transactions:
            transaction_text = f"${value} on {date} - {detail}"
            transaction_label = ctk.CTkLabel(self.transaction_tab, text=transaction_text)
            transaction_label.pack(pady=(5, 0))




    def show_budget_popup(self):
        self.budget_popup = ctk.CTkToplevel(self)
        self.budget_popup.title("Set Monthly Budget")
        self.budget_popup.geometry("300x150")

        budget_label = ctk.CTkLabel(self.budget_popup, text="Enter Monthly Budget:", font=("Helvetica Neue", 14, "bold"))
        budget_label.pack(pady=10)

        self.budget_entry = ctk.CTkEntry(self.budget_popup, placeholder_text="Enter your budget")
        self.budget_entry.pack(pady=5)

        set_budget_button = ctk.CTkButton(self.budget_popup, text="Set Budget", fg_color="#A020F0", command=self.set_budget)
        set_budget_button.pack(pady=10)

        clear_button = ctk.CTkButton(self.budget_popup, text="Clear Budget", font=("Helvetica Neue", 11, "underline"), text_color="white", fg_color="transparent", command=self.clear_budget)
        clear_button.place(relx=0.5, rely=0.92, anchor='center')

        self.budget_popup.protocol("WM_DELETE_WINDOW", self.on_budget_popup_close)
    
    def on_budget_popup_close(self):
        self.budget_popup.destroy()
    
    def clear_budget(self):
        self.tracker.clear_budget()
        self.update_budget_status()
        messagebox.showinfo("Budget Cleared", "Your budget and expenses have been cleared.")

    def set_budget(self):
        try:
            new_budget = float(self.budget_entry.get())
            self.tracker.set_budget(new_budget)
            messagebox.showinfo("Budget Set", f"Your budget has been set to: ${new_budget}")
            self.update_budget_status()
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid number.")

    def update_budget_status(self):
        spent = self.tracker.spent
        budget = self.tracker.get_budget()
        remaining_budget = budget - spent
        self.budget_status_label.configure(text=f"${remaining_budget}\n\n${budget}")



    def go_back(self):
        if self.selection_frame:
            self.selection_frame.pack_forget()
            self.main_frame.pack(fill="both", expand=True)
        
    def show_main_frame(self):
        self.welcome_frame.pack_forget()
        self.main_frame.pack(fill="both", expand=True)



    
    def add_entry(self):
        self.main_frame.pack_forget()
        self.welcome_frame.pack_forget()

        self.selection_frame = ctk.CTkFrame(self, width=340, height=650, fg_color="transparent")
        self.selection_frame.pack(fill="both", expand=True)

        #BACK BUTTON
        back_button = ctk.CTkButton(self.selection_frame, width=60, text="Back", fg_color="#A020F0", font=("Helvetica Neue", 11, "underline"), text_color="white", command=self.go_back)
        back_button.place(relx=0.05, rely=0.05, anchor='nw')

        #EXPENSE FRAME
        self.expense_frame = ctk.CTkFrame(self.selection_frame, width=300, height=200, corner_radius=10, 
        fg_color="#737373")
        self.expense_frame.place(relx=0.5, rely=0.3, anchor='center')

        expense_label_title = ctk.CTkLabel(self.expense_frame, text="EXPENSE", font=("Helvetica Neue", 22, "bold"), text_color="white")
        expense_label_title.place(relx=0.08, rely=0.15)

        #INCOME FRAME
        self.income_frame = ctk.CTkFrame(self.selection_frame, width=300, height=200, corner_radius=10, 
        fg_color="#737373")
        self.income_frame.place(relx=0.5, rely=0.65, anchor='center')

        income_label_title = ctk.CTkLabel(self.income_frame, text="INCOME", font=("Helvetica Neue", 22, "bold"), text_color="white")
        income_label_title.place(relx=0.08, rely=0.15)

        #ADD INCOME
        add_income_entry = ctk.CTkButton(self.income_frame, width=265, text="New Income", font=("Helvetica Neue", 18), fg_color="white", text_color="#737373", command=self.add_income_popup)
        add_income_entry.place(relx=0.5, rely=0.45, anchor='center')

        #EDIT INCOME
        edit_income_entry = ctk.CTkButton(self.income_frame, width=265, text="Edit Income Record", font=("Helvetica Neue", 18), fg_color="white", text_color="#737373", command=self.edit_income_popup)
        edit_income_entry.place(relx=0.5, rely=0.65, anchor='center')

        #REMOVE INCOME
        remove_income_entry = ctk.CTkButton(self.income_frame, width=265, text="Remove Income Record", font=("Helvetica Neue", 18), fg_color="white", text_color="#737373", command=self.remove_income_popup)
        remove_income_entry.place(relx=0.5, rely=0.85, anchor='center')


        #ADD EXPENSE
        add_expense_entry = ctk.CTkButton(self.expense_frame, width=265, text="New Expense", font=("Helvetica Neue", 18), fg_color="white", text_color="#737373", command=self.add_expense_popup)
        add_expense_entry.place(relx=0.5, rely=0.45, anchor='center')

        #EDIT EXPENSE
        edit_expense_entry = ctk.CTkButton(self.expense_frame, width=265, text="Edit Expense Record", font=("Helvetica Neue", 18), fg_color="white", text_color="#737373", command=self.edit_expense_popup)
        edit_expense_entry.place(relx=0.5, rely=0.65, anchor='center')

        #REMOVE EXPENSE
        remove_expense_entry = ctk.CTkButton(self.expense_frame, width=265, text="Remove Expense Record", font=("Helvetica Neue", 18), fg_color="white", text_color="#737373", command=self.remove_expense_popup)
        remove_expense_entry.place(relx=0.5, rely=0.85, anchor='center')

        #VIEW FULL HISTORY
        view_history_button = ctk.CTkButton(self.selection_frame, height=3, text="View Expense History", font=("Helvetica Neue", 10, "underline"), text_color="white", fg_color="transparent", command=self.view_expense_history)
        view_history_button.place(relx=0.8, rely=0.47, anchor='center')

        view_income_button = ctk.CTkButton(self.selection_frame, height=3, text="View Income History", font=("Helvetica Neue", 10, "underline"), text_color="white", fg_color="transparent", command=self.view_income_history)
        view_income_button.place(relx=0.8, rely=0.82, anchor='center')




    def view_expense_history(self):
        self.view_expenses_window = ctk.CTkToplevel(self)
        self.view_expenses_window.title("Expense History")
        self.view_expenses_window.geometry("340x650")

        expense_text = scrolledtext.ScrolledText(self.view_expenses_window, wrap='word', width=40, height=30)
        expense_text.pack(padx=10, pady=10)

        
        full_expense_history = self.tracker.view_full_expense_history()  


        if not full_expense_history:
            expense_text.insert("end", "No expense history available.\n")
        else:
            expense_text.insert("end", "\tDate\tDetail\tAmount\n")
            expense_text.insert("end", "-" * 40 + "\n")
            for value, date, detail in full_expense_history:
                expense_text.insert("end", f"{date}\t{detail}\t{value}\n")
            
        close_button = ctk.CTkButton(self.view_expenses_window, text="Close", text_color="white", fg_color="#A020F0", command=self.view_expenses_window.destroy)
        close_button.pack(pady=10)

        clear_expense_button = ctk.CTkButton(self.view_expenses_window, text="Clear Expense History", text_color="white", fg_color="red", command=self.clear_expense_history)
        clear_expense_button.pack(pady=10)

    def view_income_history(self):
        self.view_income_window = ctk.CTkToplevel(self)
        self.view_income_window.title("Income History")
        self.view_income_window.geometry("340x650")

        
        income_text = scrolledtext.ScrolledText(self.view_income_window, wrap='word', width=40, height=30)
        income_text.pack(padx=10, pady=10)

        full_income_history = self.tracker.view_full_income_history()  

        if not full_income_history:
            income_text.insert("end", "No income history available.\n")
        else:
        
            income_text.insert("end", "\tDate\tDetail\tAmount\n")
            income_text.insert("end", "-" * 40 + "\n")
            for value, date, detail in full_income_history:
                income_text.insert("end", f"{date}\t{detail}\t{value}\n")

        
        close_button = ctk.CTkButton(self.view_income_window, text="Close", text_color="white", fg_color="#A020F0",  command=self.view_income_window.destroy)
        close_button.pack(pady=10)

        clear_income_button = ctk.CTkButton(self.view_income_window, text="Clear Income History", text_color="white", fg_color="red", command=self.clear_income_history)
        clear_income_button.pack(pady=10)
        




    def add_income_popup(self):
        self.add_income_window = ctk.CTkToplevel(self)
        self.add_income_window.title("Add Income")
        self.add_income_window.geometry("340x400")

        self.new_income_frame = ctk.CTkFrame(self.add_income_window, width=300, height=300, corner_radius=10, fg_color="#737373")
        self.new_income_frame.place(relx=0.5, rely=0.5, anchor='center')

        self.income_label = ctk.CTkLabel(self.new_income_frame, text="Add Income", font=("Helvetica Neue", 25, "bold"), text_color="white")
        self.income_label.place(relx=0.5, rely=0.1, anchor='center')

        amount_label = ctk.CTkLabel(self.new_income_frame, text="Enter amount:", font=("Helvetica Neue", 14), text_color="white")
        amount_label.place(relx=0.1, rely=0.25, anchor='w')

        self.income_value_entry = ctk.CTkEntry(self.new_income_frame, width=240, placeholder_text="Income Amount", corner_radius=0, fg_color="white", text_color="#737373")
        self.income_value_entry.place(relx=0.1, rely=0.34, anchor='w')

        date_label = ctk.CTkLabel(self.new_income_frame, text="Enter Date:", font=("Helvetica Neue", 14), text_color="white")
        date_label.place(relx=0.1, rely=0.45, anchor='w')

        self.income_date_entry = DateEntry(self.new_income_frame, background='darkgray', foreground='black', width=28, borderwidth=1, date_pattern='yyyy-mm-dd', mindate=datetime(1900, 1, 1))
        self.income_date_entry.place(relx=0.1, rely=0.52, anchor='w')
        self.income_date_entry.focus_set()

        detail_label = ctk.CTkLabel(self.new_income_frame, text="Enter Detail:", font=("Helvetica Neue", 14), text_color="white")
        detail_label.place(relx=0.1, rely=0.62, anchor='w')

        self.income_detail_entry = ctk.CTkEntry(self.new_income_frame, placeholder_text="Income Detail", width=240, corner_radius=0, fg_color="white", text_color="#737373")
        self.income_detail_entry.place(relx=0.1, rely=0.7, anchor='w')

        self.add_income_button = ctk.CTkButton(self.new_income_frame, text="Add Income", text_color="#737373", fg_color="white", corner_radius=10, command=self.add_income)
        self.add_income_button.place(relx=0.5, rely=0.85, anchor='center')

    def add_income(self):
        try:
            income = float(self.income_value_entry.get())
            date = self.income_date_entry.get_date()
            detail = self.income_detail_entry.get()
            self.tracker.add_income(income, date, detail)
            messagebox.showinfo("Success", "Income added successfully!")
            self.update_recent_transaction()
            self.on_add_income_close()
        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid income and date.")
     
    def on_add_income_close(self):
        self.income_value_entry.delete(0, 'end')
        self.income_date_entry.set_date(datetime.now())
        self.income_detail_entry.delete(0, 'end')

        self.add_income_window.destroy()





    def add_expense_popup(self):
        self.add_expense_window = ctk.CTkToplevel(self)
        self.add_expense_window.title("Add Expense")
        self.add_expense_window.geometry("340x400")

        self.new_expense_frame = ctk.CTkFrame(self.add_expense_window, width=300, height=300, corner_radius=10, fg_color="#737373")
        self.new_expense_frame.place(relx=0.5, rely=0.5, anchor='center')

        self.expense_label = ctk.CTkLabel(self.new_expense_frame, text="Add Expense", font=("Helvetica Neue", 25, "bold"), text_color="white")
        self.expense_label.place(relx=0.5, rely=0.1, anchor='center')

        amount_label = ctk.CTkLabel(self.new_expense_frame, text="Enter amount:", font=("Helvetica Neue", 14), text_color="white")
        amount_label.place(relx=0.1, rely=0.25, anchor='w')

        self.expense_value_entry = ctk.CTkEntry(self.new_expense_frame, width=240, placeholder_text="Expense Amount", corner_radius=0, fg_color="white", text_color="#737373")
        self.expense_value_entry.place(relx=0.1, rely=0.34, anchor='w')

        date_label = ctk.CTkLabel(self.new_expense_frame, text="Enter Date:", font=("Helvetica Neue", 14), text_color="white")
        date_label.place(relx=0.1, rely=0.45, anchor='w')

        self.expense_date_entry = DateEntry(self.new_expense_frame, background='darkgray', foreground='black', width=28, borderwidth=1, date_pattern='yyyy-mm-dd', mindate=datetime(1900, 1, 1))
        self.expense_date_entry.place(relx=0.1, rely=0.52, anchor='w')
        self.expense_date_entry.focus_set()

        detail_label = ctk.CTkLabel(self.new_expense_frame, text="Enter Detail:", font=("Helvetica Neue", 14), text_color="white")
        detail_label.place(relx=0.1, rely=0.62, anchor='w')

        self.expense_detail_entry = ctk.CTkEntry(self.new_expense_frame, placeholder_text="Expense Detail", width=240, corner_radius=0, fg_color="white", text_color="#737373")
        self.expense_detail_entry.place(relx=0.1, rely=0.7, anchor='w')

        self.add_expense_button = ctk.CTkButton(self.new_expense_frame, text="Add Expense", text_color="#737373", fg_color="white", corner_radius=10, command=self.add_expense)
        self.add_expense_button.place(relx=0.5, rely=0.85, anchor='center')

    def add_expense(self):
        try:
            expense = float(self.expense_value_entry.get())
            date = self.expense_date_entry.get_date()
            detail = self.expense_detail_entry.get()
            self.tracker.add_expense(expense, date, detail)
            messagebox.showinfo("Success", "Expense added successfully!")
            self.update_budget_status()
            self.update_recent_expenses()
            self.on_add_expense_close()
        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid expense and date.")

    def on_add_expense_close(self):
        self.expense_value_entry.delete(0, 'end')
        self.expense_date_entry.set_date(datetime.now()) 
        self.expense_detail_entry.delete(0, 'end') 

        self.add_expense_window.destroy()
    




    def edit_income_popup(self):
        self.edit_income_window = ctk.CTkToplevel(self)
        self.edit_income_window.title("Edit Income Record")
        self.edit_income_window.geometry("340x400")

        self.edit_income_frame = ctk.CTkFrame(self.edit_income_window, width=300, height=350, corner_radius=10, fg_color="#737373")
        self.edit_income_frame.place(relx=0.5, rely=0.5, anchor='center')

        self.edit_income_label = ctk.CTkLabel(self.edit_income_frame, text="Edit Income", font=("Helvetica Neue", 25, "bold"), text_color="white")
        self.edit_income_label.place(relx=0.5, rely=0.1, anchor='center')

        # Original detail
        original_detail_label = ctk.CTkLabel(self.edit_income_frame, text="Original Detail:", font=("Helvetica Neue", 14), text_color="white")
        original_detail_label.place(relx=0.1, rely=0.21, anchor='w')

        self.original_income_detail_entry = ctk.CTkEntry(self.edit_income_frame, width=240, placeholder_text="Original Detail", corner_radius=0, fg_color="white", text_color="#737373")
        self.original_income_detail_entry.place(relx=0.1, rely=0.28, anchor='w')

        # New value
        new_value_label = ctk.CTkLabel(self.edit_income_frame, text="New Amount:", font=("Helvetica Neue", 14), text_color="white")
        new_value_label.place(relx=0.1, rely=0.39, anchor='w')

        self.new_income_value_entry = ctk.CTkEntry(self.edit_income_frame, width=240, placeholder_text="New Income Amount", corner_radius=0, fg_color="white", text_color="#737373")
        self.new_income_value_entry.place(relx=0.1, rely=0.48, anchor='w')

        # New date
        new_date_label = ctk.CTkLabel(self.edit_income_frame, text="New Date:", font=("Helvetica Neue", 14), text_color="white")
        new_date_label.place(relx=0.1, rely=0.59, anchor='w')

        self.new_income_date_entry = DateEntry(self.edit_income_frame, background='darkgray', foreground='black', width=28, borderwidth=1, date_pattern='yyyy-mm-dd', mindate=datetime(1900, 1, 1))
        self.new_income_date_entry.place(relx=0.1, rely=0.66, anchor='w')

        # New detail
        new_detail_label = ctk.CTkLabel(self.edit_income_frame, text="New Detail:", font=("Helvetica Neue", 14), text_color="white")
        new_detail_label.place(relx=0.1, rely=0.74, anchor='w')

        self.new_income_detail_entry = ctk.CTkEntry(self.edit_income_frame, width=240, placeholder_text="New Income Detail", corner_radius=0, fg_color="white", text_color="#737373")
        self.new_income_detail_entry.place(relx=0.1, rely=0.82, anchor='w')

        self.edit_income_button = ctk.CTkButton(self.edit_income_frame, text="Update Income", text_color="#737373", fg_color="white", corner_radius=10, command=self.edit_income)
        self.edit_income_button.place(relx=0.5, rely=0.93, anchor='center')
    
    def edit_income(self):
        try:
            original_detail = self.original_income_detail_entry.get()
            original_date = self.new_income_date_entry.get_date()
            new_value = float(self.new_income_value_entry.get()) if self.new_income_value_entry.get() else None
            new_date = self.new_income_date_entry.get_date() if self.new_income_date_entry.get_date() else None
            new_detail = self.new_income_detail_entry.get() if self.new_income_detail_entry.get() else None

           
            self.tracker.edit_entry('income', original_detail=original_detail, original_date=original_date, new_value=new_value, new_date=new_date, new_detail=new_detail)
            
            messagebox.showinfo("Success", "Income updated successfully!")
            self.edit_income_window.destroy()
        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid values.")

    def on_edit_income_popup_close(self):
        self.edit_income_popup.destroy ()




    def edit_expense_popup(self):
        self.edit_expense_window = ctk.CTkToplevel(self)
        self.edit_expense_window.title("Edit Encome Record")
        self.edit_expense_window.geometry("340x400")

        self.edit_expense_frame = ctk.CTkFrame(self.edit_expense_window, width=300, height=350, corner_radius=10, fg_color="#737373")
        self.edit_expense_frame.place(relx=0.5, rely=0.5, anchor='center')

        self.edit_expense_label = ctk.CTkLabel(self.edit_expense_frame, text="Edit Expense", font=("Helvetica Neue", 25, "bold"), text_color="white")
        self.edit_expense_label.place(relx=0.5, rely=0.1, anchor='center')

        original_detail_label = ctk.CTkLabel(self.edit_expense_frame, text="Original Detail:", font=("Helvetica Neue", 14), text_color="white")
        original_detail_label.place(relx=0.1, rely=0.21, anchor='w')

        self.original_expense_detail_entry = ctk.CTkEntry(self.edit_expense_frame, width=240, placeholder_text="Original Detail", corner_radius=0, fg_color="white", text_color="#737373")
        self.original_expense_detail_entry.place(relx=0.1, rely=0.28, anchor='w')

        new_value_label = ctk.CTkLabel(self.edit_expense_frame, text="New Amount:", font=("Helvetica Neue", 14), text_color="white")
        new_value_label.place(relx=0.1, rely=0.39, anchor='w')

        self.new_expense_value_entry = ctk.CTkEntry(self.edit_expense_frame, width=240, placeholder_text="New Expense Amount", corner_radius=0, fg_color="white", text_color="#737373")
        self.new_expense_value_entry.place(relx=0.1, rely=0.48, anchor='w')

        new_date_label = ctk.CTkLabel(self.edit_expense_frame, text="New Date:", font=("Helvetica Neue", 14), text_color="white")
        new_date_label.place(relx=0.1, rely=0.59, anchor='w')

        self.new_expense_date_entry = DateEntry(self.edit_expense_frame, background='darkgray', foreground='black', width=28, borderwidth=1, date_pattern='yyyy-mm-dd', mindate=datetime(1900, 1, 1))
        self.new_expense_date_entry.place(relx=0.1, rely=0.66, anchor='w')

        new_detail_label = ctk.CTkLabel(self.edit_expense_frame, text="New Detail:", font=("Helvetica Neue", 14), text_color="white")
        new_detail_label.place(relx=0.1, rely=0.74, anchor='w')

        self.new_expense_detail_entry = ctk.CTkEntry(self.edit_expense_frame, width=240, placeholder_text="New Expense Detail", corner_radius=0, fg_color="white", text_color="#737373")
        self.new_expense_detail_entry.place(relx=0.1, rely=0.82, anchor='w')

        self.edit_expense_button = ctk.CTkButton(self.edit_expense_frame, text="Update Expense", text_color="#737373", fg_color="white", corner_radius=10, command=self.edit_expense)
        self.edit_expense_button.place(relx=0.5, rely=0.93, anchor='center')
    
    def edit_expense(self):
        try:
            original_detail = self.original_expense_detail_entry.get()
            original_date = self.new_expense_date_entry.get_date()  

            new_value = float(self.new_expense_value_entry.get()) if self.new_expense_value_entry.get() else None
            new_date = self.new_expense_date_entry.get_date() if self.new_expense_date_entry.get_date() else None
            new_detail = self.new_expense_detail_entry.get() if self.new_expense_detail_entry.get() else None

            self.tracker.edit_entry(
                'expense',
                original_detail=original_detail,
                original_date=original_date,
                new_value=new_value,
                new_date=new_date,
                new_detail=new_detail
            )

            messagebox.showinfo("Success", "Expense updated successfully!")
            self.edit_expense_window.destroy()
        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid values.")

    def on_edit_expense_popup_close(self):
            self.edit_expense_popup.destroy ()




    def remove_income_popup(self):
        self.remove_income_window = ctk.CTkToplevel(self)
        self.remove_income_window.title("Remove Income")
        self.remove_income_window.geometry("340x300")

        self.remove_income_frame = ctk.CTkFrame(self.remove_income_window, width=300, height=200, corner_radius=10, fg_color="#737373")
        self.remove_income_frame.place(relx=0.5, rely=0.5, anchor='center')

        label = ctk.CTkLabel(self.remove_income_frame, text="Remove Income", font=("Helvetica Neue", 25, "bold"), text_color="white")
        label.place(relx=0.5, rely=0.12, anchor='center')

        detail_label = ctk.CTkLabel(self.remove_income_frame, text="Enter Detail:", font=("Helvetica Neue", 14), text_color="white")
        detail_label.place(relx=0.1, rely=0.28, anchor='w')

        self.remove_income_detail_entry = ctk.CTkEntry(self.remove_income_frame, placeholder_text="Income Detail", width=240, corner_radius=0, fg_color="white", text_color="#737373")
        self.remove_income_detail_entry.place(relx=0.1, rely=0.39, anchor='w')

        date_label = ctk.CTkLabel(self.remove_income_frame, text="Enter Date:", font=("Helvetica Neue", 14), text_color="white")
        date_label.place(relx=0.1, rely=0.53, anchor='w')

        self.remove_income_date_entry = DateEntry(self.remove_income_frame, background='darkgray', foreground='black', width=28, borderwidth=1, date_pattern='yyyy-mm-dd', mindate=datetime(1900, 1, 1))
        self.remove_income_date_entry.place(relx=0.1, rely=0.62, anchor='w')

        remove_button = ctk.CTkButton(self.remove_income_frame, text="Remove Income", text_color="#737373", fg_color="white", corner_radius=10, command=self.remove_income)
        remove_button.place(relx=0.5, rely=0.82, anchor='center')

    def remove_income(self):
        detail = self.remove_income_detail_entry.get()
        date = self.remove_income_date_entry.get_date()
        self.tracker.remove_income(date, detail)
        messagebox.showinfo("Success", "Income removed successfully!")
        self.remove_income_window.destroy()




    def remove_expense_popup(self):
        self.remove_expense_window = ctk.CTkToplevel(self)
        self.remove_expense_window.title("Remove Expense")
        self.remove_expense_window.geometry("340x300")

        self.remove_expense_frame = ctk.CTkFrame(self.remove_expense_window, width=300, height=200, corner_radius=10, fg_color="#737373")
        self.remove_expense_frame.place(relx=0.5, rely=0.5, anchor='center')

        label = ctk.CTkLabel(self.remove_expense_frame, text="Remove Expense", font=("Helvetica Neue", 25, "bold"), text_color="white")
        label.place(relx=0.5, rely=0.12, anchor='center')

        detail_label = ctk.CTkLabel(self.remove_expense_frame, text="Enter Detail:", font=("Helvetica Neue", 14), text_color="white")
        detail_label.place(relx=0.1, rely=0.28, anchor='w')

        self.remove_expense_detail_entry = ctk.CTkEntry(self.remove_expense_frame, placeholder_text="Expense Detail", width=240, corner_radius=0, fg_color="white", text_color="#737373")
        self.remove_expense_detail_entry.place(relx=0.1, rely=0.39, anchor='w')

        date_label = ctk.CTkLabel(self.remove_expense_frame, text="Enter Date:", font=("Helvetica Neue", 14), text_color="white")
        date_label.place(relx=0.1, rely=0.53, anchor='w')

        self.remove_expense_date_entry = DateEntry(self.remove_expense_frame, background='darkgray', foreground='black', width=28, borderwidth=1, date_pattern='yyyy-mm-dd', mindate=datetime(1900, 1, 1))
        self.remove_expense_date_entry.place(relx=0.1, rely=0.62, anchor='w')

        remove_button = ctk.CTkButton(self.remove_expense_frame, text="Remove Expense", text_color="#737373", fg_color="white", corner_radius=10, command=self.remove_expense)
        remove_button.place(relx=0.5, rely=0.82, anchor='center')

    def remove_expense(self):
        detail = self.remove_expense_detail_entry.get()
        date = self.remove_expense_date_entry.get_date()
        self.tracker.remove_expense(date, detail)
        messagebox.showinfo("Success", "Expense removed successfully!")
        self.remove_expense_window.destroy()
    



    def clear_income_history(self):
        if messagebox.askyesno("Confirm", "Are you sure you want to clear the income history?"):
            self.tracker.clear_income_history()
            self.tracker.reset_balance()
            messagebox.showinfo("Success", "Income history cleared.")

    def clear_expense_history(self):
        if messagebox.askyesno("Confirm", "Are you sure you want to clear the expense history?"):
            self.tracker.clear_expense_history()
            self.tracker.reset_balance()
            messagebox.showinfo("Success", "Expense history cleared.")
    
    


    def generate_monthly_report_popup(self):
        self.report_window = ctk.CTkToplevel(self)
        self.report_window.title("Monthly Report")
        self.report_window.geometry("300x200")

        month_label = ctk.CTkLabel(self.report_window, text="Month (1-12):")
        month_label.pack(pady=5)
        self.month_entry = ctk.CTkEntry(self.report_window)
        self.month_entry.pack(pady=5)

        year_label = ctk.CTkLabel(self.report_window, text="Year:")
        year_label.pack(pady=5)
        self.year_entry = ctk.CTkEntry(self.report_window)
        self.year_entry.pack(pady=5)

        generate_button = ctk.CTkButton(self.report_window, text="Generate", fg_color="#A020F0", command=self.show_report)
        generate_button.pack(pady=10)

        close_button = ctk.CTkButton(self.report_window, text="Close", fg_color="#A020F0", command=self.report_window.destroy)
        close_button.pack(pady=5)
    
    def show_report(self):
        try:
            month = int(self.month_entry.get())
            year = int(self.year_entry.get())
            
            report = self.tracker.generate_monthly_report(month, year)
            
            report_text = f"Monthly Report for {month}/{year}:\n"
            report_text += f"Total Income: {report['total_income']}\n"
            report_text += f"Total Expenses: {report['total_expenses']}\n"
            report_text += f"Disposable Income: {report['disposable_income']}\n"
            report_text += "\nIncome Details:\n" + "\n".join(report['income_details'])
            report_text += "\n\nExpense Details:\n" + "\n".join(report['expense_details'])

            
            report_display_window = ctk.CTkToplevel(self)
            report_display_window.title("Report")
            report_display_window.geometry("400x300")

            report_label = ctk.CTkLabel(report_display_window, text=report_text, justify='left')
            report_label.pack(pady=10)

            close_button = ctk.CTkButton(report_display_window, text="Close", fg_color="#A020F0", command=report_display_window.destroy)
            close_button.pack(pady=5)
            
        except ValueError:
            print("Please enter valid month and year values.")

    def show_insights_popup(self):
        insights = self.tracker.get_insights()
        
        self.insights_window = ctk.CTkToplevel(self)
        self.insights_window.title("Insights")
        self.insights_window.geometry("300x250")
        
        insights_text = scrolledtext.ScrolledText(self.insights_window, wrap='word', width=40, height=10)
        insights_text.pack(padx=10, pady=10)

        insights_text.insert("end", f"Total Income: {insights['total_income']}\n")
        insights_text.insert("end", f"Total Expenses: {insights['total_expenses']}\n")
        insights_text.insert("end", f"Net Balance: {insights['net_balance']}\n")
        insights_text.insert("end", f"Expenses vs Income Ratio: {insights['expenses_vs_income']:.2f}\n")
        
        close_button = ctk.CTkButton(self.insights_window, text="Close", fg_color="#A020F0", command=self.insights_window.destroy)
        close_button.pack(pady=10)




    def on_closing(self, event=0):
        self.destroy()
    

    def start(self):
        self.mainloop()
    
if __name__ == "__main__":
    app = App()
    app.start()