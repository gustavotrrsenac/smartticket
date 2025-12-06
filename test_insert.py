#!/usr/bin/env python3
"""
Script para testar INSERTs no sistema Smart Ticket
Testa apenas operações básicas sem dependências complexas
"""
import sys
from uuid import uuid4
from datetime import datetime
import hashlib

# Adiciona diretório ao path
sys.path.append('.')

def hash_senha(senha):
    """Gera hash SHA-256 para senha."""
    return hashlib.sha256(senha.encode()).hexdigest()

def testar_conexao():
    """Testa se consegue conectar ao banco."""
    print("🔍 Testando conexão com o banco...")
    try:
        from database import db
        db.connect()
        print("✅ Conexão estabelecida com sucesso!")
        db.close()
        return True
    except Exception as e:
        print(f"❌ Erro na conexão: {e}")
        print("\n💡 Dica: Verifique seu database.py")
        return False

def testar_insert_usuario():
    """Testa inserção de usuário."""
    print("\n👤 Testando INSERT de usuário...")
    
    try:
        from models import Usuario
        
        # Dados de teste
        usuario_data = {
            "id": str(uuid4()),
            "nome": "Cliente Teste",
            "email": f"cliente_{uuid4().hex[:8]}@teste.com",
            "password_hash": hash_senha("Teste123!"),
            "role": "cliente",
            "status_aprovacao": "aprovado",
            "telefone": "(11) 99999-9999",
            "criado_em": datetime.now(),
            "atualizado_em": datetime.now()
        }
        
        # Inserir
        usuario = Usuario.create(**usuario_data)
        print(f"✅ Usuário inserido com sucesso!")
        print(f"   ID: {usuario.id}")
        print(f"   Nome: {usuario.nome}")
        print(f"   Email: {usuario.email}")
        print(f"   Role: {usuario.role}")
        
        # Verificar se foi salvo
        usuario_db = Usuario.get_by_id(usuario.id)
        print(f"   Verificação: Usuário encontrado no banco? {'✅ Sim' if usuario_db else '❌ Não'}")
        
        return usuario.id
        
    except Exception as e:
        print(f"❌ Erro ao inserir usuário: {e}")
        import traceback
        traceback.print_exc()
        return None

def testar_insert_perguntas_triagem():
    """Testa inserção de perguntas de triagem."""
    print("\n❓ Testando INSERT de perguntas de triagem...")
    
    try:
        from models import PerguntaTriagem
        
        perguntas = [
            {
                "id": str(uuid4()),
                "pergunta": "Qual é a natureza do seu problema?",
                "resposta_padrao": "Selecione uma opção: Hardware, Software, Rede, Outro",
                "categoria": "geral",
                "ordem_pergunta": 1,
                "ativo": True
            },
            {
                "id": str(uuid4()),
                "pergunta": "Há quanto tempo o problema ocorre?",
                "resposta_padrao": "Selecione uma opção: Hoje, Esta semana, Este mês, Mais de um mês",
                "categoria": "tempo",
                "ordem_pergunta": 2,
                "ativo": True
            }
        ]
        
        ids_perguntas = []
        for pergunta_data in perguntas:
            pergunta = PerguntaTriagem.create(**pergunta_data)
            ids_perguntas.append(pergunta.id)
            print(f"✅ Pergunta inserida: '{pergunta.pergunta[:30]}...'")
        
        # Contar perguntas
        total = PerguntaTriagem.select().count()
        print(f"📊 Total de perguntas no banco: {total}")
        
        return ids_perguntas
        
    except Exception as e:
        print(f"❌ Erro ao inserir perguntas: {e}")
        return []

def testar_insert_ticket(usuario_id):
    """Testa inserção de ticket."""
    if not usuario_id:
        print("⚠️  Não é possível testar ticket sem usuário")
        return None
    
    print("\n🎫 Testando INSERT de ticket...")
    
    try:
        from models import Ticket
        
        ticket_data = {
            "id": str(uuid4()),
            "cliente_id": usuario_id,
            "titulo": "Problema de login - TESTE",
            "descricao": "Não consigo acessar o sistema com minhas credenciais.",
            "status": "aberto",
            "criado_em": datetime.now(),
            "atualizado_em": datetime.now()
        }
        
        # Inserir
        ticket = Ticket.create(**ticket_data)
        print(f"✅ Ticket inserido com sucesso!")
        print(f"   ID: {ticket.id}")
        print(f"   Título: {ticket.titulo}")
        print(f"   Status: {ticket.status}")
        print(f"   Cliente ID: {ticket.cliente_id}")
        
        return ticket.id
        
    except Exception as e:
        print(f"❌ Erro ao inserir ticket: {e}")
        import traceback
        traceback.print_exc()
        return None

