import json
import random

USERS = []
CURRENT_USER = None


def generate_account_number():
    return "".join(str(random.randint(0, 9)) for _ in range(10))


def load_users():
    global USERS
    try:
        with open("USERS.json", "r") as file:
            USERS = json.load(file)
            return True
    except (FileNotFoundError, json.JSONDecodeError):
        USERS = []
        return False


def save_changes():
    with open("USERS.json", "w") as file:
        json.dump(USERS, file, indent=4)


def find_user(account_number: str):
    for user in USERS:
        if user.get("account_number") == account_number:
            return user
    return None


class User:
    def __init__(self, first_name, last_name, age, sex, nationality):
        account_number = generate_account_number()
        while find_user(account_number) is not None:
            account_number = generate_account_number()

        self.details = {
            "first_name": first_name,
            "last_name": last_name,
            "age": age,
            "sex": sex,
            "nationality": nationality,
            "account_number": account_number,
            "balance": 0.0,
            "transactions": [],
        }
        USERS.append(self.details)
        save_changes()


class Account:
    @staticmethod
    def check_balance(user):
        return user.get("balance", 0.0)

    @staticmethod
    def add_funds(user, amount: float):
        if amount <= 0:
            return False, "Amount must be positive."
        user["balance"] = round(user.get("balance", 0.0) + amount, 2)
        user["transactions"].append({
            "type": "deposit",
            "amount": amount,
        })
        save_changes()
        return True, "Deposit successful."

    @staticmethod
    def withdraw(user, amount: float):
        if amount <= 0:
            return False, "Amount must be positive."
        if user.get("balance", 0.0) < amount:
            return False, "Insufficient funds."
        user["balance"] = round(user.get("balance", 0.0) - amount, 2)
        user["transactions"].append({
            "type": "withdraw",
            "amount": amount
        })
        save_changes()
        return True, "Withdrawal successful."

    @staticmethod
    def transfer(from_user, to_account_number: str, amount: float):
        if amount <= 0:
            return False, "Amount must be positive."
        to_user = find_user(to_account_number)
        if to_user is None:
            return False, "Destination account not found."
        if from_user.get("balance", 0.0) < amount:
            return False, "Insufficient funds."
        from_user["balance"] = round(from_user.get("balance", 0.0) - amount, 2)
        to_user["balance"] = round(to_user.get("balance", 0.0) + amount, 2)
        t = {"type": "transfer_out", "amount": amount, "to": to_account_number}
        from_user["transactions"].append(t)
        t2 = {"type": "transfer_in", "amount": amount, "from": from_user["account_number"]}
        to_user["transactions"].append(t2)
        save_changes()
        return True, "Transfer complete."


def input_positive_float(prompt: str):
    while True:
        v = input(prompt)
        try:
            amt = float(v)
            if amt <= 0:
                print("Enter an amount greater than zero.")
                continue
            return amt
        except ValueError:
            print("Please enter a valid number.")


def user_menu(user):
    while True:
        print("\nChoose an option:\n1) Check balance\n2) Deposit\n3) Withdraw\n4) Transfer\n5) Transactions\n6) My information\n7) Exit")
        choice = input(": ").strip()
        if choice == "1":
            bal = Account.check_balance(user)
            print(f"Balance: {bal:.2f}")
        elif choice == "2":
            amt = input_positive_float("Amount to deposit: ")
            ok, msg = Account.add_funds(user, amt)
            print(msg)
        elif choice == "3":
            amt = input_positive_float("Amount to withdraw: ")
            ok, msg = Account.withdraw(user, amt)
            print(msg)
        elif choice == "4":
            to_acct = input("Destination account number: ").strip()
            amt = input_positive_float("Amount to transfer: ")
            ok, msg = Account.transfer(user, to_acct, amt)
            print(msg)
        elif choice == "5":
            txs = user.get("transactions", [])
            if not txs:
                print("No transactions yet.")
            else:
                for t in txs[-10:]:
                    print(t)
        elif choice == "6":
            print(json.dumps({k: v for k, v in user.items() if k != "transactions"}, indent=2))
        elif choice == "7":
            print("Goodbye.")
            break
        else:
            print("Invalid choice.")


def main():
    global CURRENT_USER
    load_users()
    answer = input("Welcome — are you a new user or an existing user? (new/existing): ").strip().lower()
    if answer in ("existing", "e", "existing user", "user"):
        acct_num = input("Enter your account number: ").strip()
        user = find_user(acct_num)
        if user:
            CURRENT_USER = user
            print(f"Welcome back, {user.get('first_name')}!")
            user_menu(user)
        else:
            print("Account not found.")
    elif answer in ("new", "n", "new user"):
        first_name = input("First name: ").strip().capitalize()
        last_name = input("Last name: ").strip().capitalize()
        while True:
            try:
                age = int(input("Age: ").strip())
                if 1 <= age <= 119:
                    break
                print("Enter a valid age.")
            except ValueError:
                print("Enter a valid integer for age.")
        sex = input("Sex (M/F): ").strip().upper()
        nationality = input("Nationality: ").strip().capitalize()
        new_user = User(first_name, last_name, age, sex, nationality)
        print("Account created. Your account number is:", new_user.details["account_number"])
        user_menu(new_user.details)
    else:
        print("Invalid response.")


if __name__ == "__main__":
    main()





