import requests
import pandas as pd

url = 'https://www.quantist.co.kr/status_y1'
html = requests.get(url).content
df_list = pd.read_html(html)
#print(df_list)
df = df_list[-1]
#print(df)
#df.to_csv('my data.csv')

abc = pd.read_html(url)
#print(abc)

df = abc[0]
print(df['VAA'])
print(df.columns)