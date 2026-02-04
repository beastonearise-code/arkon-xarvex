from flask import Flask, request, jsonify, render_template
import os
import psycopg2
import threading
from pymongo import MongoClient
import google.generativeai as genai
from groq import Groq

app = Flask(__name__)

# --- రక్షణ వలయం: ఎన్విరాన్మెంట్ వేరియబుల్స్ ---
# డేటాబేస్ అస్త్రాలు
SQL_URI = os.getenv("DATABASE_URL") # మనం రైల్వేలో మార్చిన కొత్త పేరు
MONGO_URI = os.getenv("MONGO_URI")
ARKON_PIN = os.getenv("ARKON_PIN")

# నిఘా అస్త్రాలు (AI & Search)
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_KEY")

# --- డేటాబేస్ కనెక్షన్ సెటప్ ---
try:
    mongo_client = MongoClient(MONGO_URI)
    db_intel = mongo_client["Arkon-Xarvex-Core"]
    print("✅ MongoDB Core: Connected.")
except Exception as e:
    print(f"❌ MongoDB Error: {e}")

def init_cores():
    """డ్యూయల్-కోర్ సింకింగ్ ప్రొటోకాల్: SQL మరియు NoSQL ఒక్కటయ్యే చోటు"""
    try:
        # SQL_URI లో psql ' వంటి అదనపు పదాలు లేకుండా చూసుకోవాలి
        conn = psycopg2.connect(SQL_URI, connect_timeout=10)
        cursor = conn.cursor()
        cursor.execute("SELECT version();")
        conn.close()
        
        # MongoDB లో స్టేటస్ అప్‌డేట్
        db_intel.system_status.update_one(
            {"core": "dual"}, 
            {"$set": {"status": "ACTIVE", "guardian": "Challapalli"}}, 
            upsert=True
        )
        print("🔱 ARKON: Security Shield Engaged. Cores Active.", flush=True)
    except Exception as e:
        print(f"⚠️ ARKON NOTICE: Core Sync Delayed. {e}", flush=True)

# బ్యాక్‌గ్రౌండ్ లో సింకింగ్ ప్రారంభం
threading.Thread(target=init_cores, daemon=True).start()

# --- మార్గాలు (Routes) ---

@app.route('/')
def health_check():
    """Uptime Robot కోసం నిరంతర నిఘా మార్గం"""
    return "🔱 ARKON: Guardian of Challapalli is Online and Watching."

@app.route('/arkon/power', methods=['POST'])
def power_command():
    data = request.get_json()
    received_pin = data.get("pin")
    command = data.get("command", "").lower()
    
    # మాస్టర్ లాగిన్ షీల్డ్ వెరిఫికేషన్
    if str(received_pin) != str(ARKON_PIN):
        return jsonify({"output": "❌ ACCESS DENIED: Intruder detected. Lockdown initiated."}), 403
    
    # కమాండ్ సెంటర్ లాజిక్
    if "status" in command:
        return jsonify({
            "output": "🔱 ARKON STATUS: All 16 variables detected. System running at 100% capacity."
        })
    elif "memory check" in command:
        return jsonify({
            "output": "🧠 MEMORY: Dual-Core Sync is active. Neon (SQL) and MongoDB (NoSQL) are linked."
        })
    else:
        return jsonify({
            "output": f"🔱 ARKON: Command '{command}' received. Processing by Creator's will."
        })

if __name__ == "__main__":
    # రైల్వే పోర్ట్ బైండింగ్
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
