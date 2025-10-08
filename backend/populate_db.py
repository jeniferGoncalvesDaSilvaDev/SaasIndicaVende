
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import User, Lead, LeadStatus
from datetime import datetime, timedelta
import random

def populate_database():
    db = SessionLocal()
    
    # Buscar usuários existentes
    vendedores = db.query(User).filter(User.role == "vendedor").all()
    indicadores = db.query(User).filter(User.role == "indicador").all()
    
    if not vendedores or not indicadores:
        print("Erro: É necessário ter pelo menos 1 vendedor e 1 indicador cadastrados")
        return
    
    # Nomes de clientes variados
    nomes = [
        "Maria Silva", "João Santos", "Ana Costa", "Pedro Oliveira", "Carla Souza",
        "Lucas Ferreira", "Juliana Lima", "Roberto Alves", "Fernanda Rocha", "Bruno Martins",
        "Patricia Gomes", "Rafael Barbosa", "Camila Ribeiro", "Diego Cardoso", "Leticia Dias",
        "Marcos Pereira", "Renata Castro", "Thiago Monteiro", "Gabriela Freitas", "Felipe Araujo",
        "Beatriz Cunha", "Andre Teixeira", "Vanessa Pinto", "Ricardo Moreira", "Amanda Correia",
        "Gustavo Ramos", "Larissa Cavalcanti", "Fabio Melo", "Tatiana Borges", "Rodrigo Nunes"
    ]
    
    cidades = [
        "São Paulo/SP", "Rio de Janeiro/RJ", "Belo Horizonte/MG", "Curitiba/PR", 
        "Porto Alegre/RS", "Salvador/BA", "Brasília/DF", "Fortaleza/CE",
        "Recife/PE", "Manaus/AM", "Goiânia/GO", "Campinas/SP", "Florianópolis/SC"
    ]
    
    telefones_base = ["11", "21", "31", "41", "51", "71", "61", "85", "81", "92", "62", "19", "48"]
    
    observacoes = [
        "Cliente interessado em pacote premium",
        "Indicado por cliente atual",
        "Precisa de atendimento urgente",
        "Solicitou orçamento detalhado",
        "Cliente corporativo - grande potencial",
        "Aguardando resposta de proposta",
        "Demonstrou muito interesse no produto",
        "Cliente já conhece a marca",
        None,
        "Primeiro contato - avaliar necessidades"
    ]
    
    status_opcoes = [
        LeadStatus.NOVO,
        LeadStatus.EM_CONTATO,
        LeadStatus.EM_NEGOCIACAO,
        LeadStatus.FECHADO,
        LeadStatus.PERDIDO
    ]
    
    # Pesos para distribuição mais realista (mais leads novos/em contato, menos fechados/perdidos)
    status_pesos = [0.3, 0.25, 0.2, 0.15, 0.1]
    
    # Criar leads distribuídos nos últimos 60 dias
    hoje = datetime.now()
    leads_criados = 0
    
    for i in range(150):  # Criar 150 leads
        # Distribuir leads ao longo dos últimos 60 dias
        dias_atras = random.randint(0, 60)
        data_criacao = hoje - timedelta(days=dias_atras)
        
        # Selecionar dados aleatórios
        nome = random.choice(nomes)
        cidade = random.choice(cidades)
        ddd = random.choice(telefones_base)
        telefone = f"({ddd}) 9{random.randint(1000, 9999)}-{random.randint(1000, 9999)}"
        observacao = random.choice(observacoes)
        status = random.choices(status_opcoes, weights=status_pesos)[0]
        
        vendedor = random.choice(vendedores)
        indicador = random.choice(indicadores)
        
        # Criar lead
        lead = Lead(
            client_name=nome,
            phone=telefone,
            city_state=cidade,
            observation=observacao,
            status=status,
            indicador_id=indicador.id,
            vendedor_id=vendedor.id,
            created_at=data_criacao
        )
        
        db.add(lead)
        leads_criados += 1
    
    db.commit()
    print(f"✅ {leads_criados} leads criados com sucesso!")
    print(f"📊 Distribuídos entre {len(vendedores)} vendedor(es) e {len(indicadores)} indicador(es)")
    db.close()

if __name__ == "__main__":
    populate_database()
