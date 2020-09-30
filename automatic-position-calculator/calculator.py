import pandas as pd
import questrade as qt
import sys


TRANSACTION_COST = 5


class portfolio_rebalancing_calculator():
    
    TRANSACTION_COST = 5
    
    def __init__(self, symbols, weights):
        
        self.symbols = symbols
        self.weights = weights
    
    def valid_input():
        
        for symbol in self.symbols:
            if qt.check_symbol_exists(symbol) == False:
                print('{} | NON-TRADABLE SYMBOL'.format(symbol))
                sys.exit()
        
        if sum(self.weights) < 0 or sum(self.weights) > 1:
            print('INVALID INPUT')
            sys.exit()
    
    
            
            
            
    
            
        
    
    
    