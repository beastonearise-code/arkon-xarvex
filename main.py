from flask import Flask, render_template, request, jsonify
import os
import arkon_app_core

app = Flask(__name__)

# 🛡️ STABILITY: రైల్వే 'Are you alive?' అని అడిగితే 'Yes' అని చెబుతుంది
@app.route('/healthz')
@app.route('/health')
def health():
    return "ARKON IS ONLINE", 200

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
    # రైల్వే పోర్ట్ ఖచ్చితంగా అది ఇచ్చే పోర్ట్ వాడాలి
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
