from agents import alpha_agent, delta_agent, FastResponder

def test_personalities():
    query = "We should rewrite our entire backend in Rust to make it 5% faster."

    print(f"🔥 QUERY: '{query}'\n")

    # 1. Test Alpha (Teknikeren)
    print("--- 🔵 ALPHA (Tech) SPEAKING ---")
    res_alpha = alpha_agent(query)
    print(f"{res_alpha.analysis}\n")

    # 2. Test Delta (Økonomen)
    print("--- 🟢 DELTA (Finance) SPEAKING ---")
    res_delta = delta_agent(query)
    print(f"{res_delta.analysis}\n")

    # 3. Test Fast Lane (Bare for at tjekke den virker)
    print("--- 🚀 FAST LANE CHECK ---")
    fast = FastResponder()
    res_fast = fast("What is Rust?")
    print(f"Answer: {res_fast.answer}\n")

if __name__ == "__main__":
    test_personalities()
