from __future__ import print_function, unicode_literals
from PyInquirer import prompt, print_json
# from examples import custom_style_2
import json
import os
from questrade import QuestradeBot
from credentials import QUANT_ACCOUNT_NUM, STANDARD_ACCOUNT_NUM
from pyfiglet import Figlet
from tabulate import tabulate
from initialize import _select_account

def main_menu():
    # initialize questradebot
    qb = _select_account()

    menu_questions = [
        {
            'type': 'list',
            'name': 'main_menu',
            'message': 'Select Menu',
            'choices': ['Account Summary', 'Strategy Rebalancing']
        }
    ]
    menu_answers = prompt(menu_questions)

    if menu_answers.get('main_menu') == 'Account Summary':
        account_summary(qb)

    if menu_answers.get('main_menu') == 'Strategy Rebalancing':
        rebalance_strategy(qb)

def _check_dividends(div):
    if (div['Monthly_Dividend_Income'] == 0).all():
        print()
        print("No Dividend Received")
        print()
    else:
        div.loc["Total"] = div.sum()
        print()
        print(tabulate(div, headers='keys'))
        print()   


def account_summary(qb):
    while True:
            summary = [
                {
                    'type': 'list',
                    'name': 'operation',
                    'message': 'Select Operation',
                    'choices': [
                        'Balance Summary', 
                        'Investment Summary',
                        'Portfolio Performance',
                        'Historical Dividends', 
                        'Go to Account Selection',
                        'Exit Program'
                    ]
                }
            ]

            summary_answers = prompt(summary)

            if summary_answers.get('operation') == 'Balance Summary':
                bal = qb.get_account_balance_summary()
                print()
                print(tabulate(bal, headers='keys'))
                print()
            elif summary_answers.get('operation') == 'Investment Summary':
                invest = qb.get_investment_summary()

                print()
                print(tabulate(invest, headers='keys'))
                print()
            elif summary_answers.get('operation') == 'Portfolio Performance':
                ret = qb.calculate_portfolio_performance()

                print()
                print(tabulate(ret, headers='keys'))
                print()
            elif summary_answers.get('operation') == 'Historical Dividends':
                div_questions = [
                    {
                        'type': 'list',
                        'name': 'div_period',
                        'message': 'Choose Period',
                        'choices': ['Past 3 Months', 'Past 6 Months', 'Past 1 Year', 'Past 3 Years']
                    }
                ]
                div_answers = prompt(div_questions)
                
                    
                if div_answers.get('div_period') == 'Past 3 Months':
                    div = qb.get_historical_dividend_income(90)
                    _check_dividends(div)
                    
                if div_answers.get('div_period') == 'Past 6 Months':
                    div = qb.get_historical_dividend_income(180)
                    _check_dividends(div)
                    
                if div_answers.get('div_period') == 'Past 1 Year':
                    div = qb.get_historical_dividend_income(365)
                    _check_dividends(div)
                    
                if div_answers.get('div_period') == 'Past 3 Years':
                    div = qb.get_historical_dividend_income(1095)
                    _check_dividends(div)               

            elif summary_answers.get('operation') == 'Go to Account Selection':
                qb = _select_account()                
            elif summary_answers.get('operation') == 'Exit Program':
                quit()

            

def rebalance_strategy(qb):

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

if __name__ == "__main__":
    os.system("clear")
    fig = Figlet(font='slant')
    print(fig.renderText("PyQuant"))
    main_menu()















