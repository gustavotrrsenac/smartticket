import subprocess
import os

def check_mysql_service():
    """Verifica se o MySQL está rodando"""
    print("🔍 Verificando status do MySQL...")
    
    # Tentar diferentes comandos dependendo do sistema
    commands = [
        ['netstat', '-ano', '|', 'findstr', ':3306'],
        ['sc', 'query', 'mysql'],
        ['services.msc']
    ]
    
    mysql_running = False
    
    try:
        # Tentar conectar via Python
        import pymysql
        connection = pymysql.connect(
            host='localhost',
            user='root',
            password='senac',
            connect_timeout=5
        )
        connection.close()
        mysql_running = True
        print("✅ MySQL está rodando e acessível")
        
    except pymysql.err.OperationalError as e:
        print(f"❌ MySQL não está acessível: {e}")
        
        # Tentar iniciar o MySQL
        print("\n🔄 Tentando soluções automáticas...")
        
        # Solução 1: Verificar via serviços Windows
        try:
            result = subprocess.run(
                ['sc', 'query', 'mysql'],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if 'RUNNING' in result.stdout:
                print("✅ Serviço MySQL está rodando")
                mysql_running = True
            elif 'STOPPED' in result.stdout:
                print("ℹ️  Serviço MySQL parado")
                print("Tentando iniciar...")
                
                # Tentar iniciar o serviço
                subprocess.run(['net', 'start', 'mysql'], shell=True)
                mysql_running = True
                
        except:
            pass
            
    except ImportError:
        print("❌ pymysql não instalado. Execute:")
        print("pip install pymysql")
    
    return mysql_running

if __name__ == "__main__":
    check_mysql_service()