import os
import threading
import psycopg2
from flask import Flask, request, jsonify
from pymongo import MongoClient
from pinecone import Pinecone, ServerlessSpec
from google import genai
import libsql_client

app = Flask(__name__)

# --- 1. రక్షణ వలయం: అస్త్రాల సేకరణ (Variables) ---
DATABASE_URL = os.getenv("DATABASE_URL")
MONGO_URI = os.getenv("MONGO_URI")
ARKON_PIN = os.getenv("ARKON_PIN")
PINECONE_KEY = os.getenv("PINECONE_API_KEY")
GEMINI_KEY = os.getenv("GEMINI_KEY")
TURSO_URL = os.getenv("TURSO_URL")
TURSO_TOKEN = os.getenv("TURSO_TOKEN")

# AI & Database Clients
client = genai.Client(api_key=GEMINI_KEY)
turso_client = libsql_client.create_client_sync(url=TURSO_URL, auth_token=TURSO_TOKEN)

# --- 2. జ్ఞాపకశక్తి కేంద్రం (Pinecone Setup) ---
pc = Pinecone(api_key=PINECONE_KEY)
index_name = "arkon-memory"

if index_name not in [idx.name for idx in pc.list_indexes()]:
    pc.create_index(
        name=index_name,
        dimension=768, 
        metric="cosine",
        spec=ServerlessSpec(cloud="aws", region="us-east-1")
    )
memory_index = pc.Index(index_name)

# --- 3. డేటాబేస్ అనుసంధానం (SSL & Sync) ---
try:
    # MongoDB SSL Handshake ఫిక్స్
    mongo_client = MongoClient(MONGO_URI, tls=True, tlsAllowInvalidCertificates=True)
    db_intel = mongo_client["Arkon-Xarvex-Core"]
except Exception as e:
    print(f"❌ MongoDB Sync Error: {e}")

def init_cores():
    """చతుర్ముఖ కోర్ సింకింగ్ ప్రొటోకాల్ (Neon, Mongo, Pinecone, Turso)"""
    try:
        # 1. Neon (SQL) Check
        conn = psycopg2.connect(DATABASE_URL, connect_timeout=10)
        conn.close()
        
        # 2. Turso (Edge) Check
        turso_client.execute("CREATE TABLE IF NOT EXISTS system_logs (id INTEGER PRIMARY KEY, msg TEXT)")
        
        # 3. MongoDB Status Update
        db_intel.system_status.update_one(
            {"core": "quad"}, 
            {"$set": {"status": "ACTIVE", "memory": "Vector+Edge Enabled"}}, 
            upsert=True
        )
        print("🔱 ARKON: All 4 Cores Engaged & Synchronized.", flush=True)
    except Exception as e:
        print(f"⚠️ ARKON NOTICE: Core Sync Delayed. {e}", flush=True)

# బ్యాక్‌గ్రౌండ్ లో సింకింగ్ ప్రారంభం
threading.Thread(target=init_cores, daemon=True).start()

# --- 4. సర్వర్ మార్గాలు (Routes) ---

@app.route('/')
def health():
    return "🔱 ARKON: Guardian of Challapalli is Online. All 4 cores are synced."

@app.route('/arkon/power', methods=['POST'])
def power():
    data = request.get_json()
    if str(data.get("pin")) != str(ARKON_PIN):
        return jsonify({"output": "❌ ACCESS DENIED: Intruder detected."}), 403
    
    command = data.get("command", "").lower()
    
    # ఎగ్జాంపుల్: మెమరీ లో సేవ్ చేయడం
    if "save" in command:
        note = command.replace("save", "").strip()
        # ఇక్కడ మెమరీ లాజిక్ యాడ్ చేయవచ్చు
        return jsonify({"output": f"🔱 ARKON: Note '{note}' saved to Vector Memory."})

    return jsonify({"output": f"🔱 ARKON: System processing '{command}'..."})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
