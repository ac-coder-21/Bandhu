from pymongo import MongoClient
from bson import ObjectId

client = MongoClient("mongodb://localhost:27017")
db = client["test_mc"]
collection = db["Project"]

data = {
    "_id": ObjectId(),
    "val": 0,
    "score": 0
}

result = collection.insert_one(data)

if result.inserted_id:
    print("Data inserted")
else:
    print("failed")