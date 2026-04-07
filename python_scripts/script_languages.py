import pandas as pd
import ast

def texto_sql(texto):
    if pd.isna(texto) or str(texto).strip() == "": return "NULL"
    texto_limpo = str(texto).replace("'", "''")
    return f"'{texto_limpo}'"

def tratar_lista(valor):
    if pd.isna(valor) or str(valor).strip() in ["", "[]"]:
        return []
    try:
        return ast.literal_eval(valor)
    except:
        return [i.strip().strip("'").strip('"') for i in str(valor).replace("[", "").replace("]", "").split(",")]

def gerar_inserts_tabela_languages():
    df = pd.read_csv('games.csv', usecols=['Supported languages', 'Full audio languages'])
    
    idiomas_unicos = set()
    for col in ['Supported languages', 'Full audio languages']:
        for entrada in df[col].dropna():
            idiomas_unicos.update(tratar_lista(entrada))
    
    with open('inserts_languages.sql', 'w', encoding='utf-8') as f:
        for i, lang in enumerate(sorted(idiomas_unicos), 1):
            f.write(f"INSERT INTO languages (id, language_name) VALUES ({i}, {texto_sql(lang)});\n")

if __name__ == "__main__":
    gerar_inserts_tabela_languages()