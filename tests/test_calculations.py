import pytest
from app.calculations import add, subtract, multiply, divide, BankAccount, InsuffecientFunds


@pytest.mark.parametrize("num1, num2, expected", [
    (3, 2, 5),
    (7, 1, 8),
    (12, 4, 16)
])
def test_add(num1, num2, expected):
    print("testing addition")
    assert add(num1, num2) == expected


def test_sub():
    print('testing subtraction')
    assert subtract(1, 1) == 0


def test_mul():
    print('testing multipication')
    assert multiply(1, 1) == 1


def test_div():
    print('testing division')
    assert divide(1, 1) == 1, "division failed"

# here we can see that the code is repeating in each of the testing case we can remove that by using fixture.


@pytest.fixture
def zero_bank_account():
    return BankAccount()


@pytest.fixture
def bank_account():
    return BankAccount(50)


def test_bank_set_initial_amount(bank_account):
    # bank_account = BankAccount()
    assert bank_account.balance == 50


def test_bank_default_amount(zero_bank_account):
    # bank_account = BankAccount()
    assert zero_bank_account.balance == 0


def test_withdraw(bank_account):
    # bank_account = BankAccount()
    bank_account.withdraw(20)
    assert bank_account.balance == 30


def test_deposit(zero_bank_account):
    # bank_account = BankAccount()
    zero_bank_account.deposit(80)
    assert zero_bank_account.balance == 80


def test_interest(bank_account):
    # bank_account = BankAccount(50)
    bank_account.collect_interest()
    assert int(bank_account.balance) == 55


@pytest.mark.parametrize("deposited,withdrawed,exptected", [
    (100, 50, 50),
    (500, 100, 400),
    (327, 37, 290)
])
def test_bank_transaction(zero_bank_account, deposited, withdrawed, exptected):
    zero_bank_account.deposit(deposited)
    zero_bank_account.withdraw(withdrawed)
    assert zero_bank_account.balance == exptected

# test to handle the insuffecient funds


def test_insuffecient_funds(zero_bank_account):
    # with pytest.raises(Exception):
    with pytest.raises(InsuffecientFunds):
        zero_bank_account.withdraw(100)
