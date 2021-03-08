import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import yfinance as yf
import datetime as dt
import pandas_datareader.data as web


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

symbol = 'jnj'
symbol = symbol.upper()

symbol2 = 'FB'

symbol3 = 'AMZN'

# data = yf.Ticker(symbol)

# historical_prices = data.history(action=True)

# historical_prices.remove_index(inplace=True)

# print(historical_prices)
START_DATE = dt.datetime(2010, 1, 1)
df = web.DataReader(symbol, 'yahoo', START_DATE, dt.datetime.today())

# df.remove_index(inplace=True)
print(df)


fig = go.Figure(
    
    data = [
        
        go.Candlestick(
            
            x = df.index,
            low = df['Low'],
            high = df['High'],
            close = df['Close'],
            open = df['Open']           
            
            
            )
        
        ]
    
    
    )

# figure.show()


# fig = px.line(historical_prices, x='Open', y="Close")
# fig.show()




app.layout = html.Div(children=[
    html.H1(children='Dividend Investing Dashboard'),
    html.Div(['Stock Symbol: ', 
              dcc.Input(id='symbol-input',value='MTL', type='text')]),
    html.Br(),
    html.Div(id='symbol-output'),   
    
    html.Div(dcc.Graph(figure=fig))
    
    
])

@app.callback(
    Output(component_id='symbol-output', component_property='children'),
    [Input(component_id='symbol-input', component_property='value')]
)

def update_output_div(input_value):
    return 'Output: {}'.format(input_value)



if __name__ == '__main__':
    app.run_server(debug=True)