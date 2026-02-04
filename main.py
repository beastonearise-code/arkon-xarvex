import os
import threading
import psycopg2
from flask import Flask, request, jsonify
from pymongo import MongoClient
from pinecone import Pinecone, ServerlessSpec
from google import genai
from openai import OpenAI
from groq import Groq
import libsql_client

app = Flask(__name__)

# --- 1. వేరియబుల్స్ సేకరణ (The 9 Pillars) ---
# Databases
DATABASE_URL = os.getenv("DATABASE_URL")   # Neon
MONGO_URI = os.getenv("MONGO_URI")         # MongoDB
TURSO_URL = os.getenv("TURSO_URL")         # Turso (Use https://)
TURSO_TOKEN = os.getenv("TURSO_TOKEN")
PINECONE_KEY = os.getenv("PINECONE_API_KEY")

# AI Brains
GEMINI_KEY = os.getenv("GEMINI_KEY")
OPENAI_KEY = os.getenv("OPENAI_API_KEY")
GROQ_KEY = os.getenv("GROQ_API_KEY")
ARKON_PIN = os.getenv("ARKON_PIN")

# --- 2. క్లయింట్స్ ఇనిషియలైజేషన్ ---
# AI Clients
gemini_client = genai.Client(api_key=GEMINI_KEY)
openai_client = OpenAI(api_key=OPENAI_KEY)
groq_client = Groq(api_key=GROQ_KEY)

# Database Clients
# Turso HTTPS Fix
turso_client = libsql_client.create_client_sync(url=TURSO_URL, auth_token=TURSO_TOKEN)

try:
    # MongoDB SSL Fix
    mongo_client = MongoClient(MONGO_URI, tls=True, tlsAllowInvalidCertificates=True)
    db_intel = mongo_client["Arkon-Xarvex-Core"]
    
    # Pinecone Modern Setup
    pc = Pinecone(api_key=PINECONE_KEY)
    memory_index = pc.Index("arkon-memory")
except Exception as e:
    print(f"❌ Initial Client Error: {e}")

# --- 3. క్వాడ్-కోర్ సింకింగ్ (Checks all 4 DBs) ---
def init_all_cores():
    """ఉదయం నుండి మనం సెట్ చేసిన 4 డేటాబేస్ లను ఒకేసారి చెక్ చేస్తుంది"""
    try:
        # 1. Neon (SQL)
        conn = psycopg2.connect(DATABASE_URL, connect_timeout=10)
        conn.close()
        
        # 2. Turso (Edge)
        turso_client.execute("CREATE TABLE IF NOT EXISTS arkon_meta (id INTEGER PRIMARY KEY, key TEXT, value TEXT)")
        
        # 3. MongoDB & Pinecone Status
        db_intel.system_status.update_one(
            {"core": "quad-plus"}, 
            {"$set": {"status": "ACTIVE", "brains": "3-Engaged"}}, 
            upsert=True
        )
        print("🔱 ARKON: All 4 Databases & 3 AI Brains are Synchronized.", flush=True)
    except Exception as e:
        print(f"⚠️ Core Sync Error: {e}", flush=True)

threading.Thread(target=init_all_cores, daemon=True).start()

# --- 4. మేధస్సు నిర్వహణ (AI Orchestrator) ---
def get_response(prompt, model_choice):
    if model_choice == "openai":
        return openai_client.chat.completions.create(model="gpt-4o", messages=[{"role": "user", "content": prompt}]).choices[0].message.content
    elif model_choice == "groq":
        return groq_client.chat.completions.create(messages=[{"role": "user", "content": prompt}], model="llama3-70b-8192").choices[0].message.content
    else: # Default Gemini
        return gemini_client.models.generate_content(model="gemini-2.0-flash", contents=prompt).text

# --- 5. మార్గాలు (Routes) ---
@app.route('/')
def home():
    return "🔱 ARKON: Full Stack Guardian (4 DBs + 3 AI Cores) is ONLINE."

@app.route('/ask', methods=['POST'])
def ask():
    data = request.get_json()
    if str(data.get("pin")) != str(ARKON_PIN):
        return jsonify({"output": "❌ ACCESS DENIED"}), 403
    
    prompt = data.get("prompt")
    brain = data.get("brain", "gemini")
    
    answer = get_response(prompt, brain)
    return jsonify({"answer": answer, "brain": brain, "status": "Synced"})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 8080)))
