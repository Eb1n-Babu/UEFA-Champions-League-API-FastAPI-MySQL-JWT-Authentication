import uvicorn
from mysql import connector
from fastapi import FastAPI

app = FastAPI()

mydb = connector.connect(
    host="localhost",
    user="root",
    password="@Ebinbabu2209",
    database="uefa_champions_league"
)

if mydb.is_connected():
    print("Connected successfully!")

@app.get("/teams")
def read_teams():
    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM teams")
    teams = cursor.fetchall()
    return {"teams": teams}


if __name__ == '__main__':
    uvicorn.run(app, host="localhost", port=8000)
