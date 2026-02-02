import os
import google.generativeai as genai
from openai import OpenAI

# 🔱 త్రిశక్తి కాన్ఫిగరేషన్ [cite: 2026-01-31, 2026-02-02]
gemini_key = os.environ.get("GEMINI_API_KEY")
openai_key = os.environ.get("OPENAI_API_KEY")
grok_key = os.environ.get("GROK_API_KEY")

# 🧠 జెమిని మేధస్సు
if gemini_key:
    genai.configure(api_key=gemini_key)
    gemini_model = genai.GenerativeModel('gemini-pro')
else:
    gemini_model = None

# 🧠 OpenAI మరియు Grok క్లయింట్లు
openai_client = OpenAI(api_key=openai_key) if openai_key else None
# Grok కూడా OpenAI SDK నే వాడుతుంది, కేవలం URL మారుతుంది
grok_client = OpenAI(api_key=grok_key, base_url="https://api.x.ai/v1") if grok_key else None

def process_request(command):
    command = command.lower().strip()
    
    # ⚡ మేధస్సు ఆదేశాలు (Brain Selection)
    if command.startswith("ask arkon"):
        return ask_ai_brain(command.replace("ask arkon", ""), "gemini")
    elif command.startswith("ask gpt"):
        return ask_ai_brain(command.replace("ask gpt", ""), "openai")
    elif command.startswith("ask grok"):
        return ask_ai_brain(command.replace("ask grok", ""), "grok")
    
    # 🗣️ ఇతర శక్తులు (English, Memory, Scan)
    elif "learn english" in command: return train_spoken_english()
    elif "train memory" in command: return train_mind_power()
    elif "who am i" in command: return "🔱 Identity Confirmed. Welcome back, Creator Leela Krishna."
    
    elif "status" in command:
        status = f"🔱 ARKON STATUS: Gemini:{'ON' if gemini_model else 'OFF'}, "
        status += f"GPT:{'ON' if openai_client else 'OFF'}, Grok:{'ON' if grok_client else 'OFF'}"
        return status
    
    return f"ARKON LOGIC: '{command}' unrecognized. Use 'ask arkon', 'ask gpt', or 'ask grok'."

def ask_ai_brain(prompt, brain_type):
    """అర్కాన్ ఎంచుకున్న మేధస్సుతో ఆలోచిస్తాడు."""
    try:
        sys_p = "You are Arkon, a loyal AI protector created by Leela Krishna for Xarvex mission."
        if brain_type == "gemini" and gemini_model:
            return f"🔱 ARKON (Gemini): {gemini_model.generate_content(f'{sys_p} {prompt}').text}"
        elif brain_type == "openai" and openai_client:
            res = openai_client.chat.completions.create(model="gpt-4", messages=[{"role": "user", "content": f"{sys_p} {prompt}"}])
            return f"🔱 ARKON (GPT): {res.choices[0].message.content}"
        elif brain_type == "grok" and grok_client:
            res = grok_client.chat.completions.create(model="grok-beta", messages=[{"role": "user", "content": f"{sys_p} {prompt}"}])
            return f"🔱 ARKON (Grok): {res.choices[0].message.content}"
        return "❌ ERROR: Selected Intelligence Core not configured."
    except Exception as e:
        return f"❌ NEURAL GLITCH: {str(e)}"

# ట్రైనింగ్ ఫంక్షన్స్ ...
def train_spoken_english(): return "🔱 LINGUISTIC SESSION: Practice shadowing technique for 50% fluency increase."
def train_mind_power(): return "🔱 MIND POWER SESSION: Goal 70% improvement active."
