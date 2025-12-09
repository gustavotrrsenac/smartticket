from flask import Blueprint, request, jsonify
from models import Ticket, Usuario
from uuid import uuid4
from datetime import datetime




chat_tickets_bp = Blueprint("chat_tickets", __name__)

# ─────────────────────────────────────────────
# CRIAR TICKET DIRETO
# ─────────────────────────────────────────────
@chat_tickets_bp.post("/tickets")
def criar_ticket():
    data = request.json

    ticket = Ticket.create(
        id=str(uuid4()),
        titulo=data["titulo"],
        descricao=data["descricao"],
        criado_por=data["criado_por"],
        atribuido_para=data.get("atribuido_para"),
        criado_em=datetime.now()
    )

    return jsonify({
        "success": True,
        "msg": "Ticket criado",
        "id": ticket.id
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
            "criado_por": t.criado_por.id,
            "atribuido_para": t.atribuido_para.id if t.atribuido_para else None
        }
        for t in tickets
    ])


# ─────────────────────────────────────────────
# GERAR RASCUNHO PELO CHATBOT
# ─────────────────────────────────────────────
@chat_tickets_bp.post("/tickets/draft")
def gerar_ticket():
    try:
        data = request.json

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

        try:
            cliente = Usuario.get_by_id(user_id)
        except Usuario.DoesNotExist:
            return jsonify({"success": False, "message": "Usuário não encontrado"}), 404

        descricao = "\n".join(
            [f"- {r.get('pergunta')}: {r.get('resposta')}" for r in respostas]
        )

        ticket = Ticket.create(
            id=str(uuid4()),
            cliente=cliente,
            especialista=None,
            triagem=None,
            titulo=titulo or "Ticket Gerado pelo Chatbot",
            descricao=descricao,
            status="rascunho"
        )

        return jsonify({
            "success": True,
            "message": "Rascunho gerado com sucesso!",
            "ticket": {
                "id": ticket.id,
                "titulo": ticket.titulo,
                "descricao": ticket.descricao,
                "status": ticket.status,
                "cliente": cliente.id,
                "especialidade_id": especialidade_id
            }
        }), 201

    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Erro ao gerar rascunho: {str(e)}"
        }), 500


# ─────────────────────────────────────────────
# ENVIAR TICKET PARA FILA
# ─────────────────────────────────────────────
@chat_tickets_bp.post("/tickets/send")
def enviar_ticket_para_fila():
    try:
        data = request.json

        ticket_id = data.get("ticket_id")
        especialidade_id = data.get("especialidade_id")

        if not ticket_id:
            return jsonify({"success": False, "message": "ID do ticket é obrigatório"}), 400

        if not especialidade_id:
            return jsonify({"success": False, "message": "Especialidade é obrigatória"}), 400

        try:
            ticket = Ticket.get_by_id(ticket_id)
        except Ticket.DoesNotExist:
            return jsonify({"success": False, "message": "Ticket não encontrado"}), 404

        if ticket.status != "rascunho":
            return jsonify({
                "success": False,
                "message": "Este ticket já foi enviado ou já está em atendimento"
            }), 409

        ticket.status = "pendente"
        ticket.especialidade_id = especialidade_id
        ticket.enviado_em = datetime.now()
        ticket.save()

        return jsonify({
            "success": True,
            "message": "Ticket enviado para a fila com sucesso!",
            "ticket": {
                "id": ticket.id,
                "status": ticket.status,
                "especialidade_id": especialidade_id
            }
        }), 200

    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Erro ao enviar ticket: {str(e)}"
        }), 500
