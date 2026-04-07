import pandas as pd

def texto_sql(texto):
    if pd.isna(texto) or str(texto).strip() in ["", "nan", "None"]: return "NULL"
    # Duplica aspas simples internas (ex: Garry's Mod -> 'Garry''s Mod') e envolve com aspas
    texto_limpo = str(texto).replace("'", "''") 
    return f"'{texto_limpo}'"

def numero_sql(valor):
    if pd.isna(valor) or str(valor).strip() in ["", "nan", "None"]: return "NULL"
    try:
        f_val = float(valor)
        # Se por acaso o float resultar em NaN matemático
        if pd.isna(f_val): return "NULL"
        return str(int(f_val)) if f_val.is_integer() else str(f_val)
    except ValueError:
        return "NULL"

def gerar_inserts_game():
    colunas = ['AppID', 'Name', 'Release date', 'Estimated owners', 'Peak CCU', 'Required age', 'Price', 'Discount', 'DLC count', 'About the game', 'Supported languages', 'Full audio languages', 'Reviews', 'Header image', 'Website', 'Support url', 'Support email', 'Windows', 'Mac', 'Linux', 'Metacritic score', 'Metacritic url', 'User score', 'Positive', 'Negative', 'Score rank', 'Achievements', 'Recommendations', 'Notes', 'Average playtime forever', 'Average playtime two weeks', 'Median playtime forever', 'Median playtime two weeks', 'Developers', 'Publishers', 'Categories', 'Genres', 'Tags', 'Screenshots', 'Movies']
    
    # low_memory=False ajuda a evitar avisos de tipos de dados mistos no Pandas
    df = pd.read_csv('games.csv', header=0, names=colunas, low_memory=False)
    
    # Forçamos a coluna a ser tratada como texto (str) antes de dar o split
    df[['est_min', 'est_max']] = df['Estimated owners'].astype(str).str.split(' - ', expand=True)

    with open('inserts_game.sql', 'w', encoding='utf-8') as f:
        for _, row in df.iterrows():
            appid = numero_sql(row['AppID'])
            name = texto_sql(row['Name'])
            rel_date = texto_sql(row['Release date'])
            est_min = numero_sql(row['est_min'])
            est_max = numero_sql(row['est_max'])
            peak = numero_sql(row['Peak CCU'])
            age = numero_sql(row['Required age'])
            price = numero_sql(row['Price'])
            disc = numero_sql(row['Discount'])
            dlc = numero_sql(row['DLC count'])
            ach = numero_sql(row['Achievements'])
            rec = numero_sql(row['Recommendations'])
            rank = numero_sql(row['Score rank'])
            med_for = numero_sql(row['Median playtime forever'])
            med_2w = numero_sql(row['Median playtime two weeks'])
            avg_for = numero_sql(row['Average playtime forever'])
            avg_2w = numero_sql(row['Average playtime two weeks'])
            
            about = texto_sql(row['About the game'])
            web = texto_sql(row['Website'])
            meta = texto_sql(row['Metacritic url'])
            sup_e = texto_sql(row['Support email'])
            sup_u = texto_sql(row['Support url'])
            notes = texto_sql(row['Notes'])
            header = texto_sql(row['Header image'])

            f.write(f"INSERT INTO game (appid, name, release_date, estimated_owners_min, estimated_owners_max, peak_ccu, required_age, price, discount, dlc_count, about_the_game, website, achievements, recommendations, metacritic_url, support_email, support_url, notes, score_rank, header_image, median_playtime_forever, median_playtime_two_weeks, average_playtime_forever, average_playtime_two_weeks) VALUES ({appid}, {name}, {rel_date}, {est_min}, {est_max}, {peak}, {age}, {price}, {disc}, {dlc}, {about}, {web}, {ach}, {rec}, {meta}, {sup_e}, {sup_u}, {notes}, {rank}, {header}, {med_for}, {med_2w}, {avg_for}, {avg_2w});\n")

if __name__ == "__main__":
    gerar_inserts_game()