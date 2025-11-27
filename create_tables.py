from models import (
    Usuario,
    PerfilCliente,
    PerfilEspecialista,
    Admin,
    Triagem,
    PerguntaTriagem,
    TriagemResposta,
    Ticket,
    Mensagem
)
from database import db

def create_tables():
    with db:
        db.create_tables([
            Usuario,
            PerfilCliente,
            PerfilEspecialista,
            Admin,
            Triagem,
            PerguntaTriagem,
            TriagemResposta,
            Ticket,
            Mensagem
        ])
        print("Todas as tabelas foram criadas com sucesso! 🎉")

if __name__ == "__main__":
    create_tables()
