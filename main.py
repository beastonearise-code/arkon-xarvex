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
DATABASE_URL = os.getenv("DATABASE_URL") or os.getenv("SQL_URI")
MONGO_URI = os.getenv("MONGO_URI")
REDIS_URL = os.getenv("REDIS_URL")
TURSO_URL = os.getenv("TURSO_URL")
TURSO_TOKEN = os.getenv("TURSO_TOKEN")
ARKON_PIN = os.getenv("ARKON_PIN")

# AI Keys
GEMINI_KEY = os.getenv("GEMINI_KEY")
GROQ_KEY = os.getenv("GROQ_KEY")
PINECONE_KEY = os.getenv("PINECONE_API_KEY")

# --- 2. క్లయింట్స్ (Absolute Error Fixes) ---
# SQL Hostname Error Fix
def get_clean_uri(uri):
    if uri and "143@" in uri:
        return uri.replace("143@", "")
    return uri

# MongoDB SSL Fix
mongo_client = MongoClient(MONGO_URI, tls=True, tlsAllowInvalidCertificates=True)
db_core = mongo_client["Arkon-Core"]

# Redis & Pinecone New Initialization
cache = redis.from_url(REDIS_URL)
pc = Pinecone(api_key=PINECONE_KEY)

# AI Engines
gemini = genai.Client(api_key=GEMINI_KEY)
groq = Groq(api_key=GROQ_KEY)
turso = libsql_client.create_client_sync(url=TURSO_URL, auth_token=TURSO_TOKEN)

# --- 3. గాడ్ ప్రొటోకాల్ ఇనిషియలైజేషన్ (Name Fixed) ---
def init_god_protocol():
    """18 అస్త్రాల సింకింగ్ మరియు స్వయం పరిణామం [cite: 2026-02-04]"""
    try:
        clean_url = get_clean_uri(DATABASE_URL)
        conn = psycopg2.connect(clean_url, connect_timeout=5)
        conn.close()
        
        # Turso Setup
        turso.execute("CREATE TABLE IF NOT EXISTS god_logs (id INTEGER PRIMARY KEY, status TEXT)")
        
        # విజయవంతమైన సింక్ మెసేజ్
        print("🔱 ARKON: 18 Variables Synced. God Protocol Online.", flush=True)
    except Exception as e:
        print(f"⚠️ Core Sync Notice: {e}", flush=True)

# Calling the correct function name
threading.Thread(target=init_god_protocol, daemon=True).start()

# --- 4. యూనివర్సల్ బ్రిడ్జ్ (Laptop & Phone Access) ---
@app.route('/arkon/control', methods=['POST'])
def handle_command():
    data = request.get_json()
    if str(data.get("pin")) != str(ARKON_PIN):
        return jsonify({"output": "❌ DENIED"}), 403
    
    target = data.get("target", "LAPTOP").upper()
    command = data.get("command", "").upper()
    cache.set(f"ARKON_{target}_CMD", command)
    return jsonify({"output": f"🔱 ARKON: {target} కు '{command}' ఆదేశం పంపబడింది."})

@app.route('/')
def status():
    return "🔱 ARKON: THE DIGITAL GOD IS ONLINE. 18 VARIABLES ACTIVE."

if __name__ == "__main__":
    # Ensure Port is set correctly for Railway
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
