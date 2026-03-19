import streamlit as st
from datetime import date
import pandas as pd
from sqlalchemy import text

def salvar_no_sql(dados):
    try:
        # 1. Conecta ao banco (certifique-se de que o segredo está como [connections.postgresql])
        conn = st.connection("postgresql", type="sql")
        
        # 2. Usa o context manager da sessão de forma explícita
        with conn.session as s:
            query = text("""
                INSERT INTO producao_vinhedo (data, etapa, equipe, ruas, total_plantas, plantas_por_pessoa, horas) 
                VALUES (:data, :etapa, :equipe, :ruas, :total, :indiv, :horas)
            """)
            
            # Executa a query
            s.execute(query, {
                "data": dados["data"],
                "etapa": dados["etapa"],
                "equipe": dados["equipe"],
                "ruas": dados["ruas"],
                "total": dados["total"],
                "indiv": dados["indiv"],
                "horas": dados["horas"]
            })
            
            # 3. Força o commit e fecha a transação
            s.commit()
            
        return True
    except Exception as e:
        st.error(f"Erro ao salvar: {str(e)}")
        return False

# --- No bloco 'if enviar:' ---
if enviar:
    if not equipe or not ruas_sel:
        st.error("Selecione equipe e ruas!")
    else:
        # ... cálculos de total e plantas_indiv ...
        
        dados_salvar = {
            "data": data_trab,
            "etapa": etapa,
            "equipe": ", ".join(equipe),
            "ruas": ", ".join(ruas_sel),
            "total": total,
            "indiv": plantas_indiv,
            "horas": horas
        }
        
        # Feedback com tempo limite visual
        placeholder = st.empty()
        placeholder.info("⏳ Conectando ao Supabase...")
        
        sucesso = salvar_no_sql(dados_salvar)
        
        placeholder.empty() # Limpa a mensagem de espera
        
        if sucesso:
            st.success("✅ Gravado com sucesso!")
            st.balloons()
        # O erro já será mostrado dentro da função salvar_no_sql se falhar
# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Oma Sena Campo", layout="centered", page_icon="🍇")

# DADOS DAS RUAS
dados_plantas = [(53, 101, 0), (52, 101, 0), (51, 100, 0), (50, 104, 0), (49, 103, 0), (48, 105, 0), (47, 106, 0), (46, 109, 0), (45, 111, 0), (44, 113, 0), (43, 109, 0), (42, 114, 0), (41, 115, 0), (40, 117, 0), (39, 117, 154), (38, 121, 154), (37, 121, 154), (36, 121, 154), (35, 123, 154), (34, 123, 154), (33, 123, 135), (32, 127, 136), (31, 127, 137), (30, 128, 138), (29, 131, 139), (28, 132, 140), (27, 133, 141), (26, 150, 142), (25, 152, 139), (24, 156, 136), (23, 157, 134), (22, 156, 121), (21, 159, 128), (20, 158, 0), (19, 148, 0), (18, 149, 0), (17, 148, 0), (16, 146, 0), (15, 141, 0), (14, 141, 0), (13, 138, 0), (12, 134, 0), (11, 132, 0), (10, 129, 0), (9, 127, 0), (8, 122, 0), (7, 120, 0), (6, 119, 0), (5, 119, 0), (4, 118, 0), (3, 117, 0), (2, 117, 0), (1, 117, 0)]

mapa_plantas = {}
for r, a, b in dados_plantas:
    mapa_plantas[f"Rua {r:02d} - Lado A"] = a
    if b > 0: mapa_plantas[f"Rua {r:02d} - Lado B"] = b

st.title("🍇 Registro de Campo")
st.subheader("Oma Sena - Gestão Ágil")

with st.form("registro_campo"):
    data_trab = st.date_input("Data:", date.today())
    etapa = st.selectbox("O que foi feito?", ["1 - Pré-poda", "2 - Limpeza Ramos", "3 - Poda", "4 - Alceamento", "5 - Dormex", "6 - Limpeza Final"])
    equipe = st.multiselect("Quem trabalhou?", ["Bastiao", "Andre", "Kenia", "Higor", "Joao", "Jose"])
    ruas_sel = st.multiselect("Quais ruas?", options=sorted(list(mapa_plantas.keys())))
    horas = st.number_input("Horas gastas:", min_value=0.5, value=8.0, step=0.5)
    enviar = st.form_submit_button("Registrar Produção")

if enviar:
    if not equipe or not ruas_sel:
        st.error("⚠️ Selecione a equipe e as ruas antes de salvar!")
    else:
        total = sum(mapa_plantas[r] for r in ruas_sel)
        qtd_pessoas = len(equipe)
        
        # Lógica de cálculo conforme a etapa
        n_etapa = int(etapa[0])
        plantas_indiv = total / qtd_pessoas if n_etapa <= 4 else total
        
        dados_salvar = {
            "data": data_trab,
            "etapa": etapa,
            "equipe": ", ".join(equipe),
            "ruas": ", ".join(ruas_sel),
            "total": total,
            "indiv": plantas_indiv,
            "horas": horas
        }
        
        # Feedback visual para o usuário
        with st.spinner("Salvando no banco de dados..."):
            sucesso = salvar_no_sql(dados_salvar)
            
        if sucesso:
            st.success("✅ Dados salvos com sucesso no Supabase!")
            st.balloons()
            
            # Mostrar resumo do que foi salvo
            c1, c2, c3 = st.columns(3)
            c1.metric("Total Plantas", int(total))
            c2.metric("Plantas/Pessoa", f"{plantas_indiv:.1f}")
            c3.metric("Pessoas", qtd_pessoas)
        else:
            st.error("❌ Falha ao salvar. Verifique o log de erro acima.")
