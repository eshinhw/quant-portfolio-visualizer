from questrade_api import Questrade

#================================================================
# Questrade Account Information Importer
#================================================================

q = Questrade()



def get_account_num():
    """
    Returns a list of account numbers associated with API key
    """
    
    accounts = []
    print(q.accounts)
    
    for acct in q.accounts['accounts']:
        accounts.append(acct['number'])
    
    return accounts


def get_holding_symbols(acctNum):
    """
    Returns a list of symbols of holding assets
    """
    
    symbols = []
    
    for position in q.account_positions(acctNum)['positions']:
        symbols.append(position['symbol'])
    
    return symbols

def get_open_positions(acctNum):
    pass

def get_account_balance():
    pass




    
    

get_holding_symbols(get_account_num()[0])

