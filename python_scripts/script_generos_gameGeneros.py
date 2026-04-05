import pandas as pd

def gerar_inserts_generos():
    df = pd.read_csv('games.csv', usecols=['AppID', 'Genres'])

    generos = set()
    for valor in df['Genres'].dropna():
        for g in str(valor).split(','):
            g_limpo = g.strip()
            if g_limpo:
                generos.add(g_limpo)

    genero_dict = {nome: i for i, nome in enumerate(sorted(generos), 1)}

    with open('inserts_generos.sql', 'w', encoding='utf-8') as f:
        for nome, gid in genero_dict.items():
            nome_sql = nome.replace("'", "")
            f.write(f"INSERT INTO generos (id, name) VALUES ({gid}, '{nome_sql}');\n")

    with open('inserts_game_generos.sql', 'w', encoding='utf-8') as f:
        for _, row in df.iterrows():
            if pd.notna(row['Genres']):
                for g in str(row['Genres']).split(','):
                    g_limpo = g.strip()
                    if g_limpo:
                        f.write(f"INSERT INTO game_generos (id_game, id_genero) VALUES ({row['AppID']}, {genero_dict[g_limpo]});\n")

if __name__ == "__main__":
    gerar_inserts_generos()
