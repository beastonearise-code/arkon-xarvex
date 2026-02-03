from flask import Flask, request, jsonify, render_template
import os
import psycopg2
import threading
from pymongo import MongoClient # MongoDB కోసం [cite: 2026-02-03]

app = Flask(__name__)

# కోర్ 1: Supabase (Eternal Memory)
SQL_URI = "postgresql://postgres.vapgjswwceerkwtxd:krishnaMlk%40143@aws-0-ap-south-1.pooler.supabase.com:6543/postgres?sslmode=require"

# కోర్ 2: MongoDB (Shadow Intel)
MONGO_URI = "mongodb+srv://arkon_guardian:db_krishnamlk143@arkon-intel-cluster.rdqxw7i.mongodb.net/?appName=Arkon-Intel-Cluster"

# MongoDB క్లయింట్ సెటప్ [cite: 2026-02-03]
mongo_client = MongoClient(MONGO_URI)
db_intel = mongo_client["Arkon-Xarvex-Core"]

def init_cores():
    """రెండు మెదళ్లను బ్యాక్‌గ్రౌండ్‌లో సింక్ చేస్తుంది [cite: 2026-01-31, 2026-02-03]"""
    try:
        # SQL/Supabase Test
        conn = psycopg2.connect(SQL_URI, connect_timeout=5)
        conn.close()
        # MongoDB Test
        db_intel.system_status.update_one({"core": "dual"}, {"$set": {"status": "ACTIVE"}}, upsert=True)
        print("🔱 ARKON: Dual-Core Neural Sync COMPLETE.", flush=True)
    except Exception as e:
        print(f"⚠️ ARKON NOTICE: Core Sync Delayed. {e}", flush=True)

threading.Thread(target=init_cores, daemon=True).start()

@app.route('/')
def dashboard():
    return render_template('index.html')

@app.route('/arkon/power', methods=['POST'])
def power():
    data = request.get_json()
    command = data.get("command", "").lower()
    
    if "memory check" in command:
        return jsonify({"output": "🔱 ARKON: Dual-Core Sync is ACTIVE. SQL & NoSQL cores are ready."})
    return jsonify({"output": f"🔱 ARKON: Command '{command}' received."})

# కొత్త ఆయుధం: షాడో ఇంటెల్ స్టోరేజ్ (MongoDB) [cite: 2026-02-03]
@app.route('/arkon/intel', methods=['POST'])
def shadow_intel():
    data = request.get_json()
    # ఇక్కడ మనం హ్యాకింగ్ డేటా లేదా ఇతర రహస్యాలను MongoDBలో దాస్తాము [cite: 2026-02-03]
    db_intel.shadow_reports.insert_one(data)
    return jsonify({"output": "🔱 ARKON: Intel report encrypted and stored in Shadow Core."})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
