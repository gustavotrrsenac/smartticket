from flask import Blueprint, jsonify
from models import Usuario, PerfilEspecialista
from datetime import datetime

admin_bp = Blueprint("admin", __name__)

# --------------------------------------------------------
# LISTAR USUÁRIOS QUE SOLICITARAM SER ESPECIALISTAS
# --------------------------------------------------------
@admin_bp.get("/admin/especialistas/pendentes")
def listar_pendentes():
    pendentes = Usuario.select().where(
        Usuario.role == "cliente"
    )

    return jsonify([
        {
            "id": u.id,
            "nome": u.nome,
            "email": u.email,
            "telefone": u.telefone,
            "criado_em": u.criado_em.isoformat() if u.criado_em else None
        }
        for u in pendentes
    ]), 200


# --------------------------------------------------------
# DETALHES DO USUÁRIO A SER PROMOVIDO A ESPECIALISTA
# --------------------------------------------------------
@admin_bp.get("/admin/especialistas/<string:user_id>/detalhes")
def detalhes_especialista(user_id):
    user = Usuario.get_or_none(Usuario.id == user_id)

    if not user:
        return jsonify({"success": False, "message": "Usuário não encontrado"}), 404

    perfil = PerfilEspecialista.get_or_none(PerfilEspecialista.user == user)

    return jsonify({
        "success": True,
        "usuario": {
            "id": user.id,
            "nome": user.nome,
            "email": user.email,
            "telefone": user.telefone,
            "criado_em": user.criado_em.isoformat() if user.criado_em else None
        },
        "perfil": {
            "area_profissional": perfil.area_profissional if perfil else None,
            "formacao": perfil.formacao if perfil else None,
            "registro_prof": perfil.registro_prof if perfil else None,
        }
    }), 200


# --------------------------------------------------------
# ADMIN APROVA O ESPECIALISTA
# --------------------------------------------------------
@admin_bp.post("/admin/especialistas/<string:user_id>/aprovar")
def aprovar_especialista(user_id):
    user = Usuario.get_or_none(Usuario.id == user_id)

    if not user:
        return jsonify({"success": False, "message": "Usuário não encontrado"}), 404

    user.role = "especialista"
    user.atualizado_em = datetime.now()
    user.save()

    return jsonify({
        "success": True,
        "message": "Especialista aprovado com sucesso"
    }), 200
