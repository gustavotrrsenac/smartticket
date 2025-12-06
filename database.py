# database.py
from peewee import MySQLDatabase
import os
from dotenv import load_dotenv

load_dotenv()

# Use pymysql como driver
db = MySQLDatabase(
    database=os.getenv("DB_NAME", "smart_ticket"),
    user=os.getenv("DB_USER", "root"),
    password=os.getenv("DB_PASSWORD", "senac"),
    host=os.getenv("DB_HOST", "localhost"),
    port=int(os.getenv("DB_PORT", "3306")),
    charset='utf8mb4',
    autocommit=True,
    thread_safe=True
)

# Função para testar conexão
def test_connection():
    try:
        db.connect()
        print("✅ Conexão com MySQL estabelecida com sucesso!")
        db.close()
        return True
    except Exception as e:
        print(f"❌ Erro ao conectar ao MySQL: {e}")
        return False