import pandas as pd

def limpar_aspa_na_forca_bruta(texto):
    # Remove completamente qualquer aspa simples do texto.
    if pd.isna(texto):
        return "NULL"
    
    texto_sem_aspas = str(texto).replace("'", "")
    return f"'{texto_sem_aspas}'"

def gerar_inserts_reviews():
    arquivo_csv = 'games.csv'
    arquivo_sql = 'inserts_reviews.sql'
    
    print("Lendo o arquivo CSV...")
    try:
        colunas_necessarias = ['AppID', 'Reviews', 'Positive', 'Negative']
        df = pd.read_csv(arquivo_csv, usecols=colunas_necessarias)
    except FileNotFoundError:
        print(f"Erro: O arquivo '{arquivo_csv}' não foi encontrado na mesma pasta.")
        return

    print(f"Gerando os comandos SQL no arquivo '{arquivo_sql}'...")
    
    with open(arquivo_sql, 'w', encoding='utf-8') as f:
        f.write("-- ==================================================\n")
        f.write("-- INSERTS PARA A TABELA: reviews (Sem filtros de exclusão)\n")
        f.write("-- ==================================================\n\n")
        
        for index, row in df.iterrows():
            appid = row['AppID']
            review_text = limpar_aspa_na_forca_bruta(row['Reviews'])
            
            positive = int(row['Positive']) if not pd.isna(row['Positive']) else 0
            negative = int(row['Negative']) if not pd.isna(row['Negative']) else 0
            
            # Escreve o insert para TODAS as linhas do arquivo CSV
            sql = f"INSERT INTO reviews (appid, review_text, positive, negative) VALUES ({appid}, {review_text}, {positive}, {negative});\n"
            f.write(sql)

    print("Sucesso! Arquivo SQL gerado com todas as linhas do CSV.")

if __name__ == "__main__":
    gerar_inserts_reviews()