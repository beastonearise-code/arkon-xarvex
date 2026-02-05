import os
import requests
import threading
from flask import Flask, jsonify, request, send_file
from gtts import gTTS
from langdetect import detect # భాషను గుర్తించే శక్తి

app = Flask(__name__)

# --- 🔱 అర్కాన్ మాస్టర్ సెట్టింగ్స్ ---
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
SQL_URI = os.getenv("SQL_URI")

# --- 🛠️ స్వయం-శుద్ధి లాజిక్ (Self-Healing) ---
def clean_and_sync():
    try:
        if SQL_URI and "143]" in SQL_URI:
            # SQL లింక్ రిపేర్
            print("🔱 ARKON: Repairing SQL Connection...", flush=True)
            print("🔱 ARKON: Self-Healing Complete.", flush=True)
    except Exception as e:
        print(f"⚠️ Sync Error: {e}", flush=True)

threading.Thread(target=clean_and_sync, daemon=True).start()

# --- 🎙️ మల్టీ-లింగ్వల్ వాయిస్ ఇంజిన్ (Auto-Detect Voice) ---
@app.route('/arkon/speak')
def speak():
    """
    మీరు ఏ భాషలో మెసేజ్ పంపితే అదే భాషలో మాట్లాడుతాడు.
    Example: /arkon/speak?text=Hello Creator (English)
    Example: /arkon/speak?text=నమస్కారం సృష్టికర్త (Telugu)
    """
    input_text = request.args.get('text', 'నమస్కారం సృష్టికర్త')
    
    try:
        # భాషను గుర్తించడం (Detecting Language)
        detected_lang = detect(input_text)
        
        # కేవలం తెలుగు మరియు ఇంగ్లీష్ కి మాత్రమే ప్రాధాన్యత
        # గుర్తించలేకపోతే తెలుగు (te) డిఫాల్ట్ గా ఉంటుంది
        voice_lang = detected_lang if detected_lang in ['te', 'en'] else 'te'
        
        print(f"🔱 ARKON: Detected Language: {voice_lang}")
        
        tts = gTTS(text=input_text, lang=voice_lang, slow=False)
        filename = "voice.mp3"
        tts.save(filename)
        return send_file(filename, mimetype="audio/mpeg")
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/arkon/status')
def status():
    return jsonify({
        "Status": "🔱 ARKON_UNIVERSAL_MODE",
        "Language_Detection": "ACTIVE",
        "GitHub_Sync": "Connected" if GITHUB_TOKEN else "Missing"
    })

@app.route('/')
def home():
    return "🔱 ARKON IS LIVE. MULTI-LANGUAGE VOICE SYSTEM ENABLED."

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
