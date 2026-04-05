import pandas as pd

def gerar_inserts_movies():
    df = pd.read_csv('games.csv', usecols=['AppID', 'Movies'])

    with open('inserts_movies.sql', 'w', encoding='utf-8') as f:
        for _, row in df.iterrows():
            if pd.isna(row['Movies']):
                continue
            appid = row['AppID']
            for url in str(row['Movies']).split(','):
                url_limpa = url.strip().replace("'", "")
                if url_limpa:
                    f.write(f"INSERT INTO movies (movie_url, jogo_id) VALUES ('{url_limpa}', {appid});\n")

if __name__ == "__main__":
    gerar_inserts_movies()
