from database import db
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

def create_tables():
    """
    Cria todas as tabelas do banco usando Peewee.
    Esse script deve ser executado uma única vez para montar a estrutura inicial.
    """
    try:
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

    except Exception as e:
        print("Erro ao criar tabelas:", e)


if __name__ == "__main__":
    create_tables()
