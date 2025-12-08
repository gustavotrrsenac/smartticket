from flask import Flask, request, jsonify
from flask_cors import CORS
from uuid import uuid4
from datetime import datetime

# Importação das rotas existentes
from routes.indicadores_routes import indicadores_bp
from routes.routes_fila import fila_bp
from routes.admin_routes import admin_bp

# NOVAS ROTAS DO ESPECIALISTA (CORRETAS)
from routes.especialista_routes import especialista_bp

# Modelos
from models import Usuario, Ticket
from database import db

app = Flask(__name__)
CORS(app)


# ======================================
# Conexão automática com o banco
# ======================================
@app.before_request
def _db_connect():
    if db.is_closed():
        db.connect()

@app.teardown_request
def _db_close(exc):
    if not db.is_closed():
        db.close()


# ======================================
# Registro dos Blueprints
# ======================================
app.register_blueprint(indicadores_bp, url_prefix="/api")
app.register_blueprint(fila_bp, url_prefix="/api")
app.register_blueprint(admin_bp, url_prefix="/api")
app.register_blueprint(especialista_bp, url_prefix="/api")  # <---- ESSA É A NOVA ROTA DO ESPECIALISTA


# ======================================
# Validações auxiliares
# ======================================
def validar_senha(senha):
    if len(senha) < 6:
        return False, "A senha deve ter pelo menos 6 caracteres"
    return True, ""

def validar_email(email):
    return "@" in email and "." in email


# ======================================
# ROTAS DE USUÁRIOS
# ======================================
@app.post("/usuarios")
def criar_usuario():
    try:
        data = request.json

        campos_obrigatorios = ['nome', 'email', 'password', 'role']
        for campo in campos_obrigatorios:
            if not data.get(campo):
                return jsonify({
                    'success': False,
                    'message': f'O campo {campo} é obrigatório'
                }), 400

        nome = data["nome"].strip()
        email = data["email"].strip().lower()
        password = data["password"]
        role = data["role"]
        telefone = data.get("telefone")
        foto_url = data.get("foto_url")

        if role not in ['cliente', 'especialista', 'admin']:
            return jsonify({'success': False, 'message': 'Role inválida'}), 400

        if not validar_email(email):
            return jsonify({'success': False, 'message': 'Email inválido'}), 400

        senha_valida, msg_senha = validar_senha(password)
        if not senha_valida:
            return jsonify({'success': False, 'message': msg_senha}), 400

        if Usuario.select().where(Usuario.email == email).exists():
            return jsonify({'success': False, 'message': 'Email já cadastrado'}), 409

        user = Usuario.create(
            id=str(uuid4()),
            nome=nome,
            email=email,
            password_hash=password,
            role=role,
            telefone=telefone,
            foto_url=foto_url,
            criado_em=datetime.now()
        )

        return jsonify({
            "success": True,
            "message": "Usuário criado com sucesso",
            "id": user.id
        }), 201

    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


@app.get("/usuarios")
def listar_usuarios():
    usuarios = Usuario.select()
    return jsonify([
        {
            "id": u.id,
            "nome": u.nome,
            "email": u.email,
            "role": u.role,
            "criado_em": u.criado_em.isoformat() if u.criado_em else None
        }
        for u in usuarios
    ])


# ======================================
# ROTAS DE TICKETS
# ======================================
@app.post("/tickets")
def criar_ticket():
    try:
        data = request.json

        if not data.get("cliente"):
            return jsonify({"success": False, "message": "cliente é obrigatório"}), 400

        ticket = Ticket.create(
            id=str(uuid4()),
            cliente=data["cliente"],
            especialista=None,
            triagem=None,
            titulo=data.get("titulo", "Sem título"),
            descricao=data.get("descricao"),
            status="aberto",
            criado_em=datetime.now()
        )

        return jsonify({
            "success": True,
            "message": "Ticket criado",
            "id": ticket.id
        }), 201

    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


@app.get("/tickets")
def listar_tickets():
    tickets = Ticket.select()
    return jsonify([
        {
            "id": t.id,
            "titulo": t.titulo,
            "status": t.status,
            "cliente": t.cliente.id
        }
        for t in tickets
    ])


# ======================================
# ROTA HOME
# ======================================
@app.route("/")
def home():
    return {"msg": "API SmartTicket rodando"}


# ======================================
# EXECUÇÃO
# ======================================
if __name__ == "__main__":
    print("Rotas registradas:")
    print(app.url_map)
    print("API Rodando com Fila do Especialista e Admin ativado")
    app.run(debug=True)
