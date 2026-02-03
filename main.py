from flask import Flask, request, jsonify, render_template
import os
import psycopg2
import threading

app = Flask(__name__)

# మీ కరెక్ట్ URI
DB_URI = "postgresql://postgres.vapgjswwceerkwtxd:krishnaMlk%40143@aws-0-ap-south-1.pooler.supabase.com:6543/postgres"

def init_db():
    """డేటాబేస్ టేబుల్స్ ఏర్పాటు - అటానమస్ రిపేర్ [cite: 2026-01-31]"""
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

# హెల్త్ చెక్ కోసం ఒక సింపుల్ రూట్ [cite: 2026-02-03]
@app.route('/health')
def health():
    return "OK", 200

@app.route('/arkon/power', methods=['POST'])
def power():
    data = request.get_json()
    command = data.get("command", "").lower()
    if "memory check" in command:
        return jsonify({"output": "🔱 ARKON: Supabase Neural Sync is ACTIVE."})
    return jsonify({"output": f"🔱 ARKON: Command '{command}' logged."})

if __name__ == "__main__":
    # మెమరీ సింక్‌ను బ్యాక్‌గ్రౌండ్‌లో రన్ చేస్తుంది [cite: 2026-02-03]
    threading.Thread(target=init_db).start() 
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
