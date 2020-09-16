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
    
    for acct in q.accounts['accounts']:
        accounts.append(acct['number'])
    
    return accounts

def get_holding_symbols(acctNum):
    """
    Returns a list of symbols of holding assets
    ['VFV.TO', 'XBB.TO']
    """
    
    symbols = []
    
    for position in q.account_positions(acctNum)['positions']:
        symbols.append(position['symbol'])
    
    return symbols

def get_open_positions(acctNum): 
    """
    Returns a list of open positions with market info
    [{'symbol': 'VFV.TO', 'symbolId': 2874671, 'openQuantity': 6, 'currentMarketValue': 477.6, 'currentPrice': 79.6}, 
     {'symbol': 'XBB.TO', 'symbolId': 24003, 'openQuantity': 35, 'currentMarketValue': 1180.55, 'currentPrice': 33.73}]
    
    """
    
    selectedKeys = ['symbol', 'symbolId', 'openQuantity', 'currentMarketValue', 'currentPrice']
    
    openPos = []
    
    for pos in q.account_positions(acctNum)['positions']:
        posInfo = {}
        for k,v in pos.items():
            if k in selectedKeys:
                posInfo[k] = v
        
        openPos.append(posInfo)        
    
    return openPos    


def get_active_balance_cad(acctNum):
    """
    Returns a list of active balances in CAD
    {'currency': 'CAD', 'cash': 87.5525, 'marketValue': 1658.87, 'totalEquity': 1746.4225}
    """
    
    selectedKeys = ['currency','cash', 'marketValue', 'totalEquity']    
    
    for bal in q.account_balances(acctNum)['perCurrencyBalances']:        
        if bal['totalEquity'] != 0 and bal['currency'] == 'CAD': 
            tempCAD = {}
            for k,v in bal.items():
                if k in selectedKeys:
                    tempCAD[k] = v     

            return tempCAD

def get_active_balance_usd(acctNum):
    """
    Returns a list of active balances in USD   
    """
    
    selectedKeys = ['currency','cash', 'marketValue', 'totalEquity']   
    
    for bal in q.account_balances(acctNum)['perCurrencyBalances']:        
        if bal['totalEquity'] != 0 and bal['currency'] == 'USD': 
            tempUSD = {}
            for k,v in bal.items():
                if k in selectedKeys:
                    tempUSD[k] = v
            return tempUSD