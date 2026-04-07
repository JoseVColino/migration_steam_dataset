"""
Script de migração direta: lê games.csv e insere no PostgreSQL via psycopg2.
Usa execute_values para inserção em lote (batch), muito mais rápido que gerar .sql.

Uso:
    python migrate.py

Requer: pip install psycopg2-binary pandas
"""

import pandas as pd
import ast
import psycopg2
from psycopg2.extras import execute_values

# ============================================================
# CONFIGURAÇÃO DO BANCO - ALTERE AQUI
# ============================================================
DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "dbname": "vaiPelaMor",
    "user": "postgres",
    "password": "",
}

CSV_PATH = "games.csv"
BATCH_SIZE = 5000

# ============================================================
# HELPERS
# ============================================================

def limpar(texto):
    """Retorna string limpa ou None para NULL."""
    if pd.isna(texto) or str(texto).strip() == "":
        return None
    return str(texto)


def to_int(valor):
    if pd.isna(valor) or str(valor).strip() == "":
        return None
    try:
        return int(float(valor))
    except (ValueError, TypeError):
        return None


def to_float(valor):
    if pd.isna(valor) or str(valor).strip() == "":
        return None
    try:
        return float(valor)
    except (ValueError, TypeError):
        return None


def tratar_lista(valor):
    """Parseia listas no formato ['item1', 'item2'] ou separadas por vírgula."""
    if pd.isna(valor) or str(valor).strip() in ("", "[]"):
        return []
    try:
        return ast.literal_eval(valor)
    except Exception:
        return [i.strip().strip("'").strip('"') for i in str(valor).replace("[", "").replace("]", "").split(",")]


def split_csv_field(valor):
    """Divide campo separado por vírgula, retorna lista de strings limpas."""
    if pd.isna(valor):
        return []
    return [x.strip() for x in str(valor).split(",") if x.strip()]


def inserir_lote(cur, sql, dados):
    """Insere dados em lotes usando execute_values."""
    for i in range(0, len(dados), BATCH_SIZE):
        execute_values(cur, sql, dados[i:i + BATCH_SIZE])


# ============================================================
# FUNÇÕES DE MIGRAÇÃO
# ============================================================

def migrar_game(cur, df):
    print("  -> game...")
    colunas_csv = [
        'AppID', 'Name', 'Release date', 'Estimated owners', 'Peak CCU',
        'Required age', 'Price', 'Discount', 'DLC count', 'About the game',
        'Website', 'Achievements', 'Recommendations', 'Support email',
        'Support url', 'Notes', 'Score rank', 'Header image',
        'Median playtime forever', 'Median playtime two weeks',
        'Average playtime forever', 'Average playtime two weeks'
    ]

    dados = []
    for _, row in df.iterrows():
        est = str(row['Estimated owners']) if pd.notna(row['Estimated owners']) else ""
        parts = est.split(" - ")
        est_min = to_int(parts[0]) if len(parts) >= 1 else None
        est_max = to_int(parts[1]) if len(parts) >= 2 else None

        dados.append((
            to_int(row['AppID']),
            limpar(row['Name']),
            limpar(row['Release date']),
            est_min, est_max,
            to_int(row['Peak CCU']),
            to_int(row['Required age']),
            to_float(row['Price']),
            to_int(row['Discount']),
            to_int(row['DLC count']),
            limpar(row['About the game']),
            limpar(row['Website']),
            to_int(row['Achievements']),
            to_int(row['Recommendations']),
            limpar(row['Support email']),
            limpar(row['Support url']),
            limpar(row['Notes']),
            to_int(row['Score rank']),
            limpar(row['Header image']),
            to_int(row['Median playtime forever']),
            to_int(row['Median playtime two weeks']),
            to_int(row['Average playtime forever']),
            to_int(row['Average playtime two weeks']),
        ))

    sql = """INSERT INTO game (appid, name, release_date, estimated_owners_min,
        estimated_owners_max, peak_ccu, required_age, price, discount, dlc_count,
        about_the_game, website, achievements, recommendations, support_email,
        support_url, notes, score_rank, header_image, median_playtime_forever,
        median_playtime_two_weeks, average_playtime_forever,
        average_playtime_two_weeks) VALUES %s"""
    inserir_lote(cur, sql, dados)
    print(f"     {len(dados)} jogos inseridos.")


