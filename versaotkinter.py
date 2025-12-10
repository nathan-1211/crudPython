import sqlite3
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

DB_NAME = "escola.db"


# ======================================================================
# BANCO DE DADOS
# ======================================================================

def conectar():
    return sqlite3.connect(DB_NAME)


def criar_tabela():
    with conectar() as con:
        cur = con.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS alunos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                idade INTEGER NOT NULL
            )
        """)


def inserir_aluno_db(nome, idade):
    with conectar() as con:
        cur = con.cursor()
        cur.execute(
            "INSERT INTO alunos (nome, idade) VALUES (?, ?)",
            (nome, idade)
        )
        return cur.lastrowid


def listar_alunos_db():
    with conectar() as con:
        cur = con.cursor()
        cur.execute("SELECT * FROM alunos")
        return cur.fetchall()


def atualizar_aluno_db(id_aluno, nome, idade):
    with conectar() as con:
        cur = con.cursor()
        cur.execute(
            "UPDATE alunos SET nome=?, idade=? WHERE id=?",
            (nome, idade, id_aluno)
        )
        return cur.rowcount


def deletar_aluno_db(id_aluno):
    with conectar() as con:
        cur = con.cursor()
        cur.execute("DELETE FROM alunos WHERE id=?", (id_aluno,))
        return cur.rowcount


# ======================================================================
# INTERFACE TKINTER
# ======================================================================

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Cadastro de Alunos")
        self.root.geometry("600x400")

        criar_tabela()

        # Campos
        self.lbl_nome = tk.Label(root, text="Nome:")
        self.lbl_nome.pack()
        self.entry_nome = tk.Entry(root, width=40)
        self.entry_nome.pack()

        self.lbl_idade = tk.Label(root, text="Idade:")
        self.lbl_idade.pack()
        self.entry_idade = tk.Entry(root, width=10)
        self.entry_idade.pack()

        # Botões
        self.btn_inserir = tk.Button(root, text="Inserir", command=self.inserir)
        self.btn_inserir.pack(pady=4)

        self.btn_atualizar = tk.Button(root, text="Atualizar", command=self.atualizar)
        self.btn_atualizar.pack(pady=4)

        self.btn_deletar = tk.Button(root, text="Deletar", command=self.deletar)
        self.btn_deletar.pack(pady=4)

        # Lista (TreeView)
        self.tree = ttk.Treeview(root, columns=("ID", "Nome", "Idade"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Nome", text="Nome")
        self.tree.heading("Idade", text="Idade")
        self.tree.pack(expand=True, fill="both", pady=10)

        # Evento quando clica na tabela
        self.tree.bind("<<TreeviewSelect>>", self.on_select)

        # Carrega dados
        self.carregar_dados()

    # ------------------------------------------------------------------
    def carregar_dados(self):
        """Atualiza lista na tela"""
        for row in self.tree.get_children():
            self.tree.delete(row)

        for aluno in listar_alunos_db():
            self.tree.insert("", tk.END, values=aluno)

    # ------------------------------------------------------------------
    def on_select(self, event):
        """Carrega os dados do aluno selecionado nos campos."""
        item = self.tree.selection()
        if not item:
            return

        aluno = self.tree.item(item)["values"]

        self.entry_nome.delete(0, tk.END)
        self.entry_nome.insert(0, aluno[1])

        self.entry_idade.delete(0, tk.END)
        self.entry_idade.insert(0, aluno[2])

    # ------------------------------------------------------------------
    def inserir(self):
        nome = self.entry_nome.get().strip()
        idade = self.entry_idade.get().strip()

        if nome == "":
            messagebox.showerror("Erro", "Nome não pode ser vazio.")
            return

        if not idade.isdigit():
            messagebox.showerror("Erro", "Idade inválida.")
            return

        inserir_aluno_db(nome, int(idade))
        self.carregar_dados()
        messagebox.showinfo("Sucesso", "Aluno inserido!")

        self.entry_nome.delete(0, tk.END)
        self.entry_idade.delete(0, tk.END)

    # ------------------------------------------------------------------
    def atualizar(self):
        item = self.tree.selection()
        if not item:
            messagebox.showwarning("Aviso", "Selecione um aluno.")
            return

        aluno = self.tree.item(item)["values"]
        aluno_id = aluno[0]

        nome = self.entry_nome.get().strip()
        idade = self.entry_idade.get().strip()

        if nome == "":
            messagebox.showerror("Erro", "Nome não pode ser vazio.")
            return

        if not idade.isdigit():
            messagebox.showerror("Erro", "Idade inválida.")
            return

        atualizar_aluno_db(aluno_id, nome, int(idade))
        self.carregar_dados()
        messagebox.showinfo("Sucesso", "Aluno atualizado!")

    # ------------------------------------------------------------------
    def deletar(self):
        item = self.tree.selection()
        if not item:
            messagebox.showwarning("Aviso", "Selecione um aluno.")
            return

        aluno = self.tree.item(item)["values"]
        aluno_id = aluno[0]

        if messagebox.askyesno("Confirmar", "Deseja realmente excluir?"):
            deletar_aluno_db(aluno_id)
            self.carregar_dados()
            messagebox.showinfo("Sucesso", "Aluno deletado!")


# ======================================================================
# EXECUÇÃO
# ======================================================================

if __name__ == "__main__":
    root = tk.Tk()
    App(root)
    root.mainloop()
