
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
    
    inception_date, cagr, mdd, sharpe = bt.portfolio_measures(allocation)    
    
    print(helper.INDENT + "COMPOUNDED ANNUAL GROWTH RATE (CAGR): {:.2f} %".format(cagr * 100))
    print(helper.INDENT + "MAXIMUM DRAWDOWN (MDD): {:.2f} %".format(mdd * 100))
    print(helper.INDENT + "SHARPE RATIO: {:.2f}".format(sharpe))



        
        
    

if __name__ == '__main__':
    print('executed directly')

