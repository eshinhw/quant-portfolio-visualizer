from __future__ import print_function, unicode_literals
from PyInquirer import prompt, print_json
import os
from questrade import QuestradeBot
from pyfiglet import Figlet
from tabulate import tabulate
from strategies.VAA import VAA
from strategies import LAA
import accounts
import pandas as pd
import share_email


def print_dividends(div):
    if (div['Monthly_Dividend_Income'] == 0).all():
        print()
        print("No Dividend Received")
        print()
    else:
        div_nonzero = div[div['Monthly_Dividend_Income'] > 0]
        div_nonzero.loc["Total"] = div_nonzero.sum()
        print()
        print(tabulate(div_nonzero, headers='keys'))
        print()


def print_output(df):
    print()
    print(tabulate(df, headers='keys'))
    print()


def main_menu():
    ACCOUNTS = accounts.load_accounts()
    main_selection = [
        {
            'type': 'list',
            'name': 'main_menu',
            'message': 'Main Menu',
            'choices': ['Account Overview', 'Allocation Rebalancing', 'Exit Program']
        }
    ]

    main_selection_answer = prompt(main_selection)

    if main_selection_answer.get('main_menu') == 'Account Overview':
        while True:
            accounts_questions = [
                {
                    'type': 'list',
                    'name': 'account',
                    'message': 'Account Options',
                    'choices': list(ACCOUNTS.keys()) + ['Add New Account', 'Reset Saved Accounts', 'Go to Main Menu', 'Exit Program']
                }
            ]

            accounts_answer = prompt(accounts_questions)

            if accounts_answer.get('account') == 'Add New Account':
                accounts.add_new_account()
                break

            elif accounts_answer.get('account') == 'Reset Saved Accounts':
                os.remove('./accounts.json')
                ACCOUNTS = accounts.load_accounts()

            elif accounts_answer.get('account') == 'Go to Main Menu':
                break

            elif accounts_answer.get('account') == 'Exit Program':
                quit()

            else:
                acct_name = accounts_answer.get('account')
                acctNum = ACCOUNTS[acct_name]
                qb = QuestradeBot(acctNum)
                account_summary(qb)

        main_menu()

    elif main_selection_answer.get('main_menu') == 'Allocation Rebalancing':
        rebalance_strategy()

    elif main_selection_answer.get('main_menu') == 'Exit Program':
        quit()


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
                    'Share in Email',
                    'Go to Main Menu',
                    'Exit Program'
                ]
            }
        ]

        summary_answers = prompt(summary)

        if summary_answers.get('operation') == 'Balance Summary':
            bal = qb.get_account_balance_summary()
            print_output(bal)

        elif summary_answers.get('operation') == 'Investment Summary':
            invest = qb.get_investment_summary()
            print_output(invest)

        elif summary_answers.get('operation') == 'Portfolio Performance':
            ret = qb.calculate_portfolio_performance()
            print_output(ret)

        elif summary_answers.get('operation') == 'Historical Dividends':
            div_questions = [
                {
                    'type': 'list',
                    'name': 'div_period',
                    'message': 'Choose Period',
                    'choices': ['Past 3 Months', 'Past 6 Months', 'Past 1 Year', 'Past 3 Years', 'Past 10 Years']
                }
            ]
            div_answers = prompt(div_questions)

            if div_answers.get('div_period') == 'Past 3 Months':
                div = qb.get_historical_dividend_income(90)
                print_dividends(div)

            elif div_answers.get('div_period') == 'Past 6 Months':
                div = qb.get_historical_dividend_income(180)
                print_dividends(div)

            elif div_answers.get('div_period') == 'Past 1 Year':
                div = qb.get_historical_dividend_income(365)
                print_dividends(div)

            elif div_answers.get('div_period') == 'Past 3 Years':
                div = qb.get_historical_dividend_income(1095)
                print_dividends(div)

            elif div_answers.get('div_period') == 'Past 10 Years':
                div = qb.get_historical_dividend_income(3650)
                print_dividends(div)

        elif summary_answers.get('operation') == 'Share in Email':
            get_recipient_email = [
                {
                    'type': 'input',
                    'name': 'email_address',
                    'message': 'What\'s your email?',
                }
            ]

            email = prompt(get_recipient_email).get('email_address')
            bal = qb.get_account_balance_summary().to_html()
            invest = qb.get_investment_summary().to_html()
            ret = qb.calculate_portfolio_performance().to_html()
            try:
                share_email.sendEmail(
                    recipient_email=email, balance=bal, investment=invest, performance=ret)
            except Exception as e:
                print(e)
                print(
                    f"THERE IS SOMETHING WRONG WITH EMAIL SHARING. Please check your mail {email}")
            else:
                print(f'\t Email has been successfully sent to {email}')

        elif summary_answers.get('operation') == 'Go to Main Menu':
            break
        elif summary_answers.get('operation') == 'Exit Program':
            quit()

    main_menu()


def rebalance_strategy():

    while True:
        strategy_questions = {
            'type': 'list',
            'name': 'strategy_type',
            'message': 'Select Allocation Strategy',
            'choices': [
                {'name': 'Vigilant Asset Allocation (VAA)'},
                {'name': 'Lethargic Asset Allocation (LAA)'},
                {'name': 'Go to Main Menu'},
                {'name': 'Exit Program'}
            ]
        }

        strategy_answer = prompt(strategy_questions)

        if strategy_answer.get('strategy_type') == 'Vigilant Asset Allocation (VAA)':
            vaa = VAA()
            decision = vaa.decision()
            print_output(decision)

        elif strategy_answer.get('strategy_type') == 'Lethargic Asset Allocation (LAA)':
            print_output(LAA.decision())

        elif strategy_answer.get('strategy_type') == 'Go to Main Menu':
            break

        elif strategy_answer.get('strategy_type') == 'Exit Program':
            quit()

    main_menu()


if __name__ == "__main__":
    os.system("clear")
    fig = Figlet(font='slant')
    print(fig.renderText("PyQuant"))
    main_menu()
