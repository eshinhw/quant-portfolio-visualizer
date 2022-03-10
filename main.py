from __future__ import print_function, unicode_literals
from PyInquirer import prompt, print_json
# from examples import custom_style_2

import os
from questrade import QuestradeBot
from credentials import ACCOUNT_NUMBERS
from pyfiglet import Figlet



# def option_interface(qb: QuestradeBot):
#     while True:
#         f = Figlet(font='slant')
#         print(f.renderText("PyQuant"))
#         print("Select Below")
#         print("1. Account Balance")
#         print("2. Investment Summary")
#         print("3. Historical Dividends")
#         print("4. Portfolio Rebalancing")
#         print("5. Exit pyQuant")
#         user_input = input(">> ")
#         if user_input == '1':
#             print(qb.get_account_balance_summary())
#         elif user_input == '2':
#             print(qb.get_investment_summary())
#         elif user_input == '3':
#             print(qb.get_historical_dividend_income())
#         elif user_input == '4':
#             print(qb.strategy_allocation())
#         elif user_input == '5':
#             exit
#         else:
#             print("Please Select One of the Following Options")
#             continue

os.system("clear") 

f = Figlet(font='slant')
print(f.renderText("PyQuant"))


questions = [
    {
        'type': 'input',
        'name': 'cash_rate',
        'message': 'What\'s your desired cash rate?',
    },
    {
        'type': 'list',
        'name': 'account',
        'message': 'Select Account',
        'choices': ['Standard TFSA - Eddie', 'Quant TFSA - Eddie']
    },
    {
        'type': 'checkbox',
        'name': 'strategy',
        'message': 'Select Strategy (1 or more)',
        'choices': [
            {'name': 'LAA'},
            {'name': 'VAA'}
        ]
    },
    {
        'type': 'list',
        'name': 'operation',
        'message': 'Select Operation',
        'choices': ['Account Balance', 'Investment Summary', 'Historical Dividends', 'Rebalance Portfolio']
    }
]

answers = prompt(questions)
#print(answers.get("cash_rate"))
#print_json(answers)  # use the answers as input for your app

# total_strategy_weight = 0

# while True:
#     os.system("clear")
#     print(f.renderText("PyQuant"))
#     user_strategy = {}
#     strategy_options = ['1','2']
#     print("Choose portfolio strategy")
#     print("1. Lethargic Asset Allocation (LAA)")
#     print("2. Vigilant Asset Allocation (VAA)")
#     print("3. Go to Account Management")

#     option = input(">> ")

#     if option in strategy_options:
#         print("Enter Strategy Allocation Weight")
#         weight = int(input(">> "))
#         if weight < 0 or weight > (100 - cash):
#             print("weight is not correct")
#             continue
            
#         total_strategy_weight += weight
#         user_strategy[option] = weight
#         if total_strategy_weight == 100:
#             qb = QuestradeBot(ACCOUNT_NUMBERS[user_account], cash, user_strategy)
#             option_interface(qb)
        
#     elif option == '3':
#         if total_strategy_weight != (100 - cash):
#             print(cash, total_strategy_weight)
#             print("Total is not 100%, Provide Correct Weights")
#             continue    
#         qb = QuestradeBot(ACCOUNT_NUMBERS[user_account], cash, user_strategy)
#         option_interface(qb)
#     else:
#         print("Please Provide Correct Selection")
#         continue


