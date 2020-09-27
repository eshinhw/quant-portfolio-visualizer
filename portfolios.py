
import questrade as qt
import backtesting as bt


def get_description(allocation):
    
    print("■ ALLOCATION PREVIEW\n")
    
    for symbol in allocation:    
        print("\t\t{} % | {} | {}".format(allocation[symbol] * 100, 
                                      symbol, 
                                      qt.get_symbol_description(symbol)))
    print()    
    print("■ HISTORICAL PERFORMANCE MEASURES\n")
    
    measures = bt.portfolio_measures(allocation)    
    
    print("\t\tCAGR: {:.2f} %".format(measures[1] * 100))
    print("\t\tVOLATILITY: {:.2f} %".format(measures[2] * 100))
    print("\t\tSHARPE RATIO: {:.2f}".format(measures[3]))
    
        
        
    

if __name__ == '__main__':
    print('executed directly')

