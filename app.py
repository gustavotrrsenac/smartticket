from flask import Flask, request, jsonify
from models import db, Usuario, Ticket, DocumentoEspecialista
from uuid import uuid4
from datetime import datetime
import re
import hashlib

app = Flask(__name__)

# Configuração do CORS (se necessário)
# from flask_cors import CORS
# CORS(app)

@app.before_request
def _db_connect():
    """Conecta ao banco antes de cada requisição."""
    if db.is_closed():
        db.connect()

@app.teardown_request
def _db_close(exc):
    """Fecha conexão após cada requisição."""
    if not db.is_closed():
        db.close()

# VALIDAÇÕES
def validar_email(email):
    """Valida formato de email."""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validar_senha(senha):
    """Valida força da senha."""
    if len(senha) < 6:
        return False, "A senha deve ter pelo menos 6 caracteres"
    
    # Verificar requisitos
    tem_minuscula = re.search(r'[a-z]', senha)
    tem_maiuscula = re.search(r'[A-Z]', senha)
    tem_especial = re.search(r'[^a-zA-Z0-9]', senha)
    tem_numero = re.search(r'\d', senha)
    
    if not all([tem_minuscula, tem_maiuscula, tem_especial, tem_numero]):
        return False, "A senha não atende a todos os requisitos de segurança"
    
    return True, ""

def validar_documentos_especialista(documentos):
    """Valida documentos obrigatórios para especialistas."""
    if not documentos:
        return False, "Documentos são obrigatórios para especialistas"
    
    tipos_obrigatorios = ['rg', 'cpf']
    tipos_enviados = [doc.get('tipo_documento') for doc in documentos]
    
    for tipo in tipos_obrigatorios:
        if tipo not in tipos_enviados:
            return False, f"Documento {tipo.upper()} é obrigatório"
    
    return True, ""

def hash_senha(senha):
    """Gera hash SHA-256 para senha."""
    return hashlib.sha256(senha.encode()).hexdigest()

# ROTAS DE USUÁRIOS
@app.post("/usuarios")
def criar_usuario():
    """Cria um novo usuário (cliente, especialista ou admin)."""
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

        # Criar hash da senha
        password_hash = hash_senha(password)

        # Criar usuário
        user = Usuario.create(
            id=str(uuid4()),
            nome=nome,
            email=email,
            password_hash=password_hash,
            role=role,
            status_aprovacao=status_aprovacao,
            telefone=telefone,
            foto_url=foto_url,
            criado_em=datetime.now(),
            atualizado_em=datetime.now()
        )

        response_data = {
            "success": True,
            "msg": "Usuário criado com sucesso", 
            "id": user.id,
            "nome": user.nome,
            "email": user.email,
            "role": user.role,
            "status_aprovacao": status_aprovacao
        }

        # Mensagem específica para especialistas
        if role == 'especialista':
            response_data["msg"] = "Cadastro realizado! Seu perfil está em análise."

        return jsonify(response_data), 201

    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Erro interno: {str(e)}'
        }), 500

@app.post("/especialistas")
def criar_especialista():
    """Cria um especialista com documentos."""
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

        # Criar hash da senha
        password_hash = hash_senha(password)

        # Criar especialista com transação
        with db.atomic():
            especialista = Usuario.create(
                id=str(uuid4()),
                nome=nome,
                email=email,
                password_hash=password_hash,
                role='especialista',
                status_aprovacao='aguardando_validacao',
                telefone=telefone,
                foto_url=foto_url,
                criado_em=datetime.now(),
                atualizado_em=datetime.now()
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
            "msg": "Cadastro de especialista realizado! Seu perfil está em análise.",
            "id": especialista.id,
            "nome": especialista.nome,
            "email": especialista.email,
            "status_aprovacao": "aguardando_validacao"
        }), 201

    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Erro interno: {str(e)}'
        }), 500

@app.get("/usuarios")
def listar_usuarios():
    """Lista todos os usuários."""
    usuarios = Usuario.select()
    return jsonify([
        {
            "id": u.id,
            "nome": u.nome,
            "email": u.email,
            "role": u.role,
            "status_aprovacao": u.status_aprovacao,
            "telefone": u.telefone,
            "criado_em": u.criado_em.isoformat() if u.criado_em else None
        }
        for u in usuarios
    ])

@app.get("/usuarios/<user_id>")
def obter_usuario(user_id):
    """Obtém um usuário específico."""
    try:
        usuario = Usuario.get_by_id(user_id)
        return jsonify({
            "id": usuario.id,
            "nome": usuario.nome,
            "email": usuario.email,
            "role": usuario.role,
            "status_aprovacao": usuario.status_aprovacao,
            "telefone": usuario.telefone,
            "foto_url": usuario.foto_url,
            "criado_em": usuario.criado_em.isoformat() if usuario.criado_em else None
        })
    except Usuario.DoesNotExist:
        return jsonify({
            "success": False,
            "message": "Usuário não encontrado"
        }), 404
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Erro interno: {str(e)}"
        }), 500

@app.get("/especialistas/pendentes")
def listar_especialistas_pendentes():
    """Lista especialistas aguardando aprovação."""
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

@app.put("/especialistas/<especialista_id>/aprovar")
def aprovar_especialista(especialista_id):
    """Aprova um especialista."""
    try:
        usuario = Usuario.get_by_id(especialista_id)
        
        if usuario.role != 'especialista':
            return jsonify({
                "success": False,
                "message": "Usuário não é um especialista"
            }), 400
        
        usuario.status_aprovacao = 'aprovado'
        usuario.atualizado_em = datetime.now()
        usuario.save()
        
        return jsonify({
            "success": True,
            "message": "Especialista aprovado com sucesso",
            "id": usuario.id,
            "nome": usuario.nome,
            "status_aprovacao": usuario.status_aprovacao
        })
        
    except Usuario.DoesNotExist:
        return jsonify({
            "success": False,
            "message": "Especialista não encontrado"
        }), 404
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Erro interno: {str(e)}"
        }), 500

