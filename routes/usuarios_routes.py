from flask import Blueprint, jsonify, request
from models import Usuario
from playhouse.shortcuts import model_to_dict
from uuid import uuid4
from datetime import datetime

usuarios_bp = Blueprint("usuarios", __name__)

# --------------------------------------------------------
# GET /usuarios
# Lista todos os usuários
# --------------------------------------------------------
@usuarios_bp.get("/usuarios")
def listar_usuarios():
    usuarios = Usuario.select()

    return jsonify([
        {
            "id": u.id,
            "nome": u.nome,
            "email": u.email,
            "role": u.role,
            "telefone": u.telefone,
            "status_aprovacao": u.status_aprovacao,
            "criado_em": u.criado_em.isoformat() if u.criado_em else None
        }
        for u in usuarios
    ]), 200


# --------------------------------------------------------
# GET /usuarios/<id>
# Busca usuário por ID
# --------------------------------------------------------
@usuarios_bp.get("/usuarios/<string:user_id>")
def buscar_usuario(user_id):
    usuario = Usuario.get_or_none(Usuario.id == user_id)

    if not usuario:
        return jsonify({
            "success": False,
            "message": "Usuário não encontrado"
        }), 404

    return jsonify({
        "success": True,
        "usuario": {
            "id": usuario.id,
            "nome": usuario.nome,
            "email": usuario.email,
            "role": usuario.role,
            "telefone": usuario.telefone,
            "status_aprovacao": usuario.status_aprovacao,
            "criado_em": usuario.criado_em.isoformat() if usuario.criado_em else None
        }
    }), 200


# --------------------------------------------------------
# POST /usuarios
# Criação de usuário
# --------------------------------------------------------
@usuarios_bp.post("/usuarios")
def criar_usuario():
    data = request.json or {}

    campos_obrigatorios = ["nome", "email", "password"]

    for campo in campos_obrigatorios:
        if not data.get(campo):
            return jsonify({
                "success": False,
                "message": f"O campo {campo} é obrigatório"
            }), 400

    # Verifica duplicidade de email
    if Usuario.select().where(Usuario.email == data["email"]).exists():
        return jsonify({
            "success": False,
            "message": "Já existe um usuário com este email"
        }), 409

    usuario = Usuario.create(
        id=str(uuid4()),
        nome=data["nome"].strip(),
        email=data["email"].lower().strip(),
        password_hash=data["password"],  # depois a gente faz hash
        role=data.get("role", "cliente"),
        telefone=data.get("telefone"),
        status_aprovacao="aprovado",
        criado_em=datetime.now()
    )

    return jsonify({
        "success": True,
        "message": "Usuário criado com sucesso",
        "usuario": {
            "id": usuario.id,
            "nome": usuario.nome,
            "email": usuario.email,
            "role": usuario.role
        }
    }), 201
