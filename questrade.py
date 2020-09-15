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
    #print(q.accounts)
    
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
    
    selectedKeys = ['symbol', 'symbolId', 'openQuantity', 'currentMarketValue', 'currentPrice']
    
    openPos = []
    
    for pos in q.account_positions(acctNum)['positions']:
        posInfo = {}
        for k,v in pos.items():
            if k in selectedKeys:
                posInfo[k] = v
        
        openPos.append(posInfo)
        
    
    return openPos    

def get_CAD_account_balance(acctNum):
    
    selectedKeys = ['currency','cash', 'marketValue', 'totalEquity']
    
    
    for bal in q.account_balances(acctNum)['perCurrencyBalances']:
        
        if bal['currency'] == 'CAD':    
            cadBal = {}
            for k,v in bal.items():
                print(k,v)
                if k in selectedKeys:
                    cadBal[k] = v
    
    return cadBal
                
            
    
    


#print(q.account_balances(get_account_num()[0])['perCurrencyBalances'])

    
    

get_CAD_account_balance(get_account_num()[0])

#print(q.account_positions(get_account_num()[0]))