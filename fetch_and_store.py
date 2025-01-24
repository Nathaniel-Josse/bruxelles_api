import pandas as pd
import pymongo.collection
import requests
import pymongo
from fastapi import FastAPI
from pymongo.errors import DuplicateKeyError, BulkWriteError

def fetch_data(api_url):
    records = []
    offset = 0
    limit = 20
    while True:
        try:
            response = requests.get(f"{api_url}?limit={limit}&offset={offset}")
            response.raise_for_status()
            data = response.json()
            results = data.get("results", [])
            records.extend(results)
            if len(results) < limit:
                break
            offset += limit
        except requests.RequestException as e:
            print(f"Erreur lors de l'appel API {api_url}: {e}")
            break
    return records

def clean_data(records):
    df = pd.DataFrame(records)
    df = df.fillna("Inconnu")
    if "id" not in df.columns:
        df["id"] = range(1, len(df) + 1)
    return df.to_dict(orient="records")

def insert_into_mongo(collection: pymongo.collection.Collection, records):
    try:
        collection.insert_many(records, ordered=False)
    except BulkWriteError as e:
        print(f"Certains documents ont causé des erreurs de duplication : {e.details}")
        
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
    collection_name = url.split("/")[-2]  # Extrait le nom de la collection depuis l'URL
    print(f"Traitement de la collection: {collection_name}")
    try:
        data = fetch_data(url)
        if not data:
            print(f"Aucune donnée récupérée pour l'URL : {url}")
            continue

        cleaned_data = clean_data(data)
        collection = db[collection_name]
        insert_into_mongo(collection, cleaned_data)
        print(f"Insertion réussie pour la collection: {collection_name}")
    except BulkWriteError as bwe:
        print(f"Erreur d'insertion en masse pour {collection_name}: {bwe.details}")
    except Exception as e:
        print(f"Erreur inattendue pour {collection_name}: {e}")

print("Toutes les données ont été récupérées et insérées dans MongoDB.")