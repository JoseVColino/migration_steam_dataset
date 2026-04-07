import glob

def consolidar_sql(nome_saida='consolidado_final.sql'):
    # Pega todos os arquivos da pasta
    todos_arquivos = glob.glob('dml/inserts*.sql')
    
    # Define a ordem de importância (tabelas pai primeiro, depois as intermediárias)
    # Coloque aqui o nome (ou parte do nome) dos arquivos na ordem correta
    ordem_prioridade = [
        'inserts_game.sql',
        'inserts_reviews.sql',
        'inserts_metacritic.sql',
        'inserts_company.sql',      
        'inserts_categories.sql', 
        'inserts_generos.sql',
        'inserts_tags.sql',
        'inserts_languages.sql',
        'inserts_operating_system.sql',
        'inserts_game_company.sql',
        'inserts_game_categories.sql',
        'inserts_game_generos.sql',
        'inserts_game_tag.sql',
        'inserts_game_languages.sql',
        'inserts_game_operating_system.sql',
        'inserts_movies.sql',
        'inserts_screenshots.sql',
    ]
    
    # Filtra e ordena: primeiro os da lista de prioridade, depois o resto
    arquivos_ordenados = []
    
    # 1. Adiciona os arquivos na ordem que você definiu
    for prioridade in ordem_prioridade:
        for arq in todos_arquivos:
            if prioridade in arq:
                arquivos_ordenados.append(arq)
                break
                
    # 2. Adiciona qualquer arquivo que sobrou e não estava na lista de prioridade
    for arq in sorted(todos_arquivos):
        if arq not in arquivos_ordenados:
            arquivos_ordenados.append(arq)

    with open(nome_saida, 'w', encoding='utf-8') as f_out:
        
        for arquivo in arquivos_ordenados:
            if arquivo == nome_saida:
                continue
                
            with open(arquivo, 'r', encoding='utf-8') as f_in:
                conteudo = f_in.read()
                f_out.write(f"-- Origem: {arquivo}\n")
                f_out.write(conteudo)
                
                if not conteudo.endswith('\n'):
                    f_out.write('\n')
                f_out.write("\n")
        

if __name__ == "__main__":
    consolidar_sql()