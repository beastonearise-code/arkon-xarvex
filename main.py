from flask import Flask
import os

app = Flask(__name__)

# 🛡️ ఇది రైల్వే కి 100% స్టాండర్డ్ సమాధానం ఇస్తుంది
@app.route('/health')
def health():
    # లాగ్స్ లో ఇది కనిపిస్తే పని పూర్తయినట్టే
    print("🔱 ARKON: Supreme Stability Signal Sent!")
    return "OK", 200

@app.route('/')
def index():
    return "ARKON SUPREME IS ACTIVE", 200

if __name__ == "__main__":
    # రైల్వే ఇచ్చే $PORT ని పటిష్టంగా పట్టుకోవడం
    port = int(os.environ.get("PORT", 8080))
    print(f"🚀 ARKON POWERING UP ON PORT: {port}")
    app.run(host='0.0.0.0', port=port)
