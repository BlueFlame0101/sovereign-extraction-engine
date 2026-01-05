import sys
from router import route_query

def start_console():
    print("\n--- 🛡️ SOVEREIGN ROUTER CONSOLE 🛡️ ---")
    print("Type any question to test the AI classification.")
    print("Type 'exit' or 'quit' to stop.\n")

    while True:
        # 1. Hent input fra dig
        try:
            user_input = input("USER >> ")
        except KeyboardInterrupt:
            break

        if user_input.lower() in ["exit", "quit"]:
            print("Shutting down...")
            break

        if not user_input.strip():
            continue

        # 2. Send det til AI-routeren
        print("   Analyzing...", end="\r")
        try:
            # Vi bruger ikke force_deep her, vi vil se AI'ens ærlige mening
            result = route_query(user_input)

            # 3. Vis dommen
            lane_icon = "🚀" if result.route == "FAST_LANE" else "🧠"
            print(f"   AI JUDGEMENT: {lane_icon} {result.route}")
            print(f"   SCORE:        {result.score}/10")
            print(f"   REASONING:    {result.reasoning}\n")

        except Exception as e:
            print(f"   ❌ ERROR: {e}\n")

if __name__ == "__main__":
    start_console()
