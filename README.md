# 💰 Personal Finance Manager

A simple command-line-based Personal Finance Manager built with Python and SQLite. This app allows users to track their income and expenses, set monthly budgets, and generate financial reports. Backup and restore functionalities are also included.

---

## 🚀 Features

- ✅ User registration and secure login (with password input)
- 💵 Add income and expense transactions
- 📊 Generate reports showing total income, expenses, and savings
- 🎯 Set monthly budget limits by category
- 🚨 Budget over-limit warnings
- 🗄️ Backup and restore the SQLite database

---

## 🛠️ Tech Stack

- **Language**: Python
- **Database**: SQLite
- **Libraries**: 
  - `sqlite3`
  - `getpass`
  - `datetime`
  - `shutil` (for backup/restore)

---

## 📦 Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/Ananya9870/FinanceManagementSys.git
   cd FinanceManagementSys


📋 Usage
Main Menu Options
Register
Create a new user account.

Login
Log in to your existing account.

Exit
Exit the application.

After Login
Add Transaction: Add income or expense details by specifying amount, category, type, and date.

View Report: View total income, total expenses, and your savings.

Set Budget: Set a monthly spending limit for a specific category.

Backup Data: Backup the current database file (finance_app.db.backup).

Restore Data: Restore from a previously created backup.

Logout: Log out and return to the main menu.
