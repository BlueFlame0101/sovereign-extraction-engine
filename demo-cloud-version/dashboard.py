import streamlit as st
import time
from config import get_cfo_model, get_cmo_model, get_cto_model
from micro_council import consult_finance, consult_growth, consult_tech
from macro_council import DepartmentHead, Sovereign

st.set_page_config(page_title="Council of Kings", page_icon="👑", layout="wide")

st.markdown("""
<style>
    .reportview-container { background: #0e1117; }
    h1 { color: #d4af37; text-align: center; font-family: 'Helvetica', sans-serif; }
    .stButton>button { width: 100%; background-color: #d4af37; color: black; font-weight: bold; }
    .chief-card { border: 1px solid #333; padding: 20px; border-radius: 10px; background-color: #1e1e1e; }
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.image("https://img.icons8.com/color/96/throne.png", width=80)
    st.header("⚙️ Council Configuration")
    
    st.subheader("1. The Sovereign's Strategy")
    persona_choice = st.radio(
        "Choose Decision Logic:",
        ["⚖️ The Balanced Architect (Standard)", 
         "⚔️ The Wartime General (Save Cash!)", 
         "🚀 The Silicon Visionary (Growth First!)"]
    )
    
    persona_prompts = {
        "⚖️ The Balanced Architect (Standard)": "Balance Stability, Budget, and Growth equally. Seek sustainable compromises.",
        "⚔️ The Wartime General (Save Cash!)": "PRIORITIZE CASH PRESERVATION ABOVE ALL. Be extremely risk-averse. Cut costs.",
        "🚀 The Silicon Visionary (Growth First!)": "PRIORITIZE GROWTH AND SPEED. Ignore budget constraints if they slow us down. Burn cash to win."
    }
    selected_persona = persona_prompts[persona_choice]

    st.subheader("2. Department Focus")
    dept_name_fin = st.text_input("Dept A Name", "Finance")
    dept_name_gro = st.text_input("Dept B Name", "Growth")
    dept_name_tec = st.text_input("Dept C Name", "Tech")

    st.info("System Status: 🟢 ONLINE (Llama/Mistral/Hermes Active)")

st.title("👑 THE SOVEREIGN COUNCIL")
st.markdown("<p style='text-align: center; color: gray;'>Autonomous Multi-Agent Strategic Decision System</p>", unsafe_allow_html=True)

st.write("---")

query = st.text_area("📜 Enter your strategic query:", height=100, placeholder="E.g., Should we pause the AWS migration to save cash?")

if st.button("🚀 CONVENE THE COUNCIL"):
    if not query:
        st.error("Please enter a query first.")
    else:
        st.subheader("⬇️ Phase 1: Micro-Intelligence Gathering")
        col1, col2, col3 = st.columns(3)
        status_box = st.status("Activation Signal Sent... Waking up 13 Agents...", expanded=True)
        
        status_box.write(f"💰 Consultng {dept_name_fin} Dept (3 Agents working)...")
        rep_fin = consult_finance(query)
        col1.success(f"✅ {dept_name_fin} Report Ready")
        with col1.expander("📄 View Full Report"):
            st.write(rep_fin)
            
        status_box.write(f"📈 Consulting {dept_name_gro} Dept (3 Agents working)...")
        rep_gro = consult_growth(query)
        col2.success(f"✅ {dept_name_gro} Report Ready")
        with col2.expander("📄 View Full Report"):
            st.write(rep_gro)
            
        status_box.write(f"💻 Consulting {dept_name_tec} Dept (3 Agents working)...")
        rep_tec = consult_tech(query)
        col3.success(f"✅ {dept_name_tec} Report Ready")
        with col3.expander("📄 View Full Report"):
            st.write(rep_tec)
            
        status_box.update(label="✅ Phase 1 Complete: All Data Secured", state="complete", expanded=False)
        
        st.write("---")
        st.subheader("🗣️ Phase 2: Boardroom Debate (The Chiefs Speak)")
        
        cfo = DepartmentHead(f"Head of {dept_name_fin}", get_cfo_model())
        cmo = DepartmentHead(f"Head of {dept_name_gro}", get_cmo_model())
        cto = DepartmentHead(f"Head of {dept_name_tec}", get_cto_model())
        
        col_a, col_b, col_c = st.columns(3)
        
        with col_a:
            st.markdown(f"### 💰 {dept_name_fin}")
            with st.spinner("Mistral Small formulating argument..."):
                arg_fin = cfo.give_opening(rep_fin, query)
            st.info(arg_fin)

        with col_b:
            st.markdown(f"### 📈 {dept_name_gro}")
            with st.spinner("Hermes 405B formulating argument..."):
                arg_gro = cmo.give_opening(rep_gro, query)
            st.info(arg_gro)

        with col_c:
            st.markdown(f"### 💻 {dept_name_tec}")
            with st.spinner("Llama 70B formulating argument..."):
                arg_tec = cto.give_opening(rep_tec, query)
            st.info(arg_tec)

        st.write("---")
        st.subheader("⚔️ Phase 3: Cross-Examination (Rebuttals)")
        
        with st.spinner("Chiefs are analyzing each other's arguments..."):
            reb_fin = cfo.give_rebuttal(arg_fin, f"{dept_name_gro}: {arg_gro} | {dept_name_tec}: {arg_tec}")
            reb_gro = cmo.give_rebuttal(arg_gro, f"{dept_name_fin}: {arg_fin} | {dept_name_tec}: {arg_tec}")
            reb_tec = cto.give_rebuttal(arg_tec, f"{dept_name_fin}: {arg_fin} | {dept_name_gro}: {arg_gro}")

        with st.chat_message("user", avatar="💰"):
            st.write(f"**{dept_name_fin} Rebuttal:** {reb_fin}")
        with st.chat_message("assistant", avatar="📈"):
            st.write(f"**{dept_name_gro} Rebuttal:** {reb_gro}")
        with st.chat_message("user", avatar="💻"):
            st.write(f"**{dept_name_tec} Rebuttal:** {reb_tec}")

        st.write("---")
        st.header("👑 Phase 4: The Sovereign Verdict")
        
        sov = Sovereign()
        with st.spinner("The Sovereign is triangulating the optimal strategy..."):
            verdict = sov.forward(
                query, 
                persona=selected_persona,
                args={'fin': arg_fin, 'gro': arg_gro, 'tec': arg_tec},
                rebuttals={'fin': reb_fin, 'gro': reb_gro, 'tec': reb_tec}
            )
        
        with st.expander("🧠 Open Sovereign's Internal Monologue (Reasoning Process)", expanded=False):
            st.markdown(f"**Strategic Lens:** {selected_persona}")
            st.write(verdict.internal_thought_process)
            
        st.success("### 📜 OFFICIAL DECREE")
        st.markdown(f"#### {verdict.final_decision}")