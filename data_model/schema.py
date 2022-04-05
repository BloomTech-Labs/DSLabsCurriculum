from typing import Optional

from pydantic import BaseModel, validator


class LevelRangeError(Exception):

    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(message)


class MonsterModel(BaseModel):
    name: str
    type: str
    level: int
    rarity: str
    damage: str
    health: float
    energy: float
    sanity: float
    time_stamp: str

    @validator("level")
    @classmethod
    def validate_level(cls, level: int):
        if level not in range(1, 21):
            raise LevelRangeError(
                message=f"Level: {level}, outside acceptable range[1, 20]",
            )
        return level


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
