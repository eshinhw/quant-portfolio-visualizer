import requests
from bs4 import BeautifulSoup

url = "https://seekingalpha.com/symbol/JPM/dividends/scorecard"



with open(url, 'r') as html_file:
    content = html_file.read()
    soup = BeautifulSoup(content, 'lxml')
    print(soup.prettify())