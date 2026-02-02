from flask import Flask, render_template, request, jsonify
import os
import arkon_app_core

app = Flask(__name__)

# 🛡️ ఇది రైల్వే కి 100% నమ్మకాన్ని ఇస్తుంది
@app.route('/health')
def health():
    print("🔱 ARKON: Heartbeat sent to Railway!")
    return "OK", 200

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_input = data.get("message", "")
    response = arkon_app_core.process_command(user_input)
    return jsonify({"response": response})

if __name__ == "__main__":
    # ఇది అత్యంత ముఖ్యం: రైల్వే ఇచ్చే $PORT ని పట్టుకోవడం
    # ఒకవేళ PORT లేకపోతే 8080 వాడుకుంటుంది
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port, debug=False)
