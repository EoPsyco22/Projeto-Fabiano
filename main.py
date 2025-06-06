import streamlit as st
import cadastro_academia
import pagina_inicial

if "pagina" not in st.session_state:
    st.session_state["pagina"] = "login"

if st.session_state["pagina"] == "login" or st.session_state["pagina"] == "cadastro":
    cadastro_academia.app() 
elif st.session_state["pagina"] == "pagina_inicial":
    pagina_inicial.app() 
else:
    st.write("Página não encontrada")