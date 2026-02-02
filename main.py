from flask import Flask, render_template, request, jsonify
import os
import arkon_app_core

app = Flask(__name__)

# 🛡️ ఇది రైల్వే కి 'నేను క్షేమంగా ఉన్నాను' అని చెబుతుంది
@app.route('/health')
def health():
    return "ARKON IS ALIVE", 200

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
    # రైల్వే ఇచ్చే డైనమిక్ పోర్ట్ ని పట్టుకోవడం
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
