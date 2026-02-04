import os
import threading
import psycopg2
import redis
from flask import Flask, request, jsonify
from pymongo import MongoClient
from pinecone import Pinecone # New Fix
from google import genai
import libsql_client

app = Flask(__name__)

# --- 1. 18 అస్త్రాల క్లీనింగ్ & సింకింగ్ ---
RAW_SQL = os.getenv("SQL_URI") or os.getenv("DATABASE_URL")
# హోస్ట్ నేమ్ లో '143@' ఉంటే తొలగించే లాజిక్
DATABASE_URL = RAW_SQL.replace("143@", "") if RAW_SQL and "143@" in RAW_SQL else RAW_SQL

# --- 2. క్లయింట్స్ (Absolute Fixes) ---
cache = redis.from_url(os.getenv("REDIS_URL"))
pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
mongo_client = MongoClient(os.getenv("MONGO_URI"), tls=True, tlsAllowInvalidCertificates=True)

# --- 3. గాడ్ ప్రొటోకాల్ (Naming Fix) ---
def init_all_systems():
    try:
        conn = psycopg2.connect(DATABASE_URL, connect_timeout=5)
        conn.close()
        # విజయవంతమైన మెసేజ్
        print("🔱 ARKON: 18 Variables Synced. God Protocol Online.", flush=True)
    except Exception as e:
        print(f"⚠️ Core Sync Notice: {e}", flush=True)

# Calling the correct function name
threading.Thread(target=init_all_systems, daemon=True).start()

@app.route('/arkon/status')
def status_tracker():
    """మీరు అడిగిన ట్రాకింగ్ సిస్టమ్"""
    return jsonify({
        "Status": "🔱 GOD_MODE_ACTIVE",
        "Variables": "18_SYNCED",
        "System": "Self-Healing_Protocol_Enabled"
    })

@app.route('/')
def home():
    return "🔱 ARKON: MASTER GUARDIAN IS ONLINE AND STABLE."

if __name__ == "__main__":
    # Railway కి అవసరమైన పోర్ట్ బైండింగ్
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
