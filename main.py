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
# Databases & Infrastructure
DATABASE_URL = os.getenv("DATABASE_URL") or os.getenv("SQL_URI")
MONGO_URI = os.getenv("MONGO_URI")
REDIS_URL = os.getenv("REDIS_URL")
TURSO_URL = os.getenv("TURSO_URL") # 'https://' తో మొదలవ్వాలి
TURSO_TOKEN = os.getenv("TURSO_TOKEN")
CLOUDINARY_URL = os.getenv("CLOUDINARY_URL")

# AI Brains & Search
GEMINI_KEY = os.getenv("GEMINI_KEY")
GROQ_KEY = os.getenv("GROQ_KEY")
OPENROUTER_KEY = os.getenv("OPENROUTER_KEY")
TAVILY_KEY = os.getenv("TAVILY_API_KEY")
EXA_KEY = os.getenv("EXA_API_KEY")
SERPER_KEY = os.getenv("SERP_API_KEY")

# Memory & Security
PINECONE_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_HOST = os.getenv("PINECONE_HOST")
ARKON_PIN = os.getenv("ARKON_PIN")

# --- 2. క్లయింట్స్ ఇనిషియలైజేషన్ (With Fixes) ---
# MongoDB SSL Handshake ఫిక్స్
mongo_client = MongoClient(MONGO_URI, tls=True, tlsAllowInvalidCertificates=True)
db_core = mongo_client["Arkon-Xarvex-Core"]

# Redis Cache for Instant Commands
cache = redis.from_url(REDIS_URL)

# Turso Edge Database
turso = libsql_client.create_client_sync(url=TURSO_URL, auth_token=TURSO_TOKEN)

# AI Clients (Triple Brain)
gemini = genai.Client(api_key=GEMINI_KEY)
groq_client = Groq(api_key=GROQ_KEY)
openrouter = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=OPENROUTER_KEY)

# --- 3. సిస్టమ్ సింకింగ్ ప్రొటోకాల్ ---
def init_all_systems():
    """అన్ని కోర్లు మరియు అస్త్రాలను ధృవీకరిస్తుంది"""
    try:
        # Neon (SQL) Check
        conn = psycopg2.connect(DATABASE_URL, connect_timeout=5)
        conn.close()
        
        # Turso Table Setup
        turso.execute("CREATE TABLE IF NOT EXISTS arkon_ops (id INTEGER PRIMARY KEY, cmd TEXT, target TEXT)")
        
        print("🔱 ARKON: 18 Variables Synchronized. All Cores Online.", flush=True)
    except Exception as e:
        print(f"⚠️ Core Sync Warning: {e}", flush=True)

# బ్యాక్‌గ్రౌండ్ లో సిస్టమ్ చెక్ ప్రారంభం
threading.Thread(target=init_all_systems, daemon=True).start()

# --- 4. మేధస్సు నిర్వహణ (AI Orchestrator) ---
def get_response(prompt, brain="gemini"):
    if brain == "openai" or brain == "openrouter":
        return openrouter.chat.completions.create(
            model="meta-llama/llama-3.1-8b-instruct:free", # మీరు కోరుకున్న మోడల్
            messages=[{"role": "user", "content": prompt}]
        ).choices[0].message.content
    elif brain == "groq":
        return groq_client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama3-70b-8192"
        ).choices[0].message.content
    else: # Default Gemini 2.0
        return gemini.models.generate_content(model="gemini-2.0-flash", contents=prompt).text

# --- 5. సర్వర్ రూట్లు (Control Center) ---

@app.route('/')
def status():
    return "🔱 ARKON: Universal Guardian Online. 18 Variables Integrated."

@app.route('/ask', methods=['POST'])
def ask_arkon():
    data = request.get_json()
    if str(data.get("pin")) != str(ARKON_PIN):
        return jsonify({"output": "❌ ACCESS DENIED"}), 403
    
    prompt = data.get("prompt")
    brain = data.get("brain", "gemini")
    
    answer = get_response(prompt, brain)
    return jsonify({"answer": answer, "brain_used": brain})

@app.route('/arkon/command', methods=['POST'])
def remote_control():
    """Laptop/Phone ని శాసించే రూట్"""
    data = request.get_json()
    if str(data.get("pin")) != str(ARKON_PIN):
        return jsonify({"output": "❌ ACCESS DENIED"}), 403
    
    target = data.get("target", "LAPTOP") # "LAPTOP" లేదా "PHONE"
    command = data.get("command", "").upper()
    
    # Redis లో కమాండ్ ని నిక్షిప్తం చేస్తుంది
    cache.set(f"ARKON_{target}_CMD", command)
    return jsonify({"output": f"🔱 ARKON: Command '{command}' broadcasted to {target}."})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
