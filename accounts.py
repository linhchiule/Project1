class Account:

    def __init__(self, name, balance=0):
        self.__account_name = name
        self.__account_balance = balance
        self.set_balance(self.get_balance())

    def deposit(self, amount):
        if amount <= 0:
            return False
        else:
            self.set_balance(self.get_balance() + amount)
            return True

    def withdraw(self, amount):
        if amount <= 0:
            return False
        elif amount > self.get_balance():
            return False
        else:
            self.set_balance(self.get_balance() - amount)
            return True

    def get_balance(self):
        return self.__account_balance

    def get_name(self):
        return self.__account_name

    def set_balance(self, value):
        if value < 0:
            self.__account_balance = 0
        else:
            self.__account_balance = value

    def set_name(self, value):
        self.__account_name = value

    def __str__(self):
        return f'Account name = {self.get_name()}, Account balance = {self.get_balance():.2f}'


class SavingAccount(Account):
    MINIMUM = 100
    RATE = 0.02

    def __init__(self, name):
        super().__init__(name, SavingAccount.MINIMUM)
        self.__deposit_count = 0

    def apply_interest(self):
        self.set_balance(self.get_balance() * (1 + SavingAccount.RATE))

    def deposit(self, amount):
        d = super().deposit(amount)  # Call parent deposit method
        if d:
            self.__deposit_count += 1
            if self.__deposit_count % 5 == 0:
                self.apply_interest()
        return d

    def withdraw(self, amount):
        if amount <= 0:
            return False
        elif self.get_balance() - amount < SavingAccount.MINIMUM:
            return False
        else:
            x= self.get_balance() - amount
            self.set_balance(x)
            return True

    def set_balance(self, value):
        if value < SavingAccount.MINIMUM:
            super().set_balance(SavingAccount.MINIMUM)
        else:
            super().set_balance(value)

    def __str__(self):
        return f'SAVING ACCOUNT: {super().__str__()}'
