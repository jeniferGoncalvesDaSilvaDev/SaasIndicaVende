import streamlit as st
from auth import get_current_user, make_authenticated_request
import requests

def show_indicador_interface():
    user = get_current_user()
    
    menu = st.sidebar.selectbox("Menu", ["Novo Lead", "Meus Leads"])
    
    if menu == "Novo Lead":
        show_novo_lead()
    elif menu == "Meus Leads":
        show_meus_leads()

def show_novo_lead():
    st.header("📋 Novo Lead")
    
    with st.form("novo_lead_form"):
        client_name = st.text_input("Nome do Cliente *")
        phone = st.text_input("Telefone/WhatsApp *")
        city_state = st.text_input("Cidade/Estado *")
        observation = st.text_area("Observação")
        
        response = make_authenticated_request("/users/")
        if response and response.status_code == 200:
            users = response.json()
            vendedores = [u for u in users if u['role'] == 'vendedor']
            vendedor_options = {f"{v['name']} (ID: {v['id']})": v['id'] for v in vendedores}
            
            vendedor_selecionado = st.selectbox(
                "Selecionar Vendedor *",
                options=list(vendedor_options.keys())
            )
            
            submit = st.form_submit_button("Enviar Indicação")
            
            if submit:
                if not all([client_name, phone, city_state]):
                    st.error("Preencha todos os campos obrigatórios (*)")
                else:
                    lead_data = {
                        "client_name": client_name,
                        "phone": phone,
                        "city_state": city_state,
                        "observation": observation,
                        "vendedor_id": vendedor_options[vendedor_selecionado]
                    }
                    
                    response = make_authenticated_request("/leads/", "POST", lead_data)
                    if response and response.status_code == 200:
                        st.success("Lead enviado com sucesso!")
                    else:
                        st.error("Erro ao enviar lead")

def show_meus_leads():
    st.header("📊 Meus Leads")
    
    response = make_authenticated_request("/leads/")
    if response and response.status_code == 200:
        leads = response.json()
        
        if not leads:
            st.info("Nenhum lead enviado ainda.")
            return
        
        for lead in leads:
            status_color = {
                "novo": "status-novo",
                "em_contato": "status-em_contato",
                "em_negociacao": "status-em_negociacao",
                "fechado": "status-fechado",
                "perdido": "status-perdido"
            }.get(lead['status'], "")
            
            st.markdown(f"""
            <div class="lead-card {status_color}">
                <h4>{lead['client_name']}</h4>
                <p><strong>Telefone:</strong> {lead['phone']} | 
                   <strong>Cidade:</strong> {lead['city_state']} | 
                   <strong>Status:</strong> {lead['status'].replace('_', ' ').title()}</p>
                <p><strong>Observação:</strong> {lead['observation'] or 'Nenhuma'}</p>
                <small><strong>Data:</strong> {lead['created_at'][:10]} | 
                       <strong>Vendedor ID:</strong> {lead.get('vendedor_id', 'N/A')}</small>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.error("Erro ao carregar leads")
