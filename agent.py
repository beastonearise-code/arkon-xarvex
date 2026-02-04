import redis
import os
import time

# మీ Railway Redis URL ఇక్కడ ఇవ్వండి
r = redis.from_url("మీ_REDIS_URL_ఇక్కడ")

print("🔱 ARKON AGENT: వింటున్నాను సృష్టికర్త...")

while True:
    cmd = r.get("ARKON_REMOTE_CMD")
    if cmd:
        cmd = cmd.decode('utf-8')
        print(f"🔱 ఆదేశం అందింది: {cmd}")
        if cmd == "SHUTDOWN":
            os.system("shutdown /s /t 1")
        elif cmd == "OPEN_CHROME":
            os.system("start chrome")
        
        r.delete("ARKON_REMOTE_CMD") # అమలు అయ్యాక డిలీట్ చేస్తుంది
    time.sleep(5)
