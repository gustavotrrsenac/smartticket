from flask import Blueprint, jsonify
from models import Ticket, Usuario

indicadores_bp = Blueprint("indicadores", __name__)


@indicadores_bp.get("/admin/indicadores")
def indicadores_admin():
    total_usuarios = Usuario.select().count()
    total_tickets = Ticket.select().count()

    abertos = Ticket.select().where(Ticket.status == "aberto").count()
    aguardando = Ticket.select().where(Ticket.status == "aguardando").count()
    em_atendimento = Ticket.select().where(Ticket.status == "em_atendimento").count()
    concluidos = Ticket.select().where(Ticket.status == "concluido").count()

    return jsonify({
        "success": True,
        "indicadores": {
            "usuarios": total_usuarios,
            "tickets_total": total_tickets,
            "abertos": abertos,
            "aguardando": aguardando,
            "em_atendimento": em_atendimento,
            "concluidos": concluidos
        }
    })
