import dspy
import os
import sys
from dotenv import load_dotenv
from pathlib import Path

# --- 1. SIKKER INDLÆSNING AF .ENV ---
base_dir = Path(__file__).parent
env_path = base_dir / '.env'

if env_path.exists():
    load_dotenv(dotenv_path=env_path)

api_key = os.getenv("OPENROUTER_API_KEY")
if not api_key:
    api_key = os.environ.get("OPENROUTER_API_KEY")

if not api_key:
    print("\n❌ CRITICAL ERROR: API Key is missing!")
    sys.exit(1)

print(f"✅ API Key loaded. (Length: {len(api_key)})")

# --- MODEL FACTORY ---

def create_model(model_name):
    full_name = f"openrouter/{model_name}"
    return dspy.LM(
        model=full_name,
        api_key=api_key,
        api_base="https://openrouter.ai/api/v1",
        max_tokens=1000
    )

# --- MICRO WORKERS (Fodfolket - Hurtige modeller) ---
def get_worker_a(): return create_model("mistralai/mistral-7b-instruct:free")
def get_worker_b(): return create_model("meta-llama/llama-3.2-3b-instruct:free")
def get_worker_c(): return create_model("meta-llama/llama-3.3-70b-instruct:free")

TEAM_FINANCE = [get_worker_a(), get_worker_b(), get_worker_c()]
TEAM_GROWTH = [get_worker_a(), get_worker_b(), get_worker_c()]
TEAM_TECH = [get_worker_a(), get_worker_b(), get_worker_c()]

# --- MACRO CHIEFS (Bestyrelsen - Tunge, forskellige hjerner) ---

# 1. CFO: Mistral Small 24B (Fransk/Europæisk logik - God til data)
def get_cfo_model():
    return create_model("mistralai/mistral-small-3.1-24b-instruct:free")

# 2. CMO: Llama 3.1 405B (Hermes 3 - Verdens største open source model! Kreativ.)
# (Bemærk: Denne er enorm. Hvis den fejler pga. trafik, falder vi tilbage til Llama 70B)
def get_cmo_model():
    return create_model("nousresearch/hermes-3-llama-3.1-405b:free")

# 3. CTO: Llama 3.3 70B (Pålidelig ingeniør-hjerne)
def get_cto_model():
    return create_model("meta-llama/llama-3.3-70b-instruct:free")

# 4. THE SOVEREIGN: Skal være den klogeste og mest stabile.
# Vi bruger Llama 3.3 70B som dommer, da den er mest stabil til konklusioner.
BOSS_MODEL = create_model("meta-llama/llama-3.3-70b-instruct:free")
