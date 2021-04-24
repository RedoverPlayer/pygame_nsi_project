import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database="jeupygame"
)

print(mydb)
cursor = mydb.cursor()

cursor.execute(("UPDATE accounts SET KILLS = KILLS + %s, DEATHS=DEATHS+%s WHERE USERNAME = %s"), (5,2,'azerty'))

    #close the connection to the database.
mydb.commit()
cursor.close()