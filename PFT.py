import tkinter as tk
import random
from datetime import datetime

class PersonalFinanceTrackerApp:
    def __init__(self, master):
        self.master = master
        self.master.geometry("300x400")
        self.master.title("Personal Finance Tracker")
        self.transactions = []

        self.greeting = tk.Label(master, text="Welcome To Personal Finance Tracker", font=("calibri", 14))
        self.greeting.pack()

        self.username_label = tk.Label(master, text="Username", font=("calibri", 14))
        self.username_label.pack()

        self.password_label = tk.Label(master, text="Password", font=("calibri", 14))
        self.password_label.pack()

        self.user_entry = tk.Entry(master, font=("calibri", 14))
        self.user_entry.pack()

        self.pass_entry = tk.Entry(master, show="*", font=("calibri", 14))
        self.pass_entry.pack()

        self.button = tk.Button(text="Enter", width=5, height=1, bg="white", fg="black", command=self.open_pft_window)
        self.button.pack()

    def open_pft_window(self):
        pft_window = tk.Toplevel(self.master)
        pft_app = PersonalFinanceTrackerAppWindow(pft_window, self)

    def add_transaction_window(self):
        add_transaction_window = tk.Toplevel(self.master)
        add_transaction_window.title("Add Transaction")

        tk.Label(add_transaction_window, text="Transaction Type:").grid(row=0, column=0)
        transaction_type_var = tk.StringVar(add_transaction_window, value="Income")
        tk.Radiobutton(add_transaction_window, text="Income", variable=transaction_type_var, value="Income").grid(row=0, column=1)
        tk.Radiobutton(add_transaction_window, text="Expense", variable=transaction_type_var, value="Expense").grid(row=0, column=2)

        tk.Label(add_transaction_window, text="Amount:").grid(row=1, column=0)
        amount_entry = tk.Entry(add_transaction_window)
        amount_entry.grid(row=1, column=1)

        tk.Label(add_transaction_window, text="Category:").grid(row=2, column=0)
        category_entry = tk.Entry(add_transaction_window)
        category_entry.grid(row=2, column=1)

        tk.Label(add_transaction_window, text="Date (YYYY-MM-DD):").grid(row=3, column=0)
        date_entry = tk.Entry(add_transaction_window)
        date_entry.grid(row=3, column=1)

        tk.Label(add_transaction_window, text="Payee/Source:").grid(row=4, column=0)
        payee_entry = tk.Entry(add_transaction_window)
        payee_entry.grid(row=4, column=1)

        add_button = tk.Button(add_transaction_window, text="Add", command=lambda: self.add_transaction(
            transaction_type_var.get(), amount_entry.get(), category_entry.get(), date_entry.get(), payee_entry.get()))
        add_button.grid(row=5, column=1)

    def add_transaction(self, transaction_type, amount, category, date, payee):
        transaction_id = random.randint(1000, 9999)

        self.transactions.append({
            "id": transaction_id,
            "type": transaction_type,
            "amount": amount,
            "category": category,
            "date": date,
            "payee": payee
        })

        self.update_main_window()

    def update_main_window(self):
        print("Transactions:")
        for transaction in self.transactions:
            print(transaction)


class PersonalFinanceTrackerAppWindow:
    def __init__(self, master, pft_app):
        self.master = master
        self.pft_app = pft_app

        tk.Button(master, text="Add Transaction", command=self.pft_app.add_transaction_window).pack(pady=10)


def main():
    root = tk.Tk()
    app = PersonalFinanceTrackerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()


