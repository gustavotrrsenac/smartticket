from flask import Blueprint, request, jsonify
from models import Ticket
from datetime import datetime

fila_bp = Blueprint("fila", __name__)


@fila_bp.get("/fila/<especialidade>")
def listar_fila(especialidade):
    tickets = Ticket.select().where(
        (Ticket.triagem == especialidade) &
        (Ticket.status == "aberto")
    )

    return jsonify([
        {
            "id": t.id,
            "titulo": t.titulo,
            "cliente": t.cliente.id
        }
        for t in tickets
    ])


@fila_bp.post("/fila/enfileirar")
def enviar_para_fila():
    data = request.json
    ticket_id = data.get("ticket_id")
    especialidade = data.get("especialidade")

    ticket = Ticket.get_or_none(Ticket.id == ticket_id)

    if not ticket:
        return jsonify({"success": False, "message": "Ticket não existe"}), 404

    ticket.triagem = especialidade
    ticket.status = "aberto"
    ticket.atualizado_em = datetime.now()
    ticket.save()

    return jsonify({"success": True, "message": "Ticket enviado para a fila"})
