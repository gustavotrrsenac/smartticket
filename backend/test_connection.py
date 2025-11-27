from models import Usuario
import uuid

try:
    novo = Usuario.create(
        id=str(uuid.uuid4()),
        nome="Teste",
        email="teste@example.com",
        password_hash="123",
        role="cliente"
    )
    print("Inserido:", novo.id)
except Exception as e:
    print("Erro:", e)
