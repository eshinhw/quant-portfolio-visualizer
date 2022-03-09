from questrade import QuestradeBot
from credentials import ACCOUNT_NUMBERS

while True:
    account_options = ['1', '2']
    print("Select Saved Account")
    print("1. Standard TFSA - Eddie")
    print("2. Quant TFSA - Eddie")
    user_account = input()
    if user_account in account_options:
        break
    else:
        print("Please Select One of The Options Provided")
        continue    

while True:
    print("Enter Cash Allocation %")
    cash = int(input())
    if cash < 0 or cash > 100:
        print("Please Provide Correct Cash Weight")
        continue
    break

while True:
    user_strategy = {}
    strategy_options = ['1','2']
    print("Choose portfolio strategy")
    print("1. Lethargic Asset Allocation (LAA)")
    print("2. Vigilant Asset Allocation (VAA)")
    print("3. Exit")

    option = input()

    if option in strategy_options:
        print("Enter Strategy Allocation Weight")
        weight = int(input())
        if weight < 0 or weight > (100 - cash):
            continue
        user_strategy[option] = weight
    elif option == '3':
        if sum(user_strategy.values) + cash != 100:
            print("Total is not 100%, Provide Correct Weights")
            continue
        break
    else:
        print("Please Provide Correct Selection")
        continue


qb = QuestradeBot(ACCOUNT_NUMBERS[user_account], cash, )
# print(qb.get_balance())
# print(qb.get_investment_summary())
# print(qb.get_dividend_income())
# print(qb.calculate_portfolio_return())