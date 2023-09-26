import pymysql

con = pymysql.connect(user="root", passwd="mysql123", host="127.0.0.1", db="shop", charset="utf8")

mycursur = con.cursor()
