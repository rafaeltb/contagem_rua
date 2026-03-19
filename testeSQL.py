import streamlit as st
from sqlalchemy import text
import time

st.set_page_config(page_title="Debug Supabase", page_icon="🔧")

st.title("🔧 Diagnóstico de Conexão: Oma Sena")
st.write("Siga os testes um por um para isolar o erro.")

# --- TESTE 1: CONEXÃO NATIVA DO STREAMLIT ---
st.header("1. Teste de Conexão Nativa (st.connection)")
if st.button("Executar Teste 1"):
    try:
        with st.spinner("Tentando st.connection..."):
            conn = st.connection("postgresql", type="sql")
            # Tenta apenas uma query de versão do Postgres (super leve)
            df = conn.query("SELECT version();", ttl="0")
            st.success("✅ Conexão Nativa Funcionou!")
            st.dataframe(df)
    except Exception as e:
        st.error(f"❌ Falha no Teste 1: {e}")
        st.info("Dica: Verifique se o [connections.postgresql] está correto no Secrets.")

st.divider()

# --- TESTE 2: ENGINE SQLALCHEMY COM PORTA 6543 ---
st.header("2. Teste de Engine Direta (Porta 6543)")
st.write("Este teste ignora as abstrações do Streamlit e vai direto ao SQLAlchemy.")

if st.button("Executar Teste 2"):
    from sqlalchemy import create_engine
    try:
        with st.spinner("Criando Engine e conectando..."):
            # Puxa a URL do segredo
            url = st.secrets["connections"]["postgresql"]["url"]
            
            # Criamos o engine com timeout curto para não travar a tela
            engine = create_engine(
                url, 
                connect_args={"connect_timeout": 10}
            )
            
            with engine.connect() as connection:
                result = connection.execute(text("SELECT 1"))
                st.success("✅ Engine SQLAlchemy conectou com sucesso!")
                st.write(f"Resultado do SELECT 1: {result.fetchone()}")
                
    except Exception as e:
        st.error(f"❌ Falha no Teste 2: {e}")
        st.warning("Se deu 'Timeout', sua rede ou o firewall do Streamlit não está alcançando o host.")

st.divider()

# --- TESTE 3: VALIDAÇÃO DE TABELA ---
st.header("3. Teste de Existência de Tabela")
st.write("Verifica se a tabela 'producao_vinhedo' existe e é acessível.")

if st.button("Executar Teste 3"):
    try:
        conn = st.connection("postgresql", type="sql")
        # Busca o nome das colunas da sua tabela
        query_colunas = text("""
            SELECT column_name, data_type 
            FROM information_schema.columns 
            WHERE table_name = 'producao_vinhedo'
        """)
        
        with conn.session as s:
            result = s.execute(query_colunas)
            colunas = result.fetchall()
            
            if colunas:
                st.success(f"✅ Tabela encontrada! Colunas detectadas:")
                st.write(colunas)
            else:
                st.error("❌ Tabela 'producao_vinhedo' não encontrada no schema public.")
    except Exception as e:
        st.error(f"❌ Falha no Teste 3: {e}")
