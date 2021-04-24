
import questrade as qt
import backtesting as bt

def get_description(allocation):
    
    description_list = []
    for symbol in allocation.keys():
        symbol_list = []
        description = qt.get_symbol_description(symbol)
        symbol_list.append(symbol)
        symbol_list.append(description)
        symbol_list.append(allocation[symbol])
        
        description_list.append(symbol_list)
    
    return description_list

def get_performance(allocation):

    inception_date, cagr, mdd, sharpe = bt.portfolio_measures(allocation)  
    
    return [inception_date, cagr, mdd, sharpe]

    
    
    

if __name__ == '__main__':
    print('executed directly')

