import re
import csv
import os

def higienizar_cadastros():
    regex_email = r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+'
    regex_telefone = r'\b\d{2}\s?\d{4,5}-?\d{4}\b'

    pasta_atual = os.path.dirname(os.path.abspath(__file__))
    
    arquivo_entrada = os.path.join(pasta_atual, 'cadastros.txt')
    arquivo_saida = os.path.join(pasta_atual, 'clientes_limpos.csv')

    try:
        with open(arquivo_entrada, 'r', encoding='utf-8') as f_in, \
             open(arquivo_saida, 'w', encoding='utf-8', newline='') as f_out:
            
            escritor_csv = csv.writer(f_out)
            escritor_csv.writerow(['Nome', 'Email', 'Telefone'])

            for linha in f_in:
                try:
                    linha = linha.strip()
                    if not linha:
                        continue 

                    email_match = re.search(regex_email, linha)
                    tel_match = re.search(regex_telefone, linha)

                    email = email_match.group() if email_match else 'SEM_EMAIL'
                    telefone = tel_match.group() if tel_match else 'SEM_TELEFONE'

                    nome_sujo = linha.replace(email if email != 'SEM_EMAIL' else '', '')
                    nome_sujo = nome_sujo.replace(telefone if telefone != 'SEM_TELEFONE' else '', '')
                    
                    nome_limpo = re.sub(r'[^a-zA-ZÀ-ÿ\s]', '', nome_sujo)
                    nome_limpo = " ".join(nome_limpo.split())

                    escritor_csv.writerow([nome_limpo, email, telefone])
                    
                except Exception as e:
                    print(f"Erro ao processar a linha: {linha}. Causa: {e}")

        print("Processo concluído. Verifique o arquivo clientes_limpos.csv.")

    except FileNotFoundError:
        print(f"Erro: O arquivo 'cadastros.txt' não foi encontrado no local: {pasta_atual}")

higienizar_cadastros()