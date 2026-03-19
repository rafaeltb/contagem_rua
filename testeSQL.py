import streamlit as st
from sqlalchemy import text, create_engine
from datetime import date

# 1. Configuração da Página
st.set_page_config(page_title="Teste SQL Oma Sena", page_icon="🧪")

# 2. Função de Salvamento (Desta vez com o Engine Robusto)
def salvar_teste(dados):
    try:
        url = st.secrets["connections"]["postgresql"]["url"]
        # Criamos o engine aqui para garantir que ele use a URL atualizada do Secrets
        engine = create_engine(url, pool_pre_ping=True)
        
        with engine.begin() as conn:
            query = text("""
                INSERT INTO producao_vinhedo (data, etapa, equipe, ruas, total_plantas, plantas_por_pessoa, horas) 
                VALUES (:data, :etapa, :equipe, :ruas, :total, :indiv, :horas)
            """)
            conn.execute(query, dados)
        return True
    except Exception as e:
        st.error(f"Erro técnico no salvamento: {e}")
        return False

st.title("🧪 Teste de Gravação Direta")

# 3. Formulário (A variável 'enviar' nasce aqui)
with st.form("meu_form_teste"):
    st.write("Preencha dados fictícios para testar a conexão:")
    data_t = st.date_input("Data", date.today())
    etapa_t = "Teste Conexão"
    equipe_t = "Debug Expert"
    ruas_t = "Rua 01, Rua 02"
    total_t = 100
    indiv_t = 50.0
    horas_t = 8.0
    
    # O botão DEVE ser atribuído a uma variável chamada 'enviar'
    enviar = st.form_submit_button("Testar Gravação Agora")

# 4. Lógica de Execução (Só acontece DEPOIS que a variável acima existe)
if enviar:
    dados_teste = {
        "data": data_t,
        "etapa": etapa_t,
        "equipe": equipe_t,
        "ruas": ruas_t,
        "total": total_t,
        "indiv": indiv_t,
        "horas": horas_t
    }
    
    with st.spinner("Conectando ao Pooler do Supabase..."):
        if salvar_teste(dados_teste):
            st.success("✅ FUNCIONOU! O dado foi gravado no banco da Oma Sena.")
            st.balloons()
