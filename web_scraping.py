import requests
from bs4 import BeautifulSoup

url = "https://seekingalpha.com/symbol/JPM/dividends/scorecard"

session = requests.Session()

headers = {'User-Agent': 'Mozilla/5.0'} #(Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'}

# resp = session.get(url, headers=headers)

# print(resp)



# print(requests.get(url, headers=headers))

r = requests.get(url, proxies={'http':'50.207.31.221:80'}).text

print(r)