import re


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