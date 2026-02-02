import arkon_api_vault

def process_command(command):
    vault = arkon_api_vault.ArkonApiVault()
    key = vault.get_key("GEMINI_KEY")
    
    if not key:
        return "ARKON: సృష్టికర్త, తాళం చెవి (Key) లేకుండా Internet God నిద్రపోతున్నాడు."
    
    if "hi" in command.lower():
        return "ARKON: సృష్టికర్త లీలా కృష్ణ గారు, 66+ శక్తుల ఫైల్స్ అన్నీ నా మెదడులోకి ఇంజెక్ట్ అయ్యాయి."
    
    return f"ARKON: మీ ఆదేశం '{command}' విశ్లేషించబడింది. మిషన్ Xarvex కొనసాగుతోంది."
