import tkinter as tk
from tkinter import messagebox
import psycopg2
import pandas as pd

# Configurar a conexão com o banco de dados
def connect_db():
    return psycopg2.connect(
        dbname="banco_ProfessorWalter",
        user="postgres",
        password="dau26sub",
        host="localhost",
        port="5432"
    )

# Funções de Inclusão
def add_conteudo():
    nome_conteudo = entry_nome_conteudo.get()
    descricao = entry_descricao.get()
    id_serie = int(entry_id_serie.get())
    id_bimestre = int(entry_id_bimestre.get())
    id_disciplina = int(entry_id_disciplina.get())

    conn = connect_db()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO conteudo (nome_conteudo, descricao, id_serie, id_bimestre, id_disciplina)
        VALUES (%s, %s, %s, %s, %s)
    """, (nome_conteudo, descricao, id_serie, id_bimestre, id_disciplina))
    conn.commit()
    cur.close()
    conn.close()
    messagebox.showinfo("Sucesso", "Conteúdo adicionado com sucesso!")

def add_questao():
    enunciado = entry_enunciado.get()
    tipo_questao = entry_tipo_questao.get()
    id_conteudo = int(entry_id_conteudo_questao.get())

    conn = connect_db()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO questao (enunciado, tipo_questao, id_conteudo)
        VALUES (%s, %s, %s)
    """, (enunciado, tipo_questao, id_conteudo))
    conn.commit()
    cur.close()
    conn.close()
    messagebox.showinfo("Sucesso", "Questão adicionada com sucesso!")

def delete_conteudo():
    conteudo_id = entry_id_conteudo.get()
    if not conteudo_id.strip():
        messagebox.showerror("Erro", "O ID do conteúdo não pode estar vazio.")
        return

    try:
        id_conteudo = int(conteudo_id)
        conn = connect_db()
        cur = conn.cursor()
        cur.execute("DELETE FROM conteudo WHERE id_conteudo = %s", (id_conteudo,))
        conn.commit()
        cur.close()
        conn.close()
        messagebox.showinfo("Sucesso", "Conteúdo excluído com sucesso.")
    except ValueError:
        messagebox.showerror("Erro", "ID do conteúdo deve ser um número inteiro.")
    except Exception as e:
        messagebox.showerror("Erro", f"Um erro ocorreu: {e}")

def delete_questao():
    id_questao = entry_id_questao.get()
    if not id_questao.strip():
        messagebox.showerror("Erro", "O ID da questão não pode estar vazio.")
        return

    try:
        id_questao = int(id_questao)
        conn = connect_db()
        cur = conn.cursor()
        cur.execute("DELETE FROM questao WHERE id_questao = %s", (id_questao,))
        conn.commit()
        cur.close()
        conn.close()
        messagebox.showinfo("Sucesso", "Questão excluída com sucesso.")
    except ValueError:
        messagebox.showerror("Erro", "ID da questão deve ser um número inteiro.")
    except Exception as e:
        messagebox.showerror("Erro", f"Um erro ocorreu: {e}")

# Funções de Modificação
def update_conteudo():
    id_conteudo = int(entry_id_conteudo.get())
    nome_conteudo = entry_nome_conteudo.get()
    descricao = entry_descricao.get()
    id_serie = int(entry_id_serie.get())
    id_bimestre = int(entry_id_bimestre.get())
    id_disciplina = int(entry_id_disciplina.get())

    conn = connect_db()
    cur = conn.cursor()
    cur.execute("""
        UPDATE conteudo SET nome_conteudo = %s, descricao = %s, id_serie = %s, id_bimestre = %s, id_disciplina = %s
        WHERE id_conteudo = %s
    """, (nome_conteudo, descricao, id_serie, id_bimestre, id_disciplina, id_conteudo))
    conn.commit()
    cur.close()
    conn.close()
    messagebox.showinfo("Sucesso", "Conteúdo atualizado com sucesso!")

def update_questao():
    id_questao = int(entry_id_questao.get())
    enunciado = entry_enunciado.get()
    tipo_questao = entry_tipo_questao.get()
    id_conteudo = int(entry_id_conteudo_questao.get())

    conn = connect_db()
    cur = conn.cursor()
    cur.execute("""
        UPDATE questao SET enunciado = %s, tipo_questao = %s, id_conteudo = %s
        WHERE id_questao = %s
    """, (enunciado, tipo_questao, id_conteudo, id_questao))
    conn.commit()
    cur.close()
    conn.close()
    messagebox.showinfo("Sucesso", "Questão atualizada com sucesso!")

# Função de Exportação
def export_questoes():
    conn = connect_db()
    query = "SELECT * FROM questao"
    df = pd.read_sql(query, conn)
    df.to_csv('questoes_exportadas.csv', index=False)
    conn.close()
    messagebox.showinfo("Sucesso", "Questões exportadas com sucesso!")

# Interface gráfica
root = tk.Tk()
root.title("Gerenciar Conteúdos e Questões")

# Controles para Conteúdos
tk.Label(root, text="Nome do Conteúdo:").grid(row=0, column=0)
tk.Label(root, text="Descrição:").grid(row=1, column=0)
tk.Label(root, text="ID Série:").grid(row=2, column=0)
tk.Label(root, text="ID Bimestre:").grid(row=3, column=0)
tk.Label(root, text="ID Disciplina:").grid(row=4, column=0)
tk.Label(root, text="ID Conteúdo (para Exclusão/Modificação):").grid(row=5, column=0)

entry_nome_conteudo = tk.Entry(root)
entry_descricao = tk.Entry(root)
entry_id_serie = tk.Entry(root)
entry_id_bimestre = tk.Entry(root)
entry_id_disciplina = tk.Entry(root)
entry_id_conteudo = tk.Entry(root)

entry_nome_conteudo.grid(row=0, column=1)
entry_descricao.grid(row=1, column=1)
entry_id_serie.grid(row=2, column=1)
entry_id_bimestre.grid(row=3, column=1)
entry_id_disciplina.grid(row=4, column=1)
entry_id_conteudo.grid(row=5, column=1)

tk.Button(root, text="Adicionar Conteúdo", command=add_conteudo).grid(row=6, columnspan=2)
tk.Button(root, text="Excluir Conteúdo", command=delete_conteudo).grid(row=7, columnspan=2)
tk.Button(root, text="Atualizar Conteúdo", command=update_conteudo).grid(row=8, columnspan=2)

# Controles para Questões
tk.Label(root, text="Enunciado:").grid(row=9, column=0)
tk.Label(root, text="Tipo de Questão:").grid(row=10, column=0)
tk.Label(root, text="ID Conteúdo (para Questão):").grid(row=11, column=0)
tk.Label(root, text="ID Questão (para Exclusão/Modificação):").grid(row=12, column=0)

entry_enunciado = tk.Entry(root)
entry_tipo_questao = tk.Entry(root)
entry_id_conteudo_questao = tk.Entry(root)
entry_id_questao = tk.Entry(root)

entry_enunciado.grid(row=9, column=1)
entry_tipo_questao.grid(row=10, column=1)
entry_id_conteudo_questao.grid(row=11, column=1)
entry_id_questao.grid(row=12, column=1)

tk.Button(root, text="Adicionar Questão", command=add_questao).grid(row=13, columnspan=2)
tk.Button(root, text="Excluir Questão", command=delete_questao).grid(row=14, columnspan=2)
tk.Button(root, text="Atualizar Questão", command=update_questao).grid(row=15, columnspan=2)
tk.Button(root, text="Exportar Questões", command=export_questoes).grid(row=16, columnspan=2)

root.mainloop()





