import pandas as pd

def gerar_inserts_company():
    df = pd.read_csv('games.csv', usecols=['Developers', 'Publishers'])

    empresas = set()
    for col in ['Developers', 'Publishers']:
        for valor in df[col].dropna():
            for nome in str(valor).split(','):
                nome_limpo = nome.strip()
                if nome_limpo:
                    empresas.add(nome_limpo)

    with open('inserts_company.sql', 'w', encoding='utf-8') as f:
        for i, nome in enumerate(sorted(empresas), 1):
            nome_sql = nome.replace("'", "")
            f.write(f"INSERT INTO company (id, nome) VALUES ({i}, '{nome_sql}');\n")

if __name__ == "__main__":
    gerar_inserts_company()
