import mysql.connector
import datetime as dt
import yfinance as yf
import pandas_datareader.data as web
import sqlalchemy
import pandas as pd

with open('./credentials.txt', 'r') as fp:
    secret = fp.readlines()
    host_ip = secret[0].rstrip('\n')
    user_id = secret[1].rstrip('\n')
    pw = secret[2]
    fp.close()

db = mysql.connector.connect(
    host = host_ip,
    user = user_id,
    passwd = pw,
    db = 'financial_data'
)

mycursor = db.cursor()
# mycursor.execute("SHOW DATABASES")
# for x in mycursor:
#     print(x)

# engine=sqlalchemy.create_engine('mysql://')
start_date = (dt.date.today() - dt.timedelta(days=5)).strftime("%Y-%m-%d")
end_date = dt.date.today().strftime("%Y-%m-%d")

creds = {'usr': user_id,
            'pwd': pw,
            'hst': host_ip,
            'prt': 3306,
            'dbn': 'financial_data'}
# MySQL conection string.
connstr = 'mysql+mysqlconnector://{usr}:{pwd}@{hst}:{prt}/{dbn}'
# Create sqlalchemy engine for MySQL connection.
engine = sqlalchemy.create_engine(connstr.format(**creds))

#price_data = web.DataReader('MMM', 'yahoo', start_date, end_date)

# print(prices)

# print(type(prices['Open'].iloc[-1]))
symbol = 'MMM'
# mycursor.execute('USE financial_data')
# mycursor.execute("CREATE TABLE MMM (Date datetime, Open float, High float, Low float, Close float, Volume int, Dividends float)")

# db.commit()

mycursor.execute("SELECT * FROM MMM")

# print(mycursor.fetchall())

new = pd.DataFrame(mycursor.fetchall(), columns=['Date', 'Open', 'High', 'Low', 'Close', 'Volume', 'Dividends'])

print(new)
# mycursor.execute("SHOW TABLES")
# for x in mycursor:
#     print(x)
# prices = yf.Ticker(symbol).history(period='max')
# prices.reset_index(inplace=True)

# prices.to_sql(name='MMM', con=engine, if_exists='replace', index=False)

# for i, row in prices.iterrows():
#     print(i,tuple(row))

#mycursor.execute("CREATE TABLE Person (name VARCHAR(255), age smallint UNSIGNED, personID int PRIMARY KEY AUTO_INCREMENT)")
#mycursor.execute("DESCRIBE Person")
# mycursor.execute("INSERT INTO Person (name, age) VALUES (%s,%s)", ("Joe", 22))

# db.commit()

# mycursor.execute("SELECT * FROM Person")
# for x in mycursor:
#     print(x)

#mycursor.execute("CREATE TABLE Test (name VARCHAR(50) NOT NULL, created datetime NOT NULL, gender ENUM('M', 'F', 'O') NOT NULL, ID int PRIMARY KEY NOT NULL AUTO_INCREMENT)")

# mycursor.execute("INSERT INTO Test (name, created, gender) VALUES (%s,%s,%s)", ('Kimmy', datetime.now(), 'F'))
# db.commit()

# mycursor.execute("DESCRIBE Test")
# mycursor.execute("SELECT * FROM Test WHERE gender = 'M'")

# for x in mycursor:
#     print(x)

#mycursor.execute("ALTER TABLE Test ADD COLUMN food VARCHAR(50) NOT NULL")

# mycursor.execute("ALTER TABLE Test CHANGE name first_name VARCHAR(50)")


# print(mycursor.fetchall())

#mycursor.execute("ALTER TABLE Test DROP food")

# mycursor.execute("DESCRIBE Test")

# for x in mycursor:
#     print(x)

# Q1 = "CREATE TABLE Users (id int PRIMARY KEY AUTO_INCREMENT, name VARCHAR(50), passwd VARCHAR(50))"
# Q2 = "CREATE TABLE Scores (userId int PRIMARY KEY, FOREIGN KEY(userId) REFERENCES Users(id), game1 int DEFAULT 0, game2 int DEFAULT 0)"

# # mycursor.execute(Q1)
# #mycursor.execute(Q2)

# mycursor.execute("SHOW TABLES")

# for x in mycursor:
#     print(x)
