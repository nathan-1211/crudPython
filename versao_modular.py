import sqlite3
def conectar():
    con = sqlite3.connect("escola.db")
    cur = con.cursor()
    return con, cur

def criar_tabela():
    con, cur = conectar()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS alunos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        idade INTEGER
    )
    """)
    con.commit()
    con.close()

def inserir_aluno():
    con, cur = conectar()

    nome = input("Digite o nome do aluno: ").strip()
    if nome == "":
        print("Nome não pode ser vazio!")
        return

    try:
        idade = int(input("Digite a idade: "))
    except ValueError:
        print("Idade inválida!")
        return

    try:
        cur.execute("INSERT INTO alunos (nome, idade) VALUES (?, ?)", (nome, idade))
        con.commit()
        print("Aluno cadastrado com sucesso!")
    except Exception as erro:
        print("Erro ao inserir:", erro)
    finally:
        con.close()

def listar_alunos():
    con, cur = conectar()

    try:
        cur.execute("SELECT * FROM alunos")
        dados = cur.fetchall()

        if len(dados) == 0:
            print("Nenhum aluno cadastrado.")
        else:
            print("\nLISTA DE ALUNOS:")
            for linha in dados:
                print(f"ID: {linha[0]} | Nome: {linha[1]} | Idade: {linha[2]}")
            print()
    except Exception as erro:
        print("Erro ao listar:", erro)
    finally:
        con.close()

def atualizar_aluno():
    con, cur = conectar()

    try:
        id_aluno = int(input("Digite o ID do aluno que deseja atualizar: "))
    except ValueError:
        print("ID inválido!")
        return

    novo_nome = input("Digite o novo nome: ").strip()
    if novo_nome == "":
        print("Nome não pode ser vazio!")
        return

    try:
        nova_idade = int(input("Digite a nova idade: "))
    except ValueError:
        print("Idade inválida!")
        return

    try:
        cur.execute(
            "UPDATE alunos SET nome = ?, idade = ? WHERE id = ?",
            (novo_nome, nova_idade, id_aluno)
        )
        con.commit()

        if cur.rowcount == 0:
            print("ID não encontrado.")
        else:
            print("Aluno atualizado com sucesso!")
    except Exception as erro:
        print("Erro ao atualizar:", erro)
    finally:
        con.close()

def deletar_aluno():
    con, cur = conectar()

    try:
        id_aluno = int(input("Digite o ID do aluno para deletar: "))
    except ValueError:
        print("ID inválido!")
        return

    try:
        cur.execute("DELETE FROM alunos WHERE id = ?", (id_aluno,))
        con.commit()

        if cur.rowcount == 0:
            print("ID não encontrado.")
        else:
            print("Aluno deletado com sucesso!")
    except Exception as erro:
        print("Erro ao deletar:", erro)
    finally:
        con.close()

def menu():
    criar_tabela()  # garante que exista antes de tudo

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
            inserir_aluno()
        elif opcao == "2":
            listar_alunos()
        elif opcao == "3":
            atualizar_aluno()
        elif opcao == "4":
            deletar_aluno()
        elif opcao == "5":
            print("Encerrando programa...")
            break
        else:
            print("Opção inválida! Tente novamente.")
menu()
