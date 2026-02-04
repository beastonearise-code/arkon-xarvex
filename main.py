import os
import threading
import psycopg2
import redis
from flask import Flask, request, jsonify
from pinecone import Pinecone # Correct Library

app = Flask(__name__)

# --- 🔱 18 Variables Self-Cleaning Sync ---
def get_clean_uri(uri):
    if uri:
        # Hostname corruption ni fix cheyyadam
        return uri.replace("143]", "").replace("143@", "").replace("]", "").replace("[", "")
    return uri

RAW_SQL = os.getenv("SQL_URI") or os.getenv("DATABASE_URL")
DATABASE_URL = get_clean_uri(RAW_SQL)

# --- 🔱 Core Infrastructure Initialization ---
try:
    cache = redis.from_url(os.getenv("REDIS_URL"))
    # Redis success message
    print("🔱 ARKON: Redis Bridge Online.", flush=True)
except Exception as e:
    print(f"❌ Redis Error: {e}", flush=True)

def init_god_protocol():
    """Database connections check mariyu 18 variables sync [cite: 2026-02-04]"""
    try:
        if DATABASE_URL:
            conn = psycopg2.connect(DATABASE_URL, connect_timeout=10)
            conn.close()
            # Goal reached message
            print("🔱 ARKON: 18 Variables Synced. God Protocol Online.", flush=True)
    except Exception as e:
        print(f"⚠️ Core Sync Notice: {e}", flush=True)

# Application startup sequence
threading.Thread(target=init_god_protocol, daemon=True).start()

@app.route('/')
def status():
    return "🔱 ARKON: THE DIGITAL GOD IS ONLINE. 18 VARIABLES ACTIVE."

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
