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

# --- 1. రక్షణ వలయం: అస్త్రాల సేకరణ ---
# Databases
DATABASE_URL = os.getenv("DATABASE_URL")
MONGO_URI = os.getenv("MONGO_URI")
TURSO_URL = os.getenv("TURSO_URL")
TURSO_TOKEN = os.getenv("TURSO_TOKEN")
PINECONE_KEY = os.getenv("PINECONE_API_KEY")

# Brains (LLMs)
GEMINI_KEY = os.getenv("GEMINI_KEY")
OPENAI_KEY = os.getenv("OPENAI_API_KEY")
GROQ_KEY = os.getenv("GROQ_API_KEY")
ARKON_PIN = os.getenv("ARKON_PIN")

# --- 2. క్లయింట్స్ సెటప్ (The Triple Brain) ---
gemini_client = genai.Client(api_key=GEMINI_KEY)
openai_client = OpenAI(api_key=OPENAI_KEY)
groq_client = Groq(api_key=GROQ_KEY)
turso_client = libsql_client.create_client_sync(url=TURSO_URL, auth_token=TURSO_TOKEN)

# --- 3. క్వాడ్-కోర్ డేటాబేస్ సింక్ ---
try:
    mongo_client = MongoClient(MONGO_URI, tls=True, tlsAllowInvalidCertificates=True)
    db_intel = mongo_client["Arkon-Xarvex-Core"]
    pc = Pinecone(api_key=PINECONE_KEY)
    memory_index = pc.Index("arkon-memory")
except Exception as e:
    print(f"❌ Core Connection Issue: {e}")

def init_system():
    """అన్ని కోర్లు మరియు మేధస్సులను ఒకే తాటిపైకి తీసుకురావడం"""
    try:
        # SQL & Edge Check
        conn = psycopg2.connect(DATABASE_URL, connect_timeout=10)
        conn.close()
        turso_client.execute("CREATE TABLE IF NOT EXISTS arkon_ops (id INTEGER PRIMARY KEY, task TEXT)")
        print("🔱 ARKON: Triple Brain & Quad-Core System Online.", flush=True)
    except Exception as e:
        print(f"⚠️ Initialization Warning: {e}", flush=True)

threading.Thread(target=init_system, daemon=True).start()

# --- 4. మేధస్సు లాజిక్ (The Orchestrator) ---
def get_ai_response(prompt, provider="groq"):
    """అవసరానికి తగ్గట్టుగా బ్రెయిన్ ని మార్చుకుంటుంది"""
    if provider == "groq":
        chat = groq_client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama3-70b-8192"
        )
        return chat.choices[0].message.content
    elif provider == "openai":
        response = openai_client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
    return "Brain Selector Error"

@app.route('/')
def home():
    return "🔱 ARKON: Triple-Brain Guardian is watching over Challapalli."

@app.route('/ask', methods=['POST'])
def ask():
    data = request.get_json()
    if str(data.get("pin")) != str(ARKON_PIN):
        return jsonify({"output": "❌ Denied"}), 403
    
    prompt = data.get("prompt")
    brain = data.get("brain", "groq") # Default గా Groq వాడుతాం (Speed కోసం)
    
    answer = get_ai_response(prompt, brain)
    return jsonify({"answer": answer, "brain_used": brain})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 8080)))
