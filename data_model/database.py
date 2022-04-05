import json
import os
from typing import Dict, Iterable, Iterator, Optional

from MonsterLab import Monster
from pymongo import MongoClient
from pandas import DataFrame
from dotenv import load_dotenv


class MongoDB:
    load_dotenv()

    def __init__(self):
        self.url = os.getenv("MONGO_URL")
        self.database = "MonsterLab"
        self.collection = "Monsters"

    def connect(self):
        return MongoClient(self.url)[self.database][self.collection]

    def find_all(self, query_obj: Optional[Dict] = None) -> Iterator[Dict]:
        return self.connect().find(query_obj, {"_id": False})

    def insert(self, insert_obj: Dict):
        self.connect().insert_one(insert_obj)

    def insert_many(self, insert_obj: Iterable[Dict]):
        self.connect().insert_many(insert_obj)

    def update(self, query: Dict, data: Dict):
        self.connect().update_many(query, {"$set": data})

    def delete(self, query_obj: Dict):
        self.connect().delete_many(query_obj)

    def dataframe(self, query_obj: Optional[Dict] = None) -> DataFrame:
        return DataFrame(self.find_all(query_obj or {}))

    def backup(self, filename: str):
        with open(filename, "w") as file:
            json.dump(list(self.find_all()), file)

    def restore(self, filename: str):
        with open(filename, "r") as file:
            self.insert_many(json.load(file))

    def seed_db(self, amount: int):
        self.insert_many(vars(Monster()) for _ in range(amount))

    def count(self, query: Optional[Dict] = None) -> int:
        return self.connect().count_documents(query or {})

    @property
    def info(self):
        return {
            "Platform": "MongoDB",
            "Database": self.database,
            "Collection": self.collection,
            "Size": f"{self.count()} Monsters",
        }
