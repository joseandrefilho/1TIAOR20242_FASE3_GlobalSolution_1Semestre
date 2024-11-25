import oracledb
import os
from dotenv import load_dotenv

# Carrega as variáveis do arquivo .env
load_dotenv()

class DBConnection:
    def __init__(self):
        self.connection = None

    def __enter__(self):
        # Usa as variáveis de ambiente para configurar a conexão
        self.connection = oracledb.connect(
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            dsn=os.getenv("DB_DSN")
        )
        return self.connection

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.connection:
            self.connection.close()
