import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3
import re
import os
from datetime import datetime

pasta_atual = os.path.dirname(os.path.abspath(__file__))


def conectar_banco():
    caminho_banco = os.path.join(pasta_atual, 'sistema.db')
    return sqlite3.connect(caminho_banco)

def iniciar_banco():
    try:
        conn = conectar_banco()
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS funcionarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT, 
                nome TEXT, 
                cargo TEXT
            )
        ''')
        conn.commit()
        conn.close()
    except Exception as e:
        log_erro(str(e))

def log_erro(mensagem):
    pasta_logs = os.path.join(pasta_atual, 'logs_erro')
    if not os.path.exists(pasta_logs):
        os.makedirs(pasta_logs)
        
    caminho_log = os.path.join(pasta_logs, 'auditoria.txt')
    with open(caminho_log, 'a', encoding='utf-8') as f:
        data_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"[{data_hora}] ERRO: {mensagem}\n")


def acao_importar():
    caminho_dados = os.path.join(pasta_atual, 'dados_brutos.txt')
    
    try:
        if not os.path.exists(caminho_dados):
            raise FileNotFoundError(f"Arquivo não encontrado no local: {caminho_dados}")
            
        with open(caminho_dados, 'r', encoding='utf-8') as f:
            linhas = f.readlines()

        conn = conectar_banco()
        cursor = conn.cursor()
        for linha in linhas:
            partes = linha.strip().split(',')
            if len(partes) == 2:
                cursor.execute('INSERT INTO funcionarios (nome, cargo) VALUES (?, ?)', (partes[0], partes[1]))
        
        conn.commit()
        conn.close()
        messagebox.showinfo("Sucesso", "Dados importados para o banco!")
        atualizar_tabela()
        
    except Exception as e:
        log_erro(f"Falha na importação: {e}")
        messagebox.showerror("Erro", "Erro ao importar. Verifique a pasta de logs.")

def atualizar_tabela(filtro_regex=""):
    try:
        for linha in tree.get_children():
            tree.delete(linha)

        conn = conectar_banco()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM funcionarios')
        registros = cursor.fetchall()
        conn.close()

        for reg in registros:
            texto_registro = f"{reg[0]} {reg[1]} {reg[2]}"
            
            if filtro_regex:
                try:
                    if re.search(filtro_regex, texto_registro, re.IGNORECASE):
                        tree.insert('', tk.END, values=reg)
                except re.error:
                    pass 
            else:
                tree.insert('', tk.END, values=reg)
                
    except Exception as e:
        log_erro(f"Erro ao listar dados na tabela: {e}")

def acao_buscar():
    termo = entry_busca.get()
    atualizar_tabela(termo)


iniciar_banco()

root = tk.Tk()
root.title("Dashboard Definitivo")
root.geometry("600x400")

frame_top = tk.Frame(root, pady=10)
frame_top.pack()
btn_importar = tk.Button(frame_top, text="Importar de TXT (dados_brutos.txt)", command=acao_importar)
btn_importar.pack()

frame_busca = tk.Frame(root, pady=5)
frame_busca.pack()
tk.Label(frame_busca, text="Buscar (Suporta Regex):").pack(side=tk.LEFT)
entry_busca = tk.Entry(frame_busca, width=30)
entry_busca.pack(side=tk.LEFT, padx=5)
btn_buscar = tk.Button(frame_busca, text="Filtrar", command=acao_buscar)
btn_buscar.pack(side=tk.LEFT)

frame_tabela = tk.Frame(root, padx=10, pady=10)
frame_tabela.pack(fill=tk.BOTH, expand=True)

colunas = ('ID', 'Nome', 'Cargo')
tree = ttk.Treeview(frame_tabela, columns=colunas, show='headings')
for col in colunas:
    tree.heading(col, text=col)
tree.pack(fill=tk.BOTH, expand=True)

atualizar_tabela()

root.mainloop()