import pandas as pd
import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

client = MongoClient(os.getenv("MONGO_URI"))
db = client[os.getenv("DB_NAME")]
collection = db["maintenance"]


df = pd.read_csv("maintenance.csv")


df["tanggal"] = pd.to_datetime(df["tanggal"])


data = df.to_dict("records")


result = collection.insert_many(data)

print("Data berhasil diimport")
print("Jumlah data:", len(result.inserted_ids))