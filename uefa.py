import uvicorn
from mysql import connector
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone
from decouple import config

app = FastAPI()

SECRET_KEY = "my-secret-key-change-this"
ALGORITHM = "HS256"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def create_token(username: str):
    expire = datetime.now(timezone.utc) + timedelta(minutes=30)

    data = {
        "sub": username,
        "exp": expire
    }

    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)

@app.post("/login")
def login(user: OAuth2PasswordRequestForm = Depends()):

    if user.username == "ebin" and user.password == "1234":

        token = create_token(user.username)

        return {
            "access_token": token,
            "token_type": "bearer"
        }

    raise HTTPException(status_code=401, detail="Invalid username or password")

def verify_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        username = payload.get("sub")

        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")

        return username

    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

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
