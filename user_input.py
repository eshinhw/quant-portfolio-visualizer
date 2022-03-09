import os
from questrade import QuestradeBot
from credentials import ACCOUNT_NUMBERS

def option_interface(qb: QuestradeBot):
    while True:
        print("Select Below")
        print("1. Account Balance")
        print("2. Investment Summary")
        print("3. Historical Dividends")
        print("4. Portfolio Rebalancing")
        print("5. Exit pyQuant")
        user_input = input(">> ")
        if user_input == '1':
            print(qb.get_account_balance_summary())
        elif user_input == '2':
            print(qb.get_investment_summary())
        elif user_input == '3':
            print(qb.get_historical_dividend_income())
        elif user_input == '4':
            print(qb.strategy_allocation())
        elif user_input == '5':
            exit
        else:
            print("Please Select One of the Following Options")
            continue


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
        print("Current Cash Rate is {}".format(cash))
        continue
    break

total_strategy_weight = 0
os.system("clear")
while True:
    user_strategy = {}
    strategy_options = ['1','2']
    print("Choose portfolio strategy")
    print("1. Lethargic Asset Allocation (LAA)")
    print("2. Vigilant Asset Allocation (VAA)")
    print("3. Go to Account Management")

    option = input(">> ")

    if option in strategy_options:
        print("Enter Strategy Allocation Weight")
        weight = int(input(">> "))
        if weight < 0 or weight > (100 - cash):
            print("weight is not correct")
            continue
            
        total_strategy_weight += weight
        user_strategy[option] = weight
        if total_strategy_weight == 100:
            qb = QuestradeBot(ACCOUNT_NUMBERS[user_account], cash, user_strategy)
            option_interface(qb)
        
    elif option == '3':
        if total_strategy_weight != (100 - cash):
            print(cash, total_strategy_weight)
            print("Total is not 100%, Provide Correct Weights")
            continue    
        qb = QuestradeBot(ACCOUNT_NUMBERS[user_account], cash, user_strategy)
        option_interface(qb)
    else:
        print("Please Provide Correct Selection")
        continue

os.system("clear") 

