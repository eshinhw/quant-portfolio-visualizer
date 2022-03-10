from __future__ import print_function, unicode_literals
from PyInquirer import prompt, print_json
# from examples import custom_style_2

import os
from questrade import QuestradeBot
from credentials import ACCOUNT_NUMBERS, QUANT_ACCOUNT_NUM, STANDARD_ACCOUNT_NUM
from pyfiglet import Figlet
from tabulate import tabulate

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
    while True:
        summary = [
            {
                'type': 'list',
                'name': 'operation',
                'message': 'Select Operation',
                'choices': [
                    'Account Balance', 
                    'Investment Summary', 
                    'Historical Dividends', 
                    'Portfolio Return',
                    'Exit']
            }
        ]

        summary_answers = prompt(summary)

        qb = QuestradeBot(user_account)

        if summary_answers.get('operation') == 'Account Balance':
            bal = qb.get_account_balance_summary()
            print()
            print(tabulate(bal, headers='keys'))
            print()
        if summary_answers.get('operation') == 'Investment Summary':
            invest = qb.get_investment_summary()
            print()
            print(tabulate(invest, headers='keys'))
            print()
        if summary_answers.get('operation') == 'Historical Dividends':
            div = qb.get_historical_dividend_income()
            print()
            print(tabulate(div, headers='keys'))
            print()
        if summary_answers.get('opeartion') == 'Portfolio Return':
            ret = qb.calculate_account_return()
            print()
            print(tabulate(ret))
            print()
        if summary_answers.get('operation') == 'Exit':
            break
        os.system("exit")


if intro_answers.get('purpose') == 'Strategy Rebalancing':

    strategy_questions = {
        'type': 'list',
        'name': 'strategy_type',
        'message': 'Select Strategy Type',
        'choices': [
            {'name': 'Single Strategy'},
            {'name': 'Multiple Strategies'}
        ]
    }

    strategy_answers = prompt(strategy_questions)

    if strategy_answers.get('strategy_type') == 'Single Strategy':
        print("single strategy rebalancing")
    
    if strategy_answers.get('strategy_type') == 'Multiple Strategies':
        print("multiple strategies rebalancing")
    # {
    #     'type': 'checkbox',
    #     'name': 'strategy',
    #     'message': 'Select Strategy (1 or more)',
    #     'choices': [
    #         {'name': 'LAA'},
    #         {'name': 'VAA'}
    #     ]
    # },














