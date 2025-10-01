import streamlit as st
from auth import get_current_user, make_authenticated_request
import pandas as pd

def show_vendedor_interface():
    st.header("💼 Painel do Vendedor")
    
    response = make_authenticated_request("/leads/")
    if response and response.status_code == 200:
        leads = response.json()
        
        if not leads:
            st.info("Nenhum lead atribuído ainda.")
            return
        
        for lead in leads:
            with st.expander(f"🔹 {lead['client_name']} - {lead['status'].replace('_', ' ').title()}"):
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.write(f"**Telefone:** {lead['phone']}")
                    st.write(f"**Cidade/Estado:** {lead['city_state']}")
                    st.write(f"**Observação:** {lead['observation'] or 'Nenhuma'}")
                    st.write(f"**Data:** {lead['created_at'][:10]}")
                
                with col2:
                    status_options = ["novo", "em_contato", "em_negociacao", "fechado", "perdido"]
                    status_labels = {
                        "novo": "Novo",
                        "em_contato": "Em Contato",
                        "em_negociacao": "Em Negociação",
                        "fechado": "Fechado",
                        "perdido": "Perdido"
                    }
                    
                    current_index = status_options.index(lead['status'])
                    new_status = st.selectbox(
                        "Status",
                        options=status_options,
                        format_func=lambda x: status_labels[x],
                        index=current_index,
                        key=f"status_{lead['id']}"
                    )
                    
                    new_observation = st.text_area(
                        "Nova Observação",
                        value=lead['observation'] or "",
                        key=f"obs_{lead['id']}"
                    )
                    
                    if st.button("Atualizar", key=f"update_{lead['id']}"):
                        update_data = {
                            "status": new_status,
                            "observation": new_observation
                        }
                        response = make_authenticated_request(f"/leads/{lead['id']}", "PUT", update_data)
                        if response and response.status_code == 200:
                            st.success("Lead atualizado com sucesso!")
                            st.rerun()
                        else:
                            st.error("Erro ao atualizar lead")
    else:
        st.error("Erro ao carregar leads")