def testar_selects():
    """Testa operações SELECT."""
    print("\n🔎 Testando SELECTs...")
    
    try:
        from models import Usuario, PerguntaTriagem, Ticket
        
        # Contar registros
        total_usuarios = Usuario.select().count()
        total_perguntas = PerguntaTriagem.select().count()
        total_tickets = Ticket.select().count()
        
        print(f"📊 Estatísticas do banco:")
        print(f"   👤 Usuários: {total_usuarios}")
        print(f"   ❓ Perguntas de Triagem: {total_perguntas}")
        print(f"   🎫 Tickets: {total_tickets}")
        
        # Listar alguns usuários
        if total_usuarios > 0:
            print(f"\n📋 Últimos usuários cadastrados:")
            usuarios = Usuario.select().order_by(Usuario.criado_em.desc()).limit(3)
            for u in usuarios:
                print(f"   • {u.nome} ({u.email}) - {u.role}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro nos SELECTs: {e}")
        return False

def testar_api_endpoints():
    """Testa endpoints da API (simulação)."""
    print("\n🌐 Testando endpoints da API...")
    
    endpoints = [
        ("GET", "/health", "Verifica saúde da API"),
        ("POST", "/usuarios", "Cria novo usuário"),
        ("GET", "/usuarios", "Lista usuários"),
        ("POST", "/tickets", "Cria ticket"),
        ("GET", "/tickets", "Lista tickets")
    ]
    
    print("Endpoints disponíveis:")
    for metodo, endpoint, descricao in endpoints:
        print(f"   {metodo:6} {endpoint:20} - {descricao}")

def limpar_dados_teste():
    """Remove dados de teste (opcional)."""
    print("\n🧹 Deseja limpar dados de teste?")
    resposta = input("Digite 'sim' para limpar ou Enter para manter: ").lower()
    
    if resposta == 'sim':
        try:
            from models import Usuario, PerguntaTriagem, Ticket
            from database import db
            
            with db.atomic():
                # Contar antes
                antes_usuarios = Usuario.select().count()
                antes_tickets = Ticket.select().count()
                
                # Remover dados de teste
                # (Apenas remova se quiser - comente as linhas abaixo para não remover)
                # Ticket.delete().where(Ticket.titulo.contains("TESTE")).execute()
                # Usuario.delete().where(Usuario.email.contains("@teste.com")).execute()
                
                print("⚠️  Limpeza comentada para segurança.")
                print("   Descomente no código se quiser realmente limpar.")
                
        except Exception as e:
            print(f"❌ Erro ao limpar: {e}")

def main():
    """Função principal."""
    print("=" * 60)
    print("🧪 TESTE DE INSERTS - SMART TICKET")
    print("=" * 60)
    
    # 1. Testar conexão
    if not testar_conexao():
        print("\n❌ Não é possível continuar sem conexão.")
        return
    
    # 2. Testar INSERTs
    usuario_id = testar_insert_usuario()
    
    # 3. Testar perguntas (independente de usuário)
    perguntas_ids = testar_insert_perguntas_triagem()
    
    # 4. Testar ticket (depende de usuário)
    if usuario_id:
        ticket_id = testar_insert_ticket(usuario_id)
    
    # 5. Testar SELECTs
    testar_selects()
    
    # 6. Mostrar endpoints
    testar_api_endpoints()
    
    # 7. Opção de limpeza
    # limpar_dados_teste()
    
    print("\n" + "=" * 60)
    print("🎯 TESTES CONCLUÍDOS!")
    print("\n📌 Próximos passos:")
    print("   1. Execute o servidor: python app.py")
    print("   2. Teste a API com: curl http://localhost:5000/health")
    print("   3. Acesse o frontend: http://localhost:5500/cad_usu.html")
    print("=" * 60)

if __name__ == "__main__":
    main()