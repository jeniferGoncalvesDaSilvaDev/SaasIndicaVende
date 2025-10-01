import streamlit as st
import requests
import json
from auth import login, logout, get_current_user
from indicador import show_indicador_interface
from vendedor import show_vendedor_interface
from gestor import show_gestor_interface

st.set_page_config(
    page_title="IndicaVende",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1E88E5;
        text-align: center;
        margin-bottom: 2rem;
    }
    .lead-card {
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid #1E88E5;
        background-color: #f8f9fa;
        margin-bottom: 1rem;
    }
    .status-novo { border-left-color: #FF9800; }
    .status-em_contato { border-left-color: #2196F3; }
    .status-em_negociacao { border-left-color: #9C27B0; }
    .status-fechado { border-left-color: #4CAF50; }
    .status-perdido { border-left-color: #F44336; }
</style>
""", unsafe_allow_html=True)

def main():
    if 'user' not in st.session_state:
        st.session_state.user = None
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown('<div class="main-header">🚀 IndicaVende</div>', unsafe_allow_html=True)
    
    if not st.session_state.user:
        show_login_screen()
    else:
        show_main_interface()

def show_login_screen():
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.subheader("Login")
        
        with st.form("login_form"):
            email = st.text_input("Email")
            password = st.text_input("Senha", type="password")
            submit = st.form_submit_button("Entrar")
            
            if submit:
                user = login(email, password)
                if user:
                    st.session_state.user = user
                    st.rerun()
                else:
                    st.error("Credenciais inválidas")

def show_main_interface():
    user = st.session_state.user
    
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        st.write(f"Bem-vindo, **{user['name']}** ({user['role'].title()})")
    with col3:
        if st.button("Sair"):
            logout()
            st.rerun()
    
    st.markdown("---")
    
    if user['role'] == 'indicador':
        show_indicador_interface()
    elif user['role'] == 'vendedor':
        show_vendedor_interface()
    elif user['role'] == 'gestor':
        show_gestor_interface()

if __name__ == "__main__":
    main()
