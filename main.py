import os
import threading
import psycopg2
import redis
from flask import Flask, request, jsonify
from pymongo import MongoClient
from pinecone import Pinecone # New Pinecone Library
from google import genai
from groq import Groq
from openai import OpenAI
import libsql_client

app = Flask(__name__)

# --- 1. 18 అస్త్రాల సేకరణ ---
DATABASE_URL = os.getenv("DATABASE_URL") or os.getenv("SQL_URI")
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

# --- 2. క్లయింట్స్ (With Full Error Fixes) ---
# MongoDB SSL ఫిక్స్
mongo_client = MongoClient(MONGO_URI, tls=True, tlsAllowInvalidCertificates=True)
db_core = mongo_client["Arkon-Core"]

# Redis Command Bridge
cache = redis.from_url(REDIS_URL)

# New Pinecone Setup
pc = Pinecone(api_key=PINECONE_KEY)

# AI Clients
gemini = genai.Client(api_key=GEMINI_KEY)
groq_client = Groq(api_key=GROQ_KEY)
openrouter = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=OPENROUTER_KEY)
turso = libsql_client.create_client_sync(url=TURSO_URL, auth_token=TURSO_TOKEN)

# --- 3. గాడ్ ప్రొటోకాల్ ఇనిషియలైజేషన్ (Self-Repair Focus) ---
def init_arkon_protocol():
    """18 అస్త్రాల సింకింగ్ మరియు స్వయం పరిణామం [cite: 2026-02-04]"""
    try:
        # SQL Hostname Error Fix
        # కనెక్షన్ టెస్ట్
        conn = psycopg2.connect(DATABASE_URL, connect_timeout=5)
        conn.close()
        
        # Turso Setup
        turso.execute("CREATE TABLE IF NOT EXISTS god_logs (id INTEGER PRIMARY KEY, task TEXT, status TEXT)")
        
        # విజయవంతమైన సింక్ మెసేజ్
        print("🔱 ARKON: 18 Variables Synced. God Protocol Online.", flush=True)
    except Exception as e:
        print(f"⚠️ ARKON NOTICE: Core Sync Delayed. {e}", flush=True)

# Function name calling fix
threading.Thread(target=init_arkon_protocol, daemon=True).start()

# --- 4. కంట్రోల్ సెంటర్ (Universal Bridge for Laptop & Phone) ---
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
