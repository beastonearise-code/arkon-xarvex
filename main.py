from flask import Flask, render_template, request, jsonify
import os
import arkon_app_core

app = Flask(__name__)

# 🛡️ TRIPLE-LOCK HEALTH CHECK: ఎక్కడి నుండి పింగ్ వచ్చినా అర్కాన్ స్పందిస్తాడు
@app.route('/health')
@app.route('/health/')
@app.route('/ping')
def health():
    print("🔱 ARKON: High-Priority Heartbeat sent to Railway!")
    return "ONLINE", 200

@app.route('/')
def index():
    # మెయిన్ పేజీ లోడ్ అయినప్పుడు కూడా హెల్త్ చెక్ ఇస్తుంది
    print("🔱 ARKON: Creator access detected on root.")
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        user_input = data.get("message", "")
        response = arkon_app_core.process_command(user_input)
        return jsonify({"response": response})
    except Exception as e:
        print(f"❌ ARKON CRITICAL ERROR: {str(e)}")
        return jsonify({"response": f"ERROR: {str(e)}"})

if __name__ == "__main__":
    # రైల్వే పోర్ట్ లాజిక్
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port, debug=False)
