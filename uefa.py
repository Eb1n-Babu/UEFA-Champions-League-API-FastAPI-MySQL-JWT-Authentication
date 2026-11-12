import uvicorn
from mysql import connector
from fastapi import FastAPI,HTTPException
from pydantic import BaseModel

app = FastAPI()

mydb = connector.connect(
    host="localhost",
    user="root",
    password="@Ebinbabu2209",
    database="uefa_champions_league"
)

class Team(BaseModel):
    team_id: int | None = None
    team_name: str | None = None
    country: str | None = None
    coach: str | None = None




if mydb.is_connected():
    print("Connected successfully!")

@app.get("/teams")
def read_teams():
    try:
        cursor = mydb.cursor()
        cursor.execute("SELECT * FROM teams")
        teams = cursor.fetchall()
        return {"teams": teams}
    except Exception:
        raise f"could not retrieve all teams!"

@app.get("/teams/{team_id}")
def read_team(team_id: int):
    try:
        cursor = mydb.cursor()
        cursor.execute("SELECT * FROM teams WHERE team_id = %s", (team_id,))
        team = cursor.fetchone()
        return {"team": team}
    except Exception as e:
        raise f"could not retrieve team {team_id}!"
@app.post("/teams")
def create_team(team: Team):
    try:
        cursor = mydb.cursor()
        cursor.execute("INSERT INTO teams VALUES (%s,%s,%s,%s)",
                       (team.team_id, team.team_name, team.country, team.coach))
        mydb.commit()
        return f"Team {team.team_id} created!"
    except Exception:
        raise f"could not create team {team.team_id}!"

@app.put("/teams/{team_id}")
def update_team(team_id: int, team: Team):
    try:
        cursor = mydb.cursor()
        cursor.execute("UPDATE teams SET team_name = %s ,country = %s , coach = %s WHERE team_id = %s",
                       (team_id, team.team_name, team.country, team.coach))
        mydb.commit()
        return f"Team {team_id} updated!"
    except Exception:
        raise f"could not update team {team_id}!"

@app.patch("/teams/{team_id}")
def partial_update_team(team_id: int, team: Team):
   try:
       cursor = mydb.cursor()
       if team.team_name is not None:
           cursor.execute("UPDATE teams SET team_name = %s WHERE team_id = %s", (team.team_name, team_id))
       if team.country is not None:
           cursor.execute("UPDATE teams SET country = %s WHERE team_id = %s", (team.country, team_id))
       if team.coach is not None:
           cursor.execute("UPDATE teams SET coach = %s WHERE team_id = %s", (team.coach, team_id))
       mydb.commit()
       return f"Team {team_id} updated!"
   except Exception:
       raise f"could not update team {team_id}!"

@app.delete("/teams/{team_id}")
def delete_team(team_id: int):
    try:
        cursor = mydb.cursor()
        cursor.execute("DELETE FROM teams WHERE team_id = %s", (team_id,))
        mydb.commit()
    except Exception:
        raise f"could not delete team {team_id}!"

if __name__ == '__main__':
    uvicorn.run(app, host="localhost", port=8000)
