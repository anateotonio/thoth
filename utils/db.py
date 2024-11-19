import psycopg2

DB_CONFIG = {
    "host": "localhost",  # Certifique-se de que o host esteja correto (localhost se estiver local)
    "port": "5432",       # Porta correta (5432 padrão do PostgreSQL)
    "database": "thothdb",  # Nome do banco de dados correto
    "user": "admin",      # Usuário configurado no Podman
    "password": "admin"   # Senha configurada no Podman
}


def get_db_connection():
    try:
        return psycopg2.connect(**DB_CONFIG)
    except Exception as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
        return None
