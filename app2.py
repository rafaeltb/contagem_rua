import streamlit as st
from datetime import date
from sqlalchemy import text

# 1. Definição da Função (Sempre no topo)
def salvar_no_sql(dados):
    try:
        conn = st.connection("postgresql", type="sql")
        with conn.session as s:
            query = text("""
                INSERT INTO producao_vinhedo (data, etapa, equipe, ruas, total_plantas, plantas_por_pessoa, horas) 
                VALUES (:data, :etapa, :equipe, :ruas, :total, :indiv, :horas)
            """)
            s.execute(query, dados)
            s.commit()
        return True
    except Exception as e:
        st.error(f"Erro no banco: {e}")
        return False

# 2. Configurações e Dados
st.set_page_config(page_title="Oma Sena Campo", layout="centered", page_icon="🍇")

dados_plantas = [(53, 101, 0), (52, 101, 0), (51, 100, 0), (50, 104, 0), (49, 103, 0), (48, 105, 0), (47, 106, 0), (46, 109, 0), (45, 111, 0), (44, 113, 0), (43, 109, 0), (42, 114, 0), (41, 115, 0), (40, 117, 0), (39, 117, 154), (38, 121, 154), (37, 121, 154), (36, 121, 154), (35, 123, 154), (34, 123, 154), (33, 123, 135), (32, 127, 136), (31, 127, 137), (30, 128, 138), (29, 131, 139), (28, 132, 140), (27, 133, 141), (26, 150, 142), (25, 152, 139), (24, 156, 136), (23, 157, 134), (22, 156, 121), (21, 159, 128), (20, 158, 0), (19, 148, 0), (18, 149, 0), (17, 148, 0), (16, 146, 0), (15, 141, 0), (14, 141, 0), (13, 138, 0), (12, 134, 0), (11, 132, 0), (10, 129, 0), (9, 127, 0), (8, 122, 0), (7, 120, 0), (6, 119, 0), (5, 119, 0), (4, 118, 0), (3, 117, 0), (2, 117, 0), (1, 117, 0)]
mapa_plantas = {f"Rua {r:02d} - Lado A": a for r, a, b in dados_plantas}
for r, a, b in dados_plantas:
    if b > 0: mapa_plantas[f"Rua {r:02d} - Lado B"] = b

# 3. Interface do Usuário
st.title("🍇 Registro de Campo")

# CRIANDO O FORMULÁRIO
with st.form("registro_campo"):
    data_trab = st.date_input("Data:", date.today())
    etapa = st.selectbox("Etapa:", ["1 - Pré-poda", "2 - Limpeza Ramos", "3 - Poda", "4 - Alceamento", "5 - Dormex", "6 - Limpeza Final"])
    equipe = st.multiselect("Equipe:", ["Bastiao", "Andre", "Kenia", "Higor", "Joao", "Jose"])
    ruas_sel = st.multiselect("Ruas:", options=sorted(list(mapa_plantas.keys())))
    horas = st.number_input("Horas:", min_value=0.5, value=8.0)
    
    # IMPORTANTE: O botão 'enviar' deve ser a última coisa dentro do 'with st.form'
    enviar = st.form_submit_button("Registrar Produção")

# 4. Lógica após o clique (FORA DO FORMULÁRIO)
if enviar:
    if not equipe or not ruas_sel:
        st.warning("⚠️ Preencha a equipe e as ruas!")
    else:
        total = sum(mapa_plantas[r] for r in ruas_sel)
        plantas_indiv = total / len(equipe) if int(etapa[0]) <= 4 else total
        
        dados_salvar = {
            "data": data_trab,
            "etapa": etapa,
            "equipe": ", ".join(equipe),
            "ruas": ", ".join(ruas_sel),
            "total": total,
            "indiv": plantas_indiv,
            "horas": horas
        }
        
        with st.spinner("Gravando no Supabase..."):
            if salvar_no_sql(dados_salvar):
                st.success("✅ Salvo com sucesso!")
                st.balloons()
            else:
                st.error("❌ Falha ao gravar. Verifique os logs.")
