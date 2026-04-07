import pandas as pd
import ast

def tratar_lista(valor):
    if pd.isna(valor) or str(valor).strip() in ["", "[]"]:
        return []
    try:
        return ast.literal_eval(valor)
    except:
        return [i.strip().strip("'").strip('"') for i in str(valor).replace("[", "").replace("]", "").split(",")]

def gerar_inserts_tabela_game_languages():
    df = pd.read_csv('games.csv', usecols=['AppID', 'Supported languages', 'Full audio languages'])
    
    idiomas_unicos = set()
    for col in ['Supported languages', 'Full audio languages']:
        for entrada in df[col].dropna():
            idiomas_unicos.update(tratar_lista(entrada))
    
    idioma_to_id = {lang: i for i, lang in enumerate(sorted(idiomas_unicos), 1)}

    with open('inserts_game_languages.sql', 'w', encoding='utf-8') as f:
        for _, row in df.iterrows():
            appid = row['AppID']
            
            for lang in tratar_lista(row['Supported languages']):
                if lang in idioma_to_id:
                    f.write(f"INSERT INTO game_languages (appid, id_language, support_type) VALUES ({appid}, {idioma_to_id[lang]}, 'supported');\n")
            
            for lang in tratar_lista(row['Full audio languages']):
                if lang in idioma_to_id:
                    f.write(f"INSERT INTO game_languages (appid, id_language, support_type) VALUES ({appid}, {idioma_to_id[lang]}, 'audio');\n")

if __name__ == "__main__":
    gerar_inserts_tabela_game_languages()