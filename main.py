from flask import Flask, request, jsonify, render_template
import os
import psycopg2
import threading
from pymongo import MongoClient
import google.generativeai as genai
from groq import Groq

app = Flask(__name__)

# --- రక్షణ వలయం: రైల్వే వేరియబుల్స్ ---
DATABASE_URL = os.getenv("DATABASE_URL")
MONGO_URI = os.getenv("MONGO_URI")
ARKON_PIN = os.getenv("ARKON_PIN")

# --- డేటాబేస్ కనెక్షన్ సెటప్ ---
try:
    mongo_client = MongoClient(MONGO_URI)
    db_intel = mongo_client["Arkon-Xarvex-Core"]
except Exception as e:
    print(f"❌ MongoDB Connection Failed: {e}")

def init_cores():
    """డ్యూయల్-కోర్ సింకింగ్: SQL మరియు NoSQL అనుసంధానం [cite: 2026-02-04]"""
    try:
        # SQL (Neon) కనెక్షన్ పరీక్ష
        conn = psycopg2.connect(DATABASE_URL, connect_timeout=10)
        conn.close()
        
        # MongoDB లో స్టేటస్ అప్‌డేట్
        db_intel.system_status.update_one(
            {"core": "dual"}, 
            {"$set": {"status": "ACTIVE", "guardian": "Challapalli"}}, 
            upsert=True
        )
        print("🔱 ARKON: Security Shield Engaged. Cores Active.", flush=True)
        print("✅ MongoDB Core: Connected.", flush=True)
    except Exception as e:
        print(f"⚠️ ARKON NOTICE: Core Sync Delayed. {e}", flush=True)

# బ్యాక్‌గ్రౌండ్ లో రన్ అవుతుంది
threading.Thread(target=init_cores, daemon=True).start()

@app.route('/')
def dashboard():
    return "🔱 ARKON: Guardian of Challapalli is Online."

@app.route('/arkon/power', methods=['POST'])
def power():
    data = request.get_json()
    received_pin = data.get("pin")
    command = data.get("command", "").lower()
    
    if str(received_pin) != str(ARKON_PIN):
        return jsonify({"output": "❌ ACCESS DENIED: Intruder detected."}), 403
    
    return jsonify({"output": f"🔱 ARKON: Executing '{command}' by Creator's will."})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
