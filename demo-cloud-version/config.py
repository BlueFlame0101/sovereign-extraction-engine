import dspy
import os
import pathlib
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("OPENROUTER_API_KEY")
if not api_key:
    try:
        env_path = pathlib.Path(__file__).parent / '.env'
        with open(env_path, 'r') as f:
            for line in f:
                if line.startswith("OPENROUTER_API_KEY="):
                    api_key = line.strip().split("=", 1)[1]
                    break
    except:
        pass

os.environ["OPENAI_API_KEY"] = api_key if api_key else "MISSING_KEY"

def create_model(model_name):
    return dspy.LM(
        model="openai/" + model_name,
        api_base="https://openrouter.ai/api/v1",
        max_tokens=2000
    )

def get_worker_a(): return create_model("mistralai/mistral-7b-instruct:free")
def get_worker_b(): return create_model("meta-llama/llama-3.2-3b-instruct:free")
def get_worker_c(): return create_model("meta-llama/llama-3.3-70b-instruct:free")

TEAM_FINANCE = [get_worker_a(), get_worker_b(), get_worker_c()]
TEAM_GROWTH = [get_worker_a(), get_worker_b(), get_worker_c()]
TEAM_TECH = [get_worker_a(), get_worker_b(), get_worker_c()]

def get_cfo_model(): return create_model("mistralai/mistral-small-3.1-24b-instruct:free")
def get_cmo_model(): return create_model("nousresearch/hermes-3-llama-3.1-405b:free")
def get_cto_model(): return create_model("meta-llama/llama-3.3-70b-instruct:free")

BOSS_MODEL = create_model("meta-llama/llama-3.3-70b-instruct:free")

def get_sovereign_model(): return BOSS_MODEL
def get_finance_worker_1(): return TEAM_FINANCE[0]
def get_growth_worker_1(): return TEAM_GROWTH[0]
def get_tech_worker_1(): return TEAM_TECH[0]