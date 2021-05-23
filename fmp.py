import json
import secret
import requests
import mysql.connector


API_KEY = secret.FMP_API_KEYS
DB_PW = secret.DB_PASSWORDD


mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password=DB_PW
)

mycursor = mydb.cursor()

mycursor.execute("CREATE DATABASE mydatabase")


# def company_profile():

#     data =

