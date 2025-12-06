#!/usr/bin/env python3
"""
Script para inicializar o banco de dados.
Executa uma única vez para criar todas as tabelas.
"""
import sys
import os
import datetime

# Adiciona diretório atual ao path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database import db, test_connection
from models import (
    Usuario,
    PerfilCliente,
    PerfilEspecialista,
    Admin,
    Triagem,
    PerguntaTriagem,
    TriagemResposta,
    Ticket,
    Mensagem,
    DocumentoEspecialista
)

def criar_tabelas():
    """
    Cria todas as tabelas do sistema.
    """
    print(" Criando tabelas...")
    print("-" * 50)
    
    # Ordem é importante devido às foreign keys
    tabelas = [
        Usuario,              # Base para todos
        PerfilCliente,        # Depende de Usuario
        PerfilEspecialista,   # Depende de Usuario
        Admin,                # Depende de Usuario
        Triagem,              # Depende de Usuario
        PerguntaTriagem,      # Independente
        TriagemResposta,      # Depende de Triagem e PerguntaTriagem
        Ticket,               # Depende de Usuario e Triagem
        Mensagem,             # Depende de Ticket e Usuario
        DocumentoEspecialista # Depende de Usuario
    ]
    
    try:
        with db:
            # safe=True: não dá erro se tabela já existir
            db.create_tables(tabelas, safe=True)
            
            print(" Tabelas criadas com sucesso!")
            print("\n Lista de tabelas:")
            for tabela in tabelas:
                print(f"   ✓ {tabela.__name__}")
            print()
            
    except Exception as e:
        print(f" Erro ao criar tabelas: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True

def verificar_tabelas():
    """
    Verifica se todas as tabelas existem.
    """
    print(" Verificando tabelas...")
    
    #alterando a tabela (atulizando os dados conforme no db)
    tabelas = [
        'admin',
        'mensagens', 
        'perfil_cliente',
        'perfil_especialista',
        'perguntas_triagem',
        'ticket',
        'triagem',
        'triagem_resposta',
        'usuario'
    ]
    
    try:
        cursor = db.cursor()
        cursor.execute("SHOW TABLES")
        tabelas_existentes = [t[0] for t in cursor.fetchall()]
        
        print(f" Tabelas no banco: {len(tabelas_existentes)}")
        
        for tabela in tabelas:
            if tabela in tabelas_existentes:
                print(f"   ✓ {tabela}")
            else:
                print(f"   ✗ {tabela} (FALTANDO)")
        
        cursor.close()
        return True
        
    except Exception as e:
        print(f" Erro ao verificar tabelas: {e}")
        return False

def inicializar_dados():
    """
    Insere dados iniciais se necessário.
    """
    print("\n Inicializando dados...")
    
    try:
        # Criar usuário admin padrão se não existir
        from uuid import uuid4
        import hashlib
        
        admin_email = "admin@sistema.com"
        admin_existe = Usuario.select().where(Usuario.email == admin_email).exists()
        
        if not admin_existe:
            senha_hash = hashlib.sha256("admin123".encode()).hexdigest()
            
            Usuario.create(
                id=str(uuid4()),
                nome="Administrador do Sistema",
                email=admin_email,
                password_hash=senha_hash,
                role="admin",
                status_aprovacao="aprovado",
                criado_em=datetime.datetime.now(),
                atualizado_em=datetime.datetime.now()
            )
            print("    Usuário admin criado")
        else:
            print("   ⏭  Usuário admin já existe")
            
        return True
        
    except Exception as e:
        print(f"    Erro ao inicializar dados: {e}")
        return False

def main():
    """
    Função principal de inicialização.
    """
    print(" Inicializando Banco de Dados")
    print("=" * 50)
    
    # 1. Testar conexão
    print("\n1. Testando conexão com MySQL...")
    if not test_connection():
        print(" Falha na conexão. Verifique:")
        print("   • Servidor MySQL está rodando?")
        print("   • Credenciais no .env estão corretas?")
        print("   • Banco de dados existe?")
        return
    
    print("   ✅ Conexão estabelecida")
    
    # 2. Criar tabelas
    print("\n2. Configurando estrutura do banco...")
    if not criar_tabelas():
        return
    
    # 3. Verificar tabelas
    print("\n3. Verificando integridade...")
    verificar_tabelas()
    
    # 4. Inicializar dados
    from datetime import datetime
    import datetime as dt
    inicializar_dados()
    
    print("\n" + "=" * 50)
    print("🎉 Banco de dados inicializado com sucesso!")
    print("\n📌 Próximos passos:")
    print("   1. Execute o servidor Flask: python app.py")
    print("   2. Acesse: http://localhost:5000")
    print("   3. Teste o cadastro de usuários")

if __name__ == "__main__":
    main()