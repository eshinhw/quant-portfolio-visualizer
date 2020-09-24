
def get_user_input():
    print()
    print() 
    
    print('Please choose one of the following allocation strategies below')
    print()    
    
    print('1. All Weather Portfolio')
    print('2. Conservative Portfolio')
    print('3. Balanced Portfolio')
    print('4. Growth Portfolio')
    print('5. EM Portfolio')
    print('6. International Stock Portfolio')
    print('7. Crisis 100% Cash Portfolio')
    
    choice = input('Enter: ')    
    
    switcher = {
                '1': all_weather_port(),
                '2': conservative_port(),
                '3': balanced_port(),
                '4': growth_port(),
                '5': emerging_market_port(),
                '6': international_port(),
                '7': crisis_port()}
    
    return switcher.get(choice)



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

def balanced_port():
    """
    70% in Bonds and 30% in Stocks
    """
    
    allocation = {'XBB.TO': 0.5, 'VFV.TO': 0.5}
    
    return allocation
    

def growth_port():
    """
    70% in Stocks and 30% in Bonds
    """
    
    allocation = {'XBB.TO': 0.3, 'VFV.TO': 0.7}
    
    return allocation

def emerging_market_port():
    """
    50% in EM Stocks and 50% in Bonds
    """
    
    return {'XEF.TO': 0.5, 'XBB.TO': 0.5}
    
    pass

def international_port():
    """
    50% in International Stocks and 50% in Bonds
    """
    return {'XEC.TO': 0.5, 'XBB.TO': 0.5}
    
    

def crisis_port():
    """
    100% in Cash
    No holding means sell everything and hold cash
    """
    
    return {}
    

if __name__ == '__main__':
    print('executed directly')
    print(growth_port())
    print(conservative_port())

