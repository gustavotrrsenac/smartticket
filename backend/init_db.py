# init_db.py
# Executar este script antes de rodar app.py para garantir que o DB e as tabelas existam.

import os
from dotenv import load_dotenv

# CARREGA .env
load_dotenv()

# Para usar PyMySQL como driver MySQLdb
try:
    import pymysql
    pymysql.install_as_MySQLdb()
except Exception as e:
    print("Aviso: não foi possível instalar pymysql como MySQLdb — verifique o driver. Erro:", e)

# Agora importe o db e os models
from database import db
import models

# Conecta e cria tabelas
print("Tentando conectar ao DB...")
db.connect(reuse_if_open=True)
print("Conectado. Criando tabelas (se não existirem)...")

db.create_tables([
    models.Usuario,
    getattr(models, "PerfilCliente", None),
    getattr(models, "PerfilEspecialista", None),
    getattr(models, "Admin", None),
    getattr(models, "Triagem", None),
    getattr(models, "PerguntaTriagem", None),
    getattr(models, "TriagemResposta", None),
    getattr(models, "Ticket", None),
    getattr(models, "Mensagem", None),
])

print("Tabelas criadas/validadas com sucesso.")
db.close()