def migrar_reviews(cur, df):
    print("  -> reviews...")
    dados = []
    for _, row in df.iterrows():
        dados.append((
            to_int(row['AppID']),
            limpar(row['Reviews']),
            to_int(row['Positive']) or 0,
            to_int(row['Negative']) or 0,
        ))
    sql = "INSERT INTO reviews (appid, review_text, positive, negative) VALUES %s"
    inserir_lote(cur, sql, dados)
    print(f"     {len(dados)} reviews inseridas.")


def migrar_metacritic(cur, df):
    print("  -> metacritic...")
    dados = []
    for _, row in df.iterrows():
        dados.append((
            to_int(row['AppID']),
            limpar(row['Metacritic url']),
            to_int(row['Metacritic score']),
        ))
    sql = "INSERT INTO metacritic (appid, metacritic_url, metacritic_score) VALUES %s"
    inserir_lote(cur, sql, dados)
    print(f"     {len(dados)} registros de metacritic inseridos.")


def migrar_tags(cur, df):
    print("  -> tags...")
    tags_unicas = set()
    for tags in df['Tags'].dropna():
        for tag in split_csv_field(tags):
            tags_unicas.add(tag)

    tag_dict = {nome: i for i, nome in enumerate(sorted(tags_unicas), 1)}

    dados = [(tid, nome) for nome, tid in tag_dict.items()]
    sql = "INSERT INTO tags (id, name) VALUES %s"
    inserir_lote(cur, sql, dados)
    print(f"     {len(dados)} tags inseridas.")
    return tag_dict


def migrar_game_tag(cur, df, tag_dict):
    print("  -> game_tag...")
    dados = []
    for _, row in df.iterrows():
        if pd.notna(row['Tags']):
            appid = to_int(row['AppID'])
            for tag in split_csv_field(row['Tags']):
                if tag in tag_dict:
                    dados.append((appid, tag_dict[tag]))
    sql = "INSERT INTO game_tag (id_game, id_tag) VALUES %s"
    inserir_lote(cur, sql, dados)
    print(f"     {len(dados)} relações game_tag inseridas.")


def migrar_categories(cur, df):
    print("  -> categories...")
    cats_unicas = set()
    for cats in df['Categories'].dropna():
        for cat in split_csv_field(cats):
            cats_unicas.add(cat)

    cat_dict = {nome: i for i, nome in enumerate(sorted(cats_unicas), 1)}

    dados = [(cid, nome) for nome, cid in cat_dict.items()]
    sql = "INSERT INTO categories (id, name) VALUES %s"
    inserir_lote(cur, sql, dados)
    print(f"     {len(dados)} categorias inseridas.")
    return cat_dict


def migrar_game_categories(cur, df, cat_dict):
    print("  -> game_categories...")
    dados = []
    for _, row in df.iterrows():
        if pd.notna(row['Categories']):
            appid = to_int(row['AppID'])
            for cat in split_csv_field(row['Categories']):
                if cat in cat_dict:
                    dados.append((appid, cat_dict[cat]))
    sql = "INSERT INTO game_categories (appid, category_id) VALUES %s"
    inserir_lote(cur, sql, dados)
    print(f"     {len(dados)} relações game_categories inseridas.")


