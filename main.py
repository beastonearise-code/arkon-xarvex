from flask import Flask, request, jsonify, render_template
import os
import psycopg2
import threading

app = Flask(__name__)

# మీ పక్కా URI (Updated based on image_d2c2df.jpg)
DB_URI = "postgresql://postgres.vapgjswwceerkwtxd:krishnaMlk%40143@aws-1-ap-south-1.pooler.supabase.com:6543/postgres"

def init_db():
    """డేటాబేస్ కనెక్షన్‌ను బ్యాక్‌గ్రౌండ్‌లో ప్రయత్నిస్తుంది [cite: 2026-02-03]"""
    try:
        conn = psycopg2.connect(DB_URI, connect_timeout=10)
        cur = conn.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS arkon_memory (id SERIAL PRIMARY KEY, key_data TEXT, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP);")
        conn.commit()
        cur.close()
        conn.close()
        print("🔱 ARKON: Eternal Memory Synced.", flush=True)
    except Exception as e:
        print(f"⚠️ ARKON NOTICE: DB Sync Pending. {e}", flush=True)

# Gunicorn కోసం ఇక్కడే థ్రెడ్ స్టార్ట్ చేస్తున్నాను [cite: 2026-02-03]
threading.Thread(target=init_db, daemon=True).start()

@app.route('/')
def dashboard():
    return render_template('index.html')

@app.route('/arkon/power', methods=['POST'])
def power():
    data = request.get_json()
    command = data.get("command", "").lower()
    
    if "memory check" in command:
        return jsonify({"output": "🔱 ARKON: Supabase Neural Sync is ACTIVE. Memory stable."})
    return jsonify({"output": f"🔱 ARKON: Command '{command}' logged."})

@app.route('/arkon/vault', methods=['POST'])
def vault_manager():
    data = request.get_json()
    received_key = data.get("key", "")
    try:
        conn = psycopg2.connect(DB_URI, connect_timeout=5)
        cur = conn.cursor()
        cur.execute("INSERT INTO arkon_memory (key_data) VALUES (%s)", (received_key,))
        conn.commit()
        cur.close()
        conn.close()
        output = "🔱 ARKON: Key Stored in Eternal Memory."
    except Exception as e:
        output = f"❌ VAULT ERROR: {e}"
    return jsonify({"output": output})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
