from flask import Flask, render_template, request, jsonify
import os
import arkon_app_core

app = Flask(__name__)

# 🛡️ ఇది రైల్వే కి 'నేను క్షేమంగా ఉన్నాను' అని చెప్పే అత్యున్నత మార్గం
@app.route('/health')
def health():
    # లాగ్స్ లో ఈ మెసేజ్ కనిపిస్తే కోడ్ రన్ అవుతున్నట్టు అర్థం
    print("🔱 ARKON: Direct Heartbeat to Railway Engine!")
    return "OK", 200

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
    # 🚨 అత్యంత ముఖ్యం: రైల్వే ఇచ్చే డైనమిక్ పోర్ట్ ని పట్టుకోవడం
    # లాగ్స్ లో ఈ పోర్ట్ ఏంటో ప్రింట్ చేస్తుంది
    target_port = int(os.environ.get("PORT", 8080))
    print(f"🚀 ARKON DEPLOYED ON PORT: {target_port}")
    app.run(host='0.0.0.0', port=target_port, debug=False)
