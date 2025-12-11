# test_connection.py
import os
from dotenv import load_dotenv
from peewee import MySQLDatabase

# Carrega o .env
load_dotenv()

print("=== TESTANDO CONEXÃO ===")
print(f"Usuário: {os.getenv('DB_USER')}")
print(f"Senha: {'(VAZIA)' if not os.getenv('DB_PASSWORD') else '***'}")
print(f"Database: {os.getenv('DB_NAME')}")

try:
    # Conecta sem criar tabelas ainda
    db = MySQLDatabase(
        os.getenv('DB_NAME'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD', ''),
        host=os.getenv('DB_HOST'),
        port=int(os.getenv('DB_PORT', 3306))
    )
    db.connect()
    print("✅ CONEXÃO BEM SUCEDIDA!")
    
    # Verifica se consegue executar um comando simples
    cursor = db.execute_sql('SELECT 1 as test')
    result = cursor.fetchone()
    print(f"✅ Query teste OK: {result}")
    
    db.close()
    print("✅ Conexão fechada normalmente")
    
except Exception as e:
    print(f"❌ ERRO: {e}")
    print("\n👉 SOLUÇÕES:")
    print("1. Verifique se o MySQL está rodando")
    print("2. Tente conectar no terminal: mysql -u root")
    print("3. Talvez precise redefinir senha do MySQL")