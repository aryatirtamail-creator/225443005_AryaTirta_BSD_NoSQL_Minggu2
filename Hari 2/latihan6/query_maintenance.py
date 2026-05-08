import os
import pandas as pd
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

client = MongoClient(os.getenv("MONGO_URI"))
db = client[os.getenv("DB_NAME")]
collection = db["maintenance"]

print("\n=== Data biaya > 1.000.000 ===")

hasil = list(collection.find(
    {"biaya": {"$gt": 1000000}},
    {"_id": 0}
))

df = pd.DataFrame(hasil)
print(df)

print("\n=== Update Teknisi ===")

update_result = collection.update_many(
    {
        "    mesin": "CNC-01",
        "biaya": 1200000
    },
    {
        "$set": {
            "teknisi": "Dewi"
        }
    }
)

print("matched:", update_result.matched_count)
print("modified:", update_result.modified_count)

print("matched:", update_result.matched_count)
print("modified:", update_result.modified_count)


print("\n=== Total biaya per bulan ===")

pipeline = [
    {
        "$group": {
            "_id": {
                "$dateToString": {
                    "format": "%Y-%m",
                    "date": "$tanggal"
                }
            },
            "total_biaya": {
                "$sum": "$biaya"
            }
        }
    },
    {
        "$sort": {
            "_id": 1
        }
    }
]

result = list(collection.aggregate(pipeline))

df_agregasi = pd.DataFrame(result)
print(df_agregasi)

client.close()
