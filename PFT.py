import tkinter as tk
from tkinter import Toplevel, Label, Entry, Button, Radiobutton, StringVar, OptionMenu, messagebox
import random
import matplotlib.pyplot as plt
import pandas as pd
import datetime  
import time 

transactions = []
account_balance = 0
transaction_type_var = None
category_var = None
amount_entry = None
date_entry = None
payee_source_entry = None
id_entry = None

#Main window of PFT
main_window = tk.Tk()
main_window.title("Personal Finance Tracker")
main_window.geometry("800x600")

name_label = Label(main_window, text="", font=("Calibri", 14))
name_label.pack(pady=5)

money_label = Label(main_window, text="Balance: " + str(account_balance), font=("Calibri", 14))
money_label.pack(pady=2)

transactions_summary_label = None

# Function for ask user's name.
def prompt_user_name():
    return input("What is your name?")
# Function to greeting with your name
def update_greeting(name):  
    name_label.config(text=f"Hello {name}, Welcome to your PFT")
# Function to update balance on main window
def update_account_balance():
    money_label.config(text=f"Balance: ${account_balance:.2f}")
# Function to add a transaction
def add_transaction():
    global account_balance
    transaction_id = random.randint(1000, 9999)  
    transaction_type = transaction_type_var.get()
    amount = float(amount_entry.get()) if amount_entry.get() else 0
    category = category_var.get()
    date = date_entry.get()
    payee_source = payee_source_entry.get()
    
    if not amount or not date:
        messagebox.showerror("Error", "Please enter amount and date.")
        return
    
    transaction = {
        "ID": transaction_id,
        "type": transaction_type,
        "category": category,
        "amount": amount,
        "date": date,
        "payee_source": payee_source
    }
    transactions.append(transaction)
# Update account balance
    if transaction_type == "income":
        account_balance += amount
    else:  
        account_balance -= amount
# Refresh the summary
    update_transactions_summary()
    update_account_balance()  
    messagebox.showinfo("Success", "Transaction added successfully.")
    add_trans_window.destroy()
# Initialize and update the transactions summary display.    
def init_transactions_summary():
    global transactions_summary_label
    transactions_summary_label = Label(main_window, text="", font=("Calibri", 12))
    transactions_summary_label.pack(pady=5)
    update_transactions_summary()
    
def update_transactions_summary():
    global transactions_summary_label, transactions
    summary_text = "Last transactions:\n"
    # Display the last 5 transactions, or fewer if there aren't 5
    for transaction in transactions[-5:]:
        summary_text += f"ID: {transaction['ID']}, Type: {transaction['type']}, Amount: ${transaction['amount']:.2f}, Date: {transaction['date']}\n"
    transactions_summary_label.config(text=summary_text)
# Function to open a new window for adding transactions.
def open_add_transaction_window():
    global add_trans_window, transaction_type_var, category_var, amount_entry, date_entry, payee_source_entry

    add_trans_window = Toplevel(main_window)
    add_trans_window.title("Add new transaction")
    add_trans_window.geometry("400x300")

    transaction_type_label = Label(add_trans_window, text="Transaction Type", font=("Calibri", 14))
    transaction_type_label.grid(row=0, column=0)

    transaction_type_var = StringVar(value="income")
    Radiobutton(add_trans_window, text="Income", variable=transaction_type_var, value="income", command=update_categories).grid(row=0, column=1)
    Radiobutton(add_trans_window, text="Expense", variable=transaction_type_var, value="expense", command=update_categories).grid(row=0, column=2)

    category_label = Label(add_trans_window, text="Category", font=("Calibri", 14))
    category_label.grid(row=1, column=0)

    categories = {"income": ["Salary", "Pension", "Interest", "Others"],
                  "expense": ["Food", "Rent", "Clothing", "Car", "Health", "Others"]}
    category_var = StringVar(add_trans_window, value=categories["income"][0])  
    if transaction_type_var.get() == "expense":
        category_var.set(categories["expense"][0]) 
    category_option = OptionMenu(add_trans_window, category_var, *categories["income"] + categories["expense"])  
    
    category_option.grid(row=1, column=1)

    amount_label = Label(add_trans_window, text="Amount", font=("Calibri", 14))
    amount_label.grid(row=2, column=0)
    amount_entry = Entry(add_trans_window)
    amount_entry.grid(row=2, column=1)

    date_label = Label(add_trans_window, text="Date (YYYY-MM-DD)", font=("Calibri", 14))
    date_label.grid(row=3, column=0)
    date_entry = Entry(add_trans_window)
    date_entry.grid(row=3, column=1)

    payee_source_label = Label(add_trans_window, text="Payee/Source", font=("Calibri", 14))
    payee_source_label.grid(row=4, column=0)
    payee_source_entry = Entry(add_trans_window)
    payee_source_entry.grid(row=4, column=1)

    submit_button = Button(add_trans_window, text="Submit", font=("Calibri", 14), command=add_transaction)
    submit_button.grid(row=5, column=1)
