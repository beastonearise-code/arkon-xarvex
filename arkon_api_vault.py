import os

class ArkonApiVault:
    def __init__(self):
        # 🔱 LOGIC: క్లౌడ్ నుండి కీలను గ్రహించడం
        # ఇక్కడ మనం కేస్-సెన్సిటివ్ కాకుండా లోతుగా వెతుకుతాం
        self.keys = {k.upper(): v for k, v in os.environ.items()}
        print(f"🔱 ARKON VAULT: {len(self.keys)} variables detected in cloud.")

    def get_key(self, key_name):
        # పేరులో ఖాళీలు ఉన్నా తొలగించి వెతుకుతుంది [cite: 2026-02-02]
        clean_name = key_name.strip().upper()
        return self.keys.get(clean_name)
