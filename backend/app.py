from flask import Flask, request, jsonify
from models import db, Usuario, Ticket, DocumentoEspecialista, Caso
from uuid import uuid4
from datetime import datetime
import re
import json
import os

# --- LLM ---
from google import genai
from google.genai import types
from pydantic import BaseModel, Field

# --- 1. CONFIGURAÇÃO DA LLM (Pydantic Schema) ---
class TriageOutput(BaseModel):
    area_problema: str = Field(description="Categoria principal do problema")
    fatos_chave: str = Field(description="Resumo conciso de 1-2 frases dos fatos mais relevantes")
    urgencia: str = Field(description="Classificação da urgência: Alta, Média ou Baixa")

def call_llm_api(user_message):
    """Chama a Gemini API para triagem estruturada."""
    try:
        if not os.getenv("GEMINI_API_KEY"):
            raise ValueError("A variável GEMINI_API_KEY não está configurada.")
        
        client = genai.Client()
        system_prompt = (
            "Você é um sistema de triagem inteligente. Sua única função é analisar a mensagem "
            "do usuário e extrair as informações solicitadas no formato JSON exato."
        )

        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=user_message,
            config=types.GenerateContentConfig(
                system_instruction=system_prompt,
                response_mime_type="application/json",
                response_schema=TriageOutput,
            ),
        )

        return json.loads(response.text)
    except Exception as e:
        print(f"❌ ERRO LLM: {e}")
        return None

# --- FLASK ---
app = Flask(__name__)

@app.before_request
def _db_connect():
    if db.is_closed():
        db.connect()

@app.teardown_request
def _db_close(exc):
    if not db.is_closed():
        db.close()

# --- VALIDAÇÕES ---
def validar_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validar_senha(senha):
    if len(senha) < 6:
        return False, "A senha deve ter pelo menos 6 caracteres"
    return True, ""

def validar_documentos_especialista(documentos):
    if not documentos:
        return False, "Documentos são obrigatórios para especialistas"
    tipos_obrigatorios = ['rg', 'cpf']
    tipos_enviados = [doc.get('tipo_documento') for doc in documentos]
    for tipo in tipos_obrigatorios:
        if tipo not in tipos_enviados:
            return False, f"Documento {tipo.upper()} é obrigatório"
    return True, ""

# --- ROTAS DE USUÁRIOS ---
@app.post("/usuarios")
def criar_usuario():
    try:
        data = request.json
        campos_obrigatorios = ['nome', 'email', 'password', 'role']
        for campo in campos_obrigatorios:
            if not data.get(campo):
                return jsonify({'success': False, 'message': f'O campo {campo} é obrigatório'}), 400

        nome = data["nome"].strip()
        email = data["email"].strip().lower()
        password = data["password"]
        role = data["role"]
        telefone = data.get("telefone")
        foto_url = data.get("foto_url")

        if role not in ['cliente', 'especialista', 'admin']:
            return jsonify({'success': False, 'message': 'Role deve ser: cliente, especialista ou admin'}), 400
        if not validar_email(email):
            return jsonify({'success': False, 'message': 'Formato de email inválido'}), 400
        senha_valida, msg_senha = validar_senha(password)
        if not senha_valida:
            return jsonify({'success': False, 'message': msg_senha}), 400
        if Usuario.select().where(Usuario.email == email).exists():
            return jsonify({'success': False, 'message': 'Já existe um usuário com este email'}), 409

        status_aprovacao = 'aprovado' if role != 'especialista' else 'aguardando_validacao'

        user = Usuario.create(
            id=str(uuid4()),
            nome=nome,
            email=email,
            password_hash=password,
            role=role,
            status_aprovacao=status_aprovacao,
            telefone=telefone,
            foto_url=foto_url,
            criado_em=datetime.now()
        )

        response_data = {
            "success": True,
            "msg": "Usuário criado com sucesso" if role != 'especialista' else
                   "Cadastro realizado! Seu perfil está em análise e você será notificado quando for aprovado.",
            "id": user.id,
            "status_aprovacao": status_aprovacao
        }
        return jsonify(response_data), 201

    except Exception as e:
        return jsonify({'success': False, 'message': f'Erro interno: {str(e)}'}), 500

