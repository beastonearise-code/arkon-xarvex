# Arkon Heartbeat Script (Diagnostic Tool)
import os
import requests

def check_keys():
    print("🔱 ARKON DIAGNOSTIC MODE: STARTING...")
    
    # 1. Search APIs Verification
    search_apis = {
        "SERPER": f"https://google.serper.dev/search",
        "TAVILY": f"https://api.tavily.com/search",
        "EXA": f"https://api.exa.ai/search"
    }
    
    # Test Serper
    res = requests.post(search_apis["SERPER"], 
                        headers={'X-API-KEY': os.getenv("SERPER_API_KEY")}, 
                        json={'q': 'test'})
    print(f"✅ Serper API: {'Connected' if res.status_code == 200 else '❌ FAILED'}")

    # Test Tavily
    res = requests.post(search_apis["TAVILY"], 
                        json={'api_key': os.getenv("TAVILY_API_KEY"), 'query': 'test'})
    print(f"✅ Tavily API: {'Connected' if res.status_code == 200 else '❌ FAILED'}")

    # Test Exa
    res = requests.post(search_apis["EXA"], 
                        headers={'x-api-key': os.getenv("EXA_API_KEY")}, 
                        json={'query': 'test'})
    print(f"✅ Exa AI: {'Connected' if res.status_code == 200 else '❌ FAILED'}")

check_keys()
