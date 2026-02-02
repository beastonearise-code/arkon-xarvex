import os

# 🔱 ARKON API VAULT: CLOUD INJECTION PROTOCOL
class ArkonApiVault:
    def __init__(self):
        self.status = "CLOUD_VAULT_ACTIVE"
        print(f"🔱 ARKON: {self.status}")

    def get_key(self, key_name):
        return os.getenv(key_name)

if __name__ == "__main__":
    vault = ArkonApiVault()
    print("✅ [SUCCESS]: అర్కాన్ ఇప్పుడు మేల్కొన్నాడు.")
