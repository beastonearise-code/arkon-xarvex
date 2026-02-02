from flask import Flask, request, jsonify
import os

app = Flask(__name__)

# 🛡️ SUPREME LOGIC: ఏ దారిలో పింగ్ వచ్చినా 200 OK ఇస్తుంది
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    # లాగ్స్ లో మనకు క్లియర్ గా కనిపిస్తుంది
    print(f"🔱 ARKON RECEIVED PING ON: /{path}")
    return "ARKON IS ONLINE AND STABLE", 200

if __name__ == "__main__":
    # రైల్వే పోర్ట్ బైండింగ్
    port = int(os.environ.get("PORT", 8080))
    print(f"🚀 ARKON POWERING UP ON PORT: {port}")
    app.run(host='0.0.0.0', port=port, debug=False)
