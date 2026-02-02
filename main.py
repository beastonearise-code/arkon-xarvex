from flask import Flask, request, jsonify
import os

try:
    import arkon_app_core
except ImportError:
    arkon_app_core = None

app = Flask(__name__)

@app.route('/health')
@app.route('/')
def health():
    return "ARKON SYSTEM: STABLE & ONLINE 🔱", 200

@app.route('/arkon/power', methods=['POST'])
def power():
    data = request.get_json()
    command = data.get("command", "")
    
    if arkon_app_core:
        # 🧠 మెదడుకి ఆదేశం పంపడం
        result = arkon_app_core.process_request(command)
        return jsonify({"status": "success", "output": result})
    else:
        return jsonify({"status": "error", "message": "CORE_NOT_LOADED"}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