def migrar_company(cur, df):
    print("  -> company...")
    empresas = set()
    for col in ['Developers', 'Publishers']:
        for valor in df[col].dropna():
            for nome in split_csv_field(valor):
                empresas.add(nome)

    empresa_dict = {nome: i for i, nome in enumerate(sorted(empresas), 1)}

    dados = [(eid, nome) for nome, eid in empresa_dict.items()]
    sql = "INSERT INTO company (id, name) VALUES %s"
    inserir_lote(cur, sql, dados)
    print(f"     {len(dados)} empresas inseridas.")
    return empresa_dict


def migrar_game_company(cur, df, empresa_dict):
    print("  -> game_company...")
    dados = []
    for _, row in df.iterrows():
        appid = to_int(row['AppID'])
        if pd.notna(row['Developers']):
            for nome in split_csv_field(row['Developers']):
                if nome in empresa_dict:
                    dados.append((appid, empresa_dict[nome], 'developer'))
        if pd.notna(row['Publishers']):
            for nome in split_csv_field(row['Publishers']):
                if nome in empresa_dict:
                    dados.append((appid, empresa_dict[nome], 'publisher'))
    sql = "INSERT INTO game_company (id_game, id_company, type) VALUES %s"
    inserir_lote(cur, sql, dados)
    print(f"     {len(dados)} relações game_company inseridas.")


def migrar_generos(cur, df):
    print("  -> generos...")
    generos = set()
    for valor in df['Genres'].dropna():
        for g in split_csv_field(valor):
            generos.add(g)

    genero_dict = {nome: i for i, nome in enumerate(sorted(generos), 1)}

    dados = [(gid, nome) for nome, gid in genero_dict.items()]
    sql = "INSERT INTO generos (id, name) VALUES %s"
    inserir_lote(cur, sql, dados)
    print(f"     {len(dados)} gêneros inseridos.")
    return genero_dict


def migrar_game_generos(cur, df, genero_dict):
    print("  -> game_generos...")
    dados = []
    for _, row in df.iterrows():
        if pd.notna(row['Genres']):
            appid = to_int(row['AppID'])
            for g in split_csv_field(row['Genres']):
                if g in genero_dict:
                    dados.append((appid, genero_dict[g]))
    sql = "INSERT INTO game_generos (id_game, id_genero) VALUES %s"
    inserir_lote(cur, sql, dados)
    print(f"     {len(dados)} relações game_generos inseridas.")


def migrar_languages(cur, df):
    print("  -> languages...")
    idiomas = set()
    for col in ['Supported languages', 'Full audio languages']:
        for entrada in df[col].dropna():
            idiomas.update(tratar_lista(entrada))

    idioma_dict = {lang: i for i, lang in enumerate(sorted(idiomas), 1)}

    dados = [(lid, lang) for lang, lid in idioma_dict.items()]
    sql = "INSERT INTO languages (id, language_name) VALUES %s"
    inserir_lote(cur, sql, dados)
    print(f"     {len(dados)} idiomas inseridos.")
    return idioma_dict


def migrar_game_languages(cur, df, idioma_dict):
    print("  -> game_languages...")
    dados = []
    for _, row in df.iterrows():
        appid = to_int(row['AppID'])
        for lang in tratar_lista(row['Supported languages']):
            if lang in idioma_dict:
                dados.append((appid, idioma_dict[lang], 'supported'))
        for lang in tratar_lista(row['Full audio languages']):
            if lang in idioma_dict:
                dados.append((appid, idioma_dict[lang], 'audio'))
    sql = "INSERT INTO game_languages (appid, id_language, support_type) VALUES %s"
    inserir_lote(cur, sql, dados)
    print(f"     {len(dados)} relações game_languages inseridas.")


def migrar_operating_system(cur, df):
    print("  -> operating_system...")
    execute_values(cur, "INSERT INTO operating_system (id, name) VALUES %s",
                   [(1, 'Windows'), (2, 'Mac'), (3, 'Linux')])
    print("     3 sistemas operacionais inseridos.")

    print("  -> game_operating_system...")
    os_map = {'Windows': 1, 'Mac': 2, 'Linux': 3}
    dados = []
    for _, row in df.iterrows():
        appid = to_int(row['AppID'])
        for os_name, os_id in os_map.items():
            if str(row[os_name]).strip().lower() == 'true':
                dados.append((appid, os_id))
    sql = "INSERT INTO game_operating_system (appid, id_operating_system) VALUES %s"
    inserir_lote(cur, sql, dados)
    print(f"     {len(dados)} relações game_os inseridas.")


