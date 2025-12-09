from flask import Blueprint, request, jsonify
from models import Ticket, Usuario
from uuid import uuid4
from datetime import datetime

chat_tickets_bp = Blueprint("chat_tickets", __name__)

# ─────────────────────────────────────────────
# CRIAR TICKET DIRETO (FORA DO CHATBOT)
# ─────────────────────────────────────────────
@chat_tickets_bp.post("/tickets")
def criar_ticket():
    data = request.json or {}

    campos_obrigatorios = ["titulo", "descricao", "criado_por"]

    for campo in campos_obrigatorios:
        if not data.get(campo):
            return jsonify({
                "success": False,
                "message": f"O campo {campo} é obrigatório"
            }), 400

    # validar usuário criador
    criador = Usuario.get_or_none(Usuario.id == data["criado_por"])
    if not criador:
        return jsonify({
            "success": False,
            "message": "Usuário criador não encontrado"
        }), 404

    ticket = Ticket.create(
        id=str(uuid4()),
        titulo=data["titulo"],
        descricao=data["descricao"],
        criado_por=criador,
        atribuido_para=data.get("atribuido_para"),
        status="aberto",
        criado_em=datetime.now()
    )

    return jsonify({
        "success": True,
        "message": "Ticket criado com sucesso",
        "ticket_id": ticket.id
    }), 201


# ─────────────────────────────────────────────
# LISTAR TICKETS
# ─────────────────────────────────────────────
@chat_tickets_bp.get("/tickets")
def listar_tickets():
    tickets = Ticket.select()

    return jsonify([
        {
            "id": t.id,
            "titulo": t.titulo,
            "status": t.status,
            "criado_por": t.criado_por.id if t.criado_por else None,
            "atribuido_para": t.atribuido_para.id if t.atribuido_para else None
        }
        for t in tickets
    ]), 200


# ─────────────────────────────────────────────
# GERAR RASCUNHO PELO CHATBOT
# ─────────────────────────────────────────────
@chat_tickets_bp.post("/tickets/draft")
def gerar_ticket():
    data = request.json or {}

    user_id = data.get("user_id")
    especialidade_id = data.get("especialidade_id")
    respostas = data.get("respostas_chat")
    titulo = data.get("titulo")

    if not user_id:
        return jsonify({"success": False, "message": "ID do usuário é obrigatório"}), 400

    if not especialidade_id:
        return jsonify({"success": False, "message": "Especialidade é obrigatória"}), 400

    if not respostas or not isinstance(respostas, list):
        return jsonify({"success": False, "message": "Respostas do chatbot são obrigatórias"}), 400

    cliente = Usuario.get_or_none(Usuario.id == user_id)
    if not cliente:
        return jsonify({"success": False, "message": "Usuário não encontrado"}), 404

    descricao = "\n".join(
        [f"- {r.get('pergunta')}: {r.get('resposta')}" for r in respostas]
    )

    ticket = Ticket.create(
        id=str(uuid4()),
        cliente=cliente,
        especialista=None,
        titulo=titulo or "Ticket Gerado pelo Chatbot",
        descricao=descricao,
        status="rascunho",
        criado_em=datetime.now()
    )

    return jsonify({
        "success": True,
        "message": "Rascunho gerado com sucesso",
        "ticket": {
            "id": ticket.id,
            "status": ticket.status,
            "cliente": cliente.id,
            "especialidade_id": especialidade_id
        }
    }), 201


# ─────────────────────────────────────────────
# ENVIAR TICKET PARA FILA
# ─────────────────────────────────────────────
@chat_tickets_bp.post("/tickets/send")
def enviar_ticket_para_fila():
    data = request.json or {}

    ticket_id = data.get("ticket_id")
    especialidade_id = data.get("especialidade_id")

    if not ticket_id:
        return jsonify({"success": False, "message": "ID do ticket é obrigatório"}), 400

    if not especialidade_id:
        return jsonify({"success": False, "message": "Especialidade é obrigatória"}), 400

    ticket = Ticket.get_or_none(Ticket.id == ticket_id)
    if not ticket:
        return jsonify({"success": False, "message": "Ticket não encontrado"}), 404

    if ticket.status != "rascunho":
        return jsonify({
            "success": False,
            "message": "Este ticket já foi enviado ou está em atendimento"
        }), 409

    ticket.status = "pendente"
    ticket.especialidade_id = especialidade_id
    ticket.enviado_em = datetime.now()
    ticket.save()

    return jsonify({
        "success": True,
        "message": "Ticket enviado para a fila com sucesso",
        "ticket": {
            "id": ticket.id,
            "status": ticket.status
        }
    }), 200
