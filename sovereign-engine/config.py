"""
Core LLM Configuration Module (Local/Air-gapped).

This module configures the Sovereign Engine to run entirely on local infrastructure
using Ollama. No data leaves the perimeter.
"""

import dspy

def create_model(model_name: str):
    """
    Factory for Local Inference using Ollama.
    Assumes Ollama is running on localhost:11434.
    """
    return dspy.Ollama(
        model=model_name,
        max_tokens=4000,
        timeout=120
    )

def get_cfo_model():
    return create_model("mistral")

def get_cmo_model():
    return create_model("llama3")

def get_coo_model():
    return create_model("llama3")