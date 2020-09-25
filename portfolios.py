import sys

DIVIDER = "=" * 27

def get_user_input():
 
    
    while (1):    
        
        print(DIVIDER)
        print("MODEL PORTFOLIO SELECTION")
        print(DIVIDER)
        print() 
        
        print('1. Balanced Portfolio')
        print('2. EM Portfolio')
        print('3. International Stock Portfolio')
        print('4. Crisis 100% Cash Portfolio')
        print('0. Exit')
        
        port_choice = input('Selection: ')
        
        if port_choice == '0':
            print("GOODBYE!")
            sys.exit()
        
        elif port_choice == '1':
            balanced_port.description()
        
        elif port_choice == '2':
            emerging_market_port.description()
            
        elif port_choice == '3':
            international_port.description() 
            
        elif port_choice == '4':
            crisis_port.description() 
        
        print()
        print("Would you like to proceed? [Y/N]")
        
        proceed = input('Selection: ')
        
        if proceed == 'Y' or proceed == 'y':        
        
            allocation = {
                    '1': balanced_port.get_allocation(),
                    '2': emerging_market_port.get_allocation(),
                    '3': international_port.get_allocation(),
                    '4': crisis_port.get_allocation()}
            
            return allocation.get(port_choice)
        
        elif proceed == 'N' or proceed == 'n':
            continue


class balanced_port():
    """
    50% in Bonds and 50% in Stocks
    """
    def description():
        print()
        print(DIVIDER)
        print("BALANCED PORTFOLIO DESCRIPTION")
        print(DIVIDER)
        des = "50% in Bonds and 50% in Stocks"
        print(des)
    
    def get_allocation():
        return {'model': 'Balanced Portfolio', 'XBB.TO': 0.5, 'VFV.TO': 0.5}
    

class emerging_market_port():
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

class international_port():
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

class crisis_port():
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

