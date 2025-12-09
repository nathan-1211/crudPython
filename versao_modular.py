import sqlite3

DB_NAME = "escola.db"


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


# -----------------------------
#         MENU
# -----------------------------
def menu():
    criar_tabela()

    while True:
        print("""
1 - Inserir aluno
2 - Listar alunos
3 - Atualizar aluno
4 - Deletar aluno
5 - Sair
        """)

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            nome = input("Nome: ").strip()
            idade = int(input("Idade: "))

            if nome == "":
                print("Nome não pode ser vazio!")
                continue

            inserir_aluno_db(nome, idade)
            print("Aluno inserido!")

        elif opcao == "2":
            alunos = listar_alunos_db()

            if alunos:
                for a in alunos:
                    print(f"ID: {a[0]} | Nome: {a[1]} | Idade: {a[2]}")
            else:
                print("Nenhum aluno cadastrado.")

        elif opcao == "3":
            try:
                id_aluno = int(input("ID do aluno: "))
            except ValueError:
                print("ID inválido.")
                continue

            nome = input("Novo nome: ").strip()
            idade = int(input("Nova idade: "))

            linhas = atualizar_aluno_db(id_aluno, nome, idade)
            print("Atualizado!" if linhas else "ID não encontrado.")

        elif opcao == "4":
            try:
                id_aluno = int(input("ID para deletar: "))
            except ValueError:
                print("ID inválido.")
                continue

            linhas = deletar_aluno_db(id_aluno)
            print("Deletado!" if linhas else "ID não encontrado.")

        elif opcao == "5":
            print("Saindo...")
            break

        else:
            print("Opção inválida.")
menu()
