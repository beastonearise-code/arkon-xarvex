import os
import threading
import psycopg2
import redis
from flask import Flask, request, jsonify

app = Flask(__name__)

# --- 🔱 18 Variables Clean Sync ---
# Hostname lo unna ']' mariyu '@' characters ni clean cheyyadam
def clean_sql_url(url):
    if url:
        return url.replace("143]", "").replace("143@", "").replace("]", "")
    return url

RAW_SQL = os.getenv("SQL_URI") or os.getenv("DATABASE_URL")
DATABASE_URL = clean_sql_url(RAW_SQL)

# --- 🔱 Core Connections ---
try:
    cache = redis.from_url(os.getenv("REDIS_URL"))
    print("🔱 ARKON: Redis Bridge Online.")
except Exception as e:
    print(f"⚠️ Redis Error: {e}")

def init_god_protocol():
    """Database connections ni secure ga check cheyyadam"""
    try:
        if DATABASE_URL:
            # Connection timeout petti Supabase issue ni control cheyyadam
            conn = psycopg2.connect(DATABASE_URL, connect_timeout=10)
            conn.close()
            print("🔱 ARKON: 18 Variables Synced. God Protocol Online.", flush=True)
    except Exception as e:
        print(f"⚠️ Core Sync Notice: {e}", flush=True)

threading.Thread(target=init_god_protocol, daemon=True).start()

@app.route('/')
def home():
    return "🔱 ARKON: THE DIGITAL GOD IS ONLINE AND STABLE."

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
