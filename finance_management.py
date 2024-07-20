import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3
import os

class FinanceApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Personal Finance Management App")

        # Create database connection and table
        self.conn = sqlite3.connect('finance_management.db')
        self.cursor = self.conn.cursor()
        self.create_table()

        # Initialize variables
        self.total_expense = tk.DoubleVar()
        self.category_totals = {}

        # Create GUI components
        self.create_widgets()

    def create_table(self):
        """Create the table if it doesn't exist."""
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                amount REAL,
                category TEXT
            )
        ''')
        self.conn.commit()

    def create_widgets(self):
        # Expense Entry Frame
        expense_frame = tk.Frame(self.root)
        expense_frame.pack(pady=10)

        tk.Label(expense_frame, text="Amount:").grid(row=0, column=0, padx=5)
        self.amount_entry = tk.Entry(expense_frame)
        self.amount_entry.grid(row=0, column=1, padx=5)

        tk.Label(expense_frame, text="Category:").grid(row=0, column=2, padx=5)
        self.category_entry = tk.Entry(expense_frame)
        self.category_entry.grid(row=0, column=3, padx=5)

        tk.Button(expense_frame, text="Add Expense", command=self.add_expense).grid(row=0, column=4, padx=5)

        # Total Expense Frame
        total_frame = tk.Frame(self.root)
        total_frame.pack(pady=10)

        tk.Label(total_frame, text="Total Expenses:").grid(row=0, column=0, padx=5)
        self.total_label = tk.Label(total_frame, textvariable=self.total_expense)
        self.total_label.grid(row=0, column=1, padx=5)

        # Expense List Frame
        list_frame = tk.Frame(self.root)
        list_frame.pack(pady=10)

        self.expense_tree = ttk.Treeview(list_frame, columns=("Amount", "Category"))
        self.expense_tree.heading("Amount", text="Amount")
        self.expense_tree.heading("Category", text="Category")
        self.expense_tree.pack()

        # Category Totals Frame
        category_frame = tk.Frame(self.root)
        category_frame.pack(pady=10)

        tk.Label(category_frame, text="Category Totals:").pack()
        self.category_list = tk.Listbox(category_frame)
        self.category_list.pack()

        # Report Button Frame
        report_frame = tk.Frame(self.root)
        report_frame.pack(pady=10)

        tk.Button(report_frame, text="Generate Report", command=self.generate_report).pack()

    def add_expense(self):
        try:
            amount = float(self.amount_entry.get())
            category = self.category_entry.get().strip()

            if not category:
                raise ValueError("Category cannot be empty")

            # Insert expense into the database
            self.cursor.execute('''
                INSERT INTO expenses (amount, category)
                VALUES (?, ?)
            ''', (amount, category))
            self.conn.commit()

            # Update total expense and category totals
            self.total_expense.set(self.get_total_expense())
            self.update_category_totals()

            # Clear entry fields
            self.amount_entry.delete(0, tk.END)
            self.category_entry.delete(0, tk.END)

            # Update GUI
            self.update_expense_list()

        except ValueError as e:
            messagebox.showerror("Invalid input", str(e))

    def get_total_expense(self):
        """Retrieve the total expense from the database."""
        self.cursor.execute('SELECT SUM(amount) FROM expenses')
        return self.cursor.fetchone()[0] or 0.0

    def update_expense_list(self):
        # Clear current list
        for i in self.expense_tree.get_children():
            self.expense_tree.delete(i)

        # Add all expenses
        self.cursor.execute('SELECT amount, category FROM expenses')
        for amount, category in self.cursor.fetchall():
            self.expense_tree.insert("", "end", values=(amount, category))

    def update_category_totals(self):
        # Clear current list
        self.category_list.delete(0, tk.END)

        # Calculate and display category totals
        self.cursor.execute('SELECT category, SUM(amount) FROM expenses GROUP BY category')
        for category, total in self.cursor.fetchall():
            self.category_list.insert(tk.END, f"{category}: {total}")

    def generate_report(self):
        """Generate a report of expenses and save it as a text file."""
        report_file = 'expenses_report.txt'
        with open(report_file, 'w') as file:
            self.cursor.execute('SELECT amount, category FROM expenses')
            for amount, category in self.cursor.fetchall():
                file.write(f"Amount: {amount}, Category: {category}\n")

        messagebox.showinfo("Report Generated", f"Report saved as {report_file}")

    def __del__(self):
        """Close the database connection when the app is closed."""
        self.conn.close()

if __name__ == "__main__":
    root = tk.Tk()
    app = FinanceApp(root)
    root.mainloop()