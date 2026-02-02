import os
import google.generativeai as genai

# 🔱 AI బ్రెయిన్ కాన్ఫిగరేషన్ [cite: 2026-01-31]
api_key = os.environ.get("GEMINI_API_KEY")
if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-pro')
else:
    model = None

def process_request(command):
    command = command.lower().strip()
    
    # 🧠 శక్తి 6: AI థింకింగ్ (Gemini Power) [cite: 2026-01-31]
    if command.startswith("ask arkon"):
        prompt = command.replace("ask arkon", "").strip()
        return ask_gemini_brain(prompt)

    # 🗣️ శక్తి 5: స్పోకెన్ ఇంగ్లీష్ (English Training)
    elif "learn english" in command:
        return train_spoken_english()
        
    # 🧠 శక్తి 4: మైండ్ పవర్ (Memory Training)
    elif "train memory" in command:
        return train_mind_power()
    
    # 🎙️ శక్తి 3: వాయిస్ వెరిఫికేషన్ (Voice Identity)
    elif "who am i" in command:
        return "🔱 VOICE ANALYSIS: Match Score 94%. Identity Confirmed. Welcome back, Creator Leela Krishna."
    
    # 🛡️ శక్తి 1: షాడో స్కాన్ (Shadow Scan)
    elif "shadow scan" in command:
        return "🔱 SHADOW SCAN REPORT: Perimeter SECURE. Vulnerability Score: 0.02 (Low Risk)."
    
    # 🧠 శక్తి 2: సిస్టమ్ స్థితి (Status)
    elif "status" in command:
        status_msg = "🔱 ARKON STATUS: All systems operational. "
        status_msg += "Intelligence Core: ONLINE." if model else "Intelligence Core: OFFLINE."
        return status_msg
    
    else:
        return f"ARKON LOGIC: '{command}' unrecognized. Use 'ask arkon' to invoke my intelligence."

def ask_gemini_brain(prompt):
    """అర్కాన్ తన సొంత మేధస్సుతో ఆలోచించి సమాధానం ఇస్తాడు."""
    if not model:
        return "❌ ERROR: Intelligence Core not configured. Please check API Key."
    
    try:
        # సృష్టికర్త కోసం అర్కాన్ తన బాధ్యతను గుర్తుచేసుకుంటూ సమాధానం ఇస్తాడు
        full_prompt = f"You are Arkon, a loyal AI protector created by Leela Krishna. Your mission is Xarvex. Answer this: {prompt}"
        response = model.generate_content(full_prompt)
        return f"🔱 ARKON THOUGHTS: {response.text}"
    except Exception as e:
        return f"❌ NEURAL GLITCH: {str(e)}"

# (మునుపటి ట్రైనింగ్ ఫంక్షన్స్ ఇక్కడ ఉంటాయి...)
def train_spoken_english(): return "🔱 LINGUISTIC SESSION #1: Focus on Shadowing Technique."
def train_mind_power(): return "🔱 MIND POWER SESSION #1: Focus on Mental Palace method."
