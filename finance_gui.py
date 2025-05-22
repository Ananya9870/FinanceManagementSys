import sqlite3
import tkinter as tk
from tkinter import messagebox, simpledialog
from datetime import datetime
import shutil

DB_NAME = "finance_app.db"

# ========== Database Setup ==========
def create_tables():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT UNIQUE NOT NULL,
                        password TEXT NOT NULL)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS transactions (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id INTEGER,
                        amount REAL,
                        category TEXT,
                        type TEXT CHECK(type IN ('income', 'expense')),
                        date TEXT,
                        FOREIGN KEY(user_id) REFERENCES users(id))''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS budgets (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id INTEGER,
                        category TEXT,
                        limit_amount REAL,
                        FOREIGN KEY(user_id) REFERENCES users(id))''')
    conn.commit()
    conn.close()

# ========== Auth ==========
def register(username, password):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        messagebox.showinfo("Success", "Registration successful.")
    except sqlite3.IntegrityError:
        messagebox.showerror("Error", "Username already exists.")
    conn.close()

def login(username, password):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM users WHERE username=? AND password=?", (username, password))
    result = cursor.fetchone()
    conn.close()
    if result:
        return result[0]
    return None

# ========== Transactions ==========
def add_transaction(user_id, amount, category, trans_type, date):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO transactions (user_id, amount, category, type, date) 
                      VALUES (?, ?, ?, ?, ?)''', (user_id, amount, category, trans_type, date))
    conn.commit()
    conn.close()
    messagebox.showinfo("Success", "Transaction added.")

# ========== Budget ==========
def set_budget(user_id, category, limit_amount):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''INSERT OR REPLACE INTO budgets (user_id, category, limit_amount) 
                      VALUES (?, ?, ?)''', (user_id, category, limit_amount))
    conn.commit()
    conn.close()
    messagebox.showinfo("Success", "Budget set successfully.")

# ========== Report ==========
def show_report(user_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''SELECT type, SUM(amount) FROM transactions 
                      WHERE user_id = ? GROUP BY type''', (user_id,))
    totals = {"income": 0, "expense": 0}
    for row in cursor.fetchall():
        totals[row[0]] = row[1]
    conn.close()
    return totals

# ========== Backup / Restore ==========
def backup_data():
    shutil.copy(DB_NAME, DB_NAME + ".backup")
    messagebox.showinfo("Success", "Backup created.")

def restore_data():
    shutil.copy(DB_NAME + ".backup", DB_NAME)
    messagebox.showinfo("Success", "Database restored.")

# ========== GUI ==========
class FinanceApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Personal Finance Manager")
        self.user_id = None
        self.login_screen()

    def login_screen(self):
        self.clear_window()

        tk.Label(self.root, text="Username").pack()
        username_entry = tk.Entry(self.root)
        username_entry.pack()

        tk.Label(self.root, text="Password").pack()
        password_entry = tk.Entry(self.root, show="*")
        password_entry.pack()

        tk.Button(self.root, text="Login", command=lambda: self.handle_login(username_entry.get(), password_entry.get())).pack()
        tk.Button(self.root, text="Register", command=lambda: self.handle_register(username_entry.get(), password_entry.get())).pack()

    def handle_register(self, username, password):
        if username and password:
            register(username, password)

    def handle_login(self, username, password):
        user_id = login(username, password)
        if user_id:
            self.user_id = user_id
            self.dashboard()
        else:
            messagebox.showerror("Error", "Invalid credentials")

    def dashboard(self):
        self.clear_window()

        tk.Label(self.root, text="Welcome! Choose an option:").pack(pady=10)

        tk.Button(self.root, text="Add Transaction", command=self.transaction_window).pack(fill='x')
        tk.Button(self.root, text="View Report", command=self.view_report_window).pack(fill='x')
        tk.Button(self.root, text="Set Budget", command=self.set_budget_window).pack(fill='x')
        tk.Button(self.root, text="Backup Data", command=backup_data).pack(fill='x')
        tk.Button(self.root, text="Restore Data", command=restore_data).pack(fill='x')
        tk.Button(self.root, text="Logout", command=self.login_screen).pack(fill='x')

    def transaction_window(self):
        amount = simpledialog.askfloat("Amount", "Enter amount:")
        category = simpledialog.askstring("Category", "Enter category:")
        trans_type = simpledialog.askstring("Type", "Enter type (income/expense):")
        date = simpledialog.askstring("Date", "Enter date (YYYY-MM-DD):", initialvalue=datetime.today().strftime('%Y-%m-%d'))

        if amount and category and trans_type:
            add_transaction(self.user_id, amount, category, trans_type, date)

    def set_budget_window(self):
        category = simpledialog.askstring("Category", "Enter category:")
        limit = simpledialog.askfloat("Limit", "Enter budget limit:")
        if category and limit is not None:
            set_budget(self.user_id, category, limit)

    def view_report_window(self):
        totals = show_report(self.user_id)
        msg = f"Total Income: {totals['income']}\nTotal Expenses: {totals['expense']}\nSavings: {totals['income'] - totals['expense']}"
        messagebox.showinfo("Report", msg)

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

# ========== Main ==========
if __name__ == "__main__":
    create_tables()
    root = tk.Tk()
    app = FinanceApp(root)
    root.mainloop()
