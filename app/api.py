import json
import os.path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pandas import DataFrame

from data_model.database import MongoDB
from data_model.graphs import pie_chart
from data_model.schema import MonsterModel
from machine_learning.model import Model

API = FastAPI(
    title="Data Science API",
    version="0.0.1",
    docs_url="/",
    description="<h2>Full Description</h2>",
)
API.mongo = MongoDB()
API.model = Model.open(os.path.join("machine_learning", "model.joblib"))
API.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
API.info = {
    "Platform": "FastAPI",
    "Title": API.title,
    "Version": API.version,
    "Docs URL": API.docs_url,
}


@API.get("/info")
async def info():
    """ Returns json: API, Model & Database Info """
    return {
        "Web API": API.info,
        "ML Model": API.model.info,
        "Database": API.mongo.info,
    }


@API.get("/database/findall")
async def find_all_monsters():
    """ Returns all Monsters from the Collection as an Array of JSON Objects """
    return tuple(API.mongo.find_all())


@API.post("/database/insert")
async def insert_monster(monster: MonsterModel):
    """ Inserts one Custom Monster into the Collection

    Monster Schema: {
        "name": String,
        "type": String,
        "level": Integer(range[1, 20]),
        "rarity": String,
        "damage": String,
        "health": Float,
        "energy": Float,
        "sanity": Float,
        "time_stamp": String(format[YYYY-MM-DD H:M:S])
    }"""
    API.mongo.insert(vars(monster))
    return await info()


@API.post("/database/seed")
async def seed(amount: int):
    API.mongo.seed_db(amount)
    return {"result": "success"}


@API.get("/database/chart/count/type")
async def chart_count_type():
    df_type = DataFrame(API.mongo.connect().find(
        filter={},
        projection={"_id": False, "type": True},
    ))
    type_value_counts = df_type["type"].value_counts()
    chart = pie_chart(
        title="Monster Count by Type",
        labels=type_value_counts.index,
        values=type_value_counts.values,
    )
    return json.loads(chart.to_json())


@API.delete("/database/delete")
async def delete():
    API.mongo.delete({})
    return {"result": "success"}