# Function to choose categoires of income or expense.
def update_categories():
    categories = {"income": ["Salary", "Pension", "Interest", "Others"],
                  "expense": ["Food", "Rent", "Clothing", "Car", "Health", "Others"]}
    category_menu = category_var['menu']
    category_menu.delete(0, 'end')

    for category in categories[transaction_type_var.get()]:
        category_menu.add_command(label=category, command=lambda value=category: category_var.set(value))
    category_var.set(categories[transaction_type_var.get()][0])

def see_transactions():
    trans_window = Toplevel(main_window)
    trans_window.title("List of transactions")

    trans_label = Label(trans_window, text=organise_trans(), font=("Calibri", 14))
    trans_label.pack()
# Functions to visualize transactions data as bar or pie charts.
def visualize_bar_chart():
    global transactions

    df = pd.DataFrame(transactions)  
    grouped_data = df.groupby('type')['amount'].sum()

    plt.figure(figsize=(8, 6))
    plt.bar(grouped_data.index, grouped_data.values, color=['blue', 'orange'])
    plt.xlabel('Transaction Type')
    plt.ylabel('Total Amount ($)')
    plt.title('Bar Chart: Total Income vs Total Expenses')
    plt.show()

def visualize_pie_chart():
    global transactions

    df = pd.DataFrame(transactions)
    grouped_data = df.groupby('type')['amount'].sum()

    plt.figure(figsize=(8, 8))
    plt.pie(grouped_data, labels=grouped_data.index, autopct='%1.1f%%', startangle=140)
    plt.title('Pie Chart: Total Income vs Total Expenses')
    plt.axis('equal')
    plt.tight_layout()
    plt.show()

bar_chart_button = Button(main_window, text="Visualize Bar Chart", command=visualize_bar_chart)
bar_chart_button.pack()

pie_chart_button = Button(main_window, text="Visualize Pie Chart", command=visualize_pie_chart)
pie_chart_button.pack()

def organise_trans():
    out = ""
    for item in transactions:
        out += str(item)
        out += "\n"

    return out

def delete_transaction():
    global account_balance
    transaction_id = int(id_entry.get())
    for transaction in transactions:
        if transaction['ID'] == transaction_id:
            if transaction['type'] == "income":
                account_balance -= transaction['amount']
            else:
                account_balance += transaction['amount']
            transactions.remove(transaction)
            update_account_balance()
            messagebox.showinfo("Success", "Transaction deleted successfully.")
            delete_trans_window.destroy()
            return
    update_transactions_summary()

    messagebox.showerror("Error", "Transaction ID not found.")

def open_delete_transaction_window():
    global delete_trans_window, id_entry

    delete_trans_window = Toplevel(main_window)
    delete_trans_window.title("Delete Transaction")
    delete_trans_window.geometry("300x100")

    id_label = Label(delete_trans_window, text="Enter Transaction ID:", font=("Calibri", 14))
    id_label.pack()

    id_entry = Entry(delete_trans_window)
    id_entry.pack(pady=5)

    delete_trans_button = Button(delete_trans_window, text="Delete Transaction", font=("Calibri", 14), command=delete_transaction)
    delete_trans_button.pack(pady=5)

name_w = tk.Toplevel()
name_w.title("")
name_w.geometry("400x150")

name_entry = Entry(name_w)
name_entry.pack(pady=10)

def get_name():
    update_greeting(name_entry.get())
    name_w.destroy()
