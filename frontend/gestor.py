
import streamlit as st
from auth import get_current_user, make_authenticated_request
import pandas as pd
from datetime import datetime, timedelta
from collections import Counter

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
        
        # ===== ANÁLISE POR STATUS =====
        st.subheader("📊 Distribuição por Status")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            status_data = Counter([l['status'] for l in leads])
            status_labels = {
                'novo': '🆕 Novo',
                'em_contato': '📞 Em Contato',
                'em_negociacao': '💼 Em Negociação',
                'fechado': '✅ Fechado',
                'perdido': '❌ Perdido'
            }
            
            df_status = pd.DataFrame([
                {'Status': status_labels.get(k, k), 'Quantidade': v} 
                for k, v in status_data.items()
            ])
            st.bar_chart(df_status.set_index('Status'))
        
        with col2:
            st.write("**Detalhamento:**")
            for status, count in status_data.items():
                percentage = (count / total_leads * 100)
                st.write(f"{status_labels.get(status, status)}: **{count}** ({percentage:.1f}%)")
        
        st.markdown("---")
        
        # ===== ANÁLISE TEMPORAL =====
        st.subheader("📅 Evolução Temporal")
        
        # Leads dos últimos 30 dias
        hoje = datetime.now()
        ultimos_30_dias = hoje - timedelta(days=30)
        leads_recentes = [l for l in leads if l['created_date'] >= ultimos_30_dias]
        
        col1, col2, col3 = st.columns(3)
        col1.metric("📆 Últimos 7 dias", len([l for l in leads if l['created_date'] >= hoje - timedelta(days=7)]))
        col2.metric("📆 Últimos 30 dias", len(leads_recentes))
        col3.metric("📊 Média diária (30d)", f"{len(leads_recentes)/30:.1f}")
        
        # Gráfico de leads por dia (últimos 30 dias)
        if leads_recentes:
            df_temporal = pd.DataFrame(leads_recentes)
            df_temporal['data'] = pd.to_datetime(df_temporal['created_at']).dt.date
            leads_por_dia = df_temporal.groupby('data').size().reset_index(name='Quantidade')
            st.line_chart(leads_por_dia.set_index('data'))
        
        st.markdown("---")
        
        # ===== PERFORMANCE POR VENDEDOR =====
        st.subheader("👥 Performance dos Vendedores")
        
        vendedores_stats = {}
        for lead in leads:
            vid = lead.get('vendedor_id', 'Não atribuído')
            if vid not in vendedores_stats:
                vendedores_stats[vid] = {
                    'total': 0,
                    'fechados': 0,
                    'perdidos': 0,
                    'em_andamento': 0
                }
            
            vendedores_stats[vid]['total'] += 1
            if lead['status'] == 'fechado':
                vendedores_stats[vid]['fechados'] += 1
            elif lead['status'] == 'perdido':
                vendedores_stats[vid]['perdidos'] += 1
            else:
                vendedores_stats[vid]['em_andamento'] += 1
        
        df_vendedores = []
        for vid, stats in vendedores_stats.items():
            taxa = (stats['fechados'] / stats['total'] * 100) if stats['total'] > 0 else 0
            df_vendedores.append({
                'Vendedor ID': vid,
                'Total Leads': stats['total'],
                'Fechados': stats['fechados'],
                'Perdidos': stats['perdidos'],
                'Em Andamento': stats['em_andamento'],
                'Taxa Conversão': f"{taxa:.1f}%"
            })
        
        df_vendedores = pd.DataFrame(df_vendedores)
        st.dataframe(df_vendedores, use_container_width=True, hide_index=True)
        
        st.markdown("---")
        
        # ===== ANÁLISE POR INDICADOR =====
        st.subheader("🎯 Performance dos Indicadores")
        
        indicadores_stats = {}
        for lead in leads:
            iid = lead.get('indicador_id', 'Não atribuído')
            if iid not in indicadores_stats:
                indicadores_stats[iid] = {
                    'total': 0,
                    'fechados': 0
                }
            
            indicadores_stats[iid]['total'] += 1
            if lead['status'] == 'fechado':
                indicadores_stats[iid]['fechados'] += 1
        
        df_indicadores = []
        for iid, stats in indicadores_stats.items():
            taxa = (stats['fechados'] / stats['total'] * 100) if stats['total'] > 0 else 0
            df_indicadores.append({
                'Indicador ID': iid,
                'Leads Indicados': stats['total'],
                'Leads Fechados': stats['fechados'],
                'Taxa de Sucesso': f"{taxa:.1f}%"
            })
        
        df_indicadores = pd.DataFrame(df_indicadores)
        st.dataframe(df_indicadores, use_container_width=True, hide_index=True)
        
    else:
        st.error("❌ Erro ao carregar dados do dashboard")

def show_gestor_leads():
    st.header("👥 Todos os Leads")
    
    response = make_authenticated_request("/leads/")
    if response and response.status_code == 200:
        leads = response.json()
        
        if leads:
            # Filtros
            col1, col2 = st.columns(2)
            with col1:
                status_filter = st.multiselect(
                    "Filtrar por Status",
                    options=['novo', 'em_contato', 'em_negociacao', 'fechado', 'perdido'],
                    default=['novo', 'em_contato', 'em_negociacao', 'fechado', 'perdido']
                )
            
            # Aplicar filtros
            leads_filtrados = [l for l in leads if l['status'] in status_filter]
            
            df_data = []
            for lead in leads_filtrados:
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
            st.dataframe(df, use_container_width=True, hide_index=True)
            
            st.caption(f"📊 Mostrando {len(df_data)} de {len(leads)} leads")
        else:
            st.info("📭 Nenhum lead cadastrado.")
    else:
        st.error("❌ Erro ao carregar leads")

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
            st.dataframe(df, use_container_width=True, hide_index=True)
            
            # Estatísticas de usuários
            st.markdown("---")
            col_a, col_b, col_c = st.columns(3)
            col_a.metric("👥 Total Usuários", len(users))
            col_b.metric("💼 Vendedores", len([u for u in users if u['role'] == 'vendedor']))
            col_c.metric("🎯 Indicadores", len([u for u in users if u['role'] == 'indicador']))
        else:
            st.error("❌ Erro ao carregar usuários")
    
    with col2:
        st.subheader("Novo Usuário")
        with st.form("novo_usuario"):
            name = st.text_input("Nome")
            email = st.text_input("Email")
            password = st.text_input("Senha", type="password")
            role = st.selectbox("Perfil", ["gestor", "vendedor", "indicador"])
            
            if st.form_submit_button("Criar Usuário"):
                st.info("🔧 Funcionalidade em desenvolvimento")
