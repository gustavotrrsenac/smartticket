from flask import Blueprint, request, jsonify
from datetime import datetime
from models import Ticket, Usuario

fila_especialista_bp = Blueprint("fila_especialista", __name__)

# ------------------------------------------------------------
# 1. Enviar ticket para a fila do especialista
# ------------------------------------------------------------
@fila_especialista_bp.post("/tickets/<ticket_id>/enviar-fila")
def enviar_ticket_para_fila(ticket_id):
    data = request.json or {}
    especialista_id = data.get("especialista_id")

    if not especialista_id:
        return jsonify({"success": False, "message": "ID do especialista é obrigatório"}), 400

    ticket = Ticket.get_or_none(Ticket.id == ticket_id)
    especialista = Usuario.get_or_none(Usuario.id == especialista_id)

    if not ticket:
        return jsonify({"success": False, "message": "Ticket não encontrado"}), 404

    if not especialista:
        return jsonify({"success": False, "message": "Especialista não encontrado"}), 404

    if ticket.status != "pendente":
        return jsonify({
            "success": False,
            "message": "Ticket não está disponível para envio à fila"
        }), 409

    ticket.especialista = especialista
    ticket.status = "aguardando"
    ticket.atualizado_em = datetime.now()
    ticket.save()

    return jsonify({
        "success": True,
        "message": "Ticket enviado para a fila do especialista",
        "ticket_id": ticket.id
    }), 200


# ------------------------------------------------------------
# 2. Listar fila do especialista
# ------------------------------------------------------------
@fila_especialista_bp.get("/especialistas/<especialista_id>/fila")
def listar_fila_especialista(especialista_id):
    especialista = Usuario.get_or_none(Usuario.id == especialista_id)
    if not especialista:
        return jsonify({"success": False, "message": "Especialista não encontrado"}), 404

    tickets = Ticket.select().where(
        (Ticket.especialista == especialista) &
        (Ticket.status == "aguardando")
    )

    return jsonify([
        {
            "id": t.id,
            "titulo": t.titulo,
            "descricao": t.descricao,
            "status": t.status,
            "cliente": t.cliente.id,
            "atualizado_em": t.atualizado_em.isoformat() if t.atualizado_em else None
        }
        for t in tickets
    ]), 200


# ------------------------------------------------------------
# 3. Especialista assumir ticket
# ------------------------------------------------------------
@fila_especialista_bp.post("/tickets/<ticket_id>/assumir")
def assumir_ticket(ticket_id):
    data = request.json or {}
    especialista_id = data.get("especialista_id")

    ticket = Ticket.get_or_none(Ticket.id == ticket_id)
    if not ticket:
        return jsonify({"success": False, "message": "Ticket não encontrado"}), 404

    if not ticket.especialista or str(ticket.especialista.id) != str(especialista_id):
        return jsonify({"success": False, "message": "Ticket não pertence a este especialista"}), 403

    if ticket.status != "aguardando":
        return jsonify({
            "success": False,
            "message": "Ticket não pode ser assumido neste estado"
        }), 409

    ticket.status = "em_atendimento"
    ticket.atualizado_em = datetime.now()
    ticket.save()

    return jsonify({
        "success": True,
        "message": "Ticket assumido com sucesso",
        "ticket_id": ticket.id
    }), 200


# ------------------------------------------------------------
# 4. Finalizar atendimento
# ------------------------------------------------------------
@fila_especialista_bp.post("/tickets/<ticket_id>/finalizar")
def finalizar_ticket(ticket_id):
    data = request.json or {}
    especialista_id = data.get("especialista_id")

    ticket = Ticket.get_or_none(Ticket.id == ticket_id)
    if not ticket:
        return jsonify({"success": False, "message": "Ticket não encontrado"}), 404

    if not ticket.especialista or str(ticket.especialista.id) != str(especialista_id):
        return jsonify({"success": False, "message": "Ticket não pertence a este especialista"}), 403

    if ticket.status != "em_atendimento":
        return jsonify({
            "success": False,
            "message": "Ticket não está em atendimento"
        }), 409

    ticket.status = "concluido"
    ticket.atualizado_em = datetime.now()
    ticket.save()

    return jsonify({
        "success": True,
        "message": "Ticket concluído com sucesso",
        "ticket_id": ticket.id
    }), 200


# ------------------------------------------------------------
# 5. Listar atendimentos finalizados
# ------------------------------------------------------------
@fila_especialista_bp.get("/especialistas/<especialista_id>/finalizados")
def atendimentos_finalizados(especialista_id):
    especialista = Usuario.get_or_none(Usuario.id == especialista_id)
    if not especialista:
        return jsonify({"success": False, "message": "Especialista não encontrado"}), 404

    tickets = Ticket.select().where(
        (Ticket.especialista == especialista) &
        (Ticket.status == "concluido")
    )

    return jsonify([
        {
            "id": t.id,
            "titulo": t.titulo,
            "cliente": t.cliente.id,
            "finalizado_em": t.atualizado_em.isoformat() if t.atualizado_em else None
        }
        for t in tickets
    ]), 200


# ------------------------------------------------------------
# 6. Indicadores do especialista
# ------------------------------------------------------------
@fila_especialista_bp.get("/especialistas/<especialista_id>/indicadores")
def indicadores_especialista(especialista_id):
    especialista = Usuario.get_or_none(Usuario.id == especialista_id)
    if not especialista:
        return jsonify({"success": False, "message": "Especialista não encontrado"}), 404

    return jsonify({
        "success": True,
        "indicadores": {
            "total_recebidos": Ticket.select().where(Ticket.especialista == especialista).count(),
            "total_aguardando": Ticket.select().where(
                (Ticket.especialista == especialista) & (Ticket.status == "aguardando")
            ).count(),
            "total_em_atendimento": Ticket.select().where(
                (Ticket.especialista == especialista) & (Ticket.status == "em_atendimento")
            ).count(),
            "total_concluidos": Ticket.select().where(
                (Ticket.especialista == especialista) & (Ticket.status == "concluido")
            ).count(),
        }
    }), 200
