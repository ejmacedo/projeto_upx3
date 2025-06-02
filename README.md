# 🌞 Painel de Análise de Consumo Energético e Simulação de Energia Solar

Projeto desenvolvido na disciplina **UPX III – Usina de Projetos Experimentais** do Centro Universitário Facens. A proposta utiliza dados reais de consumo de energia e emissões de CO₂ por município e setor econômico no Brasil para simular o impacto da substituição parcial por energia solar.

## 📌 Objetivo

Criar um painel interativo que permita:
- Visualizar o consumo energético por estado, município, setor e ano
- Avaliar emissões de CO₂ associadas ao consumo
- Simular a substituição por energia solar com impacto ambiental e financeiro
- Apoiar a transição energética e fomentar a sustentabilidade

---

## ⚙️ Tecnologias e Ferramentas

- 🐍 **Python 3.11**
- 📊 **Pandas** – Manipulação e análise de dados
- 📈 **Altair** – Visualização interativa dos dados
- 🌐 **Streamlit** – Criação de interface web interativa
- 📑 **Excel (.xlsx)** – Fonte de dados de consumo energético

---

## 🚀 Como Executar o Projeto

1. Clone o repositório:
   ```bash
   git clone https://github.com/seu-usuario/upx-energia-renovavel.git
   cd upx-energia-renovavel

2. Crie um ambiente virtual
   ```
   python -m venv venv
   
3. Ative o ambiente Virtual
   ```
   Windows: venv\\Scripts\\activate
   Linux/Mac: source venv/bin/activate

4. Instale as dependências
   ```
   pip install -r requirements.txt

5. Execute a aplicação
   ```
   streamlit run filtrar.py
