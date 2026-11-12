import uvicorn
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from fastapi import FastAPI, Depends, HTTPException
from mysql_connect import mydb
from security import verify_token, create_token

app = FastAPI()


@app.post("/login")
def login(user: OAuth2PasswordRequestForm = Depends()):

    if user.username == "ebin" and user.password == "1234":

        token = create_token(user.username)

        return {
            "access_token": token,
            "token_type": "bearer"
        }

    raise HTTPException(status_code=401, detail="Invalid username or password")


@app.get("/teams")
def read_teams(user: str = Depends(verify_token)):
    try:
        cursor = mydb.cursor()
        cursor.execute("SELECT * FROM teams")
        teams = cursor.fetchall()
        return {"teams": teams}
    except Exception:
        raise f"could not retrieve all teams!"

@app.get("/teams/{team_id}")
def read_team(team_id: int,user: str = Depends(verify_token)):
    try:
        cursor = mydb.cursor()
        cursor.execute("SELECT * FROM teams WHERE team_id = %s", (team_id,))
        team = cursor.fetchone()
        return {"team": team}
    except Exception as e:
        raise f"could not retrieve team {team_id}!"
@app.post("/teams")
def create_team(team: Team,user: str = Depends(verify_token)):
    try:
        cursor = mydb.cursor()
        cursor.execute("INSERT INTO teams VALUES (%s,%s,%s,%s)",
                       (team.team_id, team.team_name, team.country, team.coach))
        mydb.commit()
        return f"Team {team.team_id} created!"
    except Exception:
        raise f"could not create team {team.team_id}!"

@app.put("/teams/{team_id}")
def update_team(team_id: int, team: Team,user: str = Depends(verify_token)):
    try:
        cursor = mydb.cursor()
        cursor.execute("UPDATE teams SET team_name = %s ,country = %s , coach = %s WHERE team_id = %s",
                       (team_id, team.team_name, team.country, team.coach))
        mydb.commit()
        return f"Team {team_id} updated!"
    except Exception:
        raise f"could not update team {team_id}!"

@app.patch("/teams/{team_id}")
def partial_update_team(team_id: int, team: Team,user: str = Depends(verify_token)):
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
def delete_team(team_id: int,user: str = Depends(verify_token)):
    try:
        cursor = mydb.cursor()
        cursor.execute("DELETE FROM teams WHERE team_id = %s", (team_id,))
        mydb.commit()
    except Exception:
        raise f"could not delete team {team_id}!"

if __name__ == '__main__':
    uvicorn.run(app, host="localhost", port=8000)
