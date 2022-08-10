from typing import Optional

from pydantic import BaseModel, validator, conint


class LevelRangeError(Exception):

    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(message)


class MonsterModel(BaseModel):
    name: str
    type: str
    level: conint(ge=1, le=20)
    rarity: str
    damage: str
    health: float
    energy: float
    sanity: float
    time_stamp: str


class MonsterQueryModel(BaseModel):
    name: Optional[str]
    type: Optional[str]
    level: Optional[int]
    rarity: Optional[str]
    damage: Optional[str]
    health: Optional[float]
    energy: Optional[float]
    sanity: Optional[float]
    time_stamp: Optional[str]
