"""
Interactive Router Console - Query Classification Testing Interface.

This module provides a command-line interface for testing the query
complexity router. Accepts user input and displays routing decisions
with complexity scores and reasoning.

Usage:
    python interactive.py
    
Commands:
    exit, quit: Terminate the console session.
"""

import sys
from router import route_query


def start_console():
    """
    Initialize interactive REPL for query routing validation.
    
    Continuously accepts user queries and invokes the routing classifier,
    displaying route assignment, complexity score, and reasoning output.
    Handles graceful shutdown via exit commands or keyboard interrupt.
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
            print(f"   ROUTE:     {lane_icon} {result.route}")
            print(f"   SCORE:     {result.score}/10")
            print(f"   REASONING: {result.reasoning}\n")

        except Exception as e:
            print(f"   ERROR: {e}\n")


if __name__ == "__main__":
    start_console()
