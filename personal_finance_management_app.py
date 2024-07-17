import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

class FinanceApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Personal Finance Management App")

        # variables being initialized
        self.expenses = []
        self.total_expense = tk.DoubleVar()
        self.category_totals = {}

        # Components of the GUI being created here
        self.create_widgets()

    def create_widgets(self):
        # Expense Entry Frame
        expense_frame = tk.Frame(self.root)
        expense_frame.pack(pady=10)

        tk.Label(expense_frame, text="Amount:").grid(row=0, column=0, padx=5)
        self.amount_entry = tk.Entry(expense_frame)
        self.amount_entry.grid(row=0, column=1, padx=5)

        tk.Label(expense_frame, text="Category:").grid(row=0, column=2, padx=5)
        self.category_entry = tk.Entry(expense_frame)
        self.category_entry.grid(row=0, column=3,  padx=5)

        tk.button(expense_frame, text="Add Expense", command=self.add_expense).grid(row=0, column=4, padx=5)
        