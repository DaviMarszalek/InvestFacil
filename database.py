# database.py
import sqlite3
import hashlib
from models import Imovel, Semana, Usuario

DB_NAME = 'investfacil.db'

def conectar():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn, conn.cursor()

def hash_senha(senha):
    return hashlib.sha256(senha.encode()).hexdigest()

def criar_tabelas():
    conn, cursor = conectar()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT, nome TEXT NOT NULL, cpf TEXT NOT NULL UNIQUE,
            contato TEXT, senha_hash TEXT NOT NULL
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS imoveis (
            id INTEGER PRIMARY KEY AUTOINCREMENT, nome TEXT NOT NULL, localizacao TEXT NOT NULL,
            preco_total REAL, quartos INTEGER, banheiros INTEGER, area TEXT, avaliacao TEXT
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS semanas (
            id INTEGER PRIMARY KEY AUTOINCREMENT, imovel_id INTEGER NOT NULL, numero INTEGER NOT NULL,
            periodo TEXT NOT NULL, preco REAL NOT NULL, proprietario_id INTEGER,
            FOREIGN KEY (imovel_id) REFERENCES imoveis (id),
            FOREIGN KEY (proprietario_id) REFERENCES usuarios (id)
        )
    ''')
    conn.commit()
    conn.close()

def popular_dados_iniciais():
    conn, cursor = conectar()
    cursor.execute("SELECT COUNT(id) FROM imoveis")
    if cursor.fetchone()[0] == 0:
        # 1. Criar os imóveis
        imoveis_data = [
            ("Petra Palace", "Rua dos Doces, 789, Gramado", 1200000.00, 4, 3, "150m²", "9.5 - Excelente"),
            ("ZenithPlace", "Avenida Principal, 123, Balneário Camboriú", 1500000.00, 5, 4, "200m²", "9.7 - Excelente"),
            ("Topázio Imperial Hotel", "Praia das Esmeraldas, 456, Salvador", 2000000.00, 6, 5, "250m²", "9.8 - Luxuoso")
        ]
        cursor.executemany("INSERT INTO imoveis (nome, localizacao, preco_total, quartos, banheiros, area, avaliacao) VALUES (?, ?, ?, ?, ?, ?, ?)", imoveis_data)
        conn.commit()

        # 2. Gerar e inserir as semanas para cada imóvel
        cursor.execute("SELECT id, nome, preco_total, quartos, banheiros, area, avaliacao, localizacao FROM imoveis")
        imoveis_db = cursor.fetchall()
        
        for imovel_row in imoveis_db:
            imovel_obj = Imovel(**dict(imovel_row)) # Cria objeto para gerar semanas
            
            semanas_para_inserir = []
            for semana_obj in imovel_obj.semanas:
                semanas_para_inserir.append((imovel_obj.id, semana_obj.numero, semana_obj.periodo, semana_obj.preco))
            
            cursor.executemany("INSERT INTO semanas (imovel_id, numero, periodo, preco) VALUES (?, ?, ?, ?)", semanas_para_inserir)
        conn.commit()
    conn.close()

# --- Funções de Usuário ---
def adicionar_usuario(nome, cpf, contato, senha):
    conn, cursor = conectar()
    try:
        cursor.execute("INSERT INTO usuarios (nome, cpf, contato, senha_hash) VALUES (?, ?, ?, ?)",
                       (nome, cpf, contato, hash_senha(senha)))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def verificar_usuario(cpf, senha):
    conn, cursor = conectar()
    cursor.execute("SELECT id, nome, cpf FROM usuarios WHERE cpf = ? AND senha_hash = ?", (cpf, hash_senha(senha)))
    user_data = cursor.fetchone()
    conn.close()
    if user_data:
        return Usuario(id_usuario=user_data['id'], nome=user_data['nome'], cpf=user_data['cpf'], senha='')
    return None

def buscar_usuario_por_cpf(cpf):
    conn, cursor = conectar()
    cursor.execute("SELECT * FROM usuarios WHERE cpf = ?", (cpf,))
    user_data = cursor.fetchone()
    conn.close()
    return user_data

# --- Funções de Imóvel e Semana ---
def buscar_imoveis():
    conn, cursor = conectar()
    cursor.execute("SELECT * FROM imoveis")
    return [Imovel(**dict(row)) for row in cursor.fetchall()]

def buscar_semanas_por_imovel(imovel_id):
    conn, cursor = conectar()
    query = """
        SELECT s.*, u.nome as dono_nome
        FROM semanas s
        LEFT JOIN usuarios u ON s.proprietario_id = u.id
        WHERE s.imovel_id = ?
        ORDER BY s.numero
    """
    cursor.execute(query, (imovel_id,))
    return cursor.fetchall()

def buscar_investimentos_usuario(usuario_id):
    conn, cursor = conectar()
    query = """
        SELECT i.nome as imovel_nome, s.numero, s.periodo, s.preco, s.id as semana_id
        FROM semanas s
        JOIN imoveis i ON s.imovel_id = i.id
        WHERE s.proprietario_id = ?
        ORDER BY i.nome, s.numero
    """
    cursor.execute(query, (usuario_id,))
    return cursor.fetchall()

def comprar_semana(semana_id, usuario_id):
    conn, cursor = conectar()
    # Verifica se a semana ainda está disponível
    cursor.execute("SELECT proprietario_id FROM semanas WHERE id = ?", (semana_id,))
    proprietario = cursor.fetchone()
    if proprietario and proprietario['proprietario_id'] is not None:
        conn.close()
        return False # Semana já tem dono
        
    cursor.execute("UPDATE semanas SET proprietario_id = ? WHERE id = ?", (usuario_id, semana_id))
    conn.commit()
    conn.close()
    return True

def vender_semana(semana_id):
    conn, cursor = conectar()
    cursor.execute("UPDATE semanas SET proprietario_id = NULL WHERE id = ?", (semana_id,))
    conn.commit()
    conn.close()