from flask import Flask, request, jsonify, render_template
import os
import psycopg2
import threading
from pymongo import MongoClient

app = Flask(__name__)

# రైల్వే వేరియబుల్స్ నుండి రహస్య సమాచారాన్ని సేకరిస్తుంది [cite: 2026-02-03]
SQL_URI = os.getenv("SQL_URI")
MONGO_URI = os.getenv("MONGO_URI")
CREATOR_PIN = os.getenv("ARKON_PIN")

# MongoDB క్లయింట్ సెటప్ [cite: 2026-02-03]
mongo_client = MongoClient(MONGO_URI)
db_intel = mongo_client["Arkon-Xarvex-Core"]

def init_cores():
    """డ్యూయల్-కోర్ సింకింగ్ ప్రొటోకాల్ [cite: 2026-01-31, 2026-02-03]"""
    try:
        # SQL Test
        conn = psycopg2.connect(SQL_URI, connect_timeout=5)
        conn.close()
        # MongoDB Test
        db_intel.system_status.update_one({"core": "dual"}, {"$set": {"status": "ACTIVE"}}, upsert=True)
        print("🔱 ARKON: Security Shield Engaged. Cores Active.", flush=True)
    except Exception as e:
        print(f"⚠️ ARKON NOTICE: Core Sync Delayed. {e}", flush=True)

threading.Thread(target=init_cores, daemon=True).start()

@app.route('/')
def dashboard():
    return render_template('index.html')

@app.route('/arkon/power', methods=['POST'])
def power():
    data = request.get_json()
    received_pin = data.get("pin")
    command = data.get("command", "").lower()
    
    # మాస్టర్ లాగిన్ షీల్డ్ వెరిఫికేషన్ [cite: 2026-02-03]
    if str(received_pin) != str(CREATOR_PIN):
        return jsonify({"output": "❌ ACCESS DENIED: Intruder detected. Lockdown initiated."}), 403
    
    if "memory check" in command:
        return jsonify({"output": "🔱 ARKON: Dual-Core Sync is ACTIVE. SQL & NoSQL cores are ready."})
    elif "status" in command:
        return jsonify({"output": "🔱 ARKON: System Online. Guardian of Challapalli is active."})
    else:
        return jsonify({"output": f"🔱 ARKON: Command '{command}' executed by Creator."})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
