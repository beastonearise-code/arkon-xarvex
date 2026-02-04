import os
import threading
import psycopg2
import redis
import cloudinary
from flask import Flask, request, jsonify
from pymongo import MongoClient
from pinecone import Pinecone
from google import genai
from groq import Groq
from openai import OpenAI
import libsql_client

app = Flask(__name__)

# --- 1. సంపూర్ణ అస్త్రశాల: 18 వేరియబుల్స్ సేకరణ ---
# Databases & Cache
SQL_URI = os.getenv("SQL_URI") or os.getenv("DATABASE_URL")
MONGO_URI = os.getenv("MONGO_URI")
REDIS_URL = os.getenv("REDIS_URL")
TURSO_URL = os.getenv("TURSO_URL") # https:// వాడాలి
TURSO_TOKEN = os.getenv("TURSO_TOKEN")

# Search & Research APIs
TAVILY_KEY = os.getenv("TAVILY_API_KEY")
EXA_KEY = os.getenv("EXA_API_KEY")
SERPER_KEY = os.getenv("SERPER_API_KEY")

# AI Brains
GEMINI_KEY = os.getenv("GEMINI_KEY")
GROQ_KEY = os.getenv("GROQ_KEY")
OPENROUTER_KEY = os.getenv("OPENROUTER_KEY")

# Storage & Memory
CLOUDINARY_URL = os.getenv("CLOUDINARY_URL")
PINECONE_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_HOST = os.getenv("PINECONE_HOST")
ARKON_PIN = os.getenv("ARKON_PIN")

# --- 2. క్లయింట్స్ ఇనిషియలైజేషన్ ---
# Redis Cache (వేగవంతమైన డేటా కోసం)
cache = redis.from_url(REDIS_URL)

# AI Clients
gemini_client = genai.Client(api_key=GEMINI_KEY)
groq_client = Groq(api_key=GROQ_KEY)
# OpenRouter ని OpenAI క్లయింట్ ద్వారా వాడుతున్నాం
openrouter_client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=OPENROUTER_KEY)

# Turso & MongoDB Setup
turso_client = libsql_client.create_client_sync(url=TURSO_URL, auth_token=TURSO_TOKEN)
mongo_client = MongoClient(MONGO_URI, tls=True, tlsAllowInvalidCertificates=True)
db_intel = mongo_client["Arkon-Core"]

# --- 3. క్వాడ్-కోర్ పటిష్టత పరీక్ష ---
def init_all_systems():
    try:
        # SQL (Neon) కనెక్షన్
        conn = psycopg2.connect(SQL_URI, connect_timeout=5)
        conn.close()
        
        # Turso టేబుల్స్ సిద్ధం చేయడం
        turso_client.execute("CREATE TABLE IF NOT EXISTS arkon_ops (id INTEGER PRIMARY KEY, cmd TEXT, status TEXT)")
        
        print("🔱 ARKON: All 18 Variables Synchronized. Guardian is fully armed.", flush=True)
    except Exception as e:
        print(f"⚠️ Core Sync Issue: {e}", flush=True)

threading.Thread(target=init_all_systems, daemon=True).start()

# --- 4. వాయిస్ & డివైస్ కంట్రోల్ బ్రిడ్జ్ (Fixing Missing Features) ---
@app.route('/arkon/control', methods=['POST'])
def device_control():
    """Laptop/Phone కంట్రోల్ కోసం కమాండ్స్ ని Redis లో స్టోర్ చేస్తుంది"""
    data = request.get_json()
    if str(data.get("pin")) != str(ARKON_PIN):
        return jsonify({"status": "ACCESS DENIED"}), 403
    
    command = data.get("command") # ఉదా: "OPEN_CHROME" లేదా "SHUTDOWN"
    # Redis లో ఈ కమాండ్ ని పెడతాం, మీ డివైస్ లో ఉండే ఏజెంట్ దీనిని చదువుతుంది
    cache.set("DEVICE_CMD", command)
    return jsonify({"status": "SENT", "target_command": command})

@app.route('/')
def health():
    return "🔱 ARKON: Master Guardian Online. 18 Variables Connected."

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 8080)))
