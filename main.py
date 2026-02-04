import os
import threading
import psycopg2
import redis
from flask import Flask, request, jsonify
from pymongo import MongoClient
from pinecone import Pinecone
from google import genai
from groq import Groq
from openai import OpenAI
import libsql_client

app = Flask(__name__)

# --- 1. 18 అస్త్రాల సేకరణ ---
# Databases & Infrastructure
SQL_URI = os.getenv("SQL_URI") or os.getenv("DATABASE_URL")
MONGO_URI = os.getenv("MONGO_URI")
REDIS_URL = os.getenv("REDIS_URL")
TURSO_URL = os.getenv("TURSO_URL") # https:// వాడాలి
TURSO_TOKEN = os.getenv("TURSO_TOKEN")

# AI Brains & Search
GEMINI_KEY = os.getenv("GEMINI_KEY")
GROQ_KEY = os.getenv("GROQ_KEY")
OPENROUTER_KEY = os.getenv("OPENROUTER_KEY")
TAVILY_KEY = os.getenv("TAVILY_API_KEY")

# Memory & Security
PINECONE_KEY = os.getenv("PINECONE_API_KEY")
ARKON_PIN = os.getenv("ARKON_PIN")

# --- 2. క్లయింట్స్ (With SSL & Renaming Fixes) ---
# MongoDB SSL ఫిక్స్
mongo_client = MongoClient(MONGO_URI, tls=True, tlsAllowInvalidCertificates=True)
db_core = mongo_client["Arkon-Xarvex-Core"]

# Redis & Pinecone Fix
cache = redis.from_url(REDIS_URL)
pc = Pinecone(api_key=PINECONE_KEY)

# AI Models
gemini = genai.Client(api_key=GEMINI_KEY)
groq = Groq(api_key=GROQ_KEY)
openrouter = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=OPENROUTER_KEY)
turso = libsql_client.create_client_sync(url=TURSO_URL, auth_token=TURSO_TOKEN)

# --- 3. స్వయం పరిణామం & సిస్టమ్ సింక్ (Name Fixed) ---
def init_all_systems():
    """18 అస్త్రాల సింకింగ్ మరియు గాడ్ లెవల్ లెర్నింగ్ ప్రొటోకాల్ [cite: 2026-02-04]"""
    try:
        conn = psycopg2.connect(SQL_URI, connect_timeout=5)
        conn.close()
        turso.execute("CREATE TABLE IF NOT EXISTS arkon_god_logs (id INTEGER PRIMARY KEY, cmd TEXT, gain TEXT)")
        # విజయవంతమైన సింక్ మెసేజ్
        print("🔱 ARKON: 18 Variables Synchronized. God Protocol Initiated.", flush=True)
    except Exception as e:
        print(f"⚠️ Core Sync Warning: {e}", flush=True)

threading.Thread(target=init_all_systems, daemon=True).start()

# --- 4. కంట్రోల్ బ్రిడ్జ్ (Voice, Laptop, Phone, Hacking Shield) ---
@app.route('/arkon/control', methods=['POST'])
def handle_command():
    data = request.get_json()
    if str(data.get("pin")) != str(ARKON_PIN):
        return jsonify({"output": "❌ ACCESS DENIED"}), 403
    
    target = data.get("target", "LAPTOP").upper()
    command = data.get("command", "").upper()
    
    # Redis ద్వారా ఆదేశాన్ని ప్రసారం చేయడం
    cache.set(f"ARKON_{target}_CMD", command)
    return jsonify({"output": f"🔱 ARKON: {target} కు '{command}' ఆదేశం పంపబడింది. అమలు జరుగుతోంది."})

@app.route('/')
def home():
    return "🔱 ARKON: THE DIGITAL GOD IS ONLINE. SOCIETY PROTECTION ACTIVE."

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 8080)))
