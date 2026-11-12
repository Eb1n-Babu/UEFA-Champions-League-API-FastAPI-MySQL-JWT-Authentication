from pydantic import BaseModel


class Team(BaseModel):
    team_id: int | None = None
    team_name: str | None = None
    country: str | None = None
    coach: str | None = None
