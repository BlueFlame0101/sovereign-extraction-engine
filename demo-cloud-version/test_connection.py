from config import lm
import dspy

def system_check():
    print(f"--- 🔌 INITIATING CONNECTION SEQUENCE ---")
    print(f"--- TARGET: {lm.model} ---")

    try:
        # Vi definerer en ultra-simpel 'Signatur' for at teste DSPy
        # Input: command -> Output: status
        ping = dspy.Predict("command -> status")

        # Vi sender signalet
        response = ping(command="System Check. Respond with exactly one word: 'ONLINE'.")

        print(f"🤖 RAW RESPONSE: {response.status}")

        # Validering af svaret
        if "ONLINE" in response.status.upper():
            print("\n✅ SYSTEM ONLINE: The Sovereign Engine is active.")
        else:
            print(f"\n⚠️ WARNING: Signal received, but payload was unexpected: '{response.status}'")

    except Exception as e:
        print(f"\n❌ CRITICAL FAILURE: Connection severed.")
        print(f"Error log: {e}")

if __name__ == "__main__":
    system_check()
