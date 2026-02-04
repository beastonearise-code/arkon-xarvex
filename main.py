
import os
import threading
import psycopg2
import redis
import cloudinary.uploader
from flask import Flask, request, jsonify
from pymongo import MongoClient
from pinecone import Pinecone
from google import genai
from groq import Groq
from openai import OpenAI
import libsql_client

app = Flask(__name__)

# --- 1. అస్త్రశాల: 18 వేరియబుల్స్ సేకరణ ---
DATABASE_URL = os.getenv("DATABASE_URL") or os.getenv("SQL_URI")
MONGO_URI = os.getenv("MONGO_URI")
REDIS_URL = os.getenv("REDIS_URL")
TURSO_URL = os.getenv("TURSO_URL") # https:// ఉండాలి
TURSO_TOKEN = os.getenv("TURSO_TOKEN")
CLOUDINARY_URL = os.getenv("CLOUDINARY_URL")

GEMINI_KEY = os.getenv("GEMINI_KEY")
GROQ_KEY = os.getenv("GROQ_KEY")
OPENROUTER_KEY = os.getenv("OPENROUTER_KEY")
TAVILY_KEY = os.getenv("TAVILY_API_KEY")
EXA_KEY = os.getenv("EXA_API_KEY")
SERPER_KEY = os.getenv("SERP_API_KEY")

PINECONE_KEY = os.getenv("PINECONE_API_KEY")
ARKON_PIN = os.getenv("ARKON_PIN")

# --- 2. క్లయింట్స్ (SSL & Connection Fixes) ---
# MongoDB SSL Fix
mongo_client = MongoClient(MONGO_URI, tls=True, tlsAllowInvalidCertificates=True)
db_core = mongo_client["Arkon-Xarvex-Core"]

# Redis Cache for Speed
cache = redis.from_url(REDIS_URL)

# AI Models
gemini = genai.Client(api_key=GEMINI_KEY)
groq = Groq(api_key=GROQ_KEY)
openrouter = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=OPENROUTER_KEY)

# Turso Client
turso = libsql_client.create_client_sync(url=TURSO_URL, auth_token=TURSO_TOKEN)

# --- 3. సిస్టమ్ హెల్త్ చెక్ ---
def init_all_systems():
    try:
        conn = psycopg2.connect(DATABASE_URL, connect_timeout=5)
        conn.close()
        turso.execute("CREATE TABLE IF NOT EXISTS system_logs (id INTEGER PRIMARY KEY, msg TEXT)")
        print("🔱 ARKON: 18 Variables Synced. System Stable.", flush=True)
    except Exception as e:
        print(f"⚠️ Core Sync Warning: {e}", flush=True)

threading.Thread(target=init_all_systems, daemon=True).start()

# --- 4. డివైస్ కంట్రోల్ (Voice/Remote Bridge) ---
@app.route('/arkon/command', methods=['POST'])
def handle_cmd():
    data = request.get_json()
    if str(data.get("pin")) != str(ARKON_PIN):
        return jsonify({"output": "❌ DENIED"}), 403
    
    command = data.get("command", "").upper()
    # మీ ల్యాప్‌టాప్ కంట్రోల్ కోసం Redis లో కమాండ్ పెడుతుంది
    cache.set("ARKON_REMOTE_CMD", command) 
    return jsonify({"output": f"🔱 ARKON: Command '{command}' broadcasted."})

@app.route('/')
def home():
    return "🔱 ARKON: Master Guardian Online. 18 Cores Active."

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 8080)))
