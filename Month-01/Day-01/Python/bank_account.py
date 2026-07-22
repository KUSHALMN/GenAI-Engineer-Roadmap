class BankAccount:
    def __init__(self, owner, balance=0):
        self.owner = owner
        self.balance = balance

    def deposit(self, amount):
        self.balance += amount
        print(f"Deposited {amount}. Balance: {self.balance}")

    def withdraw(self, amount):
        if amount > self.balance:
            print("Insufficient funds.")
        else:
            self.balance -= amount
            print(f"Withdrew {amount}. Balance: {self.balance}")

    def check_balance(self):
        print(f"{self.owner}'s Balance: {self.balance}")


account = BankAccount("Kushal")
account.deposit(1000)
account.withdraw(300)
account.check_balance()
