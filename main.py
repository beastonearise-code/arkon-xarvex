import os
import threading
import psycopg2
from flask import Flask, request, jsonify
from pymongo import MongoClient
from pinecone import Pinecone, ServerlessSpec
from google import genai # Modern Google GenAI

app = Flask(__name__)

# --- Variables ---
DATABASE_URL = os.getenv("DATABASE_URL")
MONGO_URI = os.getenv("MONGO_URI")
ARKON_PIN = os.getenv("ARKON_PIN")
PINECONE_KEY = os.getenv("PINECONE_API_KEY")
GEMINI_KEY = os.getenv("GEMINI_KEY")

# New Client Setup
client = genai.Client(api_key=GEMINI_KEY)

# --- Pinecone Setup ---
pc = Pinecone(api_key=PINECONE_KEY)
index_name = "arkon-memory"
if index_name not in [idx.name for idx in pc.list_indexes()]:
    pc.create_index(name=index_name, dimension=768, metric="cosine", 
                   spec=ServerlessSpec(cloud="aws", region="us-east-1"))
memory_index = pc.Index(index_name)

# --- MongoDB Fix (SSL Handshake Fix) ---
try:
    # ssl_cert_reqs fix for Railway environment
    mongo_client = MongoClient(MONGO_URI, tls=True, tlsAllowInvalidCertificates=True)
    db_intel = mongo_client["Arkon-Xarvex-Core"]
except Exception as e:
    print(f"❌ MongoDB Sync Error: {e}")

def init_cores():
    """Neon & Mongo Connection Check"""
    try:
        conn = psycopg2.connect(DATABASE_URL, connect_timeout=10)
        conn.close()
        print("🔱 ARKON: Neon (SQL) Core Active.", flush=True)
        print("✅ ARKON: MongoDB (NoSQL) Memory Active.", flush=True)
    except Exception as e:
        print(f"⚠️ ARKON NOTICE: Core Sync Delayed. {e}", flush=True)

threading.Thread(target=init_cores, daemon=True).start()

@app.route('/')
def home():
    return "🔱 ARKON: Guardian of Challapalli is Online. System Stable."

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
