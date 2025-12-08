from flask import Blueprint, jsonify, request
from models import Usuario
from playhouse.shortcuts import model_to_dict
import uuid

usuarios_bp = Blueprint("usuarios", __name__)

# ---------------------------
#  GET /usuarios
#  Lista todos os usuários
# ---------------------------
@usuarios_bp.get("/usuarios")
def listar_usuarios():
    usuarios = [model_to_dict(u) for u in Usuario.select()]
    return jsonify(usuarios), 200

# ---------------------------
#  GET /usuarios/<id>
#  Busca um usuário específico
# ---------------------------
@usuarios_bp.get("/usuarios/<user_id>")
def buscar_usuario(user_id):
    usuario = Usuario.get_or_none(Usuario.id == user_id)
    if not usuario:
        return jsonify({"erro": "Usuário não encontrado"}), 404

    return jsonify(model_to_dict(usuario)), 200

# ---------------------------
#  POST /usuarios
#  Cria um novo usuário
# ---------------------------
@usuarios_bp.post("/usuarios")
def criar_usuario():
    dados = request.json

    try:
        novo = Usuario.create(
            id=str(uuid.uuid4()),
            nome=dados.get("nome"),
            email=dados.get("email"),
            password_hash=dados.get("password"),
            role=dados.get("role", "cliente"),
            telefone=dados.get("telefone")
        )
        return jsonify(model_to_dict(novo)), 201
    
    except Exception as e:
        return jsonify({"erro": str(e)}), 400
