from flask import Flask, os

app = Flask(__name__)

# 🛡️ ఇది రైల్వే కి 100% స్టాండర్డ్ సమాధానం ఇస్తుంది
@app.route('/health')
def health():
    # లాగ్స్ లో ఇది కనిపిస్తే పని పూర్తయినట్టే
    print("🔱 ARKON: High-Priority Stability Signal Sent!")
    return "OK", 200

@app.route('/')
def index():
    return "ARKON SUPREME IS ACTIVE", 200

if __name__ == "__main__":
    # రైల్వే ఇచ్చే $PORT ని ఖచ్చితంగా వాడాలి
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
