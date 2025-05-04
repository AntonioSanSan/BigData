from pymongo import MongoClient

def connect_to_mongo():
    # Cambia esta URI si usas MongoDB Atlas
    client = MongoClient("mongodb://localhost:27017/")
    db = client["smartretail"]
    return db