import streamlit as st
from sqlalchemy import create_engine, text

def testar_conexao_robusta():
    try:
        # Puxa a URL do Secrets
        url = st.secrets["connections"]["postgresql"]["url"]
        
        # Criamos o engine com configurações que evitam o erro de IPv6
        engine = create_engine(
            url,
            connect_args={
                "connect_timeout": 15,
                "keepalives": 1,
                "keepalives_idle": 30,
                "keepalives_interval": 10,
                "keepalives_count": 5
            },
            pool_pre_ping=True
        )
        
        with engine.connect() as conn:
            res = conn.execute(text("SELECT 1"))
            return True, res.fetchone()
    except Exception as e:
        return False, str(e)

st.title("🧪 Teste de Conexão Forçada IPv4")

if st.button("Tentar Conexão Direta"):
    sucesso, resultado = testar_conexao_robusta()
    if sucesso:
        st.success(f"✅ CONECTADO! Resultado: {resultado}")
    else:
        st.error(f"❌ Erro persistente: {resultado}")
        st.info("Dica: Se aparecer 'IPv6', o Streamlit Cloud está ignorando a rota IPv4.")
