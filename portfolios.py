
import questrade as qt
import backtesting as bt
import helper


def get_description(allocation):
    
    print("■ ALLOCATION PREVIEW\n")
    
    for symbol in allocation:    
        print(helper.INDENT + "{} % | {} | {}".format(allocation[symbol] * 100, 
                                      symbol, 
                                      qt.get_symbol_description(symbol)))
    print()    
    print("■ HISTORICAL PERFORMANCE MEASURES\n")
    
    measures = bt.portfolio_measures(allocation)    
    
    print(helper.INDENT + "CAGR: {:.2f} %".format(measures[1] * 100))
    print(helper.INDENT + "VOLATILITY: {:.2f} %".format(measures[2] * 100))
    print(helper.INDENT + "SHARPE RATIO: {:.2f}".format(measures[3]))
    
        
        
    

if __name__ == '__main__':
    print('executed directly')

