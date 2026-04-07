import glob

def consolidar_sql(nome_saida='consolidado_final.sql'):
    # Localiza todos os arquivos que começam com 'inserts' e terminam em .sql
    arquivos = sorted(glob.glob('dml/inserts*.sql'))
    
    with open(nome_saida, 'w', encoding='utf-8') as f_out:
        for arquivo in arquivos:
            # Evita que o script tente ler o arquivo de saída caso ele já exista
            if arquivo == nome_saida:
                continue
                
            with open(arquivo, 'r', encoding='utf-8') as f_in:
                conteudo = f_in.read()
                f_out.write(f"-- Origem: {arquivo}\n")
                f_out.write(conteudo)
                # Garante uma quebra de linha entre o conteúdo de arquivos diferentes
                if not conteudo.endswith('\n'):
                    f_out.write('\n')
                f_out.write("\n")

if __name__ == "__main__":
    consolidar_sql()