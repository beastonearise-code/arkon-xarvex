from flask import Flask, render_template, request, jsonify
import os
import sys

# 🛡️ IMPORT PROTECTION: ఒకవేళ కోర్ ఫైల్ లో ఎర్రర్ ఉంటే ఇక్కడ తెలుస్తుంది
try:
    import arkon_app_core
except ImportError as e:
    print(f"❌ [ARKON CRITICAL]: Missing dependency or file: {str(e)}")
    sys.exit(1)

app = Flask(__name__)

# 🛡️ HEALTH CHECK: ఇది అత్యంత వేగంగా స్పందించాలి
@app.route('/health')
def health():
    return "OK", 200

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
    # రైల్వే ఇచ్చే $PORT ని పటిష్టంగా పట్టుకోవడం
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port, debug=False)
