import streamlit as st
from auth import get_current_user, make_authenticated_request
import pandas as pd

def show_gestor_interface():
    menu = st.sidebar.selectbox("Menu Gestor", ["Leads", "Usuários", "Relatórios"])
    
    if menu == "Leads":
        show_gestor_leads()
    elif menu == "Usuários":
        show_gestor_usuarios()
    elif menu == "Relatórios":
        show_gestor_relatorios()

def show_gestor_leads():
    st.header("👥 Todos os Leads")
    
    response = make_authenticated_request("/leads/")
    if response and response.status_code == 200:
        leads = response.json()
        
        if leads:
            df_data = []
            for lead in leads:
                df_data.append({
                    "ID": lead['id'],
                    "Cliente": lead['client_name'],
                    "Telefone": lead['phone'],
                    "Cidade": lead['city_state'],
                    "Indicador ID": lead.get('indicador_id', 'N/A'),
                    "Vendedor ID": lead.get('vendedor_id', 'N/A'),
                    "Status": lead['status'].replace('_', ' ').title(),
                    "Data": lead['created_at'][:10]
                })
            
            df = pd.DataFrame(df_data)
            st.dataframe(df, use_container_width=True)
        else:
            st.info("Nenhum lead cadastrado.")
    else:
        st.error("Erro ao carregar leads")

def show_gestor_usuarios():
    st.header("👥 Gestão de Usuários")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Usuários Cadastrados")
        response = make_authenticated_request("/users/")
        if response and response.status_code == 200:
            users = response.json()
            
            user_data = []
            for user in users:
                user_data.append({
                    "ID": user['id'],
                    "Nome": user['name'],
                    "Email": user['email'],
                    "Perfil": user['role'].title(),
                    "Data Cadastro": user['created_at'][:10]
                })
            
            df = pd.DataFrame(user_data)
            st.dataframe(df, use_container_width=True)
        else:
            st.error("Erro ao carregar usuários")
    
    with col2:
        st.subheader("Novo Usuário")
        with st.form("novo_usuario"):
            name = st.text_input("Nome")
            email = st.text_input("Email")
            password = st.text_input("Senha", type="password")
            role = st.selectbox("Perfil", ["gestor", "vendedor", "indicador"])
            
            if st.form_submit_button("Criar Usuário"):
                st.info("Funcionalidade em desenvolvimento")

def show_gestor_relatorios():
    st.header("📈 Relatórios")
    
    response = make_authenticated_request("/leads/")
    if response and response.status_code == 200:
        leads = response.json()
        
        if leads:
            total_leads = len(leads)
            fechados = len([l for l in leads if l['status'] == 'fechado'])
            perdidos = len([l for l in leads if l['status'] == 'perdido'])
            taxa_conversao = (fechados / total_leads * 100) if total_leads > 0 else 0
            
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Total Leads", total_leads)
            col2.metric("Fechados", fechados)
            col3.metric("Perdidos", perdidos)
            col4.metric("Taxa Conversão", f"{taxa_conversao:.1f}%")
            
            st.subheader("Leads por Status")
            status_counts = pd.Series([l['status'] for l in leads]).value_counts()
            st.bar_chart(status_counts)
        else:
            st.info("Nenhum dado disponível para relatórios.")
