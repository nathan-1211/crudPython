import sqlite3

con = sqlite3.connect("escola.db")
cur = con.cursor()

print("Conectado ao banco!")

cur.execute("""
CREATE TABLE IF NOT EXISTS alunos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    idade INTEGER
)
""")
con.commit()
print('Tabela criada')

"""
cur.execute(
    "INSERT INTO alunos (nome, idade) VALUES (?, ?)",  #o (?, ?) é responsavel pela seguranca dos dados
    ("Nathan", 24)
)
cur.execute(
    "INSERT INTO alunos (nome, idade) VALUES (?, ?)",
    ("Felipe", 18)
)
cur.execute(
    "INSERT INTO alunos (nome, idade) VALUES (?, ?)",
    ("Carlos", 20)
)

con.commit()
print('Tabela atualizada')
"""
print("Lista completa de alunos: ")
cur.execute("SELECT * FROM alunos")
dados = cur.fetchall() #Tambem pode ser fetchone() para uma linha por vez ou fetchmany(n) para porcoes de linhas
print(dados)
print()

#Podemos quebrar em linhas
cur.execute("SELECT * FROM alunos")
dados = cur.fetchall()
for linha in dados:
    print(linha)
print()

cur.execute(
    "UPDATE alunos SET nome = ?, idade = ? WHERE id = ?",
    ("Vinicius", 25, 4)
)
con.commit()
print('Tabela atualizada')


cur.execute("DELETE FROM alunos WHERE id = ?",
            (5,)
)
con.commit()
print('Registro deletado com sucesso!')


cur.close()
con.close()
print("Conexao encerrada")