from flask import Flask, request, jsonify, render_template # render_template ని జోడించాం
import os
import arkon_app_core

app = Flask(__name__)

@app.route('/')
def dashboard():
    # ఇది templates/index.html ని లోడ్ చేస్తుంది [cite: 2026-02-02]
    return render_template('index.html')

@app.route('/arkon/power', methods=['POST'])
def power():
    data = request.get_json()
    command = data.get("command", "")
    result = arkon_app_core.process_request(command)
    return jsonify({"status": "success", "output": result})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
