import os
import threading
import psycopg2
from flask import Flask, request, jsonify
from pymongo import MongoClient
from pinecone import Pinecone, ServerlessSpec
from google import genai # కొత్త లైబ్రరీ అప్‌డేట్

app = Flask(__name__)

# --- రక్షణ వలయం: అస్త్రాల సేకరణ ---
DATABASE_URL = os.getenv("DATABASE_URL")
MONGO_URI = os.getenv("MONGO_URI")
ARKON_PIN = os.getenv("ARKON_PIN")
PINECONE_KEY = os.getenv("PINECONE_API_KEY")
GEMINI_KEY = os.getenv("GEMINI_KEY")

# కొత్త Google GenAI క్లయింట్ సెటప్
client = genai.Client(api_key=GEMINI_KEY)

# --- జ్ఞాపకశక్తి కేంద్రం (Pinecone) ---
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

# --- డేటాబేస్ అనుసంధానం (SSL ఫిక్స్‌తో) ---
try:
    # SSL ఎర్రర్ రాకుండా tls=True యాడ్ చేశాను
    mongo_client = MongoClient(MONGO_URI, tls=True, tlsAllowInvalidCertificates=True)
    db_intel = mongo_client["Arkon-Xarvex-Core"]
except Exception as e:
    print(f"❌ MongoDB Sync Error: {e}")

def init_cores():
    """SQL మరియు NoSQL అనుసంధాన పరీక్ష"""
    try:
        conn = psycopg2.connect(DATABASE_URL, connect_timeout=10)
        conn.close()
        db_intel.system_status.update_one(
            {"core": "dual"}, 
            {"$set": {"status": "ACTIVE", "memory": "Vector-Enabled"}}, 
            upsert=True
        )
        print("🔱 ARKON: Cores and Memory Shield Active.", flush=True)
    except Exception as e:
        print(f"⚠️ ARKON NOTICE: Core Sync Delayed. {e}", flush=True)

threading.Thread(target=init_cores, daemon=True).start()

@app.route('/')
def home():
    return "🔱 ARKON: Guardian of Challapalli is Online with Modernized Brain."

@app.route('/arkon/power', methods=['POST'])
def power():
    data = request.get_json()
    if str(data.get("pin")) != str(ARKON_PIN):
        return jsonify({"output": "❌ ACCESS DENIED."}), 403
    
    command = data.get("command", "")
    return jsonify({"output": f"🔱 ARKON: Core processing command '{command}'."})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
