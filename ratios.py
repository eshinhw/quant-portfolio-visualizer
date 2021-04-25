from mydb import db_master


def get_financial_ratios(symbol: str):

    db = db_master(symbol)

    try:
        fr = db.download_financial_ratios_to_df()
    except:
        db.upload_financial_ratios_to_sql()
        fr = db.download_financial_ratios_to_df()

    return fr


if __name__ == '__main__':
    db = db_master('aapl')
    db.upload_financial_ratios_to_sql()
    x = get_financial_ratios('aapl')
    print(x)