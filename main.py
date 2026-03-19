from flask import Flask, jsonify, request
from pymongo import MongoClient
import os

app = Flask(__name__)

# --- CONFIGURAZIONE ---
# MongoDB Atlas URI (username, password, cluster)
MONGO_URI = os.getenv("MONGO_URI", "mongodb+srv://brothailovearch_db_user:aAq12dX4SZ360Ufs@mskev.rkz2eug.mongodb.net/")
# Database e Collection
DB_NAME = "MSKEV"
COLLECTION = "MSKSTATS"
# Protezione API
API_KEY = os.getenv("API_KEY", "MSK_!8373488rF29@*")

# Connessione a MongoDB
client = MongoClient(MONGO_URI)
db = client[DB_NAME]
collection = db[COLLECTION]

@app.route("/all_users")
def all_users():
    # Controllo API Key
    key = request.args.get("key")
    if key != API_KEY:
        return jsonify({"error":"Invalid API Key"}), 403

    users_data = {}
    # Recupera tutti i documenti
    for doc in collection.find({}):
        doc_id = doc["_id"]
        if doc_id.startswith("latest:"):
            username = doc_id.split("latest:")[1]
            users_data[username] = doc.get("data",{})
    return jsonify(users_data)

if __name__=="__main__":
    # Porta configurabile via ambiente, default 5000
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)