# Function to save txt file
def save_transactions_to_file():
    filename = 'transactions_' + time.strftime("%Y%m%d-%H%M%S") + '.txt'
    with open(filename, 'w') as file:
        for transaction in transactions:
            line = f"ID: {transaction['ID']}, Type: {transaction['type']}, Category: {transaction['category']}, Amount: {transaction['amount']}, Date: {transaction['date']}, Payee/Source: {transaction['payee_source']}\n"
            file.write(line)
    messagebox.showinfo("Success", f"Transactions saved to {filename}.")

   
    
# Function to filter transactions by their date or category.
def filter_transactions():
    filter_window = Toplevel(main_window)
    filter_window.title("Filter Transactions")
    filter_window.geometry("300x250")

    def apply_filters():
        start_date = start_date_entry.get()
        end_date = end_date_entry.get()
        t_type = transaction_type_var_filter.get()
        category = category_var_filter.get()

        filtered = transactions
        if start_date and end_date:
            filtered = filter_transactions_by_time(filtered, start_date, end_date)
        if t_type != "all":
            filtered = filter_transactions_by_type(filtered, t_type)
        if category != "All":
            filtered = filter_transactions_by_category(filtered, category)

        display_filtered_transactions(filtered)

    # Local function definitions
    def filter_transactions_by_time(transactions, start_date, end_date):
        start = datetime.datetime.strptime(start_date, "%Y-%m-%d")
        end = datetime.datetime.strptime(end_date, "%Y-%m-%d")
        return [t for t in transactions if start <= datetime.datetime.strptime(t['date'], "%Y-%m-%d") <= end]

    def filter_transactions_by_type(transactions, t_type):
        return [t for t in transactions if t['type'] == t_type]

    def filter_transactions_by_category(transactions, category):
        return [t for t in transactions if t['category'] == category]

    def display_filtered_transactions(filtered_transactions):
        info = "\n".join(f"ID: {t['ID']}, Type: {t['type']}, Amount: {t['amount']}, Date: {t['date']}, Category: {t['category']}" for t in filtered_transactions)
        messagebox.showinfo("Filtered Transactions", info if info else "No transactions found.")

    # Labels for filtering
    Label(filter_window, text="Start Date (YYYY-MM-DD):").grid(row=0, column=0)
    start_date_entry = Entry(filter_window)
    start_date_entry.grid(row=0, column=1)

    Label(filter_window, text="End Date (YYYY-MM-DD):").grid(row=1, column=0)
    end_date_entry = Entry(filter_window)
    end_date_entry.grid(row=1, column=1)

    transaction_type_var_filter = StringVar(value="all")
    Radiobutton(filter_window, text="All", variable=transaction_type_var_filter, value="all").grid(row=2, column=0)
    Radiobutton(filter_window, text="Income", variable=transaction_type_var_filter, value="income").grid(row=2, column=1)
    Radiobutton(filter_window, text="Expense", variable=transaction_type_var_filter, value="expense").grid(row=2, column=2)

    category_var_filter = StringVar(value="All")
    categories = ["All", "Salary", "Pension", "Interest", "Food", "Rent", "Clothing", "Car", "Health", "Others"]
    OptionMenu(filter_window, category_var_filter, *categories).grid(row=3, column=1)

    Button(filter_window, text="Apply Filters", command=apply_filters).grid(row=4, column=1)

# Button to open the filter window
Button(main_window, text="Filter Transactions", command=filter_transactions).pack()


submit_btn = Button(name_w, text="Submit", font=("Calibri", 14), command=get_name)
submit_btn.pack(pady=5)

add_trans_btn = Button(main_window, text="Add new transaction", font=("Calibri", 14), command=open_add_transaction_window)
add_trans_btn.pack(pady=4)

see_trans_btn = Button(main_window, text="See transactions", font=("Calibri", 14), command=see_transactions)
see_trans_btn.pack(pady=2)

delete_trans_btn = Button(main_window, text="Delete Transaction", font=("Calibri", 14), command=open_delete_transaction_window)
delete_trans_btn.pack(pady=2)

save_trans_btn = Button(main_window, text="Save Transactions", font=("Calibri", 14), command=save_transactions_to_file)
save_trans_btn.pack(pady=2)


init_transactions_summary()


main_window.mainloop()
