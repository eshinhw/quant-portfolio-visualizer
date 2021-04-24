from mydb import db_master


def get_financial_ratios(symbol: str):

    db = db_master(symbol)

    try:
        fr = db.download_financial_ratios()
    except:
        db.upload_financial_ratios_to_sql()
        fr = db.download_financial_ratios()

    return fr


if __name__ == '__main__':

    x = get_financial_ratios('MMM')
    print(x)