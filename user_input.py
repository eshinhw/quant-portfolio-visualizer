from questrade import QuestradeBot
from credentials import QUANT_ACCOUNT_NUM, QUESTRADE_API_KEY, STANDARD_ACCOUNT_NUM, ACCOUNT_NUMBERS

while True:
    print("Select Saved Account")
    print("1. Standard TFSA - Eddie")
    print("2. Quant TFSA - Eddie")
    user_account = input()
    if user_account == '1' or user_account == '2':
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
    user_input = {}
    options = ['1','2']

    print("Choose portfolio strategy")
    print("1. Lethargic Asset Allocation (LAA)")
    print("2. Vigilant Asset Allocation (VAA)")
    print("3. Exit")

    option = input()

    if option in options:
        print("Enter Strategy Allocation Weight")
        weight = int(input())
        if weight < 0 or weight > (100 - cash):
            continue
        user_input[option] = weight
    elif option == '3':
        break
    else:
        print("Please Provide Correct Selection")
        continue


# qb = QuestradeBot(QUANT_ACCOUNT_NUM)
# print(qb.get_balance())
# print(qb.get_investment_summary())
# print(qb.get_dividend_income())
# print(qb.calculate_portfolio_return())