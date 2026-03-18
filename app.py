import streamlit as st
import pandas as pd

# --- 1. CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Oma Sena - Pulverização", layout="centered", page_icon="🚜")

# --- 2. DADOS DO VINHEDO (df_vinhedo) ---
# Reconstruindo o DataFrame com base nos seus dados reais
dados_plantas = [
    (53, 101, 0), (52, 101, 0), (51, 100, 0), (50, 104, 0), (49, 103, 0),
    (48, 105, 0), (47, 106, 0), (46, 109, 0), (45, 111, 0), (44, 113, 0),
    (43, 109, 0), (42, 114, 0), (41, 115, 0), (40, 117, 0), (39, 117, 154),
    (38, 121, 154), (37, 121, 154), (36, 121, 154), (35, 123, 154), (34, 123, 154),
    (33, 123, 135), (32, 127, 136), (31, 127, 137), (30, 128, 138), (29, 131, 139),
    (28, 132, 140), (27, 133, 141), (26, 150, 142), (25, 152, 139), (24, 156, 136),
    (23, 157, 134), (22, 156, 121), (21, 159, 128), (20, 158, 0), (19, 148, 0),
    (18, 149, 0), (17, 148, 0), (16, 146, 0), (15, 141, 0), (14, 141, 0),
    (13, 138, 0), (12, 134, 0), (11, 132, 0), (10, 129, 0), (9, 127, 0),
    (8, 122, 0), (7, 120, 0), (6, 119, 0), (5, 119, 0), (4, 118, 0),
    (3, 117, 0), (2, 117, 0), (1, 117, 0)
]

# Criando a estrutura flat (Rua, Lado, Plantas)
lista_flat = []
for r, a, b in dados_plantas:
    lista_flat.append({'rua': r, 'lado': 'A', 'plantas': a})
    if b > 0:
        lista_flat.append({'rua': r, 'lado': 'B', 'plantas': b})

df_vinhedo = pd.DataFrame(lista_flat)
ruas_disponiveis = sorted(df_vinhedo['rua'].unique())

# --- 3. INTERFACE STREAMLIT ---
st.title("🚜 Planejamento de Pulverização")
st.subheader("Cálculo de Calda por Lado - Oma Sena")

with st.container():
    col1, col2 = st.columns(2)
    with col1:
        inicio = st.selectbox("Rua Início:", ruas_disponiveis, index=0)
        fim = st.selectbox("Rua Fim:", ruas_disponiveis, index=len(ruas_disponiveis)-1)
    
    with col2:
        lados_selecionados = st.multiselect("Lados:", ['A', 'B'], default=['A'])
        porcentagem = st.slider("% Última Rua:", 0, 100, 100, step=5) / 100

    btn_calcular = st.button("Calcular Calda por Lado", type="primary", use_container_width=True)

# --- 4. LÓGICA DE CÁLCULO ---
if btn_calcular:
    if not lados_selecionados:
        st.warning("⚠️ Por favor, selecione ao menos um lado (A ou B).")
    else:
        r_min, r_max = min(inicio, fim), max(inicio, fim)

        # Filtro de intervalo e lados
        df_intervalo = df_vinhedo[
            (df_vinhedo['rua'] >= r_min) &
            (df_vinhedo['rua'] <= r_max) &
            (df_vinhedo['lado'].isin(lados_selecionados))
        ].copy()

        # Soma plantas das ruas completas
        plantas_completas = df_intervalo[df_intervalo['rua'] != fim]['plantas'].sum()

        # Soma plantas da última rua com a porcentagem
        plantas_ultima_rua = df_intervalo[df_intervalo['rua'] == fim]['plantas'].sum() * porcentagem

        total_plantas = plantas_completas + plantas_ultima_rua

        # --- CÁLCULOS QUÍMICOS ---
        hectares = total_plantas / 4000
        l_dormex = hectares * 7.0
        vol_calda = total_plantas * (50 / 1900) 
        f = vol_calda / 20 

        # --- EXIBIÇÃO DOS RESULTADOS ---
        st.divider()
        st.markdown(f"### 📍 Resumo do Trecho")
        st.write(f"**Rua {inicio} até {fim}** | **Lados:** {', '.join(lados_selecionados)}")
        
        c1, c2 = st.columns(2)
        c1.metric("Total de Plantas", f"{total_plantas:.0f}")
        c2.metric("Área Estimada", f"{hectares:.3f} ha")

        st.info(f"💧 **ÁGUA TOTAL: {vol_calda:.2f} Litros**")

        st.markdown("#### 🧪 Insumos Necessários")
        res_col1, res_col2 = st.columns(2)
        with res_col1:
            st.write(f"🍇 **DORMEX:** {l_dormex:.3f} L")
            st.write(f"✨ **ESPALHANTE:** {20 * f:.1f} ml")
        with res_col2:
            st.write(f"🎯 **SCORE:** {15 * f:.1f} ml")
            st.write(f"🛡️ **ABAMECTINA:** {5 * f:.1f} ml")

        # Alerta para ruas sem Lado B
        if 'B' in lados_selecionados:
            ruas_sem_b = [r for r in range(r_min, r_max + 1) if r <= 20 or r >= 40]
            if ruas_sem_b:
                st.caption(f"ℹ️ Nota: No intervalo selecionado, algumas ruas não possuem Lado B. O sistema somou apenas o existente.")
