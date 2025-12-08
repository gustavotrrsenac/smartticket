from flask import Flask, request, jsonify
from flask_cors import CORS
from models import db, Usuario, Ticket, DocumentoEspecialista, PerfilEspecialista
from uuid import uuid4
from datetime import datetime
import re
import hashlib

app = Flask(__name__)
CORS(app)  # Habilita CORS para todas as rotas

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
            return jsonify({
                'success': False,
                'message': 'Role deve ser: cliente, especialista ou admin'
            }), 400

        if not validar_email(email):
            return jsonify({
                'success': False,
                'message': 'Formato de email inválido'
            }), 400

        senha_valida, msg_senha = validar_senha(password)
        if not senha_valida:
            return jsonify({
                'success': False,
                'message': msg_senha
            }), 400

        if Usuario.select().where(Usuario.email == email).exists():
            return jsonify({
                'success': False,
                'message': 'Já existe um usuário com este email'
            }), 409

        status_aprovacao = 'aprovado'
        if role == 'especialista':
            status_aprovacao = 'aguardando_validacao'

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

        # Se for especialista, criar perfil
        if role == 'especialista':
            area_profissional = data.get('area_profissional')
            bio = data.get('bio')
            formacao = data.get('formacao')
            registro_prof = data.get('registro_prof')
            
            PerfilEspecialista.create(
                id=str(uuid4()),
                user=user,
                area_profissional=area_profissional,
                bio=bio,
                formacao=formacao,
                registro_prof=registro_prof,
                rating=0.00,
                criado_em=datetime.now()
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

        if role == 'especialista':
            response_data["msg"] = "Cadastro realizado! Seu perfil está em análise."

        return jsonify(response_data), 201

    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Erro interno: {str(e)}'
        }), 500

# ROTAS ESPECÍFICAS PARA ESPECIALISTAS
@app.post("/especialistas")
def criar_especialista_com_documentos():
    """Cria um especialista com documentos."""
    try:
        data = request.json
        
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
        
        # Dados do perfil
        area_profissional = data.get("area_profissional")
        bio = data.get("bio")
        formacao = data.get("formacao")
        registro_prof = data.get("registro_prof")

        if not validar_email(email):
            return jsonify({
                'success': False,
                'message': 'Formato de email inválido'
            }), 400

        senha_valida, msg_senha = validar_senha(password)
        if not senha_valida:
            return jsonify({
                'success': False,
                'message': msg_senha
            }), 400

        documentos_validos, msg_documentos = validar_documentos_especialista(documentos)
        if not documentos_validos:
            return jsonify({
                'success': False,
                'message': msg_documentos
            }), 400

        if Usuario.select().where(Usuario.email == email).exists():
            return jsonify({
                'success': False,
                'message': 'Já existe um usuário com este email'
            }), 409

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

            # Criar perfil do especialista
            PerfilEspecialista.create(
                id=str(uuid4()),
                user=especialista,
                area_profissional=area_profissional,
                bio=bio,
                formacao=formacao,
                registro_prof=registro_prof,
                rating=0.00,
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

@app.get("/especialistas")
def listar_especialistas():
    """Lista todos os especialistas."""
    try:
        especialistas = Usuario.select().where(Usuario.role == 'especialista')
        
        resultados = []
        for especialista in especialistas:
            perfil = PerfilEspecialista.get_or_none(user=especialista)
            
            especialista_data = {
                "id": especialista.id,
                "nome": especialista.nome,
                "email": especialista.email,
                "telefone": especialista.telefone,
                "status_aprovacao": especialista.status_aprovacao,
                "criado_em": especialista.criado_em.isoformat() if especialista.criado_em else None
            }
            
            if perfil:
                especialista_data.update({
                    "area_profissional": perfil.area_profissional,
                    "bio": perfil.bio,
                    "formacao": perfil.formacao,
                    "registro_prof": perfil.registro_prof,
                    "rating": float(perfil.rating) if perfil.rating else 0.0
                })
            
            resultados.append(especialista_data)
        
        return jsonify(resultados)
        
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Erro ao listar especialistas: {str(e)}"
        }), 500

