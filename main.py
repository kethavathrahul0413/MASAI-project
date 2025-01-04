import os
import datetime
import random

# File names
ACCOUNTS_FILE = "accounts.txt"
TRANSACTIONS_FILE = "transactions.txt"

# Helper functions
def load_accounts():
    """Load accounts from the accounts file."""
    accounts = {}
    if os.path.exists(ACCOUNTS_FILE):
        with open(ACCOUNTS_FILE, "r") as file:
            valid_lines = []
            for line in file:
                try:
                    account_number, name, password, balance, dob, phone, email, aadhar, atm = line.strip().split(",")
                    accounts[account_number] = {
                        "name": name,
                        "password": password,
                        "balance": float(balance),
                        "dob": dob,
                        "phone": phone,
                        "email": email,
                        "aadhar": aadhar,
                        "atm": atm
                    }
                    valid_lines.append(line.strip())
                except ValueError:
                    pass  # Skip corrupted line

        # Rewrite the accounts file to only include valid lines
        with open(ACCOUNTS_FILE, "w") as file:
            for valid_line in valid_lines:
                file.write(valid_line + "\n")

    return accounts

def save_account(account_number, name, password, balance, dob, phone, email, aadhar, atm):
    """Save account details to the accounts file."""
    with open(ACCOUNTS_FILE, "a") as file:
        file.write(f"{account_number},{name},{password},{balance},{dob},{phone},{email},{aadhar},{atm}\n")

def log_transaction(account_number, transaction_type, amount):
    """Log a transaction in the transactions file."""
    date = datetime.date.today().isoformat()
    with open(TRANSACTIONS_FILE, "a") as file:
        file.write(f"{account_number},{transaction_type},{amount},{date}\n")

def calculate_age(dob):
    """Calculate age from date of birth."""
    birth_date = datetime.datetime.strptime(dob, "%Y-%m-%d").date()
    today = datetime.date.today()
    age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
    return age

def generate_account_number():
    """Generate a unique 8-digit account number where no digit repeats more than twice."""
    while True:
        account_number = "".join(str(random.randint(0, 9)) for _ in range(8))
        if all(account_number.count(digit) <= 2 for digit in account_number):
            return account_number

def create_account():
    """Create a new bank account."""
    while True:
        name = input("Enter your name: ")
        if name.isalpha():
            break
        else:
            print("Invalid name. Please enter only alphabetic characters.")

    while True:
        dob = input("Enter your date of birth (YYYY-MM-DD): ")
        try:
            age = calculate_age(dob)
            if age < 18:
                print("You must be at least 18 years old to create a savings account.")
                return
            break
        except ValueError:
            print("Invalid date format. Please enter your date of birth in YYYY-MM-DD format.")

    while True:
        phone = input("Enter your phone number: ")
        if phone.isdigit() and len(phone) == 10:
            break
        else:
            print("Invalid phone number. Please enter a 10-digit number.")

    email = input("Enter your email: ")

    while True:
        aadhar = input("Enter your Aadhar card number: ")
        if aadhar.isdigit() and len(aadhar) == 12:
            break
        else:
            print("Invalid Aadhar number. Please enter a 12-digit number.")

    while True:
        try:
            initial_deposit = float(input("Enter your initial deposit: "))
            if initial_deposit < 0:
                raise ValueError("Deposit must be a positive number.")
            break
        except ValueError as e:
            print(e)

    atm_request = input("Do you want an ATM card? (yes/no): ").strip().lower()
    atm = "YES" if atm_request == "yes" else "NO"

    account_number = generate_account_number()
    password = input("Enter a password: ")

    save_account(account_number, name, password, initial_deposit, dob, phone, email, aadhar, atm)
    print(f"Your account number: {account_number} (Save this for login)")
    print("Account created successfully!")

def login():
    """Log in to an existing bank account."""
    accounts = load_accounts()
    account_number = input("Enter your account number: ")
    password = input("Enter your password: ")

    if account_number in accounts and accounts[account_number]["password"] == password:
        print("Login successful!")
        return account_number
    else:
        print("Invalid account number or password.")
        return None

def deposit(account_number):
    """Deposit money into the account."""
    accounts = load_accounts()
    while True:
        try:
            amount = float(input("Enter amount to deposit: "))
            if amount <= 0:
                raise ValueError("Amount must be greater than zero.")
            break
        except ValueError as e:
            print(e)

    accounts[account_number]["balance"] += amount
    with open(ACCOUNTS_FILE, "w") as file:
        for acc_num, details in accounts.items():
            file.write(f"{acc_num},{details['name']},{details['password']},{details['balance']},{details['dob']},{details['phone']},{details['email']},{details['aadhar']},{details['atm']}\n")

    log_transaction(account_number, "Deposit", amount)
    print(f"Deposit successful! Current balance: {accounts[account_number]['balance']}")

def withdraw(account_number):
    """Withdraw money from the account."""
    accounts = load_accounts()
    while True:
        try:
            amount = float(input("Enter amount to withdraw: "))
            if amount <= 0:
                raise ValueError("Amount must be greater than zero.")
            if amount > accounts[account_number]["balance"]:
                raise ValueError("Insufficient balance.")
            break
        except ValueError as e:
            print(e)

    accounts[account_number]["balance"] -= amount
    with open(ACCOUNTS_FILE, "w") as file:
        for acc_num, details in accounts.items():
            file.write(f"{acc_num},{details['name']},{details['password']},{details['balance']},{details['dob']},{details['phone']},{details['email']},{details['aadhar']},{details['atm']}\n")

    log_transaction(account_number, "Withdrawal", amount)
    print(f"Withdrawal successful! Current balance: {accounts[account_number]['balance']}")

def main_menu():
    """Display the main menu."""
    while True:
        print("\nWelcome to the HR Banking System!")
        print("1. Create Account")
        print("2. Login")
        print("3. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            create_account()
        elif choice == "2":
            account_number = login()
            if account_number:
                user_menu(account_number)
        elif choice == "3":
            print("Thank you for using the HR Banking System. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

def user_menu(account_number):
    """Display the user menu after login."""
    while True:
        print("\nUser Menu:")
        print("1. Deposit")
        print("2. Withdraw")
        print("3. Logout")
        choice = input("Enter your choice: ")

        if choice == "1":
            deposit(account_number)
        elif choice == "2":
            withdraw(account_number)
        elif choice == "3":
            print("Logged out successfully.")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main_menu()
