import streamlit as st
import pandas as pd
import altair as alt
import numpy as np

@st.cache_data(show_spinner=False)
def carregar_dados(caminho_excel):
    df = pd.read_excel(caminho_excel)
    df["estado"] = df["estado"].str.upper()
    df["municipio"] = df["municipio"].str.upper()
    df["categoria de atividade"] = df["categoria de atividade"].str.upper()
    df["tipo de fonte energetica"] = df["tipo de fonte energetica"].str.upper()
    df["energia (TJ)"] = pd.to_numeric(df["energia (TJ)"], errors='coerce')
    df["emissoes de co2"] = pd.to_numeric(df["emissoes de co2"], errors='coerce')
    return df

# Caminho do arquivo
caminho_excel = "arquivo_csv/relatorio_consumo_energia.xlsx"
df = carregar_dados(caminho_excel)

estados = sorted(df["estado"].unique())
categorias = sorted(df["categoria de atividade"].unique())
fontes = sorted(df["tipo de fonte energetica"].unique())
anos = sorted(df["ano"].unique())

st.title("Painel de Consumo de Energia e Potencial de Energia Solar")

# Filtros
with st.container():
    st.markdown("### 🔍 Filtros de Análise")
    st.markdown("---")
    estado_selecionado = st.selectbox("Selecione o Estado", estados)
    municipios_estado = sorted(df[df["estado"] == estado_selecionado]["municipio"].unique())
    municipios_estado.insert(0, "TODOS")
    municipio_selecionado = st.selectbox("Selecione o Município", municipios_estado)
    categoria_selecionada = st.selectbox("Categoria de Atividade", ["TODOS"] + categorias)
    fonte_selecionada = st.selectbox("Fonte Energética", ["TODOS"] + fontes)
    ano_selecionado = st.selectbox("Ano", ["TODOS"] + [str(a) for a in anos])

# Aplicar filtros
df_filtrado = df[df["estado"] == estado_selecionado].copy()
if municipio_selecionado != "TODOS":
    df_filtrado = df_filtrado[df_filtrado["municipio"] == municipio_selecionado]
if categoria_selecionada != "TODOS":
    df_filtrado = df_filtrado[df_filtrado["categoria de atividade"] == categoria_selecionada]
if fonte_selecionada != "TODOS":
    df_filtrado = df_filtrado[df_filtrado["tipo de fonte energetica"] == fonte_selecionada]
if ano_selecionado != "TODOS":
    df_filtrado = df_filtrado[df_filtrado["ano"] == int(ano_selecionado)]

# Tabela
with st.container():
    st.subheader("📋 Tabela de Dados Filtrados")
    st.markdown("Cada linha representa um registro de consumo de energia por município, categoria de atividade e tipo de fonte energética.")
    st.dataframe(df_filtrado, use_container_width=True)

if not df_filtrado.empty:
    consumo_total = df_filtrado["energia (TJ)"].sum()
    emissoes_total = df_filtrado["emissoes de co2"].sum()

    media_consumo = df_filtrado["energia (TJ)"].mean()
    max_consumo = df_filtrado["energia (TJ)"].max()
    min_consumo = df_filtrado["energia (TJ)"].min()

    st.subheader("📊 Resumo Estatístico")
    st.metric("Consumo Total (TJ)", f"{consumo_total:.2f}")
    st.metric("Emissões Totais de CO₂ (toneladas)", f"{emissoes_total:.2f}")
    st.markdown(f"- **Média de Consumo de Energia (TJ):** {media_consumo:.2f}")
    st.markdown(f"- **Maior Consumo Registrado (TJ):** {max_consumo:.2f}")
    st.markdown(f"- **Menor Consumo Registrado (TJ):** {min_consumo:.2f}")

    # Conversões explicativas
    casas_equivalentes = consumo_total / 0.00000864
    carros_equivalentes = emissoes_total / 2

    st.markdown("### 🌍 Impacto Ambiental em Termos Reais")
    st.markdown(
        f"- O consumo total equivale à energia gasta por cerca de **{casas_equivalentes:,.0f} residências** brasileiras em 1 ano.\n"
        f"- As emissões de CO₂ correspondem ao que seria emitido por aproximadamente **{carros_equivalentes:,.0f} carros** rodando durante um ano."
    )

    # Simulação solar
    st.subheader("☀️ Simulação de Geração com Energia Solar")
    percentual_solar = st.slider(
        "Qual percentual do consumo atual você gostaria de substituir por energia solar?",
        0, 100, 30,
        help="Essa simulação calcula a economia e a redução de CO₂ ao gerar parte da energia com painéis solares."
    )

    consumo_solar = consumo_total * (percentual_solar / 100)
    energia_kwh = consumo_solar * 277778
    preco_kwh_solar = 0.22
    economia_financeira = energia_kwh * preco_kwh_solar
    reducao_co2 = consumo_solar * (emissoes_total / consumo_total)

    st.markdown(f"Ao substituir **{percentual_solar}%** do consumo por energia solar:")
    st.markdown(f"- **Energia Gerada por Painéis Solares:** {consumo_solar:.2f} TJ ({energia_kwh:,.0f} kWh)")
    st.markdown(f"- **Economia Financeira Estimada:** R$ {economia_financeira:,.2f}")
    st.markdown(f"- **Redução de Emissões de CO₂ Estimada:** {reducao_co2:,.2f} toneladas")

    st.info(
        "Esses valores simulam o impacto positivo da energia solar: menor dependência da rede elétrica, economia nas contas de luz e contribuição direta com o meio ambiente."
    )

    # ✅ Gráficos com base nos dados filtrados agrupados por ano
    st.subheader("📈 Evolução do Consumo e Emissões por Ano (com base nos filtros)")

    evolucao_filtrada = df_filtrado.groupby("ano")[["energia (TJ)", "emissoes de co2"]].sum().sort_index().reset_index()

    if evolucao_filtrada.empty:
        st.info("Não há dados suficientes para gerar os gráficos com os filtros aplicados.")
    else:
        chart_energia = alt.Chart(evolucao_filtrada).mark_line(point=True, color="#1f77b4").encode(
            x=alt.X("ano:O", title="Ano"),
            y=alt.Y("energia (TJ):Q", title="Energia Consumida (TJ)"),
            tooltip=["ano", "energia (TJ)"]
        ).properties(title="Evolução do Consumo de Energia")

        chart_emissao = alt.Chart(evolucao_filtrada).mark_line(point=True, color="#ff7f0e").encode(
            x=alt.X("ano:O", title="Ano"),
            y=alt.Y("emissoes de co2:Q", title="Emissões de CO₂ (toneladas)"),
            tooltip=["ano", "emissoes de co2"]
        ).properties(title="Evolução das Emissões de CO₂")

        st.altair_chart(chart_energia, use_container_width=True)
        st.altair_chart(chart_emissao, use_container_width=True)

    # Ranking por categoria
    st.subheader("🏭 Categorias que Mais Consomem Energia")
    ranking_categoria = df_filtrado.groupby("categoria de atividade")["energia (TJ)"].sum().sort_values(ascending=False).head(10).reset_index()

    barras = alt.Chart(ranking_categoria).mark_bar().encode(
        x=alt.X("energia (TJ):Q", title="Consumo de Energia (TJ)"),
        y=alt.Y("categoria de atividade:N", sort='-x', title="Categoria"),
        tooltip=["categoria de atividade", "energia (TJ)"]
    ).properties(title="Top 10 Categorias com Maior Consumo de Energia")

    st.altair_chart(barras, use_container_width=True)

else:
    st.warning("Nenhum dado encontrado para os filtros aplicados.")
