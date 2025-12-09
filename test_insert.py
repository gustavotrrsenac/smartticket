from models import Usuario
from database import db
from datetime import datetime
import uuid

db.connect()

print("=== Inserção 1 (original) ===")
try:
    novo1 = Usuario.create(
        id=str(uuid.uuid4()),
        nome="Teste",
        email="teste@example.com",
        password_hash="123",
        role="cliente",
        criado_em=datetime.now()
    )
    print("Inserido:", novo1.id)
except Exception as e:
    print("Erro na primeira inserção:", e)

print("\n=== Inserção 2 (nova) ===")
try:
    novo2 = Usuario.create(
        id=str(uuid.uuid4()),
        nome="Markin",
        email=f"markin{uuid.uuid4().hex[:5]}@teste.com",
        password_hash="senha123",
        role="cliente",
        criado_em=datetime.now()
    )
    print("Inserido:", novo2.id)
except Exception as e:
    print("Erro na segunda inserção:", e)

print("\n=== Consultando todos os usuários no banco ===")
try:
    usuarios = Usuario.select()
    for u in usuarios:
        print(f"- {u.id} | {u.nome} | {u.email} | criado em {u.criado_em}")
except Exception as e:
    print("Erro ao consultar:", e)

    
    print("\n=== Inserção 3 (nova) ===")
try:
    novo2 = Usuario.create(
        id=str(uuid.uuid4()),
        nome="Neymar",
        email=f"neymar{uuid.uuid4().hex[:5]}@teste.com",
        password_hash="senha456",
        role="cliente",
        criado_em=datetime.now()
    )
    print("Inserido:", novo3.id)
except Exception as e:
    print("Erro na segunda inserção:", e)

print("\n=== Consultando todos os usuários no banco ===")
try:
    usuarios = Usuario.select()
    for u in usuarios:
        print(f"- {u.id} | {u.nome} | {u.email} | criado em {u.criado_em}")
except Exception as e:
    print("Erro ao consultar:", e)

db.close()
