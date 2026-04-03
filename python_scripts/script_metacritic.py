import pandas as pd


def formatar_texto_sql(texto):
    if pd.isna(texto):
        return "NULL"
    texto_sem_aspas = str(texto).replace("'", "")
    return f"'{texto_sem_aspas}'"


def gerar_inserts_metacritic():
    arquivo_csv = 'games.csv'
    arquivo_sql = 'inserts_metacritic.sql'

    print("Lendo o arquivo CSV...")
    try:
        colunas_necessarias = ['AppID', 'Metacritic url', 'Metacritic score']
        df = pd.read_csv(arquivo_csv, usecols=colunas_necessarias)
    except FileNotFoundError:
        print(f"Erro: O arquivo '{arquivo_csv}' não foi encontrado.")
        return

    print(f"Gerando os comandos SQL em '{arquivo_sql}'...")

    with open(arquivo_sql, 'w', encoding='utf-8') as f:
        for index, row in df.iterrows():
            appid = row['AppID']
            metacritic_url = formatar_texto_sql(row['Metacritic url'])

            score_atual = row['Metacritic score']
            # Garante que seja um número inteiro ou NULL
            score_val = int(score_atual) if not pd.isna(score_atual) else "NULL"

            # CORRIGIDO: Agora usando a coluna 'metacritic_score'
            sql = f"INSERT INTO metacritic (appid, metacritic_url, metacritic_score) VALUES ({appid}, {metacritic_url}, {score_val});\n"
            f.write(sql)

    print("Sucesso! Arquivo corrigido com 'metacritic_score'.")


if __name__ == "__main__":
    gerar_inserts_metacritic()