import streamlit as st
import sqlalchemy
from sqlalchemy import create_engine, text
import psycopg2
import os

st.title("🕵️‍♂️ Diagnóstico Expert Oma Sena")

def log_debug(msg, type="info"):
    if type == "error": st.error(msg)
    elif type == "success": st.success(msg)
    else: st.info(msg)

# 1. Verificar se o segredo existe
st.header("Passo 1: Verificação de Segredos")
if "connections" in st.secrets and "postgresql" in st.secrets["connections"]:
    url = st.secrets["connections"]["postgresql"]["url"]
    st.write("✅ URL encontrada no Secrets.")
    # Mascarar senha para exibir
    masked_url = url.split(":")[0] + "://user:****@" + url.split("@")[-1]
    st.write(f"URL formatada: `{masked_url}`")
else:
    st.error("❌ Seção [connections.postgresql] não encontrada!")
    st.stop()

# 2. Teste de Conexão Nível Hard
st.header("Passo 2: Tentativas de Conexão")

if st.button("Iniciar Autópsia de Conexão"):
    
    # --- TENTATIVA A: SQLAlchemy Puro (Sem parâmetros extras) ---
    st.subheader("Tentativa A: SQLAlchemy Padrão")
    try:
        engine_a = create_engine(url)
        with engine_a.connect() as conn:
            res = conn.execute(text("SELECT 1")).fetchone()
            log_debug(f"Sucesso A! Resultado: {res}", "success")
    except Exception as e:
        log_debug(f"Falha A: {str(e)}", "error")

    # --- TENTATIVA B: Psycopg2 Direto (Ignorando SQLAlchemy) ---
    st.subheader("Tentativa B: Driver Psycopg2 Direto (Nativo)")
    try:
        # Extrair dados da URL manualmente para evitar erro de DSN
        # Formato: postgresql://user:pass@host:port/dbname
        conn_path = url.replace("postgresql://", "")
        user_pass, host_port_db = conn_path.split("@")
        user, password = user_pass.split(":")
        host_port, dbname_query = host_port_db.split("/")
        host, port = host_port.split(":")
        dbname = dbname_query.split("?")[0]

        raw_conn = psycopg2.connect(
            user=user,
            password=password,
            host=host,
            port=port,
            database=dbname,
            sslmode='require',
            connect_timeout=10
        )
        log_debug("✅ Sucesso B! O driver nativo conseguiu conectar.", "success")
        raw_conn.close()
    except Exception as e:
        log_debug(f"Falha B (Erro de Driver): {str(e)}", "error")

    # --- TENTATIVA C: Modo Transaction Pooler (Supabase Especial) ---
    st.subheader("Tentativa C: Modo Supavisor / Pgbouncer")
    try:
        # Aqui desativamos o prepare_threshold via código, não via URL
        engine_c = create_engine(
            url,
            executon_options={"isolation_level": "AUTOCOMMIT"}
        )
        with engine_c.connect() as conn:
            # Forçar um comando para limpar o cache do pooler
            conn.execute(text("DISCARD ALL"))
            res = conn.execute(text("SELECT version();")).fetchone()
            log_debug(f"Sucesso C! Versão: {res}", "success")
    except Exception as e:
        log_debug(f"Falha C: {str(e)}", "error")

st.divider()
st.write("ℹ️ **O que os resultados significam?**")
st.write("- **Falha em A e B:** Erro de rede (Porta 6543 bloqueada ou IP errado).")
# O erro "Cannot assign requested address" geralmente é rede.
st.write("- **Sucesso em B mas Falha em A:** O SQLAlchemy está tentando inventar moda na URL. Use o código da Tentativa B.")
