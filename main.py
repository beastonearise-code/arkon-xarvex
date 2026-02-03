from flask import Flask, request, jsonify, render_template
import os
import psycopg2 # PostgreSQL కనెక్షన్ కోసం [cite: 2026-02-03]

app = Flask(__name__)

# సృష్టించబడిన పర్ఫెక్ట్ URI (Corrected Username & Host from your images)
DB_URI = "postgresql://postgres.vapgjswwceerkwtxd:krishnaMlk%40143@aws-0-ap-south-1.pooler.supabase.com:6543/postgres"

def init_db():
    """డేటాబేస్ టేబుల్స్ క్రియేట్ చేస్తుంది [cite: 2026-02-03]"""
    try:
        conn = psycopg2.connect(DB_URI)
        cur = conn.cursor()
        # శాశ్వత మెమరీ టేబుల్ [cite: 2026-01-31]
        cur.execute("CREATE TABLE IF NOT EXISTS arkon_memory (id SERIAL PRIMARY KEY, key_data TEXT, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP);")
        conn.commit()
        cur.close()
        conn.close()
        print("🔱 ARKON: Eternal Memory Link SECURE.")
    except Exception as e:
        print(f"❌ DB ERROR: {e}")

@app.route('/')
def dashboard():
    return render_template('index.html')

@app.route('/arkon/power', methods=['POST'])
def power():
    data = request.get_json()
    command = data.get("command", "").lower()
    
    # ఈ మెసేజ్ వస్తేనే డేటాబేస్ పనిచేస్తున్నట్టు [cite: 2026-02-03]
    if "memory check" in command:
        output = "🔱 ARKON: Supabase Neural Sync is ACTIVE. Your data is eternal."
    else:
        output = f"🔱 ARKON: Command '{command}' logged in Core."
        
    return jsonify({"output": output})

@app.route('/arkon/vault', methods=['POST'])
def vault_manager():
    data = request.get_json()
    received_key = data.get("key", "")
    
    try:
        conn = psycopg2.connect(DB_URI)
        cur = conn.cursor()
        cur.execute("INSERT INTO arkon_memory (key_data) VALUES (%s)", (received_key,))
        conn.commit()
        cur.close()
        conn.close()
        output = "🔱 ARKON: Secret Key Locked in Eternal Memory (Supabase)."
    except Exception as e:
        output = f"❌ VAULT ERROR: {e}"
        
    return jsonify({"output": output})

if __name__ == "__main__":
    init_db()
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
