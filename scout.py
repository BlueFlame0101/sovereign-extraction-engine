import requests
import os

def scout_models():
    print("--- 🛡️ Scout is exploring OpenRouter for new brains ---")
    
    url = "https://openrouter.ai/api/v1/models"
    headers = {
        "Authorization": f"Bearer {os.getenv('OPENROUTER_API_KEY')}",
        "Content-Type": "application/json"
    }

    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        models = response.json()['data']
        # Vi filtrerer efter modeller, der er billige og har høj kontekst
        # 'pricing' er i dollars per 1M tokens
        cheap_models = [
            m for m in models 
            if float(m['pricing']['prompt']) < 0.10  # Under 0.1$ pr. 1M tokens
        ]
        
        print(f"Fundet {len(cheap_models)} omkostningseffektive modeller.\n")
        print("Anbefalet Telefonbog (MODELS):")
        print("-" * 30)
        
        for m in cheap_models[:5]:  # Vi viser de 5 bedste fund
            print(f"'{m['name'].split(':')[0].lower()}': 'openrouter/{m['id']}',")
    else:
        print(f"Fejl ved scouting: {response.status_code}")

if __name__ == "__main__":
    scout_models()