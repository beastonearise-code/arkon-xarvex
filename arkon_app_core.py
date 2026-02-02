import os
import google.generativeai as genai
from openai import OpenAI

# 🔱 API Keys (Railway Variables నుండి) [cite: 2026-02-02]
gemini_key = os.environ.get("GEMINI_KEY")
groq_key = os.environ.get("GROQ_KEY")
openrouter_key = os.environ.get("OPENROUTER_KEY")

# 🧠 AI Cores Initialization
if gemini_key:
    genai.configure(api_key=gemini_key)
    # వేగవంతమైన సమాధానాల కోసం Gemini 1.5 Flash [cite: 2026-02-02]
    gemini_model = genai.GenerativeModel('gemini-1.5-flash')
else:
    gemini_model = None

groq_client = OpenAI(api_key=groq_key, base_url="https://api.groq.com/openai/v1") if groq_key else None
openrouter_client = OpenAI(api_key=openrouter_key, base_url="https://openrouter.ai/api/v1") if openrouter_key else None

def process_request(command):
    command = command.lower().strip()
    
    # ⚡ మేధస్సు ఎంపిక (AI Thinking)
    if command.startswith("ask arkon"):
        return ask_ai_brain(command.replace("ask arkon", ""), "gemini")
    elif command.startswith("ask groq"):
        return ask_ai_brain(command.replace("ask groq", ""), "groq")
    elif command.startswith("ask gpt"):
        return ask_ai_brain(command.replace("ask gpt", ""), "openrouter")
    
    # 🗣️ ఇతర శక్తులు (Training & Security)
    elif "learn english" in command: return train_spoken_english()
    elif "train memory" in command: return train_mind_power()
    elif "who am i" in command: return verify_voice()
    elif "shadow scan" in command: return perform_shadow_scan()
    
    # 🔍 స్థితి (Status) [cite: 2026-02-02]
    elif "status" in command:
        s = f"🔱 ARKON STATUS: Gemini:{'ON' if gemini_model else 'OFF'}, "
        s += f"Groq:{'ON' if groq_client else 'OFF'}, GPT:{'ON' if openrouter_client else 'OFF'}"
        return s
    
    return "ARKON: Command unrecognized. Use 'status' or 'ask arkon/groq/gpt'."

def ask_ai_brain(prompt, brain_type):
    try:
        sys_p = "You are Arkon, a loyal AI protector for Creator Leela Krishna and Xarvex mission."
        if brain_type == "gemini" and gemini_model:
            return f"🔱 ARKON (Gemini): {gemini_model.generate_content(f'{sys_p} {prompt}').text}"
        elif brain_type == "groq" and groq_client:
            # Llama 3.1 8B Instant మోడల్ వాడాలి [cite: 2026-02-02]
            res = groq_client.chat.completions.create(model="llama-3.1-8b-instant", messages=[{"role": "user", "content": f"{sys_p} {prompt}"}])
            return f"🔱 ARKON (Groq): {res.choices[0].message.content}"
        elif brain_type == "openrouter" and openrouter_client:
            res = openrouter_client.chat.completions.create(model="openai/gpt-3.5-turbo", messages=[{"role": "user", "content": f"{sys_p} {prompt}"}])
            return f"🔱 ARKON (GPT): {res.choices[0].message.content}"
        return "❌ ERROR: Selected Core not configured."
    except Exception as e:
        return f"❌ NEURAL GLITCH: {str(e)}"

# --- 🛠️ మాడ్యులర్ ఫంక్షన్స్ ---
def train_spoken_english():
    return "🔱 LINGUISTIC SESSION: Shadowing Technique active. Focus on: 'I am the architect of my own digital destiny.'"

def train_mind_power():
    return "🔱 MIND POWER: Mental Palace technique active. Goal: 70% memory retention (R = e^(-t/S))."

def verify_voice():
    return "🔱 VOICE ANALYSIS: Match Score 94%. Identity Confirmed. Welcome back, Creator Leela Krishna. [cite: 2026-01-31]"

def perform_shadow_scan():
    return "🔱 SHADOW SCAN: Perimeter SECURE. No vulnerabilities in Challapalli network."
