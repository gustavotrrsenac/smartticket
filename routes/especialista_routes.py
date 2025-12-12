from flask import Blueprint, request, jsonify
from models import Usuario, Ticket, PerfilEspecialista, Mensagem
from uuid import uuid4
from datetime import datetime

especialista_bp = Blueprint("especialista", __name__, url_prefix="/especialista")

# =====================================================================
# 1. Especialista envia documentação (salva em PerfilEspecialista)
# =====================================================================
@especialista_bp.post("/<user_id>/documentos")
def enviar_documentos(user_id):
    data = request.json
    
    user = Usuario.get_or_none(Usuario.id == user_id)
    if not user:
        return jsonify({"success": False, "message": "Usuário não encontrado"}), 404
    
    perfil = PerfilEspecialista.get_or_none(PerfilEspecialista.user == user)
    if not perfil:
        perfil = PerfilEspecialista.create(
            id=str(uuid4()),
            user=user
        )

    perfil.area_profissional = data.get("area_profissional")
    perfil.bio = data.get("bio")
    perfil.formacao = data.get("formacao")
    perfil.registro_prof = data.get("registro_prof")
    perfil.save()

    return jsonify({"success": True, "message": "Documentação enviada e aguardando aprovação"}), 200


# =====================================================================
# 2. Especialista verifica status da validação
# =====================================================================
@especialista_bp.get("/<user_id>/validacao")
def status_validacao(user_id):
    user = Usuario.get_or_none(Usuario.id == user_id)
    if not user:
        return jsonify({"success": False, "message": "Usuário não encontrado"}), 404

    perfil = PerfilEspecialista.get_or_none(PerfilEspecialista.user == user)
    if not perfil:
        return jsonify({"success": False, "message": "Perfil não encontrado"}), 404
    
    return jsonify({
        "user_id": user_id,
        "area_profissional": perfil.area_profissional,
        "formacao": perfil.formacao,
        "registro_prof": perfil.registro_prof,
    }), 200


# =====================================================================
# 3. Listar tickets disponíveis para o especialista
# =====================================================================
@especialista_bp.get("/<user_id>/fila")
def fila_especialista(user_id):
    especialista = Usuario.get_or_none(Usuario.id == user_id)

    if not especialista:
        return jsonify({"success": False, "message": "Especialista não encontrado"}), 404

    tickets = Ticket.select().where(
        Ticket.status == "aguardando",
        Ticket.especialista.is_null(True)
    )

    return jsonify([
        {
            "id": t.id,
            "titulo": t.titulo,
            "descricao": t.descricao,
            "cliente": {
                "id": t.cliente.id,
                "nome": t.cliente.nome
            },
            "criado_em": t.criado_em.isoformat()
        }
        for t in tickets
    ]), 200


# =====================================================================
# 4. Especialista assume um ticket
# =====================================================================
@especialista_bp.post("/<user_id>/assumir/<ticket_id>")
def assumir_ticket(user_id, ticket_id):
    especialista = Usuario.get_or_none(Usuario.id == user_id)
    if not especialista:
        return jsonify({"success": False, "message": "Especialista não encontrado"}), 404

    ticket = Ticket.get_or_none(Ticket.id == ticket_id)
    if not ticket:
        return jsonify({"success": False, "message": "Ticket não encontrado"}), 404

    if ticket.especialista:
        return jsonify({"success": False, "message": "Ticket já está sendo atendido"}), 409

    ticket.especialista = especialista
    ticket.status = "em_atendimento"
    ticket.atualizado_em = datetime.now()
    ticket.save()

    return jsonify({"success": True, "message": "Ticket assumido com sucesso"}), 200


# =====================================================================
# 5. Enviar mensagens dentro do ticket
# =====================================================================
@especialista_bp.post("/<user_id>/mensagem/<ticket_id>")
def enviar_mensagem(user_id, ticket_id):
    data = request.json

    user = Usuario.get_or_none(Usuario.id == user_id)
    if not user:
        return jsonify({"success": False, "message": "Usuário não encontrado"}), 404

    ticket = Ticket.get_or_none(Ticket.id == ticket_id)
    if not ticket:
        return jsonify({"success": False, "message": "Ticket não encontrado"}), 404

    Mensagem.create(
        id=str(uuid4()),
        ticket=ticket,
        sender=user,
        mensagem=data.get("mensagem"),
        tipo="texto"
    )

    ticket.atualizado_em = datetime.now()
    ticket.save()

    return jsonify({"success": True, "message": "Mensagem enviada"}), 201


# =====================================================================
# 6. Especialista finaliza o ticket
# =====================================================================
@especialista_bp.post("/<user_id>/finalizar/<ticket_id>")
def finalizar_ticket(user_id, ticket_id):
    data = request.json
    resposta_final = data.get("resposta")

    user = Usuario.get_or_none(Usuario.id == user_id)
    if not user:
        return jsonify({"success": False, "message": "Usuário não encontrado"}), 404

    ticket = Ticket.get_or_none(Ticket.id == ticket_id)
    if not ticket:
        return jsonify({"success": False, "message": "Ticket não encontrado"}), 404

    Mensagem.create(
        id=str(uuid4()),
        ticket=ticket,
        sender=user,
        mensagem=f"[FINALIZAÇÃO]\n{resposta_final}",
        tipo="texto"
    )

    ticket.status = "concluido"
    ticket.atualizado_em = datetime.now()
    ticket.save()

    return jsonify({"success": True, "message": "Ticket finalizado"}), 200
