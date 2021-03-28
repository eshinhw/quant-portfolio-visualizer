import pandas as pd
import questrade as qt


class portfolio_rebalancing_calculator():    
    
    TRANSACTION_COST = 5
    
    def __init__(self, target, ACCOUNT_NUM):
        
        self.target = target
        self.symbols = target.keys()
        self.weights = target.values()
        self.totalEquity = qt.get_active_balance_cad(ACCOUNT_NUM)['totalEquity']
        self.cash = qt.get_active_balance_cad(ACCOUNT_NUM)['cash']
        self.current_positions = qt.get_open_positions(ACCOUNT_NUM)
        
        try:        
            for symbol in self.symbols:
                if qt.check_symbol_exists(symbol) == False:
                    raise Exception
        
            if sum(self.weights) < 0 or sum(self.weights) > 1:
                raise Exception
        
        except Exception:
            print('INVALID SYMBOLS OR WEIGHTS')
    
    def target_positions(self):
        
        target_holdings = []
        df = pd.DataFrame()
        
        for position in self.current_positions:
            symbol = position['symbol']
            target_holdings.append(symbol)
            
            df = df.append(position, ignore_index=True)
        
        for symbol in self.symbols:
            if symbol not in target_holdings:
                new = {}
                new['symbol'] = symbol
                new['openQuantity'] = 0
                new['currentMarketValue'] = 0
                new['currentPrice'] = qt.get_current_price(symbol)
                new['symbolId'] = qt.get_symbol_id(symbol)                
                df = df.append(new, ignore_index=True)
        
        df.set_index('symbol', inplace=True)
        df = df.rename(columns={'currentMarketValue': 'Prior Amt ($)', 
                           'currentPrice': 'Price',
                           'openQuantity': 'Qty'})
        
        df = df[['Price', 'Qty', 'Prior Amt ($)']]
        
        return df
    
    def order_calculation(self, df):
        
        for symbol in df.index:
            if symbol not in self.symbols: # we have to sell all shares of symbol
                df.loc[symbol, 'Post Amt ($)'] = 0
                df.loc[symbol,'Change in Amt'] = df.loc[symbol,'Post Amt ($)'] - df.loc[symbol,'Prior Amt ($)']  
                df.loc[symbol,'Qty Change'] = df.loc[symbol,'Change in Amt'] / df.loc[symbol,'Price']
            else:                            
                df.loc[symbol,'Post Amt ($)'] = (self.totalEquity * self.target[symbol])
                df.loc[symbol,'Change in Amt'] = df.loc[symbol,'Post Amt ($)'] - df.loc[symbol,'Prior Amt ($)']  
                df.loc[symbol,'Qty Change'] = df.loc[symbol,'Change in Amt'] / df.loc[symbol,'Price']
        
        # change datatype for certain columns        
        df = df.astype({'Qty Change': int, 'Qty': int})
        
        # sort by qty change so that we can sell some first and buy other later with more cash        
        df.sort_values(by=['Qty Change'], inplace=True)
        
        # iterate from the top to sell first and buy later with cash adjustment
        
        print(df)
        
        post_cash = self.cash
        
        for symbol in df.index:        
            qty = df.loc[symbol,'Qty Change']
            currP = df.loc[symbol, 'Price']
            
            # buying
            if qty > 0:
                buy = qty * currP
                
                if post_cash < buy:
                    new_qty = int(post_cash / currP)
                    buy = currP * new_qty
                    qty = new_qty            
                post_cash = post_cash - buy
                df.loc[symbol, 'Post Amt ($)'] = df.loc[symbol, 'Prior Amt ($)'] + buy
            
            # selling
            elif qty < 0:
                sell = (-qty) * currP
                post_cash = post_cash + sell - portfolio_rebalancing_calculator.TRANSACTION_COST
                df.loc[symbol, 'Post Amt ($)'] = df.loc[symbol, 'Prior Amt ($)'] - sell
            
            # no rebalancing
            else:
                df.loc[symbol, 'Post Amt ($)'] = df.loc[symbol, 'Prior Amt ($)']  
                
        # print("Prior " + str(post_cash))                
       
        # Minimize cash holding loop - extra distribution to available assets        
        # if post_cash > 0:
            
        #     df = df.sort_values(by=['Post Amt ($)'], ascending= True)
            
        #     for symbol in df.index:
                
        #         post_amt = df.loc[symbol, 'Post Amt ($)']
        #         symbol_price = df.loc[symbol, 'Price']
                
        #         if post_amt > 0 and post_cash > symbol_price:    
                    
        #             # newQty = int(post_cash / symbol_price)
        #             # post_cash = post_cash - (symbol_price * newQty)
        #             # df.loc[symbol, 'Qty Change'] = df.loc[symbol, 'Qty Change'] + newQty
        #             # df.loc[symbol, 'Post Amt ($)'] = df.loc[symbol, 'Post Amt ($)'] + (symbol_price * newQty)
                    
        #             df.loc[symbol, 'Qty Change'] = df.loc[symbol, 'Qty Change'] + 1
        #             post_cash = post_cash - symbol_price
        #             df.loc[symbol, 'Post Amt ($)'] = df.loc[symbol, 'Post Amt ($)'] + symbol_price

        df = df.astype({'Post Amt ($)': float})
        
        df = df.sort_values(by=['Qty Change'], ascending= True)
        
        for symbol in df.index:
            
            df.loc[symbol, 'Prior Amt (%)'] = (df.loc[symbol, 'Prior Amt ($)'] / self.totalEquity) * 100
            df.loc[symbol, 'Post Amt (%)'] = (df.loc[symbol, 'Post Amt ($)'] / self.totalEquity) * 100
            
        print("Post " + str(post_cash))
        summary = df[['Price', 'Qty', 'Prior Amt ($)', 'Prior Amt (%)', 'Post Amt ($)', 'Post Amt (%)', 'Qty Change']]
        
        return summary, post_cash

if __name__ == '__main__':
    
    acctNum = qt.get_account_num()[0]
    
    target = {'VFV.TO': 0.5, 'XBB.TO': 0.5}

    
    cal = portfolio_rebalancing_calculator(target, acctNum)
       
    df = cal.target_positions() 
    print(df)
    final, cash = cal.order_calculation(df)
    
    print(final)
            
            
    
            
        
    
    
    