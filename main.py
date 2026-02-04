import os
import threading
import psycopg2
from flask import Flask, request, jsonify
from pymongo import MongoClient
from pinecone import Pinecone
from google import genai
from openai import OpenAI
from groq import Groq
import libsql_client
import redis

app = Flask(__name__)

# --- 1. అస్త్రశాల: అన్ని వేరియబుల్స్ సేకరణ ---
# Databases & Storage
SQL_URI = os.getenv("SQL_URI") or os.getenv("DATABASE_URL")
MONGO_URI = os.getenv("MONGO_URI")
REDIS_URL = os.getenv("REDIS_URL")
TURSO_URL = os.getenv("TURSO_URL") # https:// వాడాలి
TURSO_TOKEN = os.getenv("TURSO_TOKEN")
CLOUDINARY_URL = os.getenv("CLOUDINARY_URL")

# AI & Search Keys
GEMINI_KEY = os.getenv("GEMINI_KEY")
GROQ_KEY = os.getenv("GROQ_KEY")
OPENROUTER_KEY = os.getenv("OPENROUTER_KEY")
TAVILY_KEY = os.getenv("TAVILY_API_KEY")
EXA_KEY = os.getenv("EXA_API_KEY")
SERPER_KEY = os.getenv("SERPER_API_KEY")

# Memory & Security
PINECONE_KEY = os.getenv("PINECONE_API_KEY")
ARKON_PIN = os.getenv("ARKON_PIN")

# --- 2. క్లయింట్స్ ఇనిషియలైజేషన్ ---
# Redis & Turso Setup
cache = redis.from_url(REDIS_URL)
turso_client = libsql_client.create_client_sync(url=TURSO_URL, auth_token=TURSO_TOKEN)

# AI Models
gemini = genai.Client(api_key=GEMINI_KEY)
groq = Groq(api_key=GROQ_KEY)

# --- 3. క్వాడ్-కోర్ కనెక్షన్ ప్రొటోకాల్ ---
def init_all_systems():
    try:
        # Neon SQL Check
        conn = psycopg2.connect(SQL_URI, connect_timeout=5)
        conn.close()
        
        # MongoDB & Turso Check
        mongo_client = MongoClient(MONGO_URI, tls=True, tlsAllowInvalidCertificates=True)
        db = mongo_client["Arkon-Core"]
        turso_client.execute("CREATE TABLE IF NOT EXISTS arkon_commands (id INTEGER PRIMARY KEY, cmd TEXT, status TEXT)")
        
        print("🔱 ARKON: All 18 Variables Synchronized. Guardian is fully armed.", flush=True)
    except Exception as e:
        print(f"⚠️ Core Sync Issue: {e}", flush=True)

threading.Thread(target=init_all_systems, daemon=True).start()

# --- 4. వాయిస్ & డివైస్ కంట్రోల్ లాజిక్ (The Bridge) ---
@app.route('/arkon/bridge', methods=['POST'])
def device_bridge():
    """Laptop/Phone కంట్రోల్ కోసం ఈ రూట్ వాడుతాం"""
    data = request.get_json()
    if str(data.get("pin")) != str(ARKON_PIN):
        return jsonify({"status": "DENIED"}), 403
    
    command = data.get("command") # ఉదా: "SHUTDOWN_LAPTOP"
    # ఈ కమాండ్ ను Turso లేదా Redis లో పెడతాం, మీ ల్యాప్‌టాప్ లో ఉండే ఏజెంట్ దీనిని చదువుతుంది
    cache.set("LATEST_CMD", command)
    return jsonify({"status": "COMMAND_QUEUED", "msg": f"Arkon sent '{command}' to your device."})

@app.route('/')
def status():
    return "🔱 ARKON: Master Guardian Online. 18 Variables Active."

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 8080)))
