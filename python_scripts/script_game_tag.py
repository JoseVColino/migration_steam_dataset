import pandas as pd

def gerar_inserts_game_tag():
    df = pd.read_csv('games.csv', usecols=['AppID', 'Tags'])
    
    tags_unicas = set()
    for tags in df['Tags'].dropna():
        for tag in tags.split(','):
            tags_unicas.add(tag.strip())
            
    tag_dict = {tag: i for i, tag in enumerate(sorted(tags_unicas), 1)}

    with open('inserts_game_tag.sql', 'w', encoding='utf-8') as f:
        for _, row in df.iterrows():
            if pd.notna(row['Tags']):
                for tag in str(row['Tags']).split(','):
                    f.write(f"INSERT INTO game_tag (id_game, id_tag) VALUES ({row['AppID']}, {tag_dict[tag.strip()]});\n")

if __name__ == "__main__":
    gerar_inserts_game_tag()