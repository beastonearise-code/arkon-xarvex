import os
import threading
import psycopg2
import redis
from flask import Flask, request, jsonify
from pymongo import MongoClient
from google import genai
from groq import Groq
from openai import OpenAI
import libsql_client

app = Flask(__name__)

# --- రక్షణ వలయం: 18 వేరియబుల్స్ సేకరణ ---
DATABASE_URL = os.getenv("DATABASE_URL") or os.getenv("SQL_URI")
MONGO_URI = os.getenv("MONGO_URI")
REDIS_URL = os.getenv("REDIS_URL")
TURSO_URL = os.getenv("TURSO_URL") # https:// ఉండాలి
TURSO_TOKEN = os.getenv("TURSO_TOKEN")
ARKON_PIN = os.getenv("ARKON_PIN")

# AI Brains
GEMINI_KEY = os.getenv("GEMINI_KEY")
GROQ_KEY = os.getenv("GROQ_KEY")
OPENROUTER_KEY = os.getenv("OPENROUTER_KEY")

# --- క్లయింట్స్ సెటప్ ---
# MongoDB SSL ఫిక్స్
mongo_client = MongoClient(MONGO_URI, tls=True, tlsAllowInvalidCertificates=True)
db_core = mongo_client["Arkon-Xarvex-Core"]
cache = redis.from_url(REDIS_URL)
gemini = genai.Client(api_key=GEMINI_KEY)
turso = libsql_client.create_client_sync(url=TURSO_URL, auth_token=TURSO_TOKEN)

def init_all_cores():
    """18 అస్త్రాల సింకింగ్ ప్రొటోకాల్ [cite: 2026-02-04]"""
    try:
        conn = psycopg2.connect(DATABASE_URL, connect_timeout=5)
        conn.close()
        turso.execute("CREATE TABLE IF NOT EXISTS arkon_log (id INTEGER PRIMARY KEY, msg TEXT)")
        print("🔱 ARKON: 18 Variables Synced. All Cores Online.", flush=True)
    except Exception as e:
        print(f"⚠️ Core Sync Warning: {e}", flush=True)

threading.Thread(target=init_all_cores, daemon=True).start()

@app.route('/arkon/control', methods=['POST'])
def device_bridge():
    """Laptop కంట్రోల్ కోసం కమాండ్స్ ని Redis లో స్టోర్ చేస్తుంది"""
    data = request.get_json()
    if str(data.get("pin")) != str(ARKON_PIN):
        return jsonify({"output": "❌ DENIED"}), 403
    
    command = data.get("command", "").upper()
    cache.set("ARKON_REMOTE_CMD", command) 
    return jsonify({"output": f"🔱 ARKON: Command '{command}' broadcasted."})

@app.route('/')
def home():
    return "🔱 ARKON: Master Guardian Online. 18 Cores Active."

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 8080)))
