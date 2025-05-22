import sqlite3
import getpass
from datetime import datetime

DB_NAME = "finance_app.db"

#Database
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

#User Authentication 
def register():
    username = input("Enter username: ")
    password = getpass.getpass("Enter password: ")
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        print("Registration successful.")
    except sqlite3.IntegrityError:
        print("Username already exists.")
    conn.close()

def login():
    username = input("Enter username: ")
    password = getpass.getpass("Enter password: ")
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM users WHERE username=? AND password=?", (username, password))
    result = cursor.fetchone()
    conn.close()
    if result:
        print("Login successful.")
        return result[0]  
    else:
        print("Invalid credentials.")
        return None

#Transactions
def add_transaction(user_id):
    amount = float(input("Enter amount: "))
    category = input("Enter category (e.g., Food, Rent): ")
    trans_type = input("Enter type (income/expense): ").lower()
    date = input("Enter date (YYYY-MM-DD): ") or datetime.today().strftime('%Y-%m-%d')
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO transactions (user_id, amount, category, type, date) 
                      VALUES (?, ?, ?, ?, ?)''', (user_id, amount, category, trans_type, date))
    conn.commit()
    conn.close()
    print("Transaction added.")

#Budgeting 
def set_budget(user_id):
    category = input("Enter category to set budget for: ")
    limit_amount = float(input("Enter monthly limit for this category: "))
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''INSERT OR REPLACE INTO budgets (user_id, category, limit_amount) 
                      VALUES (?, ?, ?)''', (user_id, category, limit_amount))
    conn.commit()
    conn.close()
    print("Budget set successfully.")

def check_budget(user_id, category):
    month = datetime.today().strftime('%Y-%m')
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''SELECT SUM(amount) FROM transactions 
                      WHERE user_id=? AND category=? AND type='expense' AND strftime('%Y-%m', date)=?''', 
                   (user_id, category, month))
    total_spent = cursor.fetchone()[0] or 0
    cursor.execute('''SELECT limit_amount FROM budgets WHERE user_id=? AND category=?''', (user_id, category))
    limit = cursor.fetchone()
    conn.close()
    if limit and total_spent > limit[0]:
        print(f"Warning: You have exceeded your budget for {category} by {total_spent - limit[0]:.2f}.")

#Reports 
def show_report(user_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''SELECT type, SUM(amount) FROM transactions 
                      WHERE user_id = ? GROUP BY type''', (user_id,))
    totals = {"income": 0, "expense": 0}
    for row in cursor.fetchall():
        totals[row[0]] = row[1]
    print(f"Total Income: {totals['income']}")
    print(f"Total Expenses: {totals['expense']}")
    print(f"Savings: {totals['income'] - totals['expense']}")
    conn.close()

#Backup and Restore 
def backup_data():
    import shutil
    shutil.copy(DB_NAME, DB_NAME + ".backup")
    print("Backup created as finance_app.db.backup")

def restore_data():
    import shutil
    shutil.copy(DB_NAME + ".backup", DB_NAME)
    print("Database restored from backup.")

#Main Menu 
def main():
    create_tables()
    print("Welcome to Personal Finance Manager")
    while True:
        print("\n1. Register\n2. Login\n3. Exit")
        choice = input("Choose an option: ")
        if choice == '1':
            register()
        elif choice == '2':
            user_id = login()
            if user_id:
                while True:
                    print("\n1. Add Transaction\n2. View Report\n3. Set Budget\n4. Backup Data\n5. Restore Data\n6. Logout")
                    user_choice = input("Choose an option: ")
                    if user_choice == '1':
                        add_transaction(user_id)
                    elif user_choice == '2':
                        show_report(user_id)
                    elif user_choice == '3':
                        set_budget(user_id)
                    elif user_choice == '4':
                        backup_data()
                    elif user_choice == '5':
                        restore_data()
                    elif user_choice == '6':
                        break
                    else:
                        print("Invalid choice.")
        elif choice == '3':
            break
        else:
            print("Invalid choice.")

if __name__ == '__main__':
    main()
