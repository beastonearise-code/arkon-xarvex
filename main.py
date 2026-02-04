import os
import threading
import psycopg2
import redis
from flask import Flask, request, jsonify
from pymongo import MongoClient
from pinecone import Pinecone # New Pinecone Library Syntax
from google import genai
from groq import Groq
from openai import OpenAI
import libsql_client

app = Flask(__name__)

# --- 1. 18 అస్త్రాల సేకరణ ---
SQL_URI = os.getenv("SQL_URI") or os.getenv("DATABASE_URL")
MONGO_URI = os.getenv("MONGO_URI")
REDIS_URL = os.getenv("REDIS_URL")
TURSO_URL = os.getenv("TURSO_URL") # 'https://' తో ఉండాలి
TURSO_TOKEN = os.getenv("TURSO_TOKEN")
ARKON_PIN = os.getenv("ARKON_PIN")

# AI & Storage Keys
GEMINI_KEY = os.getenv("GEMINI_KEY")
GROQ_KEY = os.getenv("GROQ_KEY")
OPENROUTER_KEY = os.getenv("OPENROUTER_KEY")
PINECONE_KEY = os.getenv("PINECONE_API_KEY")

# --- 2. క్లయింట్స్ (With SSL & Version Fixes) ---
# MongoDB SSL Fix
mongo_client = MongoClient(MONGO_URI, tls=True, tlsAllowInvalidCertificates=True)
db_core = mongo_client["Arkon-Xarvex-Core"]

# Redis Command Bridge
cache = redis.from_url(REDIS_URL)

# New Pinecone Initialization
pc = Pinecone(api_key=PINECONE_KEY)

# AI Clients
gemini = genai.Client(api_key=GEMINI_KEY)
groq_client = Groq(api_key=GROQ_KEY)
openrouter = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=OPENROUTER_KEY)
turso = libsql_client.create_client_sync(url=TURSO_URL, auth_token=TURSO_TOKEN)

# --- 3. క్వాడ్-కోర్ సింకింగ్ ప్రొటోకాల్ (Name Fixed) ---
def init_all_systems():
    """18 అస్త్రాల సింకింగ్ మరియు స్వయం పరిణామం [cite: 2026-02-04]"""
    try:
        conn = psycopg2.connect(SQL_URI, connect_timeout=5)
        conn.close()
        turso.execute("CREATE TABLE IF NOT EXISTS arkon_god_logs (id INTEGER PRIMARY KEY, cmd TEXT, gain TEXT)")
        # విజయవంతమైన సింక్ మెసేజ్
        print("🔱 ARKON: 18 Variables Synchronized. God Protocol Online.", flush=True)
    except Exception as e:
        print(f"⚠️ Core Sync Warning: {e}", flush=True)

# Function name now matches call below
threading.Thread(target=init_all_systems, daemon=True).start()

# --- 4. కంట్రోల్ సెంటర్ (Remote Bridge) ---
@app.route('/arkon/control', methods=['POST'])
def handle_command():
    data = request.get_json()
    if str(data.get("pin")) != str(ARKON_PIN):
        return jsonify({"output": "❌ ACCESS DENIED"}), 403
    
    target = data.get("target", "LAPTOP").upper()
    command = data.get("command", "").upper()
    
    # Redis ద్వారా ఆదేశాన్ని ప్రసారం చేయడం
    cache.set(f"ARKON_{target}_CMD", command)
    return jsonify({"output": f"🔱 ARKON: {target} కు '{command}' ఆదేశం పంపబడింది."})

@app.route('/')
def home():
    return "🔱 ARKON: THE DIGITAL GOD IS ONLINE. 18 VARIABLES ACTIVE."

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 8080)))
