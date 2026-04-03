import pandas as pd

def formatar_texto_sql(texto):
    """Trata valores nulos e remove aspas simples para o SQL."""
    if pd.isna(texto):
        return "NULL"
    texto_sem_aspas = str(texto).replace("'", "")
    return f"'{texto_sem_aspas}'"

def gerar_inserts_categories():
    arquivo_csv = 'games.csv'
    arquivo_sql_cat = 'inserts_categories.sql'
    arquivo_sql_gc = 'inserts_game_categories.sql'
    
    print("Lendo o arquivo CSV (apenas AppID e Categories)...")
    try:
        df = pd.read_csv(arquivo_csv, usecols=['AppID', 'Categories'])
    except FileNotFoundError:
        print(f"Erro: O arquivo '{arquivo_csv}' não foi encontrado na mesma pasta.")
        return

    # ==========================================
    # PASSO 1: DESCOBRIR AS CATEGORIAS ÚNICAS
    # ==========================================
    print("Processando as categorias únicas...")
    categorias_unicas = set() 
    
    for categorias_do_jogo in df['Categories'].dropna():
        lista_categorias = categorias_do_jogo.split(',')
        for cat in lista_categorias:
            categorias_unicas.add(cat.strip()) 
            
    cat_dict = {}
    id_atual = 1
    for cat in sorted(categorias_unicas):
        cat_dict[cat] = id_atual
        id_atual += 1

    # ==========================================
    # PASSO 2: GERAR O ARQUIVO DA TABELA CATEGORIES
    # ==========================================
    print(f"Gerando o arquivo '{arquivo_sql_cat}'...")
    with open(arquivo_sql_cat, 'w', encoding='utf-8') as f:
        for cat, cat_id in cat_dict.items():
            nome_limpo = formatar_texto_sql(cat)
            f.write(f"INSERT INTO categories (id, name) VALUES ({cat_id}, {nome_limpo});\n")

    # ==========================================
    # PASSO 3: GERAR O ARQUIVO DA TABELA GAME_CATEGORIES
    # ==========================================
    print(f"Gerando o arquivo '{arquivo_sql_gc}'...")



    with open(arquivo_sql_gc, 'w', encoding='utf-8') as f:
        for index, row in df.iterrows():
            appid = row['AppID']
            categorias_do_jogo = row['Categories']
            
            if not pd.isna(categorias_do_jogo):
                lista_categorias = str(categorias_do_jogo).split(',')
                
                for cat in lista_categorias:
                    cat_limpa = cat.strip()
                    id_categoria = cat_dict[cat_limpa]
                    
                    # Usando 'appid' para manter a consistência com as outras tabelas
                    f.write(f"INSERT INTO game_categories (appid, category_id) VALUES ({appid}, {id_categoria});\n")

    print("\nSucesso! Os dois scripts foram gerados com a sintaxe em inglês.")
    print(f"-> {arquivo_sql_cat}")
    print(f"-> {arquivo_sql_gc}")

if __name__ == "__main__":
    gerar_inserts_categories()