@app.get("/especialistas/<especialista_id>")
def obter_especialista(especialista_id):
    """Obtém um especialista específico com documentos."""
    try:
        especialista = Usuario.get_by_id(especialista_id)
        
        if especialista.role != 'especialista':
            return jsonify({
                "success": False,
                "message": "Usuário não é um especialista"
            }), 400
        
        perfil = PerfilEspecialista.get_or_none(user=especialista)
        documentos = DocumentoEspecialista.select().where(
            DocumentoEspecialista.especialista == especialista
        )
        
        dados_especialista = {
            "id": especialista.id,
            "nome": especialista.nome,
            "email": especialista.email,
            "telefone": especialista.telefone,
            "foto_url": especialista.foto_url,
            "status_aprovacao": especialista.status_aprovacao,
            "criado_em": especialista.criado_em.isoformat() if especialista.criado_em else None
        }
        
        if perfil:
            dados_especialista.update({
                "area_profissional": perfil.area_profissional,
                "bio": perfil.bio,
                "formacao": perfil.formacao,
                "registro_prof": perfil.registro_prof,
                "rating": float(perfil.rating) if perfil.rating else 0.0
            })
        
        dados_especialista["documentos"] = [
            {
                "id": doc.id,
                "tipo_documento": doc.tipo_documento,
                "nome_arquivo": doc.nome_arquivo,
                "arquivo_url": doc.arquivo_url,
                "criado_em": doc.criado_em.isoformat() if doc.criado_em else None
            }
            for doc in documentos
        ]
        
        return jsonify(dados_especialista)
        
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

@app.get("/especialistas/pendentes")
def listar_especialistas_pendentes():
    """Lista especialistas aguardando aprovação."""
    especialistas = Usuario.select().where(
        (Usuario.role == 'especialista') & 
        (Usuario.status_aprovacao == 'aguardando_validacao')
    )
    
    resultados = []
    for especialista in especialistas:
        perfil = PerfilEspecialista.get_or_none(user=especialista)
        
        dados = {
            "id": especialista.id,
            "nome": especialista.nome,
            "email": especialista.email,
            "telefone": especialista.telefone,
            "criado_em": especialista.criado_em.isoformat() if especialista.criado_em else None
        }
        
        if perfil:
            dados.update({
                "area_profissional": perfil.area_profissional,
                "formacao": perfil.formacao
            })
        
        resultados.append(dados)
    
    return jsonify(resultados)

@app.put("/especialistas/<especialista_id>/aprovar")
def aprovar_especialista(especialista_id):
    """Aprova um especialista."""
    try:
        especialista = Usuario.get_by_id(especialista_id)
        
        if especialista.role != 'especialista':
            return jsonify({
                "success": False,
                "message": "Usuário não é um especialista"
            }), 400
        
        especialista.status_aprovacao = 'aprovado'
        especialista.atualizado_em = datetime.now()
        especialista.save()
        
        return jsonify({
            "success": True,
            "message": "Especialista aprovado com sucesso",
            "id": especialista.id,
            "nome": especialista.nome,
            "status_aprovacao": especialista.status_aprovacao
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

@app.put("/especialistas/<especialista_id>/rejeitar")
def rejeitar_especialista(especialista_id):
    """Rejeita um especialista."""
    try:
        especialista = Usuario.get_by_id(especialista_id)
        
        if especialista.role != 'especialista':
            return jsonify({
                "success": False,
                "message": "Usuário não é um especialista"
            }), 400
        
        especialista.status_aprovacao = 'rejeitado'
        especialista.atualizado_em = datetime.now()
        especialista.save()
        
        return jsonify({
            "success": True,
            "message": "Especialista rejeitado",
            "id": especialista.id,
            "nome": especialista.nome,
            "status_aprovacao": especialista.status_aprovacao
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

@app.put("/especialistas/<especialista_id>/atualizar-rating")
def atualizar_rating_especialista(especialista_id):
    """Atualiza o rating de um especialista."""
    try:
        data = request.json
        
        if 'rating' not in data:
            return jsonify({
                "success": False,
                "message": "O campo rating é obrigatório"
            }), 400
        
        rating = float(data['rating'])
        
        if rating < 0 or rating > 5:
            return jsonify({
                "success": False,
                "message": "Rating deve estar entre 0 e 5"
            }), 400
        
        especialista = Usuario.get_by_id(especialista_id)
        
        if especialista.role != 'especialista':
            return jsonify({
                "success": False,
                "message": "Usuário não é um especialista"
            }), 400
        
        perfil = PerfilEspecialista.get(user=especialista)
        perfil.rating = rating
        perfil.save()
        
        return jsonify({
            "success": True,
            "message": "Rating atualizado com sucesso",
            "id": especialista.id,
            "nome": especialista.nome,
            "rating": float(perfil.rating)
        })
        
    except Usuario.DoesNotExist:
        return jsonify({
            "success": False,
            "message": "Especialista não encontrado"
        }), 404
    except PerfilEspecialista.DoesNotExist:
        return jsonify({
            "success": False,
            "message": "Perfil do especialista não encontrado"
        }), 404
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Erro interno: {str(e)}"
        }), 500

# ROTAS DE USUÁRIOS (mantenha as existentes)
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

# ROTAS DE TICKETS (mantenha as existentes)
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
    print("🔓 CORS habilitado")
    app.run(debug=True, host="0.0.0.0", port=5000)