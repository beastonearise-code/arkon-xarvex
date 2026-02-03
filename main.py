from flask import Flask, request, jsonify, render_template
import os
import psycopg2
import threading # హెల్త్-చెక్ ఫెయిల్ అవ్వకుండా ఉండటానికి [cite: 2026-02-03]

app = Flask(__name__)

# మీ పక్కా URI
DB_URI = "postgresql://postgres.vapgjswwceerkwtxd:krishnaMlk%40143@aws-0-ap-south-1.pooler.supabase.com:6543/postgres"

def init_db():
    """డేటాబేస్ కనెక్షన్‌ను బ్యాక్‌గ్రౌండ్‌లో ప్రయత్నిస్తుంది [cite: 2026-02-03]"""
    try:
        conn = psycopg2.connect(DB_URI, connect_timeout=10)
        cur = conn.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS arkon_memory (id SERIAL PRIMARY KEY, key_data TEXT, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP);")
        conn.commit()
        cur.close()
        conn.close()
        print("🔱 ARKON: Eternal Memory Synced.")
    except Exception as e:
        print(f"⚠️ ARKON NOTICE: DB Sync Pending. {e}")

@app.route('/')
def dashboard():
    return render_template('index.html')

@app.route('/arkon/power', methods=['POST'])
def power():
    data = request.get_json()
    command = data.get("command", "").lower()
    
    if "memory check" in command:
        try:
            conn = psycopg2.connect(DB_URI, connect_timeout=3)
            output = "🔱 ARKON: Supabase Neural Sync is ACTIVE."
            conn.close()
        except:
            output = "❌ ARKON: Database Offline. Check Supabase settings."
    else:
        output = f"🔱 ARKON: Command '{command}' received."
        
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
    # మెమరీ సింక్‌ను వేరే దారిలో (Threading) పంపిస్తున్నాను [cite: 2026-02-03]
    threading.Thread(target=init_db).start() 
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
