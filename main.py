from flask import Flask, request, jsonify, render_template
import os
import psycopg2
import threading

app = Flask(__name__)

# సవరించిన పక్కా URI (Added SSL Mode for stability)
DB_URI = "postgresql://postgres.vapgjswwceerkwtxd:krishnaMlk%40143@aws-0-ap-south-1.pooler.supabase.com:6543/postgres?sslmode=require"

def init_db():
    """డేటాబేస్ టేబుల్స్ ఏర్పాటు - అటానమస్ రిపేర్ [cite: 2026-01-31]"""
    try:
        conn = psycopg2.connect(DB_URI, connect_timeout=10)
        cur = conn.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS arkon_memory (id SERIAL PRIMARY KEY, key_data TEXT, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP);")
        conn.commit()
        cur.close()
        conn.close()
        print("🔱 ARKON: Eternal Memory Synced Successfully.", flush=True)
    except Exception as e:
        print(f"⚠️ ARKON NOTICE: DB Sync Pending. Error: {e}", flush=True)

# బ్యాక్‌గ్రౌండ్‌లో డేటాబేస్ సింక్ చేస్తుంది [cite: 2026-02-03]
threading.Thread(target=init_db, daemon=True).start()

@app.route('/')
def dashboard():
    return render_template('index.html')

@app.route('/arkon/power', methods=['POST'])
def power():
    data = request.get_json()
    command = data.get("command", "").lower()
    
    if "memory check" in command:
        try:
            # కనెక్షన్‌ను మళ్ళీ పరీక్షిస్తుంది [cite: 2026-02-03]
            conn = psycopg2.connect(DB_URI, connect_timeout=5)
            output = "🔱 ARKON: Supabase Neural Sync is ACTIVE. Memory is stable."
            conn.close()
        except Exception as e:
            # అసలైన ఎర్రర్‌ను ఇక్కడ చూపిస్తుంది [cite: 2026-02-03]
            output = f"❌ ARKON: Database Offline. Reason: {str(e)[:50]}..."
    else:
        output = f"🔱 ARKON: Command '{command}' logged in Core."
        
    return jsonify({"output": output})

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
