import json
from pymongo import MongoClient

def load_seed_data(json_path="seed_data.json", db_name="smartretail", collection_name="sales"):
    # Conexión a MongoDB local
    client = MongoClient("mongodb://localhost:27017/")
    db = client[db_name]
    collection = db[collection_name]

    # Limpiar colección anterior (opcional)
    collection.delete_many({})

    # Cargar datos desde JSON
    with open(json_path, "r", encoding="utf-8") as f:
        seed_data = json.load(f)

    # Insertar en la base de datos
    result = collection.insert_many(seed_data)
    print(f"✅ {len(result.inserted_ids)} documentos insertados en '{db_name}.{collection_name}'.")

if __name__ == "__main__":
    load_seed_data()
