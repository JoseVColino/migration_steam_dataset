import pandas as pd

def gerar_inserts_game_company():
    df = pd.read_csv('games.csv', usecols=['AppID', 'Developers', 'Publishers'])

    # Montar dicionario de empresas com mesmo ID do script_company
    empresas = set()
    for col in ['Developers', 'Publishers']:
        for valor in df[col].dropna():
            for nome in str(valor).split(','):
                nome_limpo = nome.strip()
                if nome_limpo:
                    empresas.add(nome_limpo)

    empresa_dict = {nome: i for i, nome in enumerate(sorted(empresas), 1)}

    with open('inserts_game_company.sql', 'w', encoding='utf-8') as f:
        for _, row in df.iterrows():
            appid = row['AppID']

            if pd.notna(row['Developers']):
                for nome in str(row['Developers']).split(','):
                    nome_limpo = nome.strip()
                    if nome_limpo:
                        f.write(f"INSERT INTO game_company (id_game, id_company, type) VALUES ({appid}, {empresa_dict[nome_limpo]}, 'developer');\n")

            if pd.notna(row['Publishers']):
                for nome in str(row['Publishers']).split(','):
                    nome_limpo = nome.strip()
                    if nome_limpo:
                        f.write(f"INSERT INTO game_company (id_game, id_company, type) VALUES ({appid}, {empresa_dict[nome_limpo]}, 'publisher');\n")

if __name__ == "__main__":
    gerar_inserts_game_company()
