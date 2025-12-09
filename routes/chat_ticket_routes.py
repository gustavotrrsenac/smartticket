from flask import Flask, request, jsonify, render_template
from flask_login import LoginManager, login_required, current_user
from models import Usuario, Ticket, Mensagem
from uuid import uuid4
from datetime import datetime
from database import db

app = Flask(__name__)
app.secret_key = "sua-chave-secreta"

# ==============================
# Flask-Login
# ==============================
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


@login_manager.user_loader
def load_user(user_id):
    return Usuario.get_or_none(Usuario.id == user_id)


# ==============================
# Página do Chat (somente logado)
# ==============================
@app.route("/chat", methods=["GET"])
@login_required
def chat_page():
    return render_template("chat.html", usuario=current_user)


# ==============================
# API do Chat (somente logado)
# ==============================
@app.route("/chat/message", methods=["POST"])
@login_required
def chat_message():
    data = request.get_json()
    mensagem_texto = data.get("mensagem")

    if not mensagem_texto:
        return jsonify({"erro": "Mensagem é obrigatória"}), 400

    usuario = current_user

    # ==============================
    # Busca ticket em criação
    # ==============================
    ticket = Ticket.get_or_none(
        Ticket.cliente == usuario,
        Ticket.status == "em_criacao"
    )

    # Se não existir, cria um novo ticket inicial
    if not ticket:
        ticket = Ticket.create(
            id=str(uuid4()),
            cliente=usuario,
            status="em_criacao",
            passo=1,
            criado_em=datetime.now(),
            atualizado_em=datetime.now()
        )

    # ==============================
    # Salva mensagem do usuário
    # ==============================
    Mensagem.create(
        id=str(uuid4()),
        ticket=ticket,
        sender=usuario,
        mensagem=mensagem_texto,
        tipo="texto",
        enviado_em=datetime.now()
    )

    # ==============================
    # Fluxo do chat controlado pelo ticket
    # ==============================

    # PASSO 1 – Área
    if ticket.passo == 1:
        ticket.area = mensagem_texto
        ticket.passo = 2
        ticket.save()

        resposta = "Digite a descrição da sua dúvida:"

    # PASSO 2 – Descrição
    elif ticket.passo == 2:
        ticket.descricao = mensagem_texto
        ticket.passo = 3
        ticket.save()

        resposta = "Qual o nível de urgência? (baixa, média, alta)"

    # PASSO 3 – Urgência → finaliza ticket
    elif ticket.passo == 3:
        ticket.urgencia = mensagem_texto
        ticket.titulo = f"Dúvida - {ticket.area}"
        ticket.status = "aberto"
        ticket.atualizado_em = datetime.now()
        ticket.save()

        resposta = f"✅ Ticket criado com sucesso! ID: {ticket.id}"

    else:
        resposta = "✅ Seu ticket já foi criado. Aguarde atendimento."

    # ==============================
    # Salva resposta do bot
    # ==============================
    Mensagem.create(
        id=str(uuid4()),
        ticket=ticket,
        sender=usuario,  # futuramente pode ser um usuário BOT
        mensagem=resposta,
        tipo="texto",
        enviado_em=datetime.now()
    )

    return jsonify({"resposta": resposta})


# ==============================
# Inicialização
# ==============================
if __name__ == "__main__":
    db.connect()
    app.run(debug=True)
