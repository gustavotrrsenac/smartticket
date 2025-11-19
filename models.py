from peewee import *
from database import db

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
    criado_em = DateTimeField()

class Ticket(BaseModel):
    id = CharField(primary_key=True, max_length=36)
    titulo = CharField(max_length=150)
    descricao = TextField()
    status = CharField(default='aberto')
    criado_por = ForeignKeyField(Usuario, backref='tickets_criados')
    atribuido_para = ForeignKeyField(Usuario, backref='tickets_recebidos', null=True)
    criado_em = DateTimeField()
