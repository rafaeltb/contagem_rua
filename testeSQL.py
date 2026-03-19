import streamlit as st
from sqlalchemy import create_engine, text

def salvar_no_sql_definitivo(dados):
    try:
        url = st.secrets["connections"]["postgresql"]["url"]
        
        # Criando engine otimizado para o Pooler do Supabase
        engine = create_engine(
            url,
            # Desativa os comandos preparados que causam erro no modo Transaction
            connect_args={"options": "-c statement_timeout=30000"},
            pool_pre_ping=True
        )
        
        with engine.begin() as conn:
            query = text("""
                INSERT INTO producao_vinhedo (data, etapa, equipe, ruas, total_plantas, plantas_por_pessoa, horas) 
                VALUES (:data, :etapa, :equipe, :ruas, :total, :indiv, :horas)
            """)
            conn.execute(query, dados)
        return True
    except Exception as e:
        st.error(f"Erro na Gravação: {e}")
        return False

# No seu formulário da Oma Sena:
if enviar:
    # ... (seus cálculos de total e plantas_indiv) ...
    if salvar_no_sql_definitivo(dados_salvar):
        st.success("✅ REGISTRADO COM SUCESSO!")
        st.balloons()