# ROTAS DE TICKETS
@app.post("/tickets")
def criar_ticket():
    """Cria um novo ticket."""
    try:
        data = request.json
        
        campos_obrigatorios = ['titulo', 'cliente']
        for campo in campos_obrigatorios:
            if not data.get(campo):
                return jsonify({
                    'success': False,
                    'message': f'O campo {campo} é obrigatório'
                }), 400

        ticket = Ticket.create(
            id=str(uuid4()),
            titulo=data["titulo"],
            descricao=data.get("descricao"),
            cliente=data["cliente"],
            especialista=data.get("especialista"),
            triagem=data.get("triagem"),
            status=data.get("status", "aberto"),
            criado_em=datetime.now(),
            atualizado_em=datetime.now()
        )
        
        return jsonify({
            "success": True,
            "message": "Ticket criado",
            "id": ticket.id,
            "titulo": ticket.titulo,
            "status": ticket.status
        }), 201
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Erro interno: {str(e)}'
        }), 500

@app.post("/tickets/draft")
def gerar_rascunho_ticket():
    """Gera um rascunho de ticket a partir do chatbot."""
    try:
        data = request.json

        user_id = data.get("user_id")
        respostas = data.get("respostas_chat")
        titulo = data.get("titulo")

        # Validações
        if not user_id:
            return jsonify({"success": False, "message": "ID do usuário é obrigatório"}), 400

        if not respostas or not isinstance(respostas, list):
            return jsonify({"success": False, "message": "Respostas do chatbot são obrigatórias"}), 400

        # Montar descrição
        descricao = "\n".join(
            [f"- {r.get('pergunta')}: {r.get('resposta')}" for r in respostas]
        )

        # Criar ticket como rascunho
        ticket = Ticket.create(
            id=str(uuid4()),
            cliente=user_id,
            especialista=None,
            triagem=None,
            titulo=titulo if titulo else "Ticket Gerado pelo Chatbot",
            descricao=descricao,
            status="rascunho",
            criado_em=datetime.now(),
            atualizado_em=datetime.now()
        )

        return jsonify({
            "success": True,
            "message": "Rascunho gerado com sucesso!",
            "ticket": {
                "id": ticket.id,
                "titulo": ticket.titulo,
                "descricao": ticket.descricao,
                "status": ticket.status,
                "cliente": user_id,
                "criado_em": ticket.criado_em.isoformat()
            }
        }), 201

    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Erro ao gerar rascunho: {str(e)}"
        }), 500

@app.get("/tickets")
def listar_tickets():
    """Lista todos os tickets."""
    tickets = Ticket.select()
    return jsonify([
        {
            "id": t.id,
            "titulo": t.titulo,
            "descricao": t.descricao,
            "status": t.status,
            "cliente": t.cliente.id if t.cliente else None,
            "especialista": t.especialista.id if t.especialista else None,
            "triagem": t.triagem.id if t.triagem else None,
            "criado_em": t.criado_em.isoformat() if t.criado_em else None,
            "atualizado_em": t.atualizado_em.isoformat() if t.atualizado_em else None
        }
        for t in tickets
    ])

@app.get("/tickets/<ticket_id>")
def obter_ticket(ticket_id):
    """Obtém um ticket específico."""
    try:
        ticket = Ticket.get_by_id(ticket_id)
        
        return jsonify({
            "id": ticket.id,
            "titulo": ticket.titulo,
            "descricao": ticket.descricao,
            "status": ticket.status,
            "cliente": {
                "id": ticket.cliente.id,
                "nome": ticket.cliente.nome,
                "email": ticket.cliente.email
            } if ticket.cliente else None,
            "especialista": {
                "id": ticket.especialista.id,
                "nome": ticket.especialista.nome
            } if ticket.especialista else None,
            "criado_em": ticket.criado_em.isoformat() if ticket.criado_em else None,
            "atualizado_em": ticket.atualizado_em.isoformat() if ticket.atualizado_em else None
        })
        
    except Ticket.DoesNotExist:
        return jsonify({
            "success": False,
            "message": "Ticket não encontrado"
        }), 404
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Erro interno: {str(e)}"
        }), 500

@app.put("/tickets/<ticket_id>/status")
def atualizar_status_ticket(ticket_id):
    """Atualiza o status de um ticket."""
    try:
        data = request.json
        
        if not data.get("status"):
            return jsonify({
                "success": False,
                "message": "O campo status é obrigatório"
            }), 400
        
        ticket = Ticket.get_by_id(ticket_id)
        ticket.status = data["status"]
        ticket.atualizado_em = datetime.now()
        ticket.save()
        
        return jsonify({
            "success": True,
            "message": "Status atualizado",
            "id": ticket.id,
            "status": ticket.status
        })
        
    except Ticket.DoesNotExist:
        return jsonify({
            "success": False,
            "message": "Ticket não encontrado"
        }), 404
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Erro interno: {str(e)}"
        }), 500

# ROTA DE SAÚDE
@app.get("/health")
def health_check():
    """Verifica se a API está funcionando."""
    return jsonify({
        "status": "ok",
        "message": "API está funcionando",
        "timestamp": datetime.now().isoformat()
    })

if __name__ == "__main__":
    print("🚀 Servidor Flask iniciando...")
    print(f"📅 {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print("🌐 API disponível em: http://localhost:5000")
    app.run(debug=True, host="0.0.0.0", port=5000)