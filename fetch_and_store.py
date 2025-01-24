import pandas as pd
import pymongo.collection
import requests
import pymongo
from fastapi import FastAPI
from pymongo.errors import DuplicateKeyError

def fetch_data(api_url):
    records = []
    offset = 0
    limit = 20
    while True:
        try:
            response = requests.get(f"{api_url}?limit={limit}&offset={offset}")
            response.raise_for_status()
            data = response.json()
            records.extend(data.get("records", []))
            if len(data.get("records", [])) < limit:
                break
            offset += limit
        except requests.RequestException as e:
            print(f"Erreur lors de l'appel API {api_url}: {e}")
            break
    return records

def clean_data(records):
    df = pd.DataFrame(records)
    df = df.drop_duplicates()
    df = df.fillna("Inconnu")
    return df.to_dict("records")

def insert_into_mongo(collection: pymongo.collection.Collection, records):
    for record in records:
        try:
            collection.insert_one(record)
        except DuplicateKeyError:
            pass  # Ignorer les doublons
        
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["opendata_brussels"]

API_URLS = [
    "https://opendata.brussels.be/api/explore/v2.1/catalog/datasets/bruxelles_arbres_remarquables/records",
    "https://opendata.brussels.be/api/explore/v2.1/catalog/datasets/bruxelles_parcours_bd/records",
    "https://opendata.brussels.be/api/explore/v2.1/catalog/datasets/musees-a-bruxelles/records",
    "https://opendata.brussels.be/api/explore/v2.1/catalog/datasets/bruxelles_parcs_et_jardins/records",
    "https://opendata.brussels.be/api/explore/v2.1/catalog/datasets/streetart/records"
]

for url in API_URLS:
    collection_name = url.split("/")[-2]
    print(f"Traitement de la collection: {collection_name}")
    data = fetch_data(url)
    cleaned_data = clean_data(data)
    collection = db[collection_name]
    collection.create_index("id", unique=True)  # Empêcher les doublons par ID
    insert_into_mongo(collection, cleaned_data)

print("Toutes les données ont été récupérées et insérées dans MongoDB.")