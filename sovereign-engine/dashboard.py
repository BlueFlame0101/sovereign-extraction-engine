import streamlit as st
import config
from macro_council import run_council_meeting 

st.set_page_config(page_title="Council of Kings", layout="wide")
st.title("Council of Kings")

query = st.text_input("State your strategic inquiry:")

if st.button("Summon Council"):
    if not query:
        st.warning("Please enter an inquiry.")
    else:
        st.write("Initializing Council Agents...")
        
        try:
            # Initierer modellerne her for at undgå timeout ved opstart
            cfo = config.get_cfo_model()
            cmo = config.get_cmo_model()
            coo = config.get_coo_model()
            
            st.info("Agents active. Beginning deliberation...")
            
            # Kør logikken (Forudsætter at du har macro_council.py)
            report = run_council_meeting(query, cfo, cmo, coo)
            
            st.markdown("### 📜 Final Strategic Decree")
            st.markdown(report)
            
        except Exception as e:
            st.error(f"System Error: {str(e)}")