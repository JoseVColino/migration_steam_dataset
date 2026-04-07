import pandas as pd

def texto_sql(texto):
    if pd.isna(texto) or str(texto).strip() == "": return "NULL"
    texto_limpo = str(texto).replace("'", "''")
    return f"'{texto_limpo}'"

def gerar_inserts_os():
    os_map = {
        'Windows': 1,
        'Mac': 2,
        'Linux': 3
    }

    df = pd.read_csv('games.csv', usecols=['AppID', 'Windows', 'Mac', 'Linux'])

    with open('inserts_game_operating_system.sql', 'w', encoding='utf-8') as f:
        f.write("\n-- Inserts para game_operating_system\n")
        for _, row in df.iterrows():
            appid = row['AppID']
            
            for os_name, os_id in os_map.items():
                if row[os_name] == True or str(row[os_name]).lower() == 'true':
                    f.write(f"INSERT INTO game_operating_system (appid, id_operating_system) VALUES ({appid}, {os_id});\n")

if __name__ == "__main__":
    gerar_inserts_os()