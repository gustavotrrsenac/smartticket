from database import db
from models import (
    Usuario,
    PerfilCliente,
    PerfilEspecialista,
    PerguntaTriagem,
    Ticket,
    Triagem,
    TriagemResposta
)
import uuid


def create_seed_data():
    print("🌱 Iniciando SEED (dados de teste)...")

    try:
        with db.atomic():

            # --------------------------------------
            # Criar Usuários
            # --------------------------------------
            cliente_id = str(uuid.uuid4())
            especialista_id = str(uuid.uuid4())
            admin_id = str(uuid.uuid4())

            cliente = Usuario.create(
                id=cliente_id,
                nome="Cliente Teste",
                email="cliente@test.com",
                password_hash="123456",
                role="cliente",
                telefone="11 99999-0000"
            )

            especialista = Usuario.create(
                id=especialista_id,
                nome="Especialista Teste",
                email="especialista@test.com",
                password_hash="123456",
                role="especialista",
                telefone="11 88888-0000"
            )

            admin = Usuario.create(
                id=admin_id,
                nome="Administrador",
                email="admin@test.com",
                password_hash="123456",
                role="admin"
            )

            # --------------------------------------
            # Criar Perfis
            # --------------------------------------
            PerfilCliente.create(
                id=str(uuid.uuid4()),
                user=cliente,
                telefone="11 99999-0000"
            )

            perfil_especialista = PerfilEspecialista.create(
                id=str(uuid.uuid4()),
                user=especialista,
                area_profissional="Psicologia",
                bio="Especialista em atendimentos terapêuticos.",
                formacao="Psicologia - USP",
                registro_prof="CRP 123456"
            )

            # --------------------------------------
            # Perguntas da Triagem
            # --------------------------------------
            p1 = PerguntaTriagem.create(
                id=str(uuid.uuid4()),
                pergunta="Como você está se sentindo hoje?",
                categoria="emocional",
                ordem_pergunta=1
            )

            p2 = PerguntaTriagem.create(
                id=str(uuid.uuid4()),
                pergunta="Qual é a principal situação que está enfrentando?",
                categoria="situacao",
                ordem_pergunta=2
            )

            # --------------------------------------
            # Criar Triagem
            # --------------------------------------
            triagem = Triagem.create(
                id=str(uuid.uuid4()),
                cliente=cliente,
                status_triagem_status="concluida",
                resumo_problema="Ansiedade e dificuldade para dormir."
            )

            TriagemResposta.create(
                id=str(uuid.uuid4()),
                triagem=triagem,
                pergunta_triagem=p1,
                resposta_cliente="Estou ansioso."
            )

            TriagemResposta.create(
                id=str(uuid.uuid4()),
                triagem=triagem,
                pergunta_triagem=p2,
                resposta_cliente="Estresse no trabalho."
            )

            # --------------------------------------
            # Criar Ticket
            # --------------------------------------
            Ticket.create(
                id=str(uuid.uuid4()),
                cliente=cliente,
                especialista=especialista,
                triagem=triagem,
                titulo="Preciso de atendimento",
                descricao="Quero falar sobre ansiedade.",
                status="aberto"
            )

            print("🌱 SEED concluído com sucesso!")

    except Exception as e:
        print("❌ Erro ao executar seed:", e)


if __name__ == "__main__":
    create_seed_data()
