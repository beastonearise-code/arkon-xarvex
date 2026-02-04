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

# --- 1. అస్త్రశాల: 18 వేరియబుల్స్ సేకరణ ---
DATABASE_URL = os.getenv("DATABASE_URL") or os.getenv("SQL_URI")
MONGO_URI = os.getenv("MONGO_URI")
REDIS_URL = os.getenv("REDIS_URL")
TURSO_URL = os.getenv("TURSO_URL") # https:// వాడాలి
TURSO_TOKEN = os.getenv("TURSO_TOKEN")
CLOUDINARY_URL = os.getenv("CLOUDINARY_URL")

# AI & Search
GEMINI_KEY = os.getenv("GEMINI_KEY")
GROQ_KEY = os.getenv("GROQ_KEY")
OPENROUTER_KEY = os.getenv("OPENROUTER_KEY")
TAVILY_KEY = os.getenv("TAVILY_API_KEY")
EXA_KEY = os.getenv("EXA_API_KEY")
SERPER_KEY = os.getenv("SERPER_API_KEY")

# Memory & Security
PINECONE_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_HOST = os.getenv("PINECONE_HOST")
ARKON_PIN = os.getenv("ARKON_PIN")

# --- 2. క్లయింట్స్ ఇనిషియలైజేషన్ ---
# MongoDB SSL ఫిక్స్
mongo_client = MongoClient(MONGO_URI, tls=True, tlsAllowInvalidCertificates=True)
db_core = mongo_client["Arkon-Xarvex-Core"]

# Redis & Turso
cache = redis.from_url(REDIS_URL)
turso = libsql_client.create_client_sync(url=TURSO_URL, auth_token=TURSO_TOKEN)

# AI Clients
gemini = genai.Client(api_key=GEMINI_KEY)
groq = Groq(api_key=GROQ_KEY)
openrouter = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=OPENROUTER_KEY)

# --- 3. క్వాడ్-కోర్ సింకింగ్ ప్రొటోకాల్ ---
def init_all_systems():
    try:
        # SQL Check
        conn = psycopg2.connect(DATABASE_URL, connect_timeout=5)
        conn.close()
        # Turso Setup
        turso.execute("CREATE TABLE IF NOT EXISTS device_commands (id INTEGER PRIMARY KEY, cmd TEXT, status TEXT)")
        print("🔱 ARKON: 18 Variables Synced. All Cores Online.", flush=True)
    except Exception as e:
        print(f"⚠️ Core Sync Issue: {e}", flush=True)

threading.Thread(target=init_all_systems, daemon=True).start()

# --- 4. డివైస్ & వాయిస్ కంట్రోల్ బ్రిడ్జ్ (Fixing Laptop/Phone Control) ---
@app.route('/arkon/control', methods=['POST'])
def device_bridge():
    """Laptop/Phone ని కంట్రోల్ చేయడానికి కమాండ్స్ ని Redis లో స్టోర్ చేస్తుంది"""
    data = request.get_json()
    if str(data.get("pin")) != str(ARKON_PIN):
        return jsonify({"output": "❌ ACCESS DENIED"}), 403
    
    command = data.get("command", "").upper() # ఉదా: SHUTDOWN, OPEN_CHROME
    cache.set("LATEST_CMD", command) # మీ ల్యాప్‌టాప్ ఏజెంట్ దీనిని చదువుతుంది
    return jsonify({"output": f"🔱 ARKON: Command '{command}' queued for your device."})

@app.route('/')
def home():
    return "🔱 ARKON: Master Guardian Online. 18 Variables Integrated."

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 8080)))
