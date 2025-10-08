import streamlit as st
from auth import get_current_user, make_authenticated_request
import pandas as pd
from datetime import datetime
import numpy as np
from scipy import stats

def show_gestor_interface():
    menu = st.sidebar.selectbox("Menu Gestor", ["Dashboard", "Leads", "Usuários"])
    
    if menu == "Dashboard":
        show_gestor_dashboard()
    elif menu == "Leads":
        show_gestor_leads()
    elif menu == "Usuários":
        show_gestor_usuarios()

def show_gestor_dashboard():
    st.header("📊 Dashboard Executivo")
    
    response = make_authenticated_request("/leads/")
    if response and response.status_code == 200:
        leads = response.json()
        
        if not leads:
            st.info("📭 Nenhum lead cadastrado ainda.")
            return
        
        # Converter datas
        for lead in leads:
            lead['created_date'] = datetime.strptime(lead['created_at'][:10], '%Y-%m-%d')
        
        # ===== MÉTRICAS PRINCIPAIS =====
        st.subheader("📈 Visão Geral")
        
        total_leads = len(leads)
        fechados = len([l for l in leads if l['status'] == 'fechado'])
        perdidos = len([l for l in leads if l['status'] == 'perdido'])
        em_andamento = total_leads - fechados - perdidos
        taxa_conversao = (fechados / total_leads * 100) if total_leads > 0 else 0
        
        col1, col2, col3, col4, col5 = st.columns(5)
        col1.metric("📋 Total de Leads", total_leads)
        col2.metric("✅ Fechados", fechados, delta=f"{taxa_conversao:.1f}%")
        col3.metric("❌ Perdidos", perdidos)
        col4.metric("🔄 Em Andamento", em_andamento)
        col5.metric("🎯 Taxa de Conversão", f"{taxa_conversao:.1f}%")
        
        st.markdown("---")
        
        # ===== ESTATÍSTICAS DESCRITIVAS =====
        st.subheader("📐 Estatísticas Descritivas dos Leads")
        
        df_leads = pd.DataFrame(leads)
        df_leads['data'] = pd.to_datetime(df_leads['created_at'], format='ISO8601').dt.date
        leads_por_dia_series = df_leads.groupby('data').size()

        if len(leads_por_dia_series) > 0:
            # Calcular estatísticas
            media = leads_por_dia_series.mean()
            mediana = leads_por_dia_series.median()
            desvio_padrao = leads_por_dia_series.std()

            # Verifica se temos dados suficientes para calcular intervalo de confiança e outras estatísticas
            if len(leads_por_dia_series) > 1:  
                modo_valores = leads_por_dia_series.mode()
                moda = modo_valores.iloc[0] if len(modo_valores) > 0 else 0
                minimo = leads_por_dia_series.min()
                maximo = leads_por_dia_series.max()

                # Intervalo de confiança (95%)
                confianca = 0.95
                graus_liberdade = len(leads_por_dia_series) - 1
                if graus_liberdade > 0:
                    t_critico = stats.t.ppf((1 + confianca) / 2, graus_liberdade)
                    erro_padrao = desvio_padrao / np.sqrt(len(leads_por_dia_series))
                    margem_erro = t_critico * erro_padrao
                    ic_inferior = media - margem_erro
                    ic_superior = media + margem_erro
                else:
                    ic_inferior = ic_superior = media

                # Exibir métricas em cards
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("📊 Média de Leads/Dia", f"{media:.2f}")
                    st.caption("**O que é?** A média indica quantos leads, em média, você recebe por dia.")
                with col2:
                    st.metric("📏 Mediana", f"{mediana:.1f}")
                    st.caption("**O que é?** O valor do meio quando organizamos os dados.")
                with col3:
                    st.metric("🎯 Moda", f"{moda:.0f}")
                    st.caption("**O que é?** O número de leads que aparece com mais frequência.")
                with col4:
                    st.metric("📈 Amplitude", f"{minimo:.0f} - {maximo:.0f}")
                    st.caption("**O que é?** A variação entre o menor e o maior número de leads em um único dia.")

                st.markdown("---")
                # Additional metrics ...
            
            else:
                st.info("📊 Dados insuficientes para calcular estatísticas descritivas. Aguarde mais leads serem cadastrados.")
        
        st.markdown("---")
        # Additional analysis ...
    else:
        st.error("❌ Erro ao carregar dados do dashboard")

# Make sure there are no duplicate or poorly defined function definitions