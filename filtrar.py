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

st.subheader("Tabela de Dados Filtrados")
st.markdown("Visualize abaixo os registros de consumo energético conforme os filtros aplicados. Cada linha representa um registro de consumo de energia por município, categoria de atividade e tipo de fonte energética.")
st.dataframe(df_filtrado)

if not df_filtrado.empty:
    consumo_total = df_filtrado["energia (TJ)"].sum()
    emissoes_total = df_filtrado["emissoes de co2"].sum()

    media_consumo = df_filtrado["energia (TJ)"].mean()
    max_consumo = df_filtrado["energia (TJ)"].max()
    min_consumo = df_filtrado["energia (TJ)"].min()

    st.subheader("Resumo Estatístico")
    st.markdown("Essa seção resume os principais números relacionados ao consumo de energia e emissão de CO₂ com base nos filtros escolhidos. Esses dados ajudam a entender o nível atual de dependência energética e o impacto ambiental gerado.")
    st.metric("Consumo Total (TJ)", f"{consumo_total:.2f}")
    st.metric("Emissões Totais de CO₂ (toneladas)", f"{emissoes_total:.2f}")

    st.markdown(f"- **Média de Consumo de Energia (TJ):** {media_consumo:.2f}")
    st.markdown(f"- **Maior Consumo Registrado (TJ):** {max_consumo:.2f}")
    st.markdown(f"- **Menor Consumo Registrado (TJ):** {min_consumo:.2f}")

    # Gráfico: Consumo vs Emissões
    st.subheader("Comparativo entre Consumo e Emissões")
    st.markdown("O gráfico abaixo mostra, de forma comparativa, o total de energia consumida (em Terajoules) e o total de CO₂ emitido (em toneladas). Isso permite entender a relação direta entre consumo energético e impacto ambiental. Quanto maior o consumo, maior tende a ser a emissão de poluentes.\n\nPara ilustrar melhor: **uma única tonelada de CO₂ equivale a uma viagem de carro de aproximadamente 5.000 km**. Ou seja, se um município emitir 10.000 toneladas de CO₂, isso seria como se 10.000 carros viajassem de São Paulo ao Recife sem parar. Essa comparação reforça a urgência de reduzir as emissões, especialmente substituindo fontes de energia poluentes por fontes limpas como a solar.")

    dados_totais = pd.DataFrame({
        "Indicador": ["Energia Consumida (TJ)", "Emissões de CO₂ (toneladas)"],
        "Valor": [consumo_total, emissoes_total]
    })

    chart = alt.Chart(dados_totais).mark_bar().encode(
        x=alt.X("Indicador:N", title="Indicador"),
        y=alt.Y("Valor:Q", title="Valor Total"),
        tooltip=["Indicador", "Valor"]
    ).properties(
        title="Comparativo Total entre Consumo de Energia e Emissões de CO₂"
    )
    st.altair_chart(chart, use_container_width=True)

    # Estimativa de Substituição por Energia Solar
    st.subheader("Simulação de Geração com Energia Solar")
    percentual_solar = st.slider(
        "Qual percentual do consumo atual você gostaria de substituir por energia solar?",
        0, 100, 30, help="Essa simulação calcula a economia e a redução de CO₂ ao gerar parte da energia com painéis solares."
    )
    consumo_solar = consumo_total * (percentual_solar / 100)
    energia_kwh = consumo_solar * 277778  # 1 TJ = 277.778 kWh
    preco_kwh_solar = 0.35  # valor médio estimado
    economia_financeira = energia_kwh * preco_kwh_solar
    reducao_co2 = consumo_solar * (emissoes_total / consumo_total)

    st.markdown(f"Ao substituir **{percentual_solar}%** do consumo por energia solar:")
    st.markdown(f"- **Energia Gerada por Painéis Solares:** {consumo_solar:.2f} TJ ({energia_kwh:,.0f} kWh)")
    st.markdown(f"- **Economia Financeira Estimada:** R$ {economia_financeira:,.2f}")
    st.markdown(f"- **Redução de Emissões de CO₂ Estimada:** {reducao_co2:,.2f} toneladas")

    st.info(
        "Esses valores simulam o impacto positivo da energia solar: menor dependência da rede elétrica, economia nas contas de luz e contribuição direta com o meio ambiente."
    )

else:
    st.warning("Nenhum dado encontrado para os filtros aplicados.")
