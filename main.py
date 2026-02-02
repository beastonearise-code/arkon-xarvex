from flask import Flask, render_template, request, jsonify
import os
import arkon_app_core

app = Flask(__name__)

# 🛡️ LOGICAL SHIELD: రైల్వే హెల్త్ చెక్ ని ఆమోదించడం
@app.route('/health')
def health():
    return "OK", 200

@app.route('/')
def index():
    # ఇండెక్స్ ఫైల్ ని లోడ్ చేస్తుంది [cite: 2026-02-02]
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        user_input = data.get("message", "")
        response = arkon_app_core.process_command(user_input)
        return jsonify({"response": response})
    except Exception as e:
        return jsonify({"response": f"ARKON ERROR: {str(e)}"})

if __name__ == "__main__":
    # రైల్వే ఇచ్చే PORT ని ఖచ్చితంగా వాడాలి
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
