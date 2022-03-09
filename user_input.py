import os
from questrade import QuestradeBot
from credentials import ACCOUNT_NUMBERS

 

while True:
    os.system("clear")
    account_options = ['1', '2']
    print("Select Saved Account")
    print("1. Standard TFSA - Eddie")
    print("2. Quant TFSA - Eddie")
    user_account = input(">> ")
    if user_account in account_options:
        break
    else:
        print("Please Select One of The Options Provided")
        continue   

 

while True:
    os.system("clear")
    print("Enter Cash Allocation %")
    cash = int(input(">> "))
    if cash < 0 or cash > 100:
        print("Please Provide Correct Cash Weight")
        continue
    break

total_strategy_weight = 0

while True:
    os.system("clear")
    user_strategy = {}
    strategy_options = ['1','2']
    print("Choose portfolio strategy")
    print("1. Lethargic Asset Allocation (LAA)")
    print("2. Vigilant Asset Allocation (VAA)")
    print("3. Exit")

    option = input(">> ")

    if option in strategy_options:
        print("Enter Strategy Allocation Weight")
        weight = int(input(">> "))
        if weight < 0 or weight > (100 - cash):
            print("weight is not correct")
            continue
            
        total_strategy_weight += weight
        user_strategy[option] = weight
    elif option == '3':
        if total_strategy_weight != (100 - cash):
            print(cash, total_strategy_weight)
            print("Total is not 100%, Provide Correct Weights")
            continue
        break
    else:
        print("Please Provide Correct Selection")
        continue

os.system("clear") 

qb = QuestradeBot(ACCOUNT_NUMBERS[user_account], cash, user_strategy)

qb.strategy_allocation()
