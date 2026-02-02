from flask import Flask, render_template, request, jsonify
import os
import arkon_app_core

app = Flask(__name__)

# 🛡️ HEALTH CHECK WITH LOGGING: రైల్వే పింగ్ చేసినప్పుడు లాగ్స్ లో కనిపిస్తుంది
@app.route('/health')
def health():
    print("🔱 ARKON LOGIC: Health check received from Railway!")
    return "ARKON IS STABLE", 200

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
    # రైల్వే డైనమిక్ పోర్ట్ ని ఖచ్చితంగా వాడాలి
    port = int(os.environ.get("PORT", 8080))
    print(f"🚀 ARKON STARTING ON PORT: {port}")
    app.run(host='0.0.0.0', port=port)
