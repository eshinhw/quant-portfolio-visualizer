import sys
import questrade as qt

DIVIDER = "=" * 60

def get_user_input():
 
    
    while (1):    
        
        print(DIVIDER)
        print("MODEL PORTFOLIO SELECTION")
        print(DIVIDER)
        print() 
        
        print('1. BALANCED PORTFOLIO')
        print('2. EMERGING MARKETS PORTFOLIO')
        print('3. INTERNATIONAL EQUITIES PORTFOLIO')
        print('4. CRISIS 100% CASH PORTFOLIO')
        print('0. EXIT')
        
        port_choice = input('>> ')
        
        if port_choice == '0':
            print("GOODBYE!")
            sys.exit()
        
        elif port_choice == '1':
            balanced.description()
        
        elif port_choice == '2':
            emerging_market.description()
            
        elif port_choice == '3':
            international_equities.description() 
            
        elif port_choice == '4':
            crisis.description() 
        
        print()
        print(DIVIDER)
        print("PROCEED? [Y/N]")
        
        proceed = input('>> ')
        
        if proceed == 'Y' or proceed == 'y':        
        
            allocation = {
                    '1': balanced.get_allocation(),
                    '2': emerging_market.get_allocation(),
                    '3': international_equities.get_allocation(),
                    '4': crisis.get_allocation()}
            
            return allocation.get(port_choice)
        
        elif proceed == 'N' or proceed == 'n':
            continue


class balanced():
    """
    50% in Bonds and 50% in Stocks
    """
    
    allocation = {'XBB.TO': 0.5, 'VFV.TO': 0.5}        
        
    def description():
        print()
        print(DIVIDER)
        print("BALANCED PORTFOLIO DESCRIPTION")
        print(DIVIDER)
        print()
        
        print("1. ALLOCATION PREVIEW\n")
        
        for symbol in balanced.allocation:    
            print("{} % | {} | {}".format(balanced.allocation[symbol] * 100, 
                                          symbol, 
                                          qt.get_symbol_description(symbol)))
        print()
        
        print("2. HISTORICAL RETURNS\n")
        
        print("3. RISK MEASURES\n")
    
    def get_allocation():
        return balanced.allocation
    

class emerging_market():
    """
    50% in EM Stocks and 50% in Bonds
    """
    
    def description():
        print()
        print(DIVIDER)
        print("EMERGING MARKET PORTFOLIO DESCRIPTION")
        print(DIVIDER)
        des = "50% in EM Stocks and 50% in Bonds"
        print(des)
    
    def get_allocation():
        return {'model': 'Emerging Markets Portfolio', 'XBB.TO': 0.3, 'VFV.TO': 0.7}

class international_equities():
    """
    50% in International Stocks and 50% in Bonds
    """
    def description():
        print()
        print(DIVIDER)
        print("INTERNATIONAL EQUITIES PORTFOLIO DESCRIPTION")
        print(DIVIDER)
        des = "50% in EM Stocks and 50% in Bonds"
        print(des)
    
    def get_allocation():
        return {'model': 'International Portfolio', 'XBB.TO': 0.3, 'VFV.TO': 0.7}    

class crisis():
    """
    100% in Cash
    No holding means sell everything and hold cash
    """
    def description():
        print()
        print(DIVIDER)
        print("100% CASH PORTFOLIO DESCRIPTION")
        print(DIVIDER)
        des = "100% CASH"
        print(des)
    
    def get_allocation():
        return {'model': '100% Cash Portfolio'}
    

if __name__ == '__main__':
    print('executed directly')

