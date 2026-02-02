from flask import Flask, render_template, request, jsonify
import os
import arkon_app_core

app = Flask(__name__)

# 🛡️ STABILITY LOGIC: రైల్వే హెల్త్ చెక్ కోసం
@app.route('/health')
@app.route('/ping')
def health():
    return "ARKON SYSTEM: ONLINE", 200

@app.route('/')
def index():
    # టెంప్లేట్స్ ఫోల్డర్ లోని ఫైల్ ని లోడ్ చేస్తుంది [cite: 2026-02-02]
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_input = data.get("message", "")
    response = arkon_app_core.process_command(user_input)
    return jsonify({"response": response})

if __name__ == "__main__":
    # రైల్వే పోర్ట్ బైండింగ్ (ఖచ్చితంగా 8080 ఉండాలి)
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
