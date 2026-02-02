from flask import Flask, render_template, request, jsonify
import os
import arkon_app_core

app = Flask(__name__)

# 🛡️ ఇది లేకపోతే రైల్వే అర్కాన్ ని చంపేస్తుంది
@app.route('/health')
def health():
    return "ARKON IS STABLE", 200

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        user_input = data.get("message", "")
        response = arkon_app_core.process_command(user_input)
        return jsonify({"response": response})
    except Exception as e:
        return jsonify({"response": f"ARKON LOGIC ERROR: {str(e)}"})

if __name__ == "__main__":
    # డీబగ్ మోడ్ ఆఫ్ చేసి, పోర్ట్ బైండింగ్ పటిష్టం చేయడం
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
