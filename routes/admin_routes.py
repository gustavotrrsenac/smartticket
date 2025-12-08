from flask import Blueprint, jsonify, request
from models import Usuario, PerfilEspecialista
from uuid import uuid4
from datetime import datetime

admin_bp = Blueprint("admin", __name__)


# --------------------------------------------------------
# LISTAR ESPECIALISTAS QUE AINDA NÃO SÃO "especialista"
# --------------------------------------------------------
@admin_bp.get("/admin/especialistas/pendentes")
def listar_pendentes():
    pendentes = Usuario.select().where(
        Usuario.role == "cliente"
    )

    resultado = []
    for u in pendentes:
        resultado.append({
            "id": u.id,
            "nome": u.nome,
            "email": u.email,
            "telefone": u.telefone,
            "criado_em": u.criado_em.isoformat()
        })

    return jsonify(resultado), 200


# --------------------------------------------------------
# DETALHES DO USUÁRIO A SER PROMOVIDO A ESPECIALISTA
# --------------------------------------------------------
@admin_bp.get("/admin/especialistas/<id>/detalhes")
def detalhes_especialista(id):
    user = Usuario.get_or_none(Usuario.id == id)

    if not user:
        return jsonify({"error": "Usuário não encontrado"}), 404

    perfil = PerfilEspecialista.get_or_none(PerfilEspecialista.user == id)

    return jsonify({
        "id": user.id,
        "nome": user.nome,
        "email": user.email,
        "telefone": user.telefone,
        "perfil": {
            "area_profissional": perfil.area_profissional if perfil else None,
            "formacao": perfil.formacao if perfil else None,
            "registro_prof": perfil.registro_prof if perfil else None,
        }
    })


# --------------------------------------------------------
# ADMIN APROVA O ESPECIALISTA (ATUALIZA ROLE)
# --------------------------------------------------------
@admin_bp.post("/admin/especialistas/<id>/aprovar")
def aprovar_especialista(id):
    user = Usuario.get_or_none(Usuario.id == id)

    if not user:
        return jsonify({"error": "Usuário não encontrado"}), 404

    user.role = "especialista"
    user.atualizado_em = datetime.now()
    user.save()

    return jsonify({"success": True, "message": "Especialista aprovado"}), 200
