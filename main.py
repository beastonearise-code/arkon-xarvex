import os
import threading
import psycopg2
import redis
import cloudinary
from flask import Flask, request, jsonify, render_template
from pymongo import MongoClient
from pinecone import Pinecone
from google import genai
from groq import Groq
from openai import OpenAI
import libsql_client

app = Flask(__name__)

# --- 1. అస్త్రశాల: 18 వేరియబుల్స్ సేకరణ ---
# Databases & Infrastructure
SQL_URI = os.getenv("SQL_URI") or os.getenv("DATABASE_URL")
MONGO_URI = os.getenv("MONGO_URI")
REDIS_URL = os.getenv("REDIS_URL")
TURSO_URL = os.getenv("TURSO_URL") # https:// వాడాలి
TURSO_TOKEN = os.getenv("TURSO_TOKEN")

# Search & Research
TAVILY_KEY = os.getenv("TAVILY_API_KEY")
EXA_KEY = os.getenv("EXA_API_KEY")
SERPER_KEY = os.getenv("SERPER_API_KEY")

# AI Brains
GEMINI_KEY = os.getenv("GEMINI_KEY")
GROQ_KEY = os.getenv("GROQ_KEY")
OPENROUTER_KEY = os.getenv("OPENROUTER_KEY")

# Memory & Security
PINECONE_KEY = os.getenv("PINECONE_API_KEY")
ARKON_PIN = os.getenv("ARKON_PIN")

# --- 2. క్లయింట్స్ ఇనిషియలైజేషన్ ---
cache = redis.from_url(REDIS_URL) # Redis for Instant Commands
gemini_client = genai.Client(api_key=GEMINI_KEY)
groq_client = Groq(api_key=GROQ_KEY)
turso_client = libsql_client.create_client_sync(url=TURSO_URL, auth_token=TURSO_TOKEN)

# --- 3. క్వాడ్-కోర్ పటిష్టత పరీక్ష ---
def init_all_systems():
    try:
        conn = psycopg2.connect(SQL_URI, connect_timeout=5)
        conn.close()
        turso_client.execute("CREATE TABLE IF NOT EXISTS arkon_commands (id INTEGER PRIMARY KEY, cmd TEXT, status TEXT)")
        print("🔱 ARKON: 18 Variables Synchronized. System Stable.", flush=True)
    except Exception as e:
        print(f"⚠️ Core Sync Issue: {e}", flush=True)

threading.Thread(target=init_all_systems, daemon=True).start()

# --- 4. డివైస్ కంట్రోల్ బ్రిడ్జ్ (Fixing Laptop/Phone Control) ---
@app.route('/arkon/control', methods=['POST'])
def device_control():
    """Laptop కంట్రోల్ కోసం కమాండ్స్ ని Redis లో స్టోర్ చేస్తుంది"""
    data = request.get_json()
    if str(data.get("pin")) != str(ARKON_PIN):
        return jsonify({"status": "DENIED"}), 403
    
    command = data.get("command") # ఉదా: "SHUTDOWN", "OPEN_CHROME"
    cache.set("LATEST_DEVICE_CMD", command) # ఈ కమాండ్ మీ ల్యాప్‌టాప్ లోని ఏజెంట్ చదువుతుంది
    return jsonify({"status": "SENT", "cmd": command})

@app.route('/')
def home():
    return "🔱 ARKON: Master Guardian Online. 18 Variables Connected."

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 8080)))
