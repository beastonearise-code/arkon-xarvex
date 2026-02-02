from flask import Flask, request, make_response
import os

app = Flask(__name__)

# 🛡️ SUPREME STABILITY: ఏ దారిలో పింగ్ వచ్చినా 100% స్టాండర్డ్ సమాధానం ఇస్తుంది
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    print(f"🔱 ARKON RECEIVED PING ON: /{path}")
    # రైల్వే కి అర్కాన్ క్షేమంగా ఉన్నాడని బలంగా చెబుతాము
    response = make_response("ARKON SYSTEM: ONLINE AND STABLE", 200)
    response.headers["Content-Type"] = "text/plain"
    return response

if __name__ == "__main__":
    # రైల్వే ఇచ్చే $PORT ని పటిష్టంగా పట్టుకోవడం
    port = int(os.environ.get("PORT", 8080))
    print(f"🚀 ARKON POWERING UP ON PORT: {port}")
    app.run(host='0.0.0.0', port=port, debug=False)
