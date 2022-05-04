from __future__ import print_function, unicode_literals
from PyInquirer import prompt, print_json
import json
import os
from questrade import QuestradeBot
from credentials import QUANT_ACCOUNT_NUM, STANDARD_ACCOUNT_NUM
from pyfiglet import Figlet
from tabulate import tabulate

def load_accounts():
    if os.path.exists("./accounts.json"):
        with open('./accounts.json', 'r') as fp:
            accounts = json.load(fp)
    else:
        accounts = {}
        # default accounts which are always added
        accounts['Standard_Eddie (Default)'] = STANDARD_ACCOUNT_NUM
        accounts['Quant_Eddie (Default)'] = QUANT_ACCOUNT_NUM

        with open('./accounts.json', 'w') as fp:
            json.dump(accounts, fp)
    return accounts

def init_questrade_bot(accounts, accounts_answers):
    for account in accounts.keys():
        if account == accounts_answers.get('account'):
            try:
                qb = QuestradeBot(accounts[account])
                assert accounts[account] in qb.get_acct_id()
                return qb
            except:
                while True:
                    validation_question = [
                        {
                            'type': 'password',
                            'message': 'VALIDATION ERROR: Enter new valid access code from Questrade',
                            'name': 'access_code'
                        }
                    ]
                    new_access_code = prompt(validation_question).get('access_code')
                    #print(new_access_code)
                    qb = QuestradeBot(accounts[account], accessCode=new_access_code)
                    #print(accounts[account])
                    if qb.qtrade == 100:
                        print("ACCESS CODE IS NOT VALID. PLEASE GET A NEW ONE FROM QUESTRADE.")
                    assert accounts[account] in qb.get_acct_id()
                    return qb


def select_account():

    accounts = load_accounts()

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

        return select_account()
    
    elif accounts_answers.get('account') == 'Reset Saved Accounts':
        os.remove('./accounts.json')
        return select_account()
    
    elif accounts_answers.get('account') == 'Exit Program':
        quit()

    else:
        init_questrade_bot(accounts, accounts_answers)