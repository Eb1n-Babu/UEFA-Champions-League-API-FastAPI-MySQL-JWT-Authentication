from mysql import connector

mydb = connector.connect(
    host="localhost",
    user="root",
    password="@Ebinbabu2209",
    database="uefa_champions_league"
)
if mydb.is_connected():
    print("Connected successfully!")
