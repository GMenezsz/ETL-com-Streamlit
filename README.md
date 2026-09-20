
# 📊 Análise de Vendas e Faturamento com Python e Pandas

Projeto desenvolvido para automação de análise de dados corporativos, aplicando boas práticas de manipulação de dados, agrupamentos, filtros e exportação de relatórios em Python.

## 🚀 Tecnologias Utilizadas

* **Python** (Linguagem principal)
* **Pandas** (Biblioteca para manipulação e análise de dados)

## 📈 Funcionalidades do Projeto

O script realiza as seguintes etapas de processamento de dados sobre uma base de vendas:

1. **Faturamento Total:** Calcula o valor bruto arrecadado por toda a operação.
2. **Ticket Médio:** Agrupa os dados por ID de pedido (`Order ID`) para calcular o gasto médio por compra.
3. **Faturamento por Categoria:** Agrupa e classifica o faturamento por categorias de produtos em ordem decrescente, salvando uma cópia em formato CSV.
4. **Faturamento por Região:** Analisa o desempenho de vendas geográfico e exporta o relatório consolidado.
5. **Relatório Específico de Móveis:** Filtra apenas os registros da categoria *"Furniture"* e detalha o desempenho por subcategorias (`Sub-Category`), exportando o resultado final (`relatorio_moveis.csv`).

## ⚙️ Como Executar o Projeto

1. Certifique-se de ter o Python e a biblioteca Pandas instalados na sua máquina:
   ```bash
   pip install pandas
   ```
