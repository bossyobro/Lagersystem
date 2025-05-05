import mysql.connector

dbconn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="key",
    database="lager"
)

mycursor = dbconn.cursor()

if (dbconn):
    print("Yippie!")
else:
    print("Oh no!!!")

