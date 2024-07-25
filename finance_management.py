import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import sqlite3
from datetime import datetime

# Get the current date
current_date = datetime.now().date()

class FinanceApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Personal Finance Management App")
        
        # Initialize the database and create tables if they don't exist
        self.initialize_database()

        # variables being initialized
        self.expenses = []
        self.total_expense = tk.DoubleVar()
        self.category_totals = {}

        # Components of the GUI being created here
        self.create_widgets()

    def initialize_database(self):
        # Create table if not exists
        conn = sqlite3.connect('finance_management.db')
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                amount REAL,
                category TEXT,
                date TEXT
            )
        ''')
        conn.commit()
        conn.close()

    def create_widgets(self):
        # Expense Entry Frame
        expense_frame = tk.Frame(self.root)
        expense_frame.grid(row=0, column=0, pady=10, padx=10, sticky="ew")

        tk.Label(expense_frame, text="Amount:").grid(row=0, column=0, padx=5)
        self.amount_entry = tk.Entry(expense_frame)
        self.amount_entry.grid(row=0, column=1, padx=5)

        tk.Label(expense_frame, text="Category:").grid(row=0, column=2, padx=5)
        self.category_entry = tk.Entry(expense_frame)
        self.category_entry.grid(row=0, column=3, padx=5)

        tk.Button(expense_frame, text="Add Expense", command=self.add_expense).grid(row=0, column=4, padx=5)
        
        # Delete Expense Frame
        delete_frame = tk.Frame(self.root)
        delete_frame.grid(row=1, column=0, pady=10, padx=10, sticky="ew")

        tk.Label(delete_frame, text="Expense ID to Delete:").grid(row=0, column=0, padx=5)
        self.delete_id_entry = tk.Entry(delete_frame)
        self.delete_id_entry.grid(row=0, column=1, padx=5)
        
        tk.Button(delete_frame, text="Delete Expense", command=self.delete_expense).grid(row=0, column=2, padx=5)

        # Total Expense Frame
        total_frame = tk.Frame(self.root)
        total_frame.grid(row=2, column=0, pady=10, padx=10, sticky="ew")

        tk.Label(total_frame, text="Total Expenses:").grid(row=0, column=0, padx=5)
        self.total_label = tk.Label(total_frame, textvariable=self.total_expense)
        self.total_label.grid(row=0, column=1, padx=5)

        # Expense List Frame
        list_frame = tk.Frame(self.root)
        list_frame.grid(row=3, column=0, pady=10, padx=10, sticky="ew")

        self.expense_tree = ttk.Treeview(list_frame, columns=("ID", "Amount", "Category", "Date"))
        self.expense_tree.heading("ID", text="ID")
        self.expense_tree.heading("Amount", text="Amount")
        self.expense_tree.heading("Category", text="Category")
        self.expense_tree.heading("Date", text="Date")
        self.expense_tree.pack()

        # Category Totals Frame
        category_frame = tk.Frame(self.root)
        category_frame.grid(row=4, column=0, pady=10, padx=10, sticky="ew")

        tk.Label(category_frame, text="Category Totals:").pack()
        self.category_list = tk.Listbox(category_frame)
        self.category_list.pack()

        # Report Button Frame
        report_frame = tk.Frame(self.root)
        report_frame.grid(row=5, column=0, pady=10, padx=10, sticky="ew")

        tk.Button(report_frame, text="Generate Report", command=self.generate_report).pack()

        # Exit Button Frame
        exit_frame = tk.Frame(self.root)
        exit_frame.grid(row=6, column=0, pady=10, padx=10, sticky="ew")

        tk.Button(exit_frame, text="Exit", command=self.root.quit).pack(pady=10)

    def add_expense(self):
        try:
            amount = float(self.amount_entry.get())
            category = self.category_entry.get().strip()

            if not category:
                raise ValueError("Category cannot be empty")
            
            # Add expense to list and update total
            self.expenses.append((amount, category))
            self.total_expense.set(sum(exp[0] for exp in self.expenses))

            # Insert into database
            conn = sqlite3.connect('finance_management.db')
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO expenses (amount, category, date)
                VALUES (?, ?, ?)
            ''', (amount, category, datetime.now().date()))  # Use current date
            conn.commit()
            conn.close()

            # Clear entry fields
            self.amount_entry.delete(0, tk.END)
            self.category_entry.delete(0, tk.END)

            # Update GUI
            self.update_expense_list()
            self.update_category_totals()

        except ValueError as e:
            messagebox.showerror("Invalid input", str(e))

    def delete_expense(self):
        try:
            expense_id = int(self.delete_id_entry.get())
            
            # Delete from database
            conn = sqlite3.connect('finance_management.db')
            cursor = conn.cursor()
            cursor.execute('DELETE FROM expenses WHERE id = ?', (expense_id,))
            conn.commit()
            conn.close()

            # Clear entry field
            self.delete_id_entry.delete(0, tk.END)

            # Update GUI
            self.update_expense_list()
            self.update_category_totals()

        except ValueError as e:
            messagebox.showerror("Invalid input", str(e))

    def update_expense_list(self):
        # Clear current list
        for i in self.expense_tree.get_children():
            self.expense_tree.delete(i)

        # Add all expenses from the database
        conn = sqlite3.connect('finance_management.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM expenses')
        for row in cursor.fetchall():
            self.expense_tree.insert("", "end", values=row)
        conn.close()

    def update_category_totals(self):
        # Clear current list
        self.category_list.delete(0, tk.END)

        # Update category totals
        conn = sqlite3.connect('finance_management.db')
        cursor = conn.cursor()
        cursor.execute('''
            SELECT category, SUM(amount) FROM expenses
            GROUP BY category
        ''')
        for category, total in cursor.fetchall():
            self.category_list.insert(tk.END, f"{category}: {total}")
        conn.close()

    def generate_report(self):
        # Generate report for today
        conn = sqlite3.connect('finance_management.db')
        cursor = conn.cursor()
        cursor.execute('''
            SELECT id, amount, category, date FROM expenses
        ''')
        report_data = cursor.fetchall()
        conn.close()

        # Display report
        report_window = tk.Toplevel(self.root)
        report_window.title("Expense Report")

        report_text = tk.Text(report_window, wrap='word')
        report_text.pack(expand=1, fill='both')

        report_text.insert(tk.END, "Expense Report\n\n")
        for row in report_data:
            report_text.insert(tk.END, f"ID: {row[0]} | Amount: {row[1]} | Category: {row[2]} | Date: {row[3]}\n")

    def generate_report_for_date(self, date):
        # Generate report for a specific date
        conn = sqlite3.connect('finance_management.db')
        cursor = conn.cursor()
        cursor.execute('''
            SELECT id, amount, category, date FROM expenses WHERE date = ?
        ''', (date,))
        report_data = cursor.fetchall()
        conn.close()

        # Display report for specific date
        report_window = tk.Toplevel(self.root)
        report_window.title(f"Expense Report for {date}")

        report_text = tk.Text(report_window, wrap='word')
        report_text.pack(expand=1, fill='both')

        report_text.insert(tk.END, f"Expense Report for {date}\n\n")
        for row in report_data:
            report_text.insert(tk.END, f"ID: {row[0]} | Amount: {row[1]} | Category: {row[2]} | Date: {row[3]}\n")

if __name__ == "__main__":
    root = tk.Tk()
    app = FinanceApp(root)
    root.mainloop()
