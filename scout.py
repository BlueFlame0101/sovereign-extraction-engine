"""
Model Discovery Service - OpenRouter API Scanner.

This module queries the OpenRouter model registry to identify cost-effective
LLM endpoints suitable for multi-agent orchestration. Filters by inference
cost threshold to optimize operational expenditure.

Output:
    Generates model identifier mappings for integration into agent configuration.
"""

import requests
import os


def scout_models():
    """
    Query OpenRouter API for available models and filter by cost threshold.
    
    Retrieves complete model catalog and applies pricing filter to identify
    candidates with prompt cost below $0.10 per 1M tokens. Outputs formatted
    model identifiers for configuration integration.
    
    Raises:
        Prints error status code on API failure.
    """
    print("--- Model Discovery Service Initiated ---")
    
    url = "https://openrouter.ai/api/v1/models"
    headers = {
        "Authorization": f"Bearer {os.getenv('OPENROUTER_API_KEY')}",
        "Content-Type": "application/json"
    }

    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        models = response.json()['data']
        cheap_models = [
            m for m in models 
            if float(m['pricing']['prompt']) < 0.10
        ]
        
        print(f"Identified {len(cheap_models)} cost-effective models.\n")
        print("Model Registry Output:")
        print("-" * 30)
        
        for m in cheap_models[:5]:
            print(f"'{m['name'].split(':')[0].lower()}': 'openrouter/{m['id']}',")
    else:
        print(f"API Error: {response.status_code}")


if __name__ == "__main__":
    scout_models()