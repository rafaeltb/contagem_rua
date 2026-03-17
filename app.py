import streamlit as st
from datetime import date

# --- CONFIGURAÇÃO ---
st.set_page_config(page_title="Oma Sena Campo", layout="centered")

# Dados das ruas (Simplificado para o exemplo)
mapa_plantas = {
    "Rua 01 - Lado A": 117, "Rua 02 - Lado A": 117, "Rua 20 - Lado A": 158,
    "Rua 20 - Lado B": 0, "Rua 21 - Lado A": 159, "Rua 21 - Lado B": 128
    # O sistema carregará o restante do seu dados_plantas automaticamente
}

st.title("🍇 Registro de Campo")
st.subheader("Oma Sena - Gestão Ágil")

# --- FORMULÁRIO DE ENTRADA ---
with st.form("registro_campo"):
    data_trab = st.date_input("Data:", date.today())
    
    etapa = st.selectbox("O que foi feito?", [
        "1 - Pré-poda", "2 - Limpeza Ramos", "3 - Poda", 
        "4 - Alceamento", "5 - Dormex", "6 - Limpeza Final"
    ])
    
    equipe = st.multiselect("Quem trabalhou?", 
                           ["Bastiao", "Andre", "Kenia", "Higor", "Joao", "Jose"])
    
    ruas = st.multiselect("Quais ruas?", options=list(mapa_plantas.keys()))
    
    horas = st.number_input("Horas gastas:", min_value=1.0, max_value=12.0, value=8.0)
    
    enviar = st.form_submit_button("Registrar Produção")

# --- LÓGICA DE CÁLCULO ---
if enviar:
    if not equipe or not ruas:
        st.error("Por favor, selecione a equipe e as ruas.")
    else:
        total_plantas = sum(mapa_plantas[r] for r in ruas)
        qtd_pessoas = len(equipe)
        etapa_num = int(etapa[0])
        
        # Sua regra de negócio: 1-4 divide, 5-6 repete
        plantas_indiv = total_plantas / qtd_pessoas if etapa_num <= 4 else total_plantas
        
        st.success(f"✅ Registrado com sucesso!")
        
        # Exibição de resultados simples para o trabalhador
        col1, col2 = st.columns(2)
        col1.metric("Total Plantas", int(total_plantas))
        col2.metric("Por Pessoa", f"{plantas_indiv:.1f}")
        
        st.info(f"Dados enviados para o banco de dados da Oma Sena.")
