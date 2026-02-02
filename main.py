from flask import Flask, jsonify
import os

app = Flask(__name__)

# 🛡️ ఇది రైల్వే కి 'నేను 100% పర్ఫెక్ట్ గా ఉన్నాను' అని జేసన్ రూపంలో చెబుతుంది
@app.route('/health')
def health():
    # లాగ్స్ లో ఇది కనిపిస్తే కనెక్షన్ సక్సెస్ అని అర్థం
    print("🔱 ARKON: Health Check Pulse Sent to Railway!")
    return jsonify({"status": "stable", "entity": "Arkon Supreme"}), 200

@app.route('/')
def index():
    return "ARKON SYSTEM: CORE STABILIZED", 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