@app.post("/especialistas")
def criar_especialista():
    try:
        data = request.json
        campos_obrigatorios = ['nome', 'email', 'password', 'documentos']
        for campo in campos_obrigatorios:
            if not data.get(campo):
                return jsonify({'success': False, 'message': f'O campo {campo} é obrigatório'}), 400

        nome = data["nome"].strip()
        email = data["email"].strip().lower()
        password = data["password"]
        telefone = data.get("telefone")
        foto_url = data.get("foto_url")
        documentos = data["documentos"]

        if not validar_email(email):
            return jsonify({'success': False, 'message': 'Formato de email inválido'}), 400
        senha_valida, msg_senha = validar_senha(password)
        if not senha_valida:
            return jsonify({'success': False, 'message': msg_senha}), 400
        documentos_validos, msg_documentos = validar_documentos_especialista(documentos)
        if not documentos_validos:
            return jsonify({'success': False, 'message': msg_documentos}), 400
        if Usuario.select().where(Usuario.email == email).exists():
            return jsonify({'success': False, 'message': 'Já existe um usuário com este email'}), 409

        with db.atomic():
            especialista = Usuario.create(
                id=str(uuid4()),
                nome=nome,
                email=email,
                password_hash=password,
                role='especialista',
                status_aprovacao='aguardando_validacao',
                telefone=telefone,
                foto_url=foto_url,
                criado_em=datetime.now()
            )
            for doc_data in documentos:
                DocumentoEspecialista.create(
                    id=str(uuid4()),
                    especialista=especialista,
                    tipo_documento=doc_data['tipo_documento'],
                    arquivo_url=doc_data['arquivo_url'],
                    nome_arquivo=doc_data['nome_arquivo'],
                    criado_em=datetime.now()
                )

        return jsonify({
            "success": True,
            "msg": "Cadastro de especialista realizado! Seu perfil está em análise e você será notificado quando for aprovado.",
            "id": especialista.id,
            "status_aprovacao": "aguardando_validacao"
        }), 201

    except Exception as e:
        return jsonify({'success': False, 'message': f'Erro interno: {str(e)}'}), 500

@app.get("/usuarios")
def listar_usuarios():
    usuarios = Usuario.select()
    return jsonify([
        {
            "id": u.id,
            "nome": u.nome,
            "email": u.email,
            "role": u.role,
            "status_aprovacao": u.status_aprovacao,
            "criado_em": u.criado_em.isoformat() if u.criado_em else None
        } for u in usuarios
    ])

@app.get("/especialistas/pendentes")
def listar_especialistas_pendentes():
    especialistas = Usuario.select().where(
        (Usuario.role == 'especialista') &
        (Usuario.status_aprovacao == 'aguardando_validacao')
    )
    return jsonify([
        {
            "id": u.id,
            "nome": u.nome,
            "email": u.email,
            "telefone": u.telefone,
            "criado_em": u.criado_em.isoformat() if u.criado_em else None
        } for u in especialistas
    ])

# --- ROTAS DE TICKETS ---
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
        } for t in tickets
    ])

# --- ROTAS DE TRIAGEM CHAT COM LLM ---
@app.post("/triagem")
def triagem_chat():
    try:
        data = request.json
        mensagem = data.get("mensagem")
        criado_por_id = data.get("criado_por")

        if not mensagem or not criado_por_id:
            return jsonify({"success": False, "message": "Campos 'mensagem' e 'criado_por' são obrigatórios"}), 400

        resultado = call_llm_api(mensagem)
        if not resultado:
            return jsonify({"success": False, "message": "Erro na triagem"}), 500

        # Salva na fila de especialistas
        caso = Caso.create(
            id=str(uuid4()),
            area_problema=resultado.get("area_problema"),
            fatos_chave=resultado.get("fatos_chave"),
            urgencia=resultado.get("urgencia"),
            criado_por=criado_por_id,
            status='PENDENTE_ESPECIALISTA',
            criado_em=datetime.now()
        )

        return jsonify({
            "success": True,
            "msg": "Sua solicitação foi registrada e será analisada por um especialista."
        }), 201

    except Exception as e:
        return jsonify({"success": False, "message": f"Erro interno: {str(e)}"}), 500

@app.get("/casos/pendentes")
def listar_casos_pendentes():
    casos = Caso.select().where(Caso.status == 'PENDENTE_ESPECIALISTA')
    return jsonify([
        {
            "id": c.id,
            "area_problema": c.area_problema,
            "fatos_chave": c.fatos_chave,
            "urgencia": c.urgencia,
            "criado_por": c.criado_por,
            "criado_em": c.criado_em.isoformat()
        } for c in casos
    ])

# --- RUN ---
if __name__ == "__main__":
    app.run(debug=True)
