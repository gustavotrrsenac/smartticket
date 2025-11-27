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
    role = CharField(choices=[('cliente', 'cliente'), ('especialista', 'especialista'), ('admin', 'admin')])
    foto_url = TextField(null=True)
    telefone = CharField(max_length=20, null=True)
    criado_em = DateTimeField(default=datetime.datetime.now)
    atualizado_em = DateTimeField(default=datetime.datetime.now)

class PerfilCliente(BaseModel):
    id = CharField(primary_key=True, max_length=36)
    user = ForeignKeyField(Usuario, backref='perfil_cliente', on_delete='CASCADE')
    telefone = CharField(max_length=20, null=True)
    criado_em = DateTimeField(default=datetime.datetime.now)

class PerfilEspecialista(BaseModel):
    id = CharField(primary_key=True, max_length=36)
    user = ForeignKeyField(Usuario, backref='perfil_especialista', on_delete='CASCADE')
    area_profissional = CharField(max_length=30, null=True)
    bio = TextField(null=True)
    formacao = CharField(max_length=50, null=True)
    registro_prof = CharField(max_length=40, null=True)
    rating = DecimalField(max_digits=3, decimal_places=2, default=0.00)
    criado_em = DateTimeField(default=datetime.datetime.now)

class Admin(BaseModel):
    id = CharField(primary_key=True, max_length=36)
    admin = ForeignKeyField(Usuario, backref='logs_admin', on_delete='CASCADE')
    acao = TextField()
    criado_em = DateTimeField(default=datetime.datetime.now)

class Triagem(BaseModel):
    id = CharField(primary_key=True, max_length=36)
    cliente = ForeignKeyField(Usuario, backref='triagens', on_delete='CASCADE')
    status_triagem_status = CharField(choices=[('iniciada', 'iniciada'), ('respondendo', 'respondendo'), ('concluida', 'concluida')], default='iniciada')
    resumo_problema = TextField(null=True)
    criado_em = DateTimeField(default=datetime.datetime.now)

class PerguntaTriagem(BaseModel):
    id = CharField(primary_key=True, max_length=36)
    pergunta = TextField()
    resposta_padrao = TextField(null=True)
    categoria = CharField(max_length=30, null=True)
    ordem_pergunta = IntegerField(null=True)
    ativo = BooleanField(default=True)

class TriagemResposta(BaseModel):
    id = CharField(primary_key=True, max_length=36)
    triagem = ForeignKeyField(Triagem, backref='respostas', on_delete='CASCADE')
    pergunta_triagem = ForeignKeyField(PerguntaTriagem, backref='respostas', on_delete='CASCADE')
    resposta_cliente = TextField(null=True)
    respondido_em = DateTimeField(default=datetime.datetime.now)

class Ticket(BaseModel):
    id = CharField(primary_key=True, max_length=36)
    cliente = ForeignKeyField(Usuario, backref='tickets_cliente', on_delete='CASCADE')
    especialista = ForeignKeyField(Usuario, backref='tickets_especialista', null=True, on_delete='SET NULL')
    triagem = ForeignKeyField(Triagem, backref='ticket', null=True, on_delete='SET NULL')
    titulo = CharField(max_length=100)
    descricao = TextField(null=True)
    status = CharField(choices=[('aberto','aberto'),('aguardando','aguardando'),('em_atendimento','em_atendimento'),('concluido','concluido')], default='aberto')
    criado_em = DateTimeField(default=datetime.datetime.now)
    atualizado_em = DateTimeField(default=datetime.datetime.now)

class Mensagem(BaseModel):
    id = CharField(primary_key=True, max_length=36)
    ticket = ForeignKeyField(Ticket, backref='mensagens', on_delete='CASCADE')
    sender = ForeignKeyField(Usuario, backref='mensagens', on_delete='CASCADE')
    mensagem = TextField()
    tipo = CharField(choices=[('texto','texto'),('imagem','imagem'),('arquivo','arquivo'),('audio','audio')], default='texto')
    enviado_em = DateTimeField(default=datetime.datetime.now)
