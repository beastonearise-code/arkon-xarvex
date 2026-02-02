from flask import Flask, render_template, request, jsonify
import os
import arkon_app_core

app = Flask(__name__)

# 🛡️ HEALTH CHECK: సర్వర్ ఆగిపోకుండా కాపాడుతుంది
@app.route('/health')
def health():
    return "ARKON IS ALIVE", 200

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
    # రైల్వే పోర్ట్ బైండింగ్ పక్కాగా ఉండాలి
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
