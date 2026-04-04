import pandas as pd

def formatar_texto_sql(texto):
    if pd.isna(texto) or str(texto).strip() == "": return "NULL"
    return f"'{str(texto).replace(chr(39), '')}'"

def gerar_inserts_tags():
    df = pd.read_csv('games.csv', usecols=['Tags'])
    tags_unicas = set()
    
    for tags in df['Tags'].dropna():
        for tag in tags.split(','):
            tags_unicas.add(tag.strip())
            
    with open('inserts_tags.sql', 'w', encoding='utf-8') as f:
        for id_atual, tag in enumerate(sorted(tags_unicas), 1):
            f.write(f"INSERT INTO tags (id, name) VALUES ({id_atual}, {formatar_texto_sql(tag)});\n")

if __name__ == "__main__":
    gerar_inserts_tags()