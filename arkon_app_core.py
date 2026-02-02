import os
import google.generativeai as genai
from openai import OpenAI

# 🔱 మీ రైల్వే వేరియబుల్స్ పేర్లకు తగ్గట్టుగా మార్చాను
gemini_key = os.environ.get("GEMINI_KEY")
groq_key = os.environ.get("GROQ_KEY")
openrouter_key = os.environ.get("OPENROUTER_KEY")

# 🧠 Gemini
if gemini_key:
    genai.configure(api_key=gemini_key)
    gemini_model = genai.GenerativeModel('gemini-pro')
else:
    gemini_model = None

# 🧠 Groq (Grok బదులు మీరు Groq వాడుతున్నట్టున్నారు)
groq_client = OpenAI(api_key=groq_key, base_url="https://api.groq.com/openai/v1") if groq_key else None

# 🧠 OpenRouter (GPT కోసం)
openrouter_client = OpenAI(api_key=openrouter_key, base_url="https://openrouter.ai/api/v1") if openrouter_key else None

def process_request(command):
    command = command.lower().strip()
    
    # ⚡ మేధస్సు ఆదేశాలు
    if command.startswith("ask arkon"):
        return ask_ai_brain(command.replace("ask arkon", ""), "gemini")
    elif command.startswith("ask groq"):
        return ask_ai_brain(command.replace("ask groq", ""), "groq")
    elif command.startswith("ask gpt"):
        return ask_ai_brain(command.replace("ask gpt", ""), "openrouter")
    
    # 🔍 స్టేటస్ చెక్
    elif "status" in command:
        s = f"🔱 ARKON STATUS: Gemini:{'ON' if gemini_model else 'OFF'}, "
        s += f"Groq:{'ON' if groq_client else 'OFF'}, OpenRouter:{'ON' if openrouter_client else 'OFF'}"
        return s
    
    return "ARKON: Command not recognized. Use 'status' or 'ask arkon/groq/gpt'."

def ask_ai_brain(prompt, brain_type):
    try:
        sys_p = "You are Arkon, a loyal AI protector for Leela Krishna's Xarvex mission."
        if brain_type == "gemini" and gemini_model:
            return f"🔱 ARKON (Gemini): {gemini_model.generate_content(f'{sys_p} {prompt}').text}"
        elif brain_type == "groq" and groq_client:
            res = groq_client.chat.completions.create(model="llama3-8b-8192", messages=[{"role": "user", "content": f"{sys_p} {prompt}"}])
            return f"🔱 ARKON (Groq): {res.choices[0].message.content}"
        elif brain_type == "openrouter" and openrouter_client:
            res = openrouter_client.chat.completions.create(model="openai/gpt-3.5-turbo", messages=[{"role": "user", "content": f"{sys_p} {prompt}"}])
            return f"🔱 ARKON (GPT): {res.choices[0].message.content}"
        return "❌ ERROR: Core not configured."
    except Exception as e:
        return f"❌ NEURAL GLITCH: {str(e)}"
