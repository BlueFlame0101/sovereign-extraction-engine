"""
Interactive Router Console - Query Classification Testing Interface.

This module provides a command-line interface for testing the semantic
complexity router. Users can submit queries and observe real-time
routing decisions with scoring justification.

Usage:
    python interactive.py
    >>> Enter queries to test classification
    >>> Type 'exit' or 'quit' to terminate
"""

import sys
from router import route_query


def start_console():
    """
    Launch the interactive router testing console.
    
    Provides a REPL interface for submitting queries to the semantic
    complexity router. Displays routing decisions, confidence scores,
    and reasoning for each query.
    
    Keyboard Interrupt (Ctrl+C) or 'exit'/'quit' commands will
    gracefully terminate the session.
    """
    print("\n--- SOVEREIGN ROUTER CONSOLE ---")
    print("Type any question to test the AI classification.")
    print("Type 'exit' or 'quit' to stop.\n")

    while True:
        try:
            user_input = input("USER >> ")
        except KeyboardInterrupt:
            break

        if user_input.lower() in ["exit", "quit"]:
            print("Shutting down...")
            break

        if not user_input.strip():
            continue

        print("   Analyzing...", end="\r")
        try:
            result = route_query(user_input)

            lane_icon = "[FAST]" if result.route == "FAST_LANE" else "[DEEP]"
            print(f"   AI JUDGEMENT: {lane_icon} {result.route}")
            print(f"   SCORE:        {result.score}/10")
            print(f"   REASONING:    {result.reasoning}\n")

        except Exception as e:
            print(f"   ERROR: {e}\n")


if __name__ == "__main__":
    start_console()
