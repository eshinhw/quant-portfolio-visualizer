import requests as rq
from bs4 import BeautifulSoup

url = 'https://finviz.com/screener.ashx?v=111&f=cap_large,fa_div_o3,idx_sp500,ta_sma200_pa,ta_sma50_pa'
data = rq.get(url)
data