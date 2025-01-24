import pymongo.collection
import pymongo
from fastapi import FastAPI

app = FastAPI()
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["opendata_brussels"]

@app.get("/")
async def list_collections():
    collections = db.list_collection_names()
    return {"collections": collections}

@app.get("/{collection_name}/search")
def search_data(collection_name: str, field: str, value: str):
    collection = db[collection_name]
    results = collection.find({field: value}, {"_id": 0})
    return list(results)

@app.get("/{collection_name}/stats")
def get_stats(collection_name: str):
    collection = db[collection_name]
    count = collection.count_documents({})
    return {"total_records": count}

@app.get("/{collection_name}/")
def get_data(collection_name: str):
    collection = db[collection_name]
    results = collection.find({}, {"_id": 0})
    return list(results)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)