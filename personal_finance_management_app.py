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

    def add_expense(self):
        try:
            amount = float(self.amount_entry.get())
            category = self.category_entry.get().strip()

            if not category:
                raise ValueError("Category cannot be empty")
            
            # Add expense to list and update total
            self.expenses.append((amount, category))
            self.total_expense.set(sum(exp[0] for exp in self.expenses))

            # Update category totals
            if category in self.category_totals:
                self.category_totals[category] += amount
            else:
                self.category_totals[category] = amount

            # Clear entry fields
            self.amount_entry.delete(0, tk.END)
            self.category_entry.delete(0, tk.END)

            # Update GUI
            self.update_expense_list()
            self.update_category_totals()

        except ValueError as e:
            messagebox.showerror("Invalid input", str(e))

    def update_expense_list(self):
        # Clear current list
        for i in self.expense_tree.get_children():
            self.expense_tree.delete(i)

        # Add all expenses
        for amount, category in self.expenses:
            self.expense_tree.insert("", "end", values=(amount,  category))

    def update_category_totals(self):
        # Clear current list
        self.category_list.delete(0, tk.END)

        # Add all category totals
        for category, total in self.category_totals.items():
            self.category_list.insert(tk.END, f"{category}: {total}")

if __name__ == "__main__":
    root = tk.Tk()
    app = FinanceApp(root)
    root.mainloop()
                                         
