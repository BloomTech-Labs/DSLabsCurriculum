""" Run this script to create a serialized model: `model.joblib` """
import time

from data_model.database import MongoDB
from machine_learning.model import Model


db = MongoDB()
print(f"Monster Count: {db.count()}\n")

print("Training from Database:")
start = time.perf_counter()
model = Model(
    df=db.dataframe(),
    target="rarity",
    features=["level", "health", "energy", "sanity"],
)
stop = time.perf_counter()
print(f"Time to Train: {stop - start:.3f}s\n")

print("Serializing and Saving Model:")
start = time.perf_counter()
model.save("model.joblib")
stop = time.perf_counter()
print(f"Time to Save: {stop - start:.3f}s\n")

print("Opening Serialized Model:")
start = time.perf_counter()
model = Model.open("model.joblib")
stop = time.perf_counter()
print(f"Time to Open: {stop - start:.3f}s\n")
