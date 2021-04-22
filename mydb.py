import mysql.connector
from datetime import datetime

with open('./credentials.txt', 'r') as fp:
    secret = fp.readlines()
    host_ip = secret[0].rstrip('\n')
    user_id = secret[1].rstrip('\n')
    pw = secret[2]

db = mysql.connector.connect(
    host="192.168.2.21",
    user="eddie",
    passwd="abc123"
)

mycursor = db.cursor()
mycursor.execute("SHOW DATABASES")
for x in mycursor:
    print(x)
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
