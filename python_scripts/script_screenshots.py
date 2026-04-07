import pandas as pd

def texto_sql(texto):
    if pd.isna(texto) or str(texto).strip() == "": return "NULL"
    texto_limpo = str(texto).replace("'", "''")
    return f"'{texto_limpo}'"

def gerar_inserts_screenshots():
    df = pd.read_csv('games.csv', usecols=['AppID', 'Screenshots'])

    with open('inserts_screenshots.sql', 'w', encoding='utf-8') as f:
        for _, row in df.iterrows():
            appid = row['AppID']
            urls_raw = row['Screenshots']
            
            if pd.notna(urls_raw):
                urls = str(urls_raw).split(',')
                for url in urls:
                    url_limpa = url.strip()
                    if url_limpa:
                        f.write(f"INSERT INTO screenshots (screenshot_url, appid) VALUES ({texto_sql(url_limpa)}, {appid});\n")

if __name__ == "__main__":
    gerar_inserts_screenshots()