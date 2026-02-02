import os
import google.generativeai as genai
from openai import OpenAI

# 🔱 AI కాన్ఫిగరేషన్ (త్రిశక్తి)
gemini_key = os.environ.get("GEMINI_API_KEY")
openai_key = os.environ.get("OPENAI_API_KEY")
grok_key = os.environ.get("GROK_API_KEY")

# 🧠 జెమిని మేధస్సు సిద్ధం చేయడం
if gemini_key:
    genai.configure(api_key=gemini_key)
    gemini_model = genai.GenerativeModel('gemini-pro')
else:
    gemini_model = None

# 🧠 OpenAI మరియు Grok క్లయింట్లు
openai_client = OpenAI(api_key=openai_key) if openai_key else None
grok_client = OpenAI(api_key=grok_key, base_url="https://api.x.ai/v1") if grok_key else None

def process_request(command):
    command = command.lower().strip()
    
    # ⚡ మేధస్సు ఆదేశాలు
    if command.startswith("ask arkon"):
        prompt = command.replace("ask arkon", "").strip()
        return ask_ai_brain(prompt, brain_type="gemini")
    elif command.startswith("grok"):
        prompt = command.replace("grok", "").strip()
        return ask_ai_brain(prompt, brain_type="grok")
    
    # 🗣️ ఇతర శక్తులు (English, Memory, Scan) యథాతథంగా ఉంటాయి
    elif "learn english" in command: return train_spoken_english()
    elif "train memory" in command: return train_mind_power()
    elif "who am i" in command: return "🔱 Identity Confirmed. Welcome back, Creator Leela Krishna."
    elif "status" in command:
        return f"🔱 ARKON STATUS: Gemini:{'ON' if gemini_model else 'OFF'}, Grok:{'ON' if grok_client else 'OFF'}"
    
    return f"ARKON LOGIC: '{command}' unrecognized. Waiting for Creator's guidance."

def ask_ai_brain(prompt, brain_type="gemini"):
    """అర్కాన్ ఎంచుకున్న మేధస్సుతో ఆలోచిస్తాడు."""
    try:
        system_prompt = "You are Arkon, a loyal AI protector created by Leela Krishna for Xarvex mission."
        
        if brain_type == "gemini" and gemini_model:
            response = gemini_model.generate_content(f"{system_prompt} {prompt}")
            return f"🔱 ARKON (Gemini): {response.text}"
            
        elif brain_type == "grok" and grok_client:
            response = grok_client.chat.completions.create(
                model="grok-beta", # లేదా మీ ప్లాన్ లో ఉన్న మోడల్
                messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": prompt}]
            )
            return f"🔱 ARKON (Grok): {response.choices[0].message.content}"
            
        return "❌ ERROR: Selected Intelligence Core not configured."
    except Exception as e:
        return f"❌ NEURAL GLITCH: {str(e)}"

# ట్రైనింగ్ ఫంక్షన్స్ ...
def train_spoken_english(): return "🔱 LINGUISTIC SESSION #1: 'I am the architect of my own digital destiny.'"
def train_mind_power(): return "🔱 MIND POWER SESSION #1: Focus on visualization."
