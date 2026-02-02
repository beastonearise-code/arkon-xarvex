from flask import Flask, render_template, request, jsonify
import os
import arkon_app_core

app = Flask(__name__)

# 🛡️ STABILITY LOGIC: రైల్వే హెల్త్ చెక్ ని ఆమోదించడం
@app.route('/health')
def health():
    return "ARKON SYSTEM: STABLE", 200

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
    # రైల్వే పోర్ట్ బైండింగ్ (ఖచ్చితంగా 8080 ఉండాలి)
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
