# CLI Banking App

A simple command-line banking system written in Python. Users can create an account, then deposit, withdraw, transfer money, and review their transaction history. All data is stored locally in a JSON file.

## Features

- Create a new account with a randomly generated, unique 10-digit account number
- Log in as an existing user with your account number
- Check balance
- Deposit and withdraw funds
- Transfer money to another account
- View your 10 most recent transactions
- View your account information
- Input validation for amounts, age, and menu choices
- Automatic persistence to `USERS.json` after every change

## Requirements

- Python 3.6+
- No third-party dependencies (uses only `json` and `random` from the standard library)

## Getting Started

```bash
python main.py
```

On launch you will be asked whether you are a new or existing user.

**New user:** enter your first name, last name, age (1-119), sex (M/F), and nationality. Your account number is displayed once the account is created. Keep it, as it is needed to log in later.

**Existing user:** enter your account number to log in.

## Menu

```
1) Check balance
2) Deposit
3) Withdraw
4) Transfer
5) Transactions
6) My information
7) Exit
```

## Data Storage

Accounts are saved to `USERS.json` in the directory you run the program from. The file is created automatically on first save. Each user record looks like this:

```json
{
    "first_name": "Ada",
    "last_name": "Lovelace",
    "age": 30,
    "sex": "F",
    "nationality": "British",
    "account_number": "4827105936",
    "balance": 150.0,
    "transactions": [
        {"type": "deposit", "amount": 200.0},
        {"type": "withdraw", "amount": 50.0}
    ]
}
```

Transaction types: `deposit`, `withdraw`, `transfer_out` (includes `to`), and `transfer_in` (includes `from`).

## Project Structure

| Component | Purpose |
|---|---|
| `generate_account_number()` | Produces a random 10-digit account number |
| `load_users()` / `save_changes()` | Read and write `USERS.json` |
| `find_user()` | Look up a user by account number |
| `User` | Creates a new user record and saves it |
| `Account` | Static methods for balance, deposit, withdraw, and transfer |
| `input_positive_float()` | Prompts until a valid positive number is entered |
| `user_menu()` | Interactive menu loop for a logged-in user |
| `main()` | Entry point: new vs. existing user flow |

## Limitations

This is a learning project and is not suitable for real financial use.

- **No authentication:** anyone with an account number can log in
- **Plain-text storage:** data is saved unencrypted in `USERS.json`
- **Floating-point money:** balances use `float` rounded to 2 decimals; `decimal.Decimal` or integer cents would be more accurate
- **Non-secure account numbers:** generated with `random` rather than `secrets`
- **Transfers to self** are not blocked
- **No concurrency safety:** running multiple instances at once can overwrite each other's changes

## Possible Improvements

- Add PIN or password login with hashed credentials
- Switch to `Decimal` for monetary values
- Add timestamps to transactions
- Prevent transfers to your own account
- Use `secrets` for account number generation
- Add unit tests for the `Account` methods
