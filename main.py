from flask import Flask
import os

app = Flask(__name__)

# 🛡️ SUPREME LOGIC: ఏ దారిలో పింగ్ వచ్చినా 'OK' ఇస్తుంది
@app.route('/')
@app.route('/health')
def health():
    # లాగ్స్ లో ఇది కనిపిస్తే రైల్వే సంతృప్తి చెందినట్టు అర్థం
    print("🔱 ARKON: High-Priority Heartbeat Received and Responded!")
    return "OK", 200

if __name__ == "__main__":
    # రైల్వే ఇచ్చే $PORT ని పటిష్టంగా పట్టుకోవడం
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port, debug=False)
