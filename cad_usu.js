// URL do backend - ajuste conforme necessário
const BACKEND_URL = 'http://localhost:5000';

// Elementos do DOM
const form = document.getElementById('form-cadastro');
const roleSelect = document.getElementById('role');
const especialistaFields = document.getElementById('especialista-fields');
const mensagemDiv = document.getElementById('mensagem');
const btnCadastrar = document.getElementById('btn-cadastrar');

// Mostrar/ocultar campos de especialista
roleSelect.addEventListener('change', function() {
    if (this.value === 'especialista') {
        especialistaFields.style.display = 'block';
        // Tornar obrigatórios os campos de especialista
        document.getElementById('area_profissional').required = true;
    } else {
        especialistaFields.style.display = 'none';
        // Remover obrigatoriedade
        document.getElementById('area_profissional').required = false;
    }
});

// Validação em tempo real da senha
const senhaInput = document.getElementById('senha');
const confirmarInput = document.getElementById('confirmar');

function validarSenha(senha) {
    const requisitos = {
        minuscula: /[a-z]/.test(senha),
        maiuscula: /[A-Z]/.test(senha),
        especial: /[!@#$%^&*(),.?":{}|<>]/.test(senha),
        numero: /\d/.test(senha),
        tamanho: senha.length >= 6
    };
    
    return requisitos;
}

function atualizarRequisitos(senha, confirmar) {
    const requisitos = validarSenha(senha);
    const confirmacaoValida = senha === confirmar && senha.length > 0;
    
    document.getElementById('req-minuscula').className = requisitos.minuscula ? 'ok' : 'erro';
    document.getElementById('req-maiuscula').className = requisitos.maiuscula ? 'ok' : 'erro';
    document.getElementById('req-especial').className = requisitos.especial ? 'ok' : 'erro';
    document.getElementById('req-numero').className = requisitos.numero ? 'ok' : 'erro';
    document.getElementById('req-tamanho').className = requisitos.tamanho ? 'ok' : 'erro';
    document.getElementById('req-confirmar').className = confirmacaoValida ? 'ok' : 'erro';
    
    // Verificar se todos os requisitos estão atendidos
    const todosRequisitos = Object.values(requisitos).every(v => v) && confirmacaoValida;
    btnCadastrar.disabled = !todosRequisitos;
    
    return todosRequisitos;
}

senhaInput.addEventListener('input', () => {
    atualizarRequisitos(senhaInput.value, confirmarInput.value);
});

confirmarInput.addEventListener('input', () => {
    atualizarRequisitos(senhaInput.value, confirmarInput.value);
});

// Função para mostrar mensagens
function mostrarMensagem(texto, tipo = 'info') {
    mensagemDiv.innerHTML = `<div class="mensagem ${tipo}">${texto}</div>`;
    
    // Auto-remover mensagem após 5 segundos (exceto erro)
    if (tipo !== 'erro') {
        setTimeout(() => {
            if (mensagemDiv.firstChild) {
                mensagemDiv.innerHTML = '';
            }
        }, 5000);
    }
}

// Envio do formulário
form.addEventListener('submit', async function(event) {
    event.preventDefault();
    
    // Coletar dados do formulário
    const formData = {
        nome: document.getElementById('nome').value.trim(),
        email: document.getElementById('email').value.trim().toLowerCase(),
        password: senhaInput.value,
        role: roleSelect.value,
        telefone: document.getElementById('telefone').value || null,
        foto_url: null // Pode implementar upload de foto depois
    };
    
    // Validações básicas
    if (!formData.role) {
        mostrarMensagem('Por favor, selecione o tipo de cadastro.', 'erro');
        return;
    }
    
    // Verificar se senhas coincidem
    if (senhaInput.value !== confirmarInput.value) {
        mostrarMensagem('As senhas não coincidem.', 'erro');
        return;
    }
    
    // Verificar requisitos da senha
    if (!atualizarRequisitos(formData.password, confirmarInput.value)) {
        mostrarMensagem('A senha não atende a todos os requisitos.', 'erro');
        return;
    }
    
    // Adicionar campos específicos para especialistas
    if (formData.role === 'especialista') {
        formData.area_profissional = document.getElementById('area_profissional').value;
        formData.formacao = document.getElementById('formacao').value || null;
        formData.registro_prof = document.getElementById('registro_prof').value || null;
        formData.bio = document.getElementById('bio').value || null;
        
        if (!formData.area_profissional) {
            mostrarMensagem('Para cadastro como especialista, a área profissional é obrigatória.', 'erro');
            return;
        }
    }
    
    // Desabilitar botão durante o envio
    btnCadastrar.disabled = true;
    btnCadastrar.textContent = 'Cadastrando...';
    
    // Enviar para o backend
    try {
        const resposta = await fetch(`${BACKEND_URL}/cadastro_usuario`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(formData)
        });
        
        const dados = await resposta.json();
        
        if (dados.success) {
            mostrarMensagem(dados.msg, 'sucesso');
            
            // Limpar formulário
            form.reset();
            especialistaFields.style.display = 'none';
            
            // Redirecionar após 3 segundos
            setTimeout(() => {
                if (formData.role === 'cliente') {
                    window.location.href = 'login.html';
                } else if (formData.role === 'especialista') {
                    // Mostrar mensagem especial para especialistas
                    mostrarMensagem('Seu cadastro foi realizado! Em breve você terá acesso ao sistema.', 'info');
                } else {
                    window.location.href = 'dashboard.html';
                }
            }, 3000);
        } else {
            mostrarMensagem(dados.message, 'erro');
            btnCadastrar.disabled = false;
            btnCadastrar.textContent = 'Cadastrar';
        }
        
    } catch (erro) {
        console.error('Erro:', erro);
        mostrarMensagem('Erro ao conectar com o servidor. Tente novamente.', 'erro');
        btnCadastrar.disabled = false;
        btnCadastrar.textContent = 'Cadastrar';
    }
});

// Inicializar validação da senha
atualizarRequisitos('', '');