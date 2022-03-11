from __future__ import print_function, unicode_literals
from PyInquirer import prompt, print_json
# from examples import custom_style_2
import json
import os
from questrade import QuestradeBot
from credentials import QUANT_ACCOUNT_NUM, STANDARD_ACCOUNT_NUM
from pyfiglet import Figlet
from tabulate import tabulate

def _select_account():
    if os.path.exists("./accounts.json"):
        with open('./accounts.json', 'r') as fp:
            accounts = json.load(fp)
    else:
        accounts = {}
        accounts['Standard_Eddie (Default)'] = STANDARD_ACCOUNT_NUM
        accounts['Quant_Eddie (Default)'] = QUANT_ACCOUNT_NUM

        with open('./accounts.json', 'w') as fp:
            json.dump(accounts, fp)

    accounts_questions = [
        {
            'type': 'list',
            'name': 'account',
            'message': 'Select Account',
            'choices': list(accounts.keys()) + ['Add New Account', 'Reset Saved Accounts', 'Exit Program']
        }
    ]

    accounts_answers = prompt(accounts_questions)

    if accounts_answers.get('account') == 'Add New Account':
        add_new_account = [
            {
                'type': 'input',
                'name': 'new_account_name',
                'message': 'What\'s the name of new account?'     
            },
            {
                'type': 'input',
                'name': 'new_account_num',
                'message': 'What\'s the account number?'
            }
        ]

        add_new_account_answers = prompt(add_new_account)

        with open('./accounts.json', 'r') as fp:
            accounts = json.load(fp)
        
        accounts[add_new_account_answers.get('new_account_name')] = add_new_account_answers.get('new_account_num')

        with open('./accounts.json', 'w') as fp:
            json.dump(accounts, fp)

        return _select_account()
    
    elif accounts_answers.get('account') == 'Reset Saved Accounts':
        os.remove('./accounts.json')
        return _select_account()
    
    elif accounts_answers.get('account') == 'Exit Program':
        quit()

    else:
        for account in accounts.keys():
            if account == accounts_answers.get('account'):
                return QuestradeBot(accounts[account])


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
                        'Account Performance', 
                        'Historical Dividends', 
                        'Go to Account Selection',
                        'Exit Program']
                }
            ]

            summary_answers = prompt(summary)

            if summary_answers.get('operation') == 'Balance Summary':
                bal = qb.get_account_balance_summary()
                print()
                print(tabulate(bal, headers='keys'))
                print()
            if summary_answers.get('operation') == 'Investment Summary':
                invest = qb.get_investment_summary()
                print()
                print(tabulate(invest, headers='keys'))
                print()
            if summary_answers.get('opeartion') == 'Account Performance':
                ret = qb.calculate_portfolio_performance()
                print()
                print(tabulate(ret))
                print()
            if summary_answers.get('operation') == 'Historical Dividends':
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

                    if (div['Monthly_Dividend_Income'] == 0).all():
                        print()
                        print("No Dividend Received")
                        print()
                    else:
                        div.loc["Total"] = div.sum()
                        print()
                        print(tabulate(div, headers='keys'))
                        print()
                    
                if div_answers.get('div_period') == 'Past 6 Months':
                    div = qb.get_historical_dividend_income(180)

                    if (div['Monthly_Dividend_Income'] == 0).all():
                        print()
                        print("No Dividend Received")
                        print()
                    else:
                        div.loc["Total"] = div.sum()
                        print()
                        print(tabulate(div, headers='keys'))
                        print()              

                    
                if div_answers.get('div_period') == 'Past 1 Year':
                    div = qb.get_historical_dividend_income(365)

                    if (div['Monthly_Dividend_Income'] == 0).all():
                        print()
                        print("No Dividend Received")
                        print()
                    else:
                        div.loc["Total"] = div.sum()
                        print()
                        print(tabulate(div, headers='keys'))
                        print()             

                    
                if div_answers.get('div_period') == 'Past 3 Years':
                    div = qb.get_historical_dividend_income(1095)

                    if (div['Monthly_Dividend_Income'] == 0).all():
                        print()
                        print("No Dividend Received")
                        print()
                    else:
                        div.loc["Total"] = div.sum()
                        print()
                        print(tabulate(div, headers='keys'))
                        print()                 
             
                    
                
                # print()
                # print(tabulate(div, headers='keys'))
                # print()

            if summary_answers.get('operation') == 'Go to Account Selection':
                qb = _select_account()                
            if summary_answers.get('operation') == 'Exit Program':
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