def migrar_movies(cur, df):
    print("  -> movies...")
    dados = []
    for _, row in df.iterrows():
        if pd.isna(row['Movies']):
            continue
        appid = to_int(row['AppID'])
        for url in split_csv_field(row['Movies']):
            if url:
                dados.append((url, appid))
    sql = "INSERT INTO movies (movie_url, jogo_id) VALUES %s"
    inserir_lote(cur, sql, dados)
    print(f"     {len(dados)} movies inseridos.")


def migrar_screenshots(cur, df):
    print("  -> screenshots...")
    dados = []
    for _, row in df.iterrows():
        if pd.isna(row['Screenshots']):
            continue
        appid = to_int(row['AppID'])
        for url in split_csv_field(row['Screenshots']):
            if url:
                dados.append((url, appid))
    sql = "INSERT INTO screenshots (screenshot_url, appid) VALUES %s"
    inserir_lote(cur, sql, dados)
    print(f"     {len(dados)} screenshots inseridos.")


# ============================================================
# MAIN
# ============================================================

def main():
    print("Lendo CSV...")
    colunas = [
        'AppID', 'Name', 'Release date', 'Estimated owners', 'Peak CCU',
        'Required age', 'Price', 'Discount', 'DLC count', 'About the game',
        'Supported languages', 'Full audio languages', 'Reviews', 'Header image',
        'Website', 'Support url', 'Support email', 'Windows', 'Mac', 'Linux',
        'Metacritic url', 'Metacritic score', 'User score', 'Positive', 'Negative',
        'Score rank', 'Achievements', 'Recommendations', 'Notes',
        'Average playtime forever', 'Average playtime two weeks',
        'Median playtime forever', 'Median playtime two weeks',
        'Developers', 'Publishers', 'Categories', 'Genres', 'Tags',
        'Screenshots', 'Movies'
    ]
    df = pd.read_csv(CSV_PATH, header=0, names=colunas, low_memory=False)
    print(f"  {len(df)} linhas carregadas.\n")

    print("Conectando ao banco...")
    conn = psycopg2.connect(**DB_CONFIG)
    conn.autocommit = False
    cur = conn.cursor()

    try:
        print("Inserindo dados...\n")

        # 1) Tabela principal
        migrar_game(cur, df)

        # 2) Tabelas 1:N dependentes de game
        migrar_reviews(cur, df)
        migrar_metacritic(cur, df)

        # 3) Tabelas de domínio (lookup)
        empresa_dict = migrar_company(cur, df)
        cat_dict = migrar_categories(cur, df)
        genero_dict = migrar_generos(cur, df)
        tag_dict = migrar_tags(cur, df)
        idioma_dict = migrar_languages(cur, df)
        migrar_operating_system(cur, df)  # insere operating_system + game_operating_system

        # 4) Tabelas de relacionamento M:N
        migrar_game_company(cur, df, empresa_dict)
        migrar_game_categories(cur, df, cat_dict)
        migrar_game_generos(cur, df, genero_dict)
        migrar_game_tag(cur, df, tag_dict)
        migrar_game_languages(cur, df, idioma_dict)

        # 5) Tabelas restantes
        migrar_movies(cur, df)
        migrar_screenshots(cur, df)

        conn.commit()
        print("\nMigração concluída com sucesso!")

    except Exception as e:
        conn.rollback()
        print(f"\nERRO: {e}")
        print("Rollback realizado. Nenhum dado foi inserido.")
        raise
    finally:
        cur.close()
        conn.close()


if __name__ == "__main__":
    main()
