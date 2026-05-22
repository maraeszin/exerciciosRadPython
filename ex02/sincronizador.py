import os
import json
import sqlite3

def importar_vendas_json():
    pasta_atual = os.path.dirname(os.path.abspath(__file__))
    
    pasta_json = os.path.join(pasta_atual, 'vendas_json')
    caminho_banco = os.path.join(pasta_atual, 'banco_vendas.db')
    
    conn = sqlite3.connect(caminho_banco)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS vendas (
            id INTEGER PRIMARY KEY AUTOINCREMENT, 
            produto TEXT, 
            quantidade INTEGER, 
            valor REAL
        )
    ''')
    conn.commit()

    if not os.path.exists(pasta_json):
        print(f"Erro: A pasta não foi encontrada no local: {pasta_json}")
        conn.close()
        return

    for arquivo in os.listdir(pasta_json):
        if arquivo.endswith('.json'):
            caminho_arquivo = os.path.join(pasta_json, arquivo)
            
            try:
                with open(caminho_arquivo, 'r', encoding='utf-8') as f:
                    dados = json.load(f)
                
                lista_insercao = []
                for item in dados:
                    lista_insercao.append((item.get('produto'), item.get('quantidade'), item.get('valor')))

                cursor.executemany('INSERT INTO vendas (produto, quantidade, valor) VALUES (?, ?, ?)', lista_insercao)
                conn.commit()
                print(f"Arquivo {arquivo} importado com sucesso!")

            except json.JSONDecodeError:
                print(f"Erro: O arquivo {arquivo} está mal formatado. Desfazendo operações deste arquivo.")
                conn.rollback() 
                
            except Exception as e:
                print(f"Erro inesperado no arquivo {arquivo}: {e}")
                conn.rollback()
                
            finally:
                pass

    conn.close()
    print("Sincronização finalizada.")

importar_vendas_json()