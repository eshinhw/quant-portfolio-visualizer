from __future__ import print_function, unicode_literals
from PyInquirer import prompt, print_json
import json
import os
from questrade import QuestradeBot
from credentials import QUANT_ACCOUNT_NUM, STANDARD_ACCOUNT_NUM
from pyfiglet import Figlet
from tabulate import tabulate

def add_new_account():
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

    with open('./accounts.json', 'r') as fp:
        accounts = json.load(fp)
    
    accounts[prompt(add_new_account).get('new_account_name')] = prompt(add_new_account).get('new_account_num')

    with open('./accounts.json', 'w') as fp:
        json.dump(accounts, fp)

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