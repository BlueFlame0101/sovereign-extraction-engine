import urllib.request
import json
import os
from pathlib import Path

# 1. Find API Nøglen manuelt (for at være sikker)
base_dir = Path(__file__).parent
env_path = base_dir / '.env'

api_key = None
if env_path.exists():
    with open(env_path, 'r') as f:
        for line in f:
            if line.startswith("OPENROUTER_API_KEY="):
                api_key = line.strip().split("=", 1)[1]
                break

if not api_key:
    # Fallback til environment variable
    api_key = os.environ.get("OPENROUTER_API_KEY")

if not api_key:
    print("❌ KUNNE IKKE FINDE NØGLEN. Tjek .env filen.")
    exit()

# 2. Spørg OpenRouter API
print("🔄 Henter model-liste fra OpenRouter...")
req = urllib.request.Request("https://openrouter.ai/api/v1/models")
req.add_header("Authorization", f"Bearer {api_key}")

try:
    with urllib.request.urlopen(req) as response:
        data = json.loads(response.read().decode())

        print("\n✅ HER ER DE GRATIS MODELLER DU KAN BRUGE NU:")
        print("-" * 50)

        count = 0
        # Vi leder efter modeller der slutter på ':free' eller koster 0
        for model in data['data']:
            id = model['id']
            pricing = model.get('pricing', {})
            prompt_price = pricing.get('prompt', '1')

            # Tjek om den er gratis (enten via ID eller pris)
            if ":free" in id or prompt_price == "0" or prompt_price == 0:
                print(f"• {id}")
                count += 1

        print("-" * 50)
        print(f"Total fundet: {count}")
        print("Kopier denne liste ind i chatten!")

except Exception as e:
    print(f"❌ Fejl ved API kald: {e}")
