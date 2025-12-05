from peewee import *
from database import db
import datetime

class BaseModel(Model):
    class Meta:
        database = db

class Usuario(BaseModel):
    id = CharField(primary_key=True, max_length=36)
    nome = CharField(max_length=150)
    email = CharField(max_length=150, unique=True)
    password_hash = TextField()
    role = CharField(choices=[
        ('cliente', 'Cliente'),
        ('especialista', 'Especialista'), 
        ('admin', 'Administrador')
    ])
    
    # Campo NOVO - usado no app.py
    status_aprovacao = CharField(
        choices=[
            ('aprovado', 'Aprovado'),
            ('aguardando_validacao', 'Aguardando Validação'),
            ('rejeitado', 'Rejeitado')
        ],
        default='aprovado'
    )
    
    foto_url = TextField(null=True)
    telefone = CharField(max_length=20, null=True)
    criado_em = DateTimeField(default=datetime.datetime.now)
    atualizado_em = DateTimeField(default=datetime.datetime.now)
    
    class Meta:
        table_name = 'usuarios'

class PerfilCliente(BaseModel):
    id = CharField(primary_key=True, max_length=36)
    user = ForeignKeyField(Usuario, backref='perfil_cliente', on_delete='CASCADE')
    telefone = CharField(max_length=20, null=True)
    criado_em = DateTimeField(default=datetime.datetime.now)
    
    class Meta:
        table_name = 'perfis_cliente'

class PerfilEspecialista(BaseModel):
    id = CharField(primary_key=True, max_length=36)
    user = ForeignKeyField(Usuario, backref='perfil_especialista', on_delete='CASCADE')
    area_profissional = CharField(max_length=30, null=True)
    bio = TextField(null=True)
    formacao = CharField(max_length=50, null=True)
    registro_prof = CharField(max_length=40, null=True)
    rating = DecimalField(max_digits=3, decimal_places=2, default=0.00)
    criado_em = DateTimeField(default=datetime.datetime.now)
    
    class Meta:
        table_name = 'perfis_especialista'

class Admin(BaseModel):
    id = CharField(primary_key=True, max_length=36)
    admin = ForeignKeyField(Usuario, backref='logs_admin', on_delete='CASCADE')
    acao = TextField()
    criado_em = DateTimeField(default=datetime.datetime.now)
    
    class Meta:
        table_name = 'admins'

class Triagem(BaseModel):
    id = CharField(primary_key=True, max_length=36)
    cliente = ForeignKeyField(Usuario, backref='triagens', on_delete='CASCADE')
    status_triagem_status = CharField(
        choices=[
            ('iniciada', 'Iniciada'),
            ('respondendo', 'Respondendo'),
            ('concluida', 'Concluída')
        ],
        default='iniciada'
    )
    resumo_problema = TextField(null=True)
    criado_em = DateTimeField(default=datetime.datetime.now)
    
    class Meta:
        table_name = 'triagens'

class PerguntaTriagem(BaseModel):
    id = CharField(primary_key=True, max_length=36)
    pergunta = TextField()
    resposta_padrao = TextField(null=True)
    categoria = CharField(max_length=30, null=True)
    ordem_pergunta = IntegerField(null=True)
    ativo = BooleanField(default=True)
    
    class Meta:
        table_name = 'perguntas_triagem'

class TriagemResposta(BaseModel):
    id = CharField(primary_key=True, max_length=36)
    triagem = ForeignKeyField(Triagem, backref='respostas', on_delete='CASCADE')
    pergunta_triagem = ForeignKeyField(PerguntaTriagem, backref='respostas', on_delete='CASCADE')
    resposta_cliente = TextField(null=True)
    respondido_em = DateTimeField(default=datetime.datetime.now)
    
    class Meta:
        table_name = 'triagens_respostas'

class Ticket(BaseModel):
    id = CharField(primary_key=True, max_length=36)
    
    # Relacionamentos
    cliente = ForeignKeyField(
        Usuario, 
        backref='tickets_cliente', 
        on_delete='CASCADE'
    )
    
    especialista = ForeignKeyField(
        Usuario, 
        backref='tickets_especialista',
        null=True,
        on_delete='SET NULL'
    )
    
    triagem = ForeignKeyField(
        Triagem,
        backref='ticket',
        null=True,
        on_delete='SET NULL'
    )
    
    # Campos básicos
    titulo = CharField(max_length=100)
    descricao = TextField(null=True)
    
    # Status atualizado com 'rascunho'
    status = CharField(
        choices=[
            ('rascunho', 'Rascunho'),
            ('aberto', 'Aberto'),
            ('aguardando', 'Aguardando'),
            ('em_atendimento', 'Em Atendimento'),
            ('concluido', 'Concluído')
        ],
        default='rascunho'
    )
    
    # Campos de data
    criado_em = DateTimeField(default=datetime.datetime.now)
    atualizado_em = DateTimeField(default=datetime.datetime.now)
    
    class Meta:
        table_name = 'tickets'

class Mensagem(BaseModel):
    id = CharField(primary_key=True, max_length=36)
    ticket = ForeignKeyField(Ticket, backref='mensagens', on_delete='CASCADE')
    sender = ForeignKeyField(Usuario, backref='mensagens', on_delete='CASCADE')
    mensagem = TextField()
    tipo = CharField(
        choices=[
            ('texto', 'Texto'),
            ('imagem', 'Imagem'),
            ('arquivo', 'Arquivo'),
            ('audio', 'Áudio')
        ],
        default='texto'
    )
    enviado_em = DateTimeField(default=datetime.datetime.now)
    
    class Meta:
        table_name = 'mensagens'

# Modelo NOVO - usado no app.py para documentos de especialistas
class DocumentoEspecialista(BaseModel):
    id = CharField(primary_key=True, max_length=36)
    especialista = ForeignKeyField(
        Usuario, 
        backref='documentos_especialista', 
        on_delete='CASCADE'
    )
    tipo_documento = CharField(max_length=50)  # 'rg', 'cpf', 'diploma', 'certificado'
    arquivo_url = TextField()
    nome_arquivo = CharField(max_length=255)
    criado_em = DateTimeField(default=datetime.datetime.now)
    
    class Meta:
        table_name = 'documentos_especialista'