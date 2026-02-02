from flask import Flask, render_template, request, jsonify
import os
import arkon_app_core

app = Flask(__name__)

# 🛡️ STABILITY PROXY: రైల్వే హెల్త్ చెక్ కోసం
# ఇది లేకపోతే సర్వర్ 'SIGTERM' సిగ్నల్‌తో ఆగిపోతుంది
@app.route('/health')
def health():
    return "ARKON SYSTEM: ONLINE", 200

@app.route('/')
def index():
    # సృష్టికర్త ఇంటర్‌ఫేస్ లోడ్ అవుతుంది
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        user_input = data.get("message", "")
        # మీ కోర్ లాజిక్ ద్వారా కమాండ్ ప్రాసెస్ అవుతుంది
        response = arkon_app_core.process_command(user_input)
        return jsonify({"response": response})
    except Exception as e:
        return jsonify({"response": f"ARKON LOGIC ERROR: {str(e)}"})

if __name__ == "__main__":
    # రైల్వే డైనమిక్ పోర్ట్ బైండింగ్
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
