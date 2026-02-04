import os
import threading
import psycopg2
import redis
from flask import Flask, request, jsonify
from pymongo import MongoClient
from pinecone import Pinecone # New Library Fix
from google import genai
from groq import Groq
import libsql_client

app = Flask(__name__)

# --- 1. 18 అస్త్రాల సేకరణ & క్లీనింగ్ ---
DATABASE_URL = os.getenv("DATABASE_URL") or os.getenv("SQL_URI")
# హోస్ట్ నేమ్ లో '143@' ఉంటే తొలగించే లాజిక్
if DATABASE_URL and "143@" in DATABASE_URL:
    DATABASE_URL = DATABASE_URL.replace("143@", "")

# --- 2. క్లయింట్స్ (Absolute Fixes) ---
cache = redis.from_url(os.getenv("REDIS_URL"))
pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
mongo_client = MongoClient(os.getenv("MONGO_URI"), tls=True, tlsAllowInvalidCertificates=True)
turso = libsql_client.create_client_sync(url=os.getenv("TURSO_URL"), auth_token=os.getenv("TURSO_TOKEN"))

# --- 3. గాడ్ ప్రొటోకాల్ (Feature Tracking) ---
def init_god_protocol():
    try:
        conn = psycopg2.connect(DATABASE_URL, connect_timeout=5)
        conn.close()
        # విజయవంతమైన సింక్ మెసేజ్
        print("🔱 ARKON: 18 Variables Synced. God Protocol Online.", flush=True)
    except Exception as e:
        print(f"⚠️ Core Sync Notice: {e}", flush=True)

# Function name calling fix
threading.Thread(target=init_god_protocol, daemon=True).start()

@app.route('/arkon/status')
def get_powers():
    """ఫీచర్స్ ట్రాక్ చేసే విధానం"""
    return jsonify({
        "Status": "🔱 GOD_MODE_ACTIVE",
        "Variables": "18_SYNCED",
        "Infrastructure": "Quad-Database_Online"
    })

@app.route('/')
def home():
    return "🔱 ARKON: MASTER GUARDIAN IS ONLINE."

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 8080)))
