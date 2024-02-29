def add(num1: int, num2: 2):
    return num1+num2


def subtract(num1: int, num2: int):
    return num1-num2


def multiply(num1: int, num2: int):
    return num1*num2


def divide(num1: int, num2: int):
    return num1/num2

# our own exception class that can handle the withdrawing method inside the BankAccount class


class InsuffecientFunds(Exception):
    pass


class BankAccount():
    def __init__(self, starting_balance=0):
        self.balance = starting_balance

    def deposit(self, amount):
        self.balance += amount

    def withdraw(self, amount):
        if self.balance >= amount:
            self.balance -= amount
        else:
            # raise Exception('Insufficient balance in the account')
            raise InsuffecientFunds("Insufficient balance in the account")
            # raise ZeroDivisionError

    def collect_interest(self):
        self.balance *= 1.1
