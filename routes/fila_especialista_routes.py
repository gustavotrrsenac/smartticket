from flask import Blueprint, request, jsonify
from uuid import uuid4
from datetime import datetime
from models import Ticket, Usuario
from database import db

fila_especialista_bp = Blueprint("fila_especialista", __name__)


# ------------------------------------------------------------
# 1. Enviar ticket para a fila do especialista
# ------------------------------------------------------------
@fila_especialista_bp.post("/tickets/<ticket_id>/enviar-fila")
def enviar_ticket_para_fila(ticket_id):
    try:
        data = request.json
        especialista_id = data.get("especialista_id")

        if not especialista_id:
            return jsonify({"success": False, "message": "ID do especialista é obrigatório"}), 400

        ticket = Ticket.get_or_none(Ticket.id == ticket_id)
        especialista = Usuario.get_or_none(Usuario.id == especialista_id)

        if not ticket:
            return jsonify({"success": False, "message": "Ticket não encontrado"}), 404

        if not especialista:
            return jsonify({"success": False, "message": "Especialista não encontrado"}), 404

        ticket.especialista = especialista
        ticket.status = "aguardando"
        ticket.atualizado_em = datetime.now()
        ticket.save()

        return jsonify({
            "success": True,
            "message": "Ticket enviado para a fila do especialista",
            "ticket_id": ticket.id
        }), 200

    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


# ------------------------------------------------------------
# 2. Listar fila do especialista (status: aguardando)
# ------------------------------------------------------------
@fila_especialista_bp.get("/especialistas/<especialista_id>/fila")
def listar_fila_especialista(especialista_id):
    try:
        tickets = Ticket.select().where(
            (Ticket.especialista == especialista_id) &
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

    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


# ------------------------------------------------------------
# 3. Especialista assumir ticket
# ------------------------------------------------------------
@fila_especialista_bp.post("/tickets/<ticket_id>/assumir")
def assumir_ticket(ticket_id):
    try:
        data = request.json
        especialista_id = data.get("especialista_id")

        ticket = Ticket.get_or_none(Ticket.id == ticket_id)

        if not ticket:
            return jsonify({"success": False, "message": "Ticket não encontrado"}), 404

        if ticket.especialista.id != especialista_id:
            return jsonify({"success": False, "message": "Ticket não pertence a este especialista"}), 403

        ticket.status = "em_atendimento"
        ticket.atualizado_em = datetime.now()
        ticket.save()

        return jsonify({
            "success": True,
            "message": "Ticket assumido com sucesso",
            "ticket_id": ticket.id
        }), 200

    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


# ------------------------------------------------------------
# 4. Finalizar atendimento
# ------------------------------------------------------------
@fila_especialista_bp.post("/tickets/<ticket_id>/finalizar")
def finalizar_ticket(ticket_id):
    try:
        data = request.json
        especialista_id = data.get("especialista_id")

        ticket = Ticket.get_or_none(Ticket.id == ticket_id)

        if not ticket:
            return jsonify({"success": False, "message": "Ticket não encontrado"}), 404

        if ticket.especialista.id != especialista_id:
            return jsonify({"success": False, "message": "Ticket não pertence a este especialista"}), 403

        ticket.status = "concluido"
        ticket.atualizado_em = datetime.now()
        ticket.save()

        return jsonify({
            "success": True,
            "message": "Ticket concluído com sucesso",
            "ticket_id": ticket.id
        }), 200

    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


# ------------------------------------------------------------
# 5. Listar atendimentos finalizados
# ------------------------------------------------------------
@fila_especialista_bp.get("/especialistas/<especialista_id>/finalizados")
def atendimentos_finalizados(especialista_id):
    try:
        tickets = Ticket.select().where(
            (Ticket.especialista == especialista_id) &
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
        ])

    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


# ------------------------------------------------------------
# 6. Indicadores do especialista
# ------------------------------------------------------------
@fila_especialista_bp.get("/especialistas/<especialista_id>/indicadores")
def indicadores_especialista(especialista_id):
    try:
        total_recebidos = Ticket.select().where(Ticket.especialista == especialista_id).count()
        total_aguardando = Ticket.select().where(
            (Ticket.especialista == especialista_id) &
            (Ticket.status == "aguardando")
        ).count()
        total_em_atendimento = Ticket.select().where(
            (Ticket.especialista == especialista_id) &
            (Ticket.status == "em_atendimento")
        ).count()
        total_concluidos = Ticket.select().where(
            (Ticket.especialista == especialista_id) &
            (Ticket.status == "concluido")
        ).count()

        return jsonify({
            "success": True,
            "indicadores": {
                "total_recebidos": total_recebidos,
                "total_aguardando": total_aguardando,
                "total_em_atendimento": total_em_atendimento,
                "total_concluidos": total_concluidos
            }
        })

    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500
