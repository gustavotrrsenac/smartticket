from flask import Flask, request, jsonify
from models import db, Usuario, Ticket
from uuid import uuid4
from datetime import datetime

app = Flask(__name__)

@app.before_request
def _db_connect():
    if db.is_closed():
        db.connect()

@app.teardown_request
def _db_close(exc):
    if not db.is_closed():
        db.close()


# ROTAS DE USUÁRIOS


@app.post("/usuarios")
def criar_usuario():
    data = request.json
    user = Usuario.create(
        id=str(uuid4()),
        nome=data["nome"],
        email=data["email"],
        password_hash=data["password"],
        role=data["role"],
        criado_em=datetime.now()
    )
    return jsonify({"msg": "Usuário criado", "id": user.id})


# ROTAS DE TICKETS


@app.post("/tickets")
def criar_ticket():
    data = request.json
    ticket = Ticket.create(
        id=str(uuid4()),
        titulo=data["titulo"],
        descricao=data["descricao"],
        criado_por=data["criado_por"],
        atribuido_para=data.get("atribuido_para"),
        criado_em=datetime.now()
    )
    return jsonify({"msg": "Ticket criado", "id": ticket.id})

@app.get("/tickets")
def listar_tickets():
    tickets = Ticket.select()
    return jsonify([
        {
            "id": t.id,
            "titulo": t.titulo,
            "status": t.status,
            "criado_por": t.criado_por.id,
            "atribuido_para": t.atribuido_para.id if t.atribuido_para else None
        }
        for t in tickets
    ])

if __name__ == "__main__":
    app.run(debug=True)
