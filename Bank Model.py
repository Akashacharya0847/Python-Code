class BankAccount:
    """Represents a simple bank account."""

    def __init__(self, account_holder, initial_balance=0.0):
        """Initialize the bank account with an account holder name and an optional initial balance."""
        self.account_holder = account_holder
        self.balance = initial_balance
        print(f"Account created for {self.account_holder} with initial balance of ${self.balance:.2f}.")

    def deposit(self, amount):
        """Deposit money into the account."""
        if amount > 0:
            self.balance += amount
            print(f"Deposited: ${amount:.2f}")
            self.check_balance()
        else:
            print("Deposit amount must be positive.")

    def withdraw(self, amount):
        """Withdraw money from the account if funds are sufficient."""
        if amount > 0:
            if self.balance >= amount:
                self.balance -= amount
                print(f"Withdrew: ${amount:.2f}")
                self.check_balance()
            else:
                print("Insufficient funds.")
        else:
            print("Withdrawal amount must be positive.")

    def check_balance(self):
        """Print the current account balance."""
        print(f"Current balance for {self.account_holder}: ${self.balance:.2f}")

# Example Usage:
if __name__ == "__main__":
    # Create an account
    my_account = BankAccount("Akash", 100.00)

    # Perform operations
    my_account.deposit(50.00)
    my_account.withdraw(30.00)
    my_account.withdraw(150.00) # This should fail due to insufficient funds
    my_account.check_balance()
