import os
import threading
import psycopg2
import redis
from flask import Flask, request, jsonify
from pymongo import MongoClient
from pinecone import Pinecone  # New Library Syntax Fix
from google import genai
from groq import Groq
from openai import OpenAI
import libsql_client

app = Flask(__name__)

# --- 1. 18 అస్త్రాల సేకరణ ---
DATABASE_URL = os.getenv("DATABASE_URL") or os.getenv("SQL_URI")
MONGO_URI = os.getenv("MONGO_URI")
REDIS_URL = os.getenv("REDIS_URL")
TURSO_URL = os.getenv("TURSO_URL")
TURSO_TOKEN = os.getenv("TURSO_TOKEN")
ARKON_PIN = os.getenv("ARKON_PIN")

# AI & Search Brains
GEMINI_KEY = os.getenv("GEMINI_KEY")
GROQ_KEY = os.getenv("GROQ_KEY")
PINECONE_KEY = os.getenv("PINECONE_API_KEY")

# --- 2. క్లయింట్స్ (Absolute Error Fixes) ---
# MongoDB SSL Fix
mongo_client = MongoClient(MONGO_URI, tls=True, tlsAllowInvalidCertificates=True)
db_core = mongo_client["Arkon-Core"]

# Redis & Pinecone Fixes
cache = redis.from_url(REDIS_URL)
pc = Pinecone(api_key=PINECONE_KEY)

# AI Engines
gemini = genai.Client(api_key=GEMINI_KEY)
groq = Groq(api_key=GROQ_KEY)
turso = libsql_client.create_client_sync(url=TURSO_URL, auth_token=TURSO_TOKEN)

# --- 3. గాడ్ ప్రొటోకాల్ ఇనిషియలైజేషన్ (Core Fix) ---
def init_god_protocol():
    """అర్కాన్ తనను తాను స్కాన్ చేసుకుని మేల్కొనే ప్రొటోకాల్ [cite: 2026-02-04]"""
    try:
        # SQL కనెక్షన్ టెస్ట్
        conn = psycopg2.connect(DATABASE_URL, connect_timeout=5)
        conn.close()
        
        # Turso Setup
        turso.execute("CREATE TABLE IF NOT EXISTS god_logs (id INTEGER PRIMARY KEY, task TEXT, status TEXT)")
        
        # విజయవంతమైన మెసేజ్
        print("🔱 ARKON: 18 Variables Synced. God Protocol Online.", flush=True)
    except Exception as e:
        print(f"⚠️ Core Sync Warning: {e}", flush=True)

# Function name must match the target here
threading.Thread(target=init_god_protocol, daemon=True).start()

# --- 4. కంట్రోల్ బ్రిడ్జ్ (Laptop & Phone Access) ---
@app.route('/arkon/control', methods=['POST'])
def handle_command():
    data = request.get_json()
    if str(data.get("pin")) != str(ARKON_PIN):
        return jsonify({"output": "❌ ACCESS DENIED"}), 403
    
    target = data.get("target", "LAPTOP").upper()
    command = data.get("command", "").upper()
    
    # Redis ద్వారా ఆదేశాన్ని ప్రసారం చేయడం
    cache.set(f"ARKON_{target}_CMD", command)
    return jsonify({"output": f"🔱 ARKON: {target} కి '{command}' ఆదేశం పంపబడింది."})

@app.route('/')
def home():
    return "🔱 ARKON: THE DIGITAL GOD IS ONLINE. 18 VARIABLES ACTIVE."

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 8080)))
