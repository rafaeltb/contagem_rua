import streamlit as st
from sqlalchemy import text

st.title("🧪 Teste de Escrita: Tabela Simples")

# Tenta ligar usando a porta 6543 definida no seu Secrets
conn = st.connection("postgresql", type="sql")

# --- PARTE 1: LEITURA ---
st.subheader("1. Teste de Leitura")
if st.button("Ler Tabela de Teste"):
    try:
        df = conn.query("SELECT * FROM teste_conexao;", ttl=0)
        st.write("Dados encontrados:")
        st.dataframe(df)
    except Exception as e:
        st.error(f"Erro ao ler: {e}")

# --- PARTE 2: ESCRITA ---
st.subheader("2. Teste de Escrita")
msg = st.text_input("Escreva algo para guardar:", "Teste via Streamlit")

if st.button("Gravar no Banco"):
    try:
        with conn.session as s:
            s.execute(
                text("INSERT INTO teste_conexao (mensagem) VALUES (:m)"),
                {"m": msg}
            )
            s.commit()
        st.success("✅ Gravado com sucesso! Clique em 'Ler Tabela' para confirmar.")
    except Exception as e:
        st.error(f"Erro ao gravar: {e}")
        st.info("Se o erro for 'Timeout', confirme se a porta no Secrets é a 6543.")
