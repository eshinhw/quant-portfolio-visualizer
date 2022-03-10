from __future__ import print_function, unicode_literals
from PyInquirer import prompt, print_json
# from examples import custom_style_2

import os
from questrade import QuestradeBot
from credentials import ACCOUNT_NUMBERS, QUANT_ACCOUNT_NUM, STANDARD_ACCOUNT_NUM
from pyfiglet import Figlet

os.system("clear") 

f = Figlet(font='slant')
print(f.renderText("PyQuant"))


intro = [
    {
        'type': 'list',
        'name': 'account',
        'message': 'Select Account',
        'choices': ['Standard Account', 'Quant Account']
    },
    {
        'type': 'list',
        'name': 'purpose',
        'message': 'Select Purpose',
        'choices': ['Account Summary', 'Strategy Rebalancing']
    },
]

intro_answers = prompt(intro)

if intro_answers.get('account') == 'Standard Account':
    user_account = STANDARD_ACCOUNT_NUM
if intro_answers.get('account') == 'Quant Account':
    user_account = QUANT_ACCOUNT_NUM

if intro_answers.get('purpose') == 'Account Summary':
    summary = [
        {
            'type': 'list',
            'name': 'operation',
            'message': 'Select Operation',
            'choices': [
                'Account Balance', 
                'Investment Summary', 
                'Historical Dividends', 
                'Rebalance Portfolio',
                'Portfolio Return']
        }
    ]

    summary_answers = prompt(summary)

    qb = QuestradeBot(user_account)

    if summary_answers.get('operation') == 'Account Balance':
    qb.get_account_balance_summary()
    if summary_answers.get('operation') == 'Investment Summary':
        qb.get_investment_summary()
    if summary_answers.get('operation') == 'Historical Dividends':
        qb.get_historical_dividend_income()
    if summary_answers.get('operation') == 'Rebalance Portfolio':
        qb.strategy_allocation()
    if summary_answers.get('opeartion') == 'Portfolio Return':
        qb.calculate_account_return()

    {
        'type': 'list',
        'name': 'strategy_type',
        'message': 'Select Strategy Type',
        'choices': [
            {'name': 'Single Strategy'},
            {'name': 'Multiple Strategies'}
        ]
    }
    # {
    #     'type': 'checkbox',
    #     'name': 'strategy',
    #     'message': 'Select Strategy (1 or more)',
    #     'choices': [
    #         {'name': 'LAA'},
    #         {'name': 'VAA'}
    #     ]
    # },

]



# print(answers.get('strategy'))
# if answers.get('strategy') == 'LAA':
#     user_strategy = 'LAA'









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
#         
#         option_interface(qb)
#     else:
#         print("Please Provide Correct Selection")
#         continue


