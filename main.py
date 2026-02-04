import os
import threading
import psycopg2
from flask import Flask, request, jsonify, render_template
from pymongo import MongoClient
from pinecone import Pinecone, ServerlessSpec
import google.generativeai as genai

app = Flask(__name__)

# --- 1. రక్షణ వలయం: అస్త్రాల సేకరణ (Railway Variables) ---
DATABASE_URL = os.getenv("DATABASE_URL")
MONGO_URI = os.getenv("MONGO_URI")
ARKON_PIN = os.getenv("ARKON_PIN")
PINECONE_KEY = os.getenv("PINECONE_API_KEY")
GEMINI_KEY = os.getenv("GEMINI_KEY")

# AI కాన్ఫిగరేషన్
genai.configure(api_key=GEMINI_KEY)

# --- 2. జ్ఞాపకశక్తి కేంద్రం (Pinecone Setup) ---
pc = Pinecone(api_key=PINECONE_KEY)
index_name = "arkon-memory"

# ఇండెక్స్ లేకపోతే క్రియేట్ చేస్తుంది
if index_name not in [idx.name for idx in pc.list_indexes()]:
    pc.create_index(
        name=index_name,
        dimension=768, # Gemini Embedding dimension
        metric="cosine",
        spec=ServerlessSpec(cloud="aws", region="us-east-1")
    )
memory_index = pc.Index(index_name)

# --- 3. డేటాబేస్ అనుసంధానం (Mongo & SQL) ---
try:
    mongo_client = MongoClient(MONGO_URI)
    db_intel = mongo_client["Arkon-Xarvex-Core"]
except Exception as e:
    print(f"❌ MongoDB Sync Error: {e}")

def init_cores():
    """డ్యూయల్-కోర్ సింకింగ్ ప్రొటోకాల్"""
    try:
        # SQL (Neon) కనెక్షన్ టెస్ట్
        conn = psycopg2.connect(DATABASE_URL, connect_timeout=10)
        conn.close()
        
        # MongoDB స్టేటస్ అప్‌డేట్
        db_intel.system_status.update_one(
            {"core": "dual"}, 
            {"$set": {"status": "ACTIVE", "memory": "Vector-Enabled"}}, 
            upsert=True
        )
        print("🔱 ARKON: Security Shield Engaged. Memory Cores Active.", flush=True)
    except Exception as e:
        print(f"⚠️ ARKON NOTICE: Core Sync Delayed. {e}", flush=True)

# బ్యాక్‌గ్రౌండ్ లో సింకింగ్
threading.Thread(target=init_cores, daemon=True).start()

# --- 4. జ్ఞాపకశక్తి విధులు (Memory Functions) ---
def save_to_memory(user_id, text):
    """విషయాన్ని వెక్టార్ లాగా దాస్తుంది"""
    embedding = genai.embed_content(model="models/embedding-001", content=text)["embedding"]
    memory_index.upsert(vectors=[{
        "id": f"{user_id}_{os.urandom(3).hex()}", 
        "values": embedding, 
        "metadata": {"text": text}
    }])

def search_memory(query):
    """గత జ్ఞాపకాలను వెతుకుతుంది"""
    query_embedding = genai.embed_content(model="models/embedding-001", content=query)["embedding"]
    results = memory_index.query(vector=query_embedding, top_k=2, include_metadata=True)
    return [res['metadata']['text'] for res in results['matches']]

# --- 5. సర్వర్ మార్గాలు (Routes) ---
@app.route('/')
def home():
    return "🔱 ARKON: Guardian of Challapalli is Online with Eternal Memory."

@app.route('/arkon/power', methods=['POST'])
def power():
    data = request.get_json()
    received_pin = data.get("pin")
    command = data.get("command", "")
    
    if str(received_pin) != str(ARKON_PIN):
        return jsonify({"output": "❌ ACCESS DENIED."}), 403
    
    # ఒకవేళ కమాండ్ లో ఏదైనా సమాచారం ఉంటే దానిని జ్ఞాపకశక్తిలో దాస్తుంది
    if "save" in command.lower():
        note = command.replace("save", "").strip()
        save_to_memory("creator_leela", note)
        return jsonify({"output": f"🔱 ARKON: Information '{note}' is now immortal in my memory."})
    
    return jsonify({"output": f"🔱 ARKON: Executing '{command}'..."})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
