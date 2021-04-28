import json
import requests
from mydb import db_master


def get_financial_ratios(symbol: str):

    db = db_master(symbol)

    try:
        fr = db.download_financial_ratios_to_df()
    except:
        db.upload_financial_ratios_to_sql()
        fr = db.download_financial_ratios_to_df()

    return fr

def calculate_market_cap(symbol: str) -> float:
    response = requests.get(f'https://ycharts.com/charts/fund_data.json?securities=include%3Atrue%2Cid%3A{symbol}%2C%2C&calcs=include%3Atrue%2Cid%3Amarket_cap%2C%2C&correlations=&format=real&recessions=false&zoom=5&startDate=&endDate=&chartView=&splitType=single&scaleType=linear&note=&title=&source=false&units=false&quoteLegend=true&partner=&quotes=&legendOnChart=true&securitylistSecurityId=&clientGroupLogoUrl=&displayTicker=false&ychartsLogo=&useEstimates=false&maxPoints=880')
    response = response.json()

    return response['chart_data'][0][0]['raw_data'][-1][1] / 1000

if __name__ == '__main__':

    x = calculate_market_cap('AAPL')
    print(x)