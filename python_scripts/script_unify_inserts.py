import glob

def consolidar_sql(nome_saida='consolidado_final.sql'):
    arquivos = sorted(glob.glob('dml/inserts*.sql'))
    
    with open(nome_saida, 'w', encoding='utf-8') as f_out:
        # Inicia a transação única
        f_out.write("BEGIN;\n\n")
        
        for arquivo in arquivos:
            if arquivo == nome_saida:
                continue
                
            with open(arquivo, 'r', encoding='utf-8') as f_in:
                conteudo = f_in.read()
                f_out.write(f"-- Origem: {arquivo}\n")
                f_out.write(conteudo)
                
                if not conteudo.endswith('\n'):
                    f_out.write('\n')
                f_out.write("\n")
        
        # Finaliza e confirma a transação
        f_out.write("COMMIT;")

if __name__ == "__main__":
    consolidar_sql()