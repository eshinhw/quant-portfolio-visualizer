

def all_weather_port():
    """
    Replicate of Bridgewater's All Weather Strategy
    """
    
    allocation = {'TLT': 0.4, 'SPY': 0.3, 'IEF': 0.15, 'GLD': 0.075, 'DBC': 0.075}
    
    return allocation

def conservative_port():
    """
    70% in Bonds and 30% in Stocks
    """
    
    allocation = {'XBB.TO': 0.7, 'VFV.TO': 0.3}
    
    return allocation
    

def growth_port():
    """
    70% in Stocks and 30% in Bonds
    """
    
    allocation = {'XBB.TO': 0.3, 'VFV.TO': 0.7}
    
    return allocation

def permanent_port():
    """
    25% in Stocks, 50% in Fixed Income and 25% in Comodities
    """
    
    

def crisis_port():
    """
    100% in Cash
    No holding means sell everything and hold cash
    """
    
    return {}
    
    

