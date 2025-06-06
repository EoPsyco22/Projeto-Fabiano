import sqlite3

# Cria banco e tabela de usuários
def cria_db():
    conn = sqlite3.connect("bcodds.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            senha TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Insere um novo usuário
def entrar(nome, senha):
    conn = sqlite3.connect("bcodds.db")
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO usuarios (nome, senha) VALUES (?, ?)
    ''', (nome, senha))
    conn.commit()
    conn.close()

# Verifica login
def verificar_login(nome, senha):
    conn = sqlite3.connect("bcodds.db")
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM usuarios WHERE nome = ? AND senha = ?
    ''', (nome, senha))
    usuario = cursor.fetchone()
    conn.close()
    return usuario is not None

# Cria tabela de escolhas
def criar_tabela(nomeDB, nomeTabela):
    conn = sqlite3.connect(nomeDB)
    cursor = conn.cursor()
    cursor.execute(f'''
        CREATE TABLE IF NOT EXISTS {nomeTabela} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario TEXT NOT NULL,
            aula TEXT NOT NULL,
            dia TEXT NOT NULL,
            horario TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Salva escolha do usuário
def salvar_escolha(usuario, aula, dia, horarios):
    if isinstance(horarios, list):
        horarios = ", ".join(horarios)  # Converte lista para string

    conn = sqlite3.connect('bcodds.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO escolhas (usuario, aula, dia, horario)
        VALUES (?, ?, ?, ?)
    ''', (usuario, aula, dia, horarios))
    conn.commit()
    conn.close()

# Cria tabelas ao iniciar
cria_db()
criar_tabela("bcodds.db", "escolhas")