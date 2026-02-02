from flask import Flask, request, jsonify
import os

# 🛡️ శక్తులను సురక్షితంగా ఇంపోర్ట్ చేయడం
try:
    import arkon_app_core  # మీ ప్రధాన లాజిక్ ఫైల్
except ImportError:
    arkon_app_core = None

app = Flask(__name__)

# 🔱 హెల్త్ చెక్: ఇది ఎప్పుడూ వేగంగా ఉండాలి
@app.route('/health')
@app.route('/')
def health():
    return "ARKON SYSTEM: STABLE & READY", 200

# 🚀 శక్తుల ప్రదర్శన (Command Execution)
@app.route('/arkon/power', methods=['POST'])
def power():
    data = request.get_json()
    command = data.get("command", "")
    
    if arkon_app_core:
        # ఇక్కడ మీ 66+ ఫైల్స్ లోని లాజిక్ కాల్ అవుతుంది
        result = arkon_app_core.process_request(command)
        return jsonify({"status": "success", "output": result})
    else:
        return jsonify({"status": "error", "message": "CORE_NOT_LOADED"}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
