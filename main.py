import pandas as pd

pd.set_option('display.max_columns', None) 
pd.set_option('display.width', 1000) 

def main():

    #------------------------------------------------------------
    #-------------------- FATURAMENTO TOTAL ---------------------
    #------------------------------------------------------------

    tabela = pd.read_csv("train.csv", encoding="utf-8")
    faturamento_total = tabela["Sales"].sum()
    print(f"Faturamento total: R${faturamento_total:,.2f}\n")  

    #------------------------------------------------------------
    #-------------------- TICKET MÉDIO --------------------------
    #------------------------------------------------------------

    venda_por_pedido = tabela.groupby("Order ID")["Sales"].sum()
    ticket_medio = venda_por_pedido.mean()
    print(f"Cada pedido em média gasta: U${ticket_medio:,.2f}\n")

    #------------------------------------------------------------

    # Removendo colunas desnecessarias·
    df = tabela.drop(columns=["Ship Date", "Ship Mode", "Customer ID", "Segment", "Postal Code", "Product ID"])
    print(df)

    #---------------------------------------------------------------------
    #-------------------- FATURAMENTO CATEGORIA --------------------------
    #---------------------------------------------------------------------

    faturamento_categoria = df[["Category", "Sales"]].groupby("Category").sum()

    faturamento_categoria_formatado = faturamento_categoria.copy()

    faturamento_categoria_formatado = faturamento_categoria_formatado.sort_values(by="Sales", ascending=False)
    print(faturamento_categoria_formatado)

    faturamento_categoria_formatado["Sales"] = faturamento_categoria_formatado["Sales"].map("R${:,.2f}".format)

    faturamento_categoria = faturamento_categoria.reset_index()

    faturamento_categoria.to_csv("Faturamento_categoria.csv", index=False)

    #---------------------------------------------------------------------
    #--------------------- FATURAMENTO REGIÃO ----------------------------
    #---------------------------------------------------------------------
    
    faturamento_regiao = df[["Region", "Sales"]].groupby("Region").sum()

    faturamento_regiao = faturamento_regiao.sort_values(by="Sales", ascending=False)
    print(faturamento_regiao)

    faturamento_regiao = faturamento_regiao.reset_index()
    faturamento_regiao.to_csv("Faturamento_região.csv", index=False)

    #---------------------------------------------------------------------
    #------------------------- VENDAS MOVEIS -----------------------------
    #---------------------------------------------------------------------

    df_moveis = df[df["Category"] == "Furniture"]

    vendas_subcategoria = (
        df_moveis.groupby("Sub-Category")["Sales"]
        .sum()
        .reset_index()
    )

    vendas_subcategoria = vendas_subcategoria.sort_values(by="Sales", ascending=False)
    print(vendas_subcategoria)

    vendas_subcategoria.to_csv("relatorio_moveis.csv", index=False)

if __name__== "__main__":
    main()