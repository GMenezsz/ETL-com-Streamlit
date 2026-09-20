# 📊 Análise de Vendas e Faturamento com Python, Pandas e Streamlit

Projeto desenvolvido para automação de análise de dados corporativos e visualização em interface web interativa, aplicando boas práticas de manipulação de dados, agrupamentos, filtros e engenharia de dados.

## 🚀 Tecnologias Utilizadas
* **Python** (Linguagem principal)
* **Pandas** (Biblioteca para manipulação e análise de dados)
* **Streamlit** (Framework para criação de aplicações web interativas)

## 📈 Funcionalidades do Projeto
O projeto realiza o processamento completo de uma base de dados de vendas:
1. **Faturamento Total:** Calcula o valor bruto arrecadado por toda a operação.
2. **Ticket Médio:** Agrupa os dados por ID de pedido (`Order ID`) para calcular o gasto médio por compra.
3. **Faturamento por Categoria:** Agrupa e classifica o faturamento por categorias de produtos em ordem decrescente, exportando relatórios em formato CSV.
4. **Faturamento por Região:** Analisa o desempenho de vendas geográfico e consolida os dados.
5. **Relatório Específico de Móveis:** Filtra registros da categoria *"Furniture"* detalhando o desempenho por subcategorias (`Sub-Category`).
6. **Interface Web Interativa (Streamlit):** Apresenta os resultados e métricas em um painel visual dinâmico.

## ⚙️ Como Executar o Projeto

1. Certifique-se de ter o Python instalado e instale as dependências necessárias executando no terminal:
   ```bash
   pip install pandas streamlit
