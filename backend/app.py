from flask import Flask, request, jsonify, render_template
from models import db, Usuario, Ticket, DocumentoEspecialista
from uuid import uuid4
from datetime import datetime
import re

app = Flask(__name__)

@app.before_request
def _db_connect():
    if db.is_closed():
        db.connect()

@app.teardown_request
def _db_close(exc):
    if not db.is_closed():
        db.close()



@app.route('/')
def index():
    return render_template('index.html')


# VALIDAÇÕES
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

# ROTAS DE USUÁRIOS
@app.post("/usuarios")
def criar_usuario():
    try:
        data = request.json
        
        # Campos obrigatórios
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

        # Validar role
        if role not in ['cliente', 'especialista', 'admin']:
            return jsonify({
                'success': False,
                'message': 'Role deve ser: cliente, especialista ou admin'
            }), 400

        # Validar email
        if not validar_email(email):
            return jsonify({
                'success': False,
                'message': 'Formato de email inválido'
            }), 400

        # Validar senha
        senha_valida, msg_senha = validar_senha(password)
        if not senha_valida:
            return jsonify({
                'success': False,
                'message': msg_senha
            }), 400

        # Verificar se email já existe
        if Usuario.select().where(Usuario.email == email).exists():
            return jsonify({
                'success': False,
                'message': 'Já existe um usuário com este email'
            }), 409

        # Definir status de aprovação
        status_aprovacao = 'aprovado'  # Default para clientes e admin
        if role == 'especialista':
            status_aprovacao = 'aguardando_validacao'

        # Criar usuário
        user = Usuario.create(
            id=str(uuid4()),
            nome=nome,
            email=email,
            password_hash=password,  # Em produção, usar hash!
            role=role,
            status_aprovacao=status_aprovacao,
            telefone=telefone,
            foto_url=foto_url,
            criado_em=datetime.now()
        )

        response_data = {
            "success": True,
            "msg": "Usuário criado com sucesso", 
            "id": user.id,
            "status_aprovacao": status_aprovacao
        }

        # Mensagem específica para especialistas
        if role == 'especialista':
            response_data["msg"] = "Cadastro realizado! Seu perfil está em análise e você será notificado quando for aprovado."

        return jsonify(response_data), 201

    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Erro interno: {str(e)}'
        }), 500

@app.post("/especialistas")
def criar_especialista():
    try:
        data = request.json
        
        # Campos obrigatórios
        campos_obrigatorios = ['nome', 'email', 'password', 'documentos']
        for campo in campos_obrigatorios:
            if not data.get(campo):
                return jsonify({
                    'success': False,
                    'message': f'O campo {campo} é obrigatório'
                }), 400

        nome = data["nome"].strip()
        email = data["email"].strip().lower()
        password = data["password"]
        telefone = data.get("telefone")
        foto_url = data.get("foto_url")
        documentos = data["documentos"]

        # Validar email
        if not validar_email(email):
            return jsonify({
                'success': False,
                'message': 'Formato de email inválido'
            }), 400

        # Validar senha
        senha_valida, msg_senha = validar_senha(password)
        if not senha_valida:
            return jsonify({
                'success': False,
                'message': msg_senha
            }), 400

        # Validar documentos
        documentos_validos, msg_documentos = validar_documentos_especialista(documentos)
        if not documentos_validos:
            return jsonify({
                'success': False,
                'message': msg_documentos
            }), 400

        # Verificar se email já existe
        if Usuario.select().where(Usuario.email == email).exists():
            return jsonify({
                'success': False,
                'message': 'Já existe um usuário com este email'
            }), 409

        # Criar especialista com status pendente
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

            # Salvar documentos
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
        return jsonify({
            'success': False,
            'message': f'Erro interno: {str(e)}'
        }), 500

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
        }
        for u in usuarios
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
        }
        for u in especialistas
    ])
    
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
    
    
@app.post("/tickets/draft")
def gerar_ticket():
    try:
        data = request.json

        user_id = data.get("user_id")
        especialidade_id = data.get("especialidade_id")
        respostas = data.get("respostas_chat")
        titulo = data.get("titulo")

        # ─────────────────────────────────────────────
        # VALIDAÇÕES BÁSICAS
        # ─────────────────────────────────────────────
        if not user_id:
            return jsonify({"success": False, "message": "ID do usuário é obrigatório"}), 400
        
        if not especialidade_id:
            return jsonify({"success": False, "message": "Especialidade é obrigatória"}), 400
        
        if not respostas or not isinstance(respostas, list):
            return jsonify({"success": False, "message": "Respostas do chatbot são obrigatórias"}), 400

        # ─────────────────────────────────────────────
        # VALIDAR QUE O USUÁRIO EXISTE
        # ─────────────────────────────────────────────
        try:
            cliente = Usuario.get_by_id(user_id)
        except Usuario.DoesNotExist:
            return jsonify({"success": False, "message": "Usuário não encontrado"}), 404

        # ─────────────────────────────────────────────
        # MONTAR DESCRIÇÃO DO TICKET
        # ─────────────────────────────────────────────
        descricao = "\n".join(
            [f"- {r.get('pergunta')}: {r.get('resposta')}" for r in respostas]
        )

        # ─────────────────────────────────────────────
        # CRIAR RASCUNHO
        # ─────────────────────────────────────────────
        ticket = Ticket.create(
            id=str(uuid4()),
            cliente=cliente,
            especialista=None,
            triagem=None,
            titulo=titulo or "Ticket Gerado pelo Chatbot",
            descricao=descricao,
            status="rascunho"
        )


        return jsonify({
            "success": True,
            "message": "Rascunho gerado com sucesso!",
            "ticket": {
                "id": ticket.id,
                "titulo": ticket.titulo,
                "descricao": ticket.descricao,
                "status": ticket.status,
                "cliente": cliente.id,
                "especialidade_id": especialidade_id
            }
        }), 201

    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Erro ao gerar rascunho: {str(e)}"
        }), 500
        
@app.post("/tickets/send")
def enviar_ticket_para_fila():
    try:
        data = request.json
        
        ticket_id = data.get("ticket_id")
        especialidade_id = data.get("especialidade_id")

        # VALIDAR CAMPOS
        if not ticket_id:
            return jsonify({"success": False, "message": "ID do ticket é obrigatório"}), 400
        
        if not especialidade_id:
            return jsonify({"success": False, "message": "Especialidade é obrigatória"}), 400

        # VALIDAR QUE O TICKET EXISTE
        try:
            ticket = Ticket.get_by_id(ticket_id)
        except Ticket.DoesNotExist:
            return jsonify({"success": False, "message": "Ticket não encontrado"}), 404

        # O TICKET SÓ PODE SER ENVIADO SE ESTIVER EM RASCUNHO
        if ticket.status != "rascunho":
            return jsonify({
                "success": False,
                "message": "Este ticket já foi enviado ou já está em atendimento"
            }), 409

        # ATUALIZAR TICKET
        ticket.status = "pendente"
        ticket.especialidade_id = especialidade_id   # salva a fila correta
        ticket.enviado_em = datetime.now()
        ticket.save()

        return jsonify({
            "success": True,
            "message": "Ticket enviado para a fila com sucesso!",
            "ticket": {
                "id": ticket.id,
                "status": ticket.status,
                "especialidade_id": especialidade_id
            }
        }), 200

    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Erro ao enviar ticket: {str(e)}"
        }), 500       
        
        


    
    

if __name__ == "__main__":
    app.run(debug=True)
    
    