from __future__ import print_function, unicode_literals
from PyInquirer import prompt, print_json
# from examples import custom_style_2

import os
from questrade import QuestradeBot
from credentials import ACCOUNT_NUMBERS, QUANT_ACCOUNT_NUM, STANDARD_ACCOUNT_NUM
from pyfiglet import Figlet
from tabulate import tabulate

USER_ACCOUNT = 

def select_account():
    intro = [
        {
            'type': 'list',
            'name': 'account',
            'message': 'Select Account',
            'choices': ['Standard Account', 'Quant Account']
        }
    ]

    intro_answers = prompt(intro)

    if intro_answers.get('account') == 'Standard Account':
        USER_ACCOUNT = STANDARD_ACCOUNT_NUM
    if intro_answers.get('account') == 'Quant Account':
        USER_ACCOUNT = QUANT_ACCOUNT_NUM


def select_purpose():
    purpose_questions = [
        {
            'type': 'list',
            'name': 'purpose',
            'message': 'Select Purpose',
            'choices': ['Account Summary', 'Strategy Rebalancing']
        }
    ]
    purpose_answers = prompt(purpose_questions)

    if purpose_answers.get('purpose') == 'Account Summary':
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
                        'Go to Account Selection',
                        'Exit Program']
                }
            ]

            summary_answers = prompt(summary)

            qb = QuestradeBot(USER_ACCOUNT)

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
                div_questions = [
                    {
                        'type': 'list',
                        'name': 'div_period',
                        'message': 'Choose Period',
                        'choices': ['1 Month', '3 Months', '6 Months', '1 Year', 'All Time']
                    }
                ]
                div_answers = prompt(div_questions)
                if div_answers.get('div_period') == '1 Month':
                    div = qb.get_historical_dividend_income(30)
                if div_answers.get('div_period') == '3 Months':
                    div = qb.get_historical_dividend_income(90)
                if div_answers.get('div_period') == '6 Months':
                    div = qb.get_historical_dividend_income(180)
                if div_answers.get('div_period') == '1 Year':
                    div = qb.get_historical_dividend_income(365)
                if div_answers.get('div_period') == 'All Time':
                    div = qb.get_historical_dividend_income(1825)
                
                print()
                print(tabulate(div, headers='keys'))
                print()
            if summary_answers.get('opeartion') == 'Portfolio Return':
                ret = qb.calculate_account_return()
                print()
                print(tabulate(ret))
                print()
            if summary_answers.get('operation') == 'Go to Account Selection':
                select_account()                
            if summary_answers.get('operation') == 'Exit Program':
                break
            os.system("exit")


    if purpose_answers.get('purpose') == 'Strategy Rebalancing':

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

if __name__ == "__main__":
    os.system("clear") 

    f = Figlet(font='slant')
    print(f.renderText("PyQuant"))
    select_account()
    select_purpose